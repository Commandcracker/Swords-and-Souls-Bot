#!/usr/bin/python3
# -*- coding: utf-8 -*-

# built-in modules
from time import time, sleep
import argparse

# pip modules
from display_server_interactions import DSI

# local modules
from training_block import Block
from training_critical import Critical
from training_dodge import Dodge

# rich printing
try:
    from rich.console import Console
    from rich.traceback import install
    __console = Console()
    install(console=__console)

    def print(*args, **kwargs):
        __console.print(
            *args,
            **kwargs,
            style="cyan"
        )
except ImportError:
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        description="A Bot that can Play Swords and Souls like a God!"
    )

    parser.add_argument(
        "mode",
        type=str,
        default="block",
        choices=["block", "critical", "dodge"],
        help="The mode to train in."
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("Mode:", args.mode)

    dsi = DSI()

    window = dsi.get_window_by_name(
        "Adobe Flash Player"
    )  # Adobe Flash Player 32

    if window is None:
        print("Waiting 2 seconds, Please open the window you want to capture.")
        sleep(2)

        window = dsi.get_active_window()

    print("Recording Window: {} (PID: {})".format(
        window.name,
        window.pid
    ))

    if args.mode == "block":
        runnable = Block(window)
    elif args.mode == "critical":
        runnable = Critical(window)
    elif args.mode == "dodge":
        runnable = Dodge(window)

    while True:
        try:
            loop_time = time()
            runnable.run()
            print("FPS {}".format(1 / (time() - loop_time)), end="\r")
            loop_time = time()
        except Exception as e:
            print("Failed to get image.")
            print(e)


if __name__ == "__main__":
    main()
