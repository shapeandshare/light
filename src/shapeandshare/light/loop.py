import sys

import pygame
from pydantic import BaseModel
from pygame import QUIT, Surface, SurfaceType
from pygame.font import Font

from shapeandshare.darkness import Chunk, CommandOptions, StateClient, Tile, TileType, World

from .const import BLACK, DIM_X, DIM_Y, FPS, TILE_X, TILE_Y, WHITE, FramePerSec
from .contracts.dtos.center_metadata import CenterMetadata
from .contracts.sprites.chunk import SpriteChunk
from .contracts.sprites.tile import TileSprite


class LabelDTO(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    text: str
    pos: tuple
    font: Font
    color: pygame.Color = pygame.Color("black")


#  https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def blit_text(surface: Surface | SurfaceType, label: LabelDTO) -> None:
    surface = surface
    text = label.text
    pos = label.pos
    font = label.font
    color = label.color

    words: list[list[str]] = [word.split(" ") for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface: Surface | SurfaceType = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


async def load_sprite_chunk(client: StateClient, world_id: str, chunk_id: str, sprite_chunk: SpriteChunk | None) -> SpriteChunk:
    # print("CHUNKLOADEVENT")
    if sprite_chunk:
        await sprite_chunk.reload_tiles(client=client, world_id=world_id, chunk_id=chunk_id)
    else:
        chunk: Chunk = await client.chunk_get(world_id=world_id, chunk_id=chunk_id, full=True)
        sprite_chunk: SpriteChunk = SpriteChunk.model_validate({**chunk.model_dump(exclude={"contents"}), "offset": (0, 0)})
        sprite_chunk.load_tiles(tiles=chunk.contents)
    return sprite_chunk


async def loop(display_surface: Surface | SurfaceType):
    options: CommandOptions = CommandOptions(sleep_time=5, retry_count=30, tld="localhost:8000", timeout=60)
    client: StateClient = StateClient(options=options)

    # see if there is a world already
    worlds: list[World] = await client.worlds_get()
    chunk_ids: list[str] = []
    if len(worlds) > 0:
        # connect to the first...
        world_id: str = worlds[0].id
        print(f"Connecting to existing world {world_id}")
        chunk_ids = list(worlds[0].ids)
    else:
        # create a new world
        world_id: str = await client.world_create(name="darkness")
        print(f"Created and connecting to new world {world_id}")

    # Determine if we can connect to a pre-existing chunk
    if len(chunk_ids) > 0:
        # connect to the first chunk
        chunk_id: str = chunk_ids[0]
        print(f"Connecting to existing chunk {chunk_id}")
    else:
        # create a new chunk
        print(f"Created and connecting to new chunk..")
        chunk_id: str = await client.chunk_create(world_id=world_id, name="roshar", dimensions=(DIM_X, DIM_Y), biome=TileType.DIRT)
        print(f"Created chunk id: {chunk_id}, moving on...")

    # Load visuals
    sprite_chunk: SpriteChunk = await load_sprite_chunk(client=client, world_id=world_id, chunk_id=chunk_id, sprite_chunk=None)
    selected_tile_label: LabelDTO | None = None

    CHUNKLOADEVENT = pygame.USEREVENT + 1
    interval: int = 5000
    pygame.time.set_timer(CHUNKLOADEVENT, interval)

    while True:
        # Review game events (of interest)
        for event in pygame.event.get():
            # print(event)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pointer_pos: tuple[int, int] = pygame.mouse.get_pos()
                # print("MOUSEMOTION")
                sprite_chunk.update_tile_hover(position=pointer_pos)

            # Determine action type
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pointer_pos: tuple[int, int] = pygame.mouse.get_pos()
                # print("MOUSEBUTTONDOWN")
                tile_sprite: TileSprite | None = sprite_chunk.update_tile_selection(position=pointer_pos)
                if tile_sprite:
                    tile: Tile = Tile.model_validate(tile_sprite.model_dump(exclude={"image", "rect", "hovered"}))
                    # print(tile.model_dump_json(indent=4))
                    center: tuple[int, int] = ((TILE_X * DIM_X), 1)
                    myfont: Font = pygame.font.SysFont("verdana", 12)
                    label = LabelDTO(text=tile.model_dump_json(indent=4), pos=center, font=myfont, color=pygame.Color("black"))
                    # print(label.text)
                    selected_tile_label = label
                else:
                    selected_tile_label = None
                    # print("unselecting tile label")

            if event.type == CHUNKLOADEVENT:
                sprite_chunk = await load_sprite_chunk(client=client, world_id=world_id, chunk_id=chunk_id, sprite_chunk=sprite_chunk)

        # Apply game logic updates
        # Redraw the surface
        display_surface.fill(WHITE)
        for _, tile in sprite_chunk.tiles.items():
            tile.draw(display_surface)

        if selected_tile_label:
            # selected_tile_label.draw(display_surface)
            blit_text(surface=display_surface, label=selected_tile_label)
        # else:

        pygame.display.update()
        FramePerSec.tick(FPS)
