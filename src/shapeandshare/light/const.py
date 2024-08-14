import pygame

# Predefined some colors
BLUE: tuple[int, int, int] = (0, 0, 255)
RED: tuple[int, int, int] = (255, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)



# TILE_X: int = 15
# TILE_Y: int = 15
# DIM_X: int = 75
# DIM_Y: int = 50


TILE_X: int = 15
TILE_Y: int = 15


DIM_X: int = 15
DIM_Y: int = 15


# 100x15=1500
WINDOW_WIDTH: int = TILE_X * DIM_X
WINDOW_HEIGHT: int = TILE_Y * DIM_Y


FPS: int = 60
FramePerSec = pygame.time.Clock()


PRODUCT_NAME: str = "light"
