from typing import TypedDict

from .common import Color, EntitySize


class Bullet(TypedDict):
    size: EntitySize
    color: Color
    velocity: float
