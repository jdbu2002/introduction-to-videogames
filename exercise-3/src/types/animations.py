from typing import TypedDict


class Animation(TypedDict):
    name: str
    start: int
    end: int
    framerate: int


class Animations(TypedDict):
    number_frames: int
    list: list[Animation]
