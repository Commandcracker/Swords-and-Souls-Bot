#!/usr/bin/python3
# -*- coding: utf-8 -*-

# pip modules
import numpy as np


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
