from typing import TypedDict

from .bullet import Bullet
from .enemy import Enemy
from .explosion import Explosion
from .interface import Interface
from .level import Level
from .player import Player
from .special import Special
from .window import Window


class Config(TypedDict):
    window: Window
    enemies: dict[str, Enemy]
    level: Level
    player: Player
    bullet: Bullet
    explosion: Explosion
    interface: Interface
    special: Special
