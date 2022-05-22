#!/usr/bin/python3
# -*- coding: utf-8 -*-

# local modules
import WindowCapture as WC
"""
TODO:   maybe switch to other libraries?

        for WindowCaptureing: 
            [python-mss](https://github.com/BoboTiG/python-mss) or
            for windows [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) or [Pillow](https://pypi.org/project/Pillow/)
            and use [PyGetWindow](https://pypi.org/project/PyGetWindow/) to get windows or
            [win32gui, win32ui, win32con](https://github.com/learncodebygaming/opencv_tutorials/blob/master/004_window_capture/windowcapture.py)
            
        for mouse and keyboard Control:
            [pynput](https://pypi.org/project/pynput/) or
            [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) or
            [directKeys](https://github.com/Code-Bullet/Storm-The-House-Auto-Clicker/blob/master/directKeys.py) {[win32gui](https://pypi.org/project/win32gui/) and [win32gui](https://pypi.org/project/win-api/)}

TODO:   make WindowCapture a seperat Package
TODO:   record mouse and keyboard movements to make helping hotkeys
TODO:   make a bot for all other Game modes
"""

# built-in modules
from sys import maxsize
import time

# pip modules
import numpy as np
import cv2


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


def closest(list: np.ndarray, value: int) -> int:
    """
    get the index of the closest value in the list to the given value
    """
    return (np.abs(list - value)).argmin()


def find_rgb(img: np.ndarray, r: int, g: int, b: int, a: int) -> np.ndarray:
    """
    Finds all pixels with the given RGB values in the given image.
    returns a numpy array of the indices of the pixels.
    format: [[x1 y1],[x2 y2], ... [xn yn]]
    """

    # ([y1 y2 ... yn], [x1 y2 ... xn])
    indices = np.where(np.all(img == (b, g, r, a), axis=-1))

    # [[y1 x1],[y2 x2], ... [yn xn]]
    indices = np.moveaxis(indices, 1, 0)

    # [[x1 y1],[x2 y2], ... [xn yn]]
    indices = np.flip(indices, 1)

    return indices


def find_closest_point_to_point(points: np.ndarray, point: np.ndarray) -> int:
    """
    Finds the closest point to the given point in the given list of points.
    Returns the index of the closest point.
    """
    distances = np.sqrt(
        (points[:, 0] - point[0])**2 + (points[:, 1] - point[1])**2
    )
    return np.argmin(distances)


def get_center(img: np.ndarray) -> np.ndarray:
    """
    Returns the center of the given image.
    """
    width = img.shape[1]
    height = img.shape[0]

    return np.array([width/2, height/2])


def get_channels(img: np.ndarray) -> np.ndarray:
    """
    Returns the channels of the given image.
    """
    return img.shape[2]


def block(window: WC.Window) -> None:
    img = window.get_image()

    appels = find_rgb(img, r=153, g=39, b=41, a=255)
    stars = find_rgb(img, r=242, g=193, b=0, a=255)

    width = img.shape[1]
    height = img.shape[0]

    center = get_center(img)

    if appels.size > 0:
        closest_appel = find_closest_point_to_point(
            appels, center
        )

        if stars.size > 0:
            closest_star = find_closest_point_to_point(
                stars, center
            )
            closest = find_closest_point_to_point(
                np.array([
                    appels[closest_appel],
                    stars[closest_star]
                ]), center
            )

            if closest == 0:
                # apple is closest
                closest_x, closest_y = appels[closest_appel]

                if window.is_active:
                    window.warp_pointer(int(closest_x), int(closest_y))
            else:
                # star is closest
                closest_x, closest_y = stars[closest_star]

                if window.is_active:
                    window.warp_pointer(
                        int(width-closest_x), int(height-closest_y))

        else:
            closest_x, closest_y = appels[closest_appel]

            if window.is_active:
                window.warp_pointer(int(closest_x), int(closest_y))
    elif stars.size > 0:
        closest_star = find_closest_point_to_point(
            stars, center
        )

        closest_x, closest_y = stars[closest_star]

        if window.is_active:
            window.warp_pointer(
                int(width-closest_x), int(height-closest_y))


def main() -> None:
    print("Waiting 2 seconds, Please open the window you want to capture.")
    time.sleep(2)

    window = WC.get_active_window()

    print("Recording Window: {} (PID: {})".format(
        window.get_name(),
        window.get_pid()
    ))

    while True:
        try:
            loop_time = time.time()
            block(window)
            print("FPS {}".format(1 / (time.time() - loop_time)), end="\r")
            loop_time = time.time()
        except Exception as e:
            print("Failed to get image.")
            print(e)


if __name__ == "__main__":
    main()
