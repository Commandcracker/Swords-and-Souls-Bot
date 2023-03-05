#!/usr/bin/python3
# -*- coding: utf-8 -*-

# build-in modules
from time import sleep

# pip modules
import numpy as np

# local modules
from runnable import Runnable
from display_server_interactions.box import Box


class Critical(Runnable):
    def run(self):
        geo = self.window.geometry
        geo = Box(
            int(geo[0]+geo[2]/4),
            int(geo[1]+geo[3]/4),
            int(geo[2]-geo[2]/2),
            int(geo[3]-geo[3]/2)
        )

        img = np.array(self.window.get_image(geo))
        sleep(0.1)  # Idk why but it fixes "float division by zero"

        red_pixels = np.logical_and(
            img[:, :, 2] == 204,
            img[:, :, 1] == 0,
            img[:, :, 0] == 0
        )

        if np.any(red_pixels):
            y, x = np.unravel_index(np.argmax(red_pixels), red_pixels.shape)

            sleep(0.2)  # Human reaction time

            print("1st *Click*"+" "*15, end="\r")
            self.window.send_mouse_click(int(x), int(y))

            sleep(0.7)  # Time between 1st and 2nd click

            print("2nd *Click*"+" "*15, end="\r")
            self.window.send_mouse_click(int(x), int(y))

            sleep(0.2)  # Human reaction time
