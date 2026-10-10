from typing import TypedDict

from .common import Color


class Size(TypedDict):
    x: float
    y: float


class Enemy(TypedDict):
    size: Size
    color: Color
    velocity_min: float
    velocity_max: float
