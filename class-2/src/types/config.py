from typing import TypedDict

from .enemy import Enemy
from .level import Level
from .player import Player
from .window import Window


class Config(TypedDict):
    window: Window
    enemies: dict[str, Enemy]
    level: Level
    player: Player
