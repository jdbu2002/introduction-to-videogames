from typing import TypedDict


class Enemy(TypedDict):
    image: str
    velocity_min: float
    velocity_max: float
