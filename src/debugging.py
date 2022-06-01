#!/usr/bin/python3
# -*- coding: utf-8 -*-

# built-in modules
from sys import maxsize

# pip modules
import cv2
import numpy as np


class Debugging(object):
    @staticmethod
    def dump_numpy_array(array: np.ndarray, filename: str = "dump.json") -> None:
        """
        Dumps a numpy array to a json file.
        """
        np.set_printoptions(threshold=maxsize)
        open(filename, "w").write(str(array))

    @staticmethod
    def dump_image(img: np.ndarray, filename: str = "dump.png") -> None:
        """
        Dumps the given image to the given filename.
        """
        cv2.imwrite(filename, img)

    @staticmethod
    def display_debug_image(img: np.ndarray, title: str = "Computer Vision") -> None:
        """
        Displays the given image Colord and in Black and White in a window with the given title.
        """
        cv2.imshow(title, img)
        cv2.waitKey(1)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow(title + " - Grayscale", img)
        cv2.waitKey(1)
