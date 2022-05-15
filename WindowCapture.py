#!/usr/bin/python3
# -*- coding: utf-8 -*-

# built-in modules
import time

# pip modules
import Xlib
import Xlib.display
import Xlib.XK
import numpy as np


def warp_pointer(x: int, y: int) -> None:
    """
    Move the pointer to the given coordinates.
    """
    display = Xlib.display.Display()
    display_root = display.screen().root
    display_root.warp_pointer(x, y)
    display.sync()


def get_active_window() -> Xlib.display.Display:
    """
    Return the active window.
    """
    display = Xlib.display.Display()
    display_root = display.screen().root
    NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')

    win_id = display_root.get_full_property(
        NET_ACTIVE_WINDOW,
        Xlib.X.AnyPropertyType
    ).value[0]

    try:
        return display.create_resource_object('window', win_id)
    except Xlib.error.XError:
        pass


class WindowCapture(object):
    def __init__(self, window: Xlib.display.Display = None):
        if window is None:
            self.window = get_active_window()
        else:
            self.window = window

    def get_image(self, x: int = None, y: int = None, width: int = None, height: int = None) -> np.ndarray:
        """
        Return the image of the window as a numpy array.
        """
        geom = self.window.get_geometry()

        x = x or geom.x
        y = y or geom.y
        width = width or geom.width
        height = height or geom.height

        img = self.window.get_image(
            x, y,
            width, height,
            Xlib.X.ZPixmap, 0xffffffff
        )
        img = np.frombuffer(img.data, dtype=np.uint8)
        img = img.reshape(height, width, 4)
        img = img[..., :3]  # drop the alpha channel
        img = np.ascontiguousarray(img)  # make image Contiguous
        return img

    def send_key(self, key: chr) -> None:
        """
        Send a key to the window.
        """
        display = Xlib.display.Display()
        display_root = display.screen().root

        keysym = Xlib.XK.string_to_keysym(key)
        keycode = display.keysym_to_keycode(keysym)

        event = Xlib.protocol.event.KeyPress(
            time=int(time.time()),
            root=display_root,
            window=self.window,
            same_screen=0, child=Xlib.X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=Xlib.X.ShiftMask if key.isupper() else 0,
            detail=keycode
        )
        self.window.send_event(event, propagate=True)

    def send_string(self, string: str):
        """
        Send a string to the window.
        """
        for char in string:
            self.send_key(char)

    def is_active(self) -> bool:
        """
        Returns True if the window is active.
        """
        return self.window.id == get_active_window().id

    def warp_pointer(self, x: int, y: int) -> None:
        """
        Move the pointer to the given coordinates.
        """
        self.window.warp_pointer(x, y)

    def get_window_name(self) -> str:
        """
        Return the name of the window.
        """
        window_name = self.window.get_wm_name()

        if len(window_name) == 0:
            dispaly = Xlib.display.Display()
            window_name = self.window.get_property(
                dispaly.get_atom("WM_NAME"),
                dispaly.get_atom("UTF8_STRING"), 0, 1024
            ).value.decode('utf-8')

        return window_name

    def get_window_pid(self) -> int:
        """
        Return the pid of the window.
        """
        display = Xlib.display.Display()

        window_pid = self.window.get_full_property(
            display.get_atom("_NET_WM_PID"),
            Xlib.X.AnyPropertyType
        ).value[0]

        return window_pid
