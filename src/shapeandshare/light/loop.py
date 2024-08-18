import sys

import pygame
from pygame import QUIT, Surface, SurfaceType

from shapeandshare.darkness import Chunk, Client, CommandOptions, TileType

from .const import DIM_X, DIM_Y, FPS, WHITE, FramePerSec
from .contracts.sprites.chunk import SpriteChunk


async def loop(display_surface: Surface | SurfaceType):
    options: CommandOptions = CommandOptions(sleep_time=5, retry_count=3, tld="127.0.0.1:8000", timeout=60)
    client: Client = Client(options=options)

    # create a new world
    world_id: str = await client.world_create(name="darkness")

    # create a new chunk
    chunk_id: str = await client.chunk_create(
        world_id=world_id, name="roshar", dimensions=(DIM_X, DIM_Y), biome=TileType.GRASS
    )
    chunk: Chunk = await client.chunk_get(world_id=world_id, chunk_id=chunk_id, full=True)

    sprite_chunk: SpriteChunk = SpriteChunk.model_validate({**chunk.model_dump(exclude={"contents"}), "offset": (0, 0)})
    sprite_chunk.load_tiles(tiles=chunk.contents)

    while True:
        # Review game events (of interest)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                pointer_pos: tuple[int, int] = pygame.mouse.get_pos()
                # print(pointer_pos)

                # Determine action type
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # print("MOUSEBUTTONDOWN")
                    sprite_chunk.update_tile_selection(position=pointer_pos)

                elif event.type == pygame.MOUSEMOTION:
                    # print("MOUSEMOTION")
                    sprite_chunk.update_tile_hover(position=pointer_pos)

        # Apply game logic updates
        # Redraw the surface
        display_surface.fill(WHITE)
        for _, tile in sprite_chunk.tiles.items():
            tile.draw(display_surface)

        pygame.display.update()
        FramePerSec.tick(FPS)
