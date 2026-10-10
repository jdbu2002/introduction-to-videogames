from typing import TypedDict

from .common import Position


class EnemySpawnEvent(TypedDict):
    time: float
    enemy_type: str
    position: Position


class PlayerSpawn(TypedDict):
    position: Position


class Level(TypedDict):
    player_spawn: PlayerSpawn
    enemy_spawn_events: list[EnemySpawnEvent]
