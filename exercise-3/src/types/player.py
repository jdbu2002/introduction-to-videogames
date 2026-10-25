from typing import TypedDict

from .animations import Animations


class Player(TypedDict):
    image: str
    animations: Animations
    input_velocity: float
