import pygame
from pygame import Surface, SurfaceType

from .const import WINDOW_HEIGHT, WINDOW_WIDTH


def build_display() -> Surface | SurfaceType:
    DISPLAYSURF: Surface | SurfaceType = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Darkness")
    return DISPLAYSURF
