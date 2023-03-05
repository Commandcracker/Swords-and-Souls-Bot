#!/usr/bin/python3
# -*- coding: utf-8 -*-

# build-in modules
from pathlib import Path

# pip modules
import numpy as np
from display_server_interactions.box import Box
from display_server_interactions.window import WindowBase
import cv2

# local modules
from runnable import Runnable


class Dodge(Runnable):
    def __init__(self, window: WindowBase) -> None:
        super().__init__(window)
        templates_path = Path(
            Path(__file__).parent,
            "templates",
            "dodge"
        )
        self.template_down = cv2.imread(
            Path(templates_path, "down.png").resolve().absolute().as_posix(),
            0
        )
        self.template_up = cv2.imread(
            Path(templates_path, "up.png").resolve().absolute().as_posix(),
            0
        )
        self.template_left = cv2.imread(
            Path(templates_path, "left.png").resolve().absolute().as_posix(),
            0
        )

    def run(self):
        geo = self.window.geometry
        geo = Box(
            int(geo[0]),
            int(geo[1]+geo[3]/4),
            int(geo[2]),
            int(geo[3]-geo[3]/2)
        )

        img = np.array(self.window.get_image(geo))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        result_down = cv2.matchTemplate(
            img,
            self.template_down,
            cv2.TM_CCOEFF_NORMED
        )
        (
            minVal_down,
            maxVal_down,
            minLoc_down,
            maxLoc_down
        ) = cv2.minMaxLoc(result_down)

        result_up = cv2.matchTemplate(
            img,
            self.template_up,
            cv2.TM_CCOEFF_NORMED
        )
        (
            minVal_up,
            maxVal_up,
            minLoc_up,
            maxLoc_up
        ) = cv2.minMaxLoc(result_up)

        result_left = cv2.matchTemplate(
            img,
            self.template_left,
            cv2.TM_CCOEFF_NORMED
        )
        (
            minVal_left,
            maxVal_left,
            minLoc_left,
            maxLoc_left
        ) = cv2.minMaxLoc(result_left)

        # https://wiki.linuxquestions.org/wiki/List_of_keysyms

        if maxVal_down >= 0.6:
            print("**match Down**", end='\r')
            self.window.send_chr("Down")

        elif maxVal_up >= 0.6:
            print("**match Up**", end='\r')
            self.window.send_chr(0x0004)

        elif maxVal_left >= 0.6:
            print("**match Left**", end='\r')
            self.window.send_chr("Left")
