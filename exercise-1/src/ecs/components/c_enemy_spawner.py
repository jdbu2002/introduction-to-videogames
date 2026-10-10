from src.types.enemy import Enemy
from src.types.level import Level


class CEnemySpawner:
    def __init__(self, enemies: dict[str, Enemy], level: Level) -> None:
        self.enemy_types = enemies
        self.events = sorted(level["enemy_spawn_events"], key=lambda x: x["time"])
        self.spawned_indexes: set[int] = set()
