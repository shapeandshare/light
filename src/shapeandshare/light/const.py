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


# DIM_X: int = 24
# DIM_Y: int = 24

# DIM_X: int = 48
# DIM_Y: int = 48

# DIM_X: int = 64
# DIM_Y: int = 48

DIM_X: int = 48
# DIM_X: int = 96
# DIM_X: int = 48
# DIM_Y: int = 32
DIM_Y: int = 48

# 100x15=1500
# WINDOW_WIDTH: int = TILE_X * DIM_X + 200
# WINDOW_HEIGHT: int = TILE_Y * DIM_Y

# WINDOW_WIDTH: int = 800
# WINDOW_HEIGHT: int = 600

# WINDOW_WIDTH: int = 2048
# WINDOW_HEIGHT: int = 1280

WINDOW_WIDTH: int = TILE_X * ((DIM_X * 1.5)+ 1)
WINDOW_HEIGHT: int = TILE_Y * (DIM_Y + 1)

FPS: int = 60
FramePerSec = pygame.time.Clock()


PRODUCT_NAME: str = "light"
