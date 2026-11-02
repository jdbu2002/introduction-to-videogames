from typing import TypedDict

from .common import Color


class Shake(TypedDict):
    duration: float
    intensity: float


class Special(TypedDict):
    cooldown: float
    duration: float
    max_radius: float
    thickness: int
    color: Color
    sound: str
    sound_ready: str
    sound_denied: str
    shake: Shake
