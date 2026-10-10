from typing import TypedDict

from .common import Position


class Level(TypedDict):
    enemy_spawn_events: list[SpawnEvent]


class SpawnEvent(TypedDict):
    time: float
    enemy_type: str
    position: Position
