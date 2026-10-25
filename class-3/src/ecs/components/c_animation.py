from src.types import Animations


class CAnimation:
    def __init__(self, animations: Animations) -> None:
        self.number_frames = animations["number_frames"]
        self.animations_list = [
            AnimationData(**animation) for animation in animations["list"]
        ]
        self.current_animation = 0
        self.current_animation_time: float = 0
        self.current_frame = self.animations_list[self.current_animation].start


class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate
