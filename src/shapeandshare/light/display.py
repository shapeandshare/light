import pygame
from pygame import Surface, SurfaceType

from .const import PRODUCT_NAME


def build_display(width: int, height: int) -> Surface | SurfaceType:
    display_surface: Surface | SurfaceType = pygame.display.set_mode(
        (width, height),
        flags=pygame.RESIZABLE | pygame.SCALED,
        # (width, height), flags=pygame.RESIZABLE
    )
    pygame.display.set_caption(PRODUCT_NAME)
    return display_surface
