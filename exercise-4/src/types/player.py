from typing import TypedDict

from .animations import Animations


class Player(TypedDict):
    image: str
    sound_move: str
    animations: Animations
    input_velocity: float
