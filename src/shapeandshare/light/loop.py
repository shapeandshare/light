import sys

import pygame
from pygame import QUIT, Surface, SurfaceType

from shapeandshare.darkness import Client, Island, TileType

from .const import FPS, WHITE, FramePerSec
from .contracts.sprites.island import SpriteIsland


def loop(display_surface: Surface | SurfaceType):
    client: Client = Client()

    # load the first island
    # island_ids: list[str] = client.islands_get()
    # island: Island = client.island_get(island_ids[0])

    # create and load
    island_id: str = client.island_create(dimensions=(80, 40), biome=TileType.GRASS)
    island: Island = client.island_get(id=island_id)

    sprite_island: SpriteIsland = SpriteIsland.model_validate(
        {**island.model_dump(exclude=["tiles"]), "offset": (0, 0)}
    )
    sprite_island.load_tiles(tiles=island.tiles)

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
                    sprite_island.update_tile_selection(position=pointer_pos)

                elif event.type == pygame.MOUSEMOTION:
                    # print("MOUSEMOTION")
                    sprite_island.update_tile_hover(position=pointer_pos)

        # Apply game logic updates
        # Redraw the surface
        display_surface.fill(WHITE)
        for _, tile in sprite_island.tiles.items():
            tile.draw(display_surface)

        pygame.display.update()
        FramePerSec.tick(FPS)
