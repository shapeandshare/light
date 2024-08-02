import sys

import pygame
from pygame import QUIT, Surface, SurfaceType
from shapeandshare.darkness import Client, Island, TileType

from .const import FPS, WHITE, FramePerSec
from .contracts.sprites.island import SpriteIsland


def loop(DISPLAYSURF: Surface | SurfaceType):
    client: Client = Client()

    # load the first island
    # island_ids: list[str] = client.islands_get()
    # island: Island = client.island_get(island_ids[0])

    # create and load
    island_id: str = client.island_create(dimensions=(35, 20), biome=TileType.GRASS)
    island: Island = client.island_get(id=island_id)

    sprite_island: SpriteIsland = SpriteIsland.model_validate(
        {**island.model_dump(exclude=["tiles"]), "offset": (40, 40)}
    )
    sprite_island.load_tiles(tiles=island.tiles)

    # there can be only one
    hovered_tile_id: str | None = None
    selected_tile_id: str | None = None

    while True:
        # Review game events (of interest)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                pointer_pos: tuple[int, int] = pygame.mouse.get_pos()
                tile_id: str | None = sprite_island.hovered_over(position=pointer_pos)

                # Determine action type
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Then we are selecting
                    if selected_tile_id == tile_id:
                        # then we are unselecting
                        # print(f"explicitly unselecting {tile_id}")
                        sprite_island.unhover_over_tile(id=selected_tile_id)
                        selected_tile_id = None
                    elif selected_tile_id != tile_id:
                        # then we need to match a change
                        if selected_tile_id:
                            # print(f"implicitly unselecting {tile_id}")
                            sprite_island.unhover_over_tile(id=selected_tile_id)
                        if tile_id:
                            selected_tile_id = tile_id
                            # print(f"selecting {tile_id}")
                            sprite_island.hover_over_tile(id=selected_tile_id)

                elif event.type == pygame.MOUSEMOTION:
                    # Then we are hovering
                    if hovered_tile_id != tile_id:
                        # then we need to match a change
                        if hovered_tile_id and hovered_tile_id != selected_tile_id:
                            sprite_island.unhover_over_tile(id=hovered_tile_id)
                        if tile_id:
                            hovered_tile_id = tile_id
                            sprite_island.hover_over_tile(id=hovered_tile_id)
                    else:
                        pass

        # Apply game logic updates

        # Redraw the surface
        DISPLAYSURF.fill(WHITE)
        for _, tile in sprite_island.tiles.items():
            tile.draw(DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(FPS)
