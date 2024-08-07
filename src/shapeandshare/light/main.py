import os

import click
import pygame

from .const import WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()


@click.command()
@click.option("--hostname", type=click.STRING, default="0.0.0.0", help="host address to bind to")
@click.option("--port", type=click.INT, default=8000, help="port to bind to")
@click.option("--sleep-time", type=click.FLOAT, default=1.0, help="api call sleep time (seconds)")
@click.option("--timeout", type=click.FLOAT, default=5.0, help="api call timeout (seconds)")
@click.option("--retries", type=click.INT, default=5, help="api call retries (integer)")
def main(hostname: str, port: int, sleep_time: float, timeout: float, retries: int):
    # Setup server runtime environment variables
    os.environ["DARKNESS_TLD"] = f"{hostname}:{port}"
    os.environ["DARKNESS_SERVICE_SLEEP_TIME"] = str(sleep_time)
    os.environ["DARKNESS_SERVICE_RETRY_COUNT"] = str(retries)
    os.environ["DARKNESS_SERVICE_TIMEOUT"] = str(timeout)

    from .display import build_display
    from .loop import loop

    loop(display_surface=build_display(width=WINDOW_WIDTH, height=WINDOW_HEIGHT))


if __name__ == "__main__":
    main()
