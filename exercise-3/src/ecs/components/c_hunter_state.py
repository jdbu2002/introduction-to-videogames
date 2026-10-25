from enum import Enum

from pygame import Vector2

from src.types import Hunter


class HunterState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2


class CHunterState:
    def __init__(self, origin: Vector2, cfg: Hunter) -> None:
        self.state = HunterState.IDLE
        self.origin = origin.copy()
        self.velocity_chase = cfg["velocity_chase"]
        self.velocity_return = cfg["velocity_return"]
        self.distance_start_chase = cfg["distance_start_chase"]
        self.distance_start_return = cfg["distance_start_return"]
