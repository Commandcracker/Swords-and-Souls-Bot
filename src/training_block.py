#!/usr/bin/python3
# -*- coding: utf-8 -*-

# local modules
from helper import find_rgb, find_closest_point_to_point, get_center

# pip modules
import numpy as np
from display_server_interactions.window import WindowBase


def block(window: WindowBase) -> None:
    img = np.array(window.get_image())

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

                if window.active:
                    window.warp_pointer(int(closest_x), int(closest_y))
            else:
                # star is closest
                closest_x, closest_y = stars[closest_star]

                if window.active:
                    window.warp_pointer(
                        int(width-closest_x), int(height-closest_y))

        else:
            closest_x, closest_y = appels[closest_appel]

            if window.active:
                window.warp_pointer(int(closest_x), int(closest_y))
    elif stars.size > 0:
        closest_star = find_closest_point_to_point(
            stars, center
        )

        closest_x, closest_y = stars[closest_star]

        if window.active:
            window.warp_pointer(
                int(width-closest_x), int(height-closest_y))
