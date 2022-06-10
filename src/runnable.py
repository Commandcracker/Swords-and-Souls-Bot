#!/usr/bin/python3
# -*- coding: utf-8 -*-

# build-in modules
from abc import ABCMeta, abstractmethod
from display_server_interactions.window import WindowBase


class Runnable(object, metaclass=ABCMeta):
    def __init__(self, window: WindowBase) -> None:
        self.window = window

    @abstractmethod
    def run(self):
        pass
