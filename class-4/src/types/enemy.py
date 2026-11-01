from typing import TypedDict

from .animations import Animations


class Asteroid(TypedDict):
    image: str
    velocity_min: float
    velocity_max: float


class Hunter(TypedDict):
    image: str
    animations: Animations
    velocity_chase: float
    velocity_return: float
    distance_start_chase: float
    distance_start_return: float


Enemy = Asteroid | Hunter
