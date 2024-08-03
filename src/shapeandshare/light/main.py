import pygame

pygame.init()


def main():
    from .display import build_display
    from .loop import loop

    loop(display_surface=build_display())


if __name__ == "__main__":
    main()
