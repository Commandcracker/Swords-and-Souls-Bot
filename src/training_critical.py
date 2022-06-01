#!/usr/bin/python3
# -*- coding: utf-8 -*-

# build-in modules
from time import sleep

# pip modules
import numpy as np
from display_server_interactions.window import WindowBase


def critical(window: WindowBase) -> None:
    geo = window.geometry
    geo = (
        int(geo[0]+geo[2]/4),
        int(geo[1]+geo[3]/4),
        int(geo[2]-geo[2]/2),
        int(geo[3]-geo[3]/2)
    )

    img = np.array(window.get_image(geo))

    red_pixels = np.logical_and(
        img[:, :, 2] == 204,
        img[:, :, 1] == 0,
        img[:, :, 0] == 0
    )

    if np.any(red_pixels):
        y, x = np.unravel_index(np.argmax(red_pixels), red_pixels.shape)

        sleep(0.2)  # Human reaction time

        print("1st *Click*"+" "*15, end="\r")
        window.send_mouse_click(int(x), int(y))

        sleep(0.7)  # Time between 1st and 2nd click

        print("2nd *Click*"+" "*15, end="\r")
        window.send_mouse_click(int(x), int(y))

        sleep(0.2)  # Human reaction time
