import pygame
from pygame import Surface, SurfaceType

from .const import PRODUCT_NAME, WINDOW_HEIGHT, WINDOW_WIDTH


def build_display() -> Surface | SurfaceType:
    display_surface: Surface | SurfaceType = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.RESIZABLE | pygame.SCALED
    )
    pygame.display.set_caption(PRODUCT_NAME)
    return display_surface
