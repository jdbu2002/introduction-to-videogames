from typing import TypedDict

from .common import Color, EntitySize


class Enemy(TypedDict):
    size: EntitySize
    color: Color
    velocity_min: float
    velocity_max: float
