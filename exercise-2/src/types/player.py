from typing import TypedDict

from .common import Color, EntitySize


class Player(TypedDict):
    size: EntitySize
    color: Color
    input_velocity: float
