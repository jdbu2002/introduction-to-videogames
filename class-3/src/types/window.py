from typing import TypedDict

from .common import Color


class Size(TypedDict):
    w: float
    h: float


class Window(TypedDict):
    title: str
    size: Size
    bg_color: Color
    framerate: int
