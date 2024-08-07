import logging
from pathlib import Path

import pygame
from pygame import Surface, SurfaceType
from pygame.rect import Rect, RectType

from shapeandshare.darkness import Tile, TileType

from ..dtos.center_metadata import CenterMetadata


class TileSprite(pygame.sprite.Sprite, Tile):
    class Config:
        arbitrary_types_allowed = True

    image: Surface | SurfaceType | None = None
    rect: Rect | RectType | None = None

    # state
    hovered: bool = False

    def set(self, center: CenterMetadata | None) -> None:
        # We are updating, pull the prior location
        if center is None:
            previous_center: tuple[int, int] = self.rect.center

        # determine image
        assets_base_path: Path = Path(__file__).parents[2] / "assets" / "tiles"

        if self.tile_type == TileType.UNKNOWN:
            image_path: Path = assets_base_path / "unknown.png"
        elif self.tile_type == TileType.OCEAN:
            image_path: Path = assets_base_path / "ocean.png"
        elif self.tile_type == TileType.WATER:
            image_path: Path = assets_base_path / "water.png"
        elif self.tile_type == TileType.SHORE:
            image_path: Path = assets_base_path / "shore.png"
        elif self.tile_type == TileType.DIRT:
            image_path: Path = assets_base_path / "dirt.png"
        elif self.tile_type == TileType.GRASS:
            image_path: Path = assets_base_path / "grass.png"
        elif self.tile_type == TileType.ROCK:
            image_path: Path = assets_base_path / "rock.png"
        elif self.tile_type == TileType.FOREST:
            image_path: Path = assets_base_path / "forest.png"
        else:
            msg: str = f"Unknown tile type ({self.tile_type})"
            logging.warning(msg)
            image_path: Path = assets_base_path / "unknown.png"

        self.image = pygame.image.load(image_path)
        self.rect: Rect | RectType = self.image.get_rect()

        if center:
            rect_center_x, rect_center_y = self.rect.center
            pos_x: tuple[int, int] = rect_center_x + center.x.offset + (center.x.itr * self.rect.width)
            pos_y: tuple[int, int] = rect_center_y + center.y.offset + (center.y.itr * self.rect.height)
            self.rect.center = (pos_x, pos_y)
        else:
            self.rect.center = previous_center

        # set hover effect
        if self.hovered:
            self.image.set_alpha(125)

    def __init__(self, center: CenterMetadata, **kwargs):
        Tile.__init__(self, **kwargs)
        pygame.sprite.Sprite.__init__(self)
        self.set(center=center)

    def hover(self):
        self.hovered = True
        self.set(center=None)

    def unhover(self):
        self.hovered = False
        self.set(center=None)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
