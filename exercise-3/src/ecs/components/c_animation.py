from src.types import Animations


class CAnimation:
    def __init__(self, animations: Animations) -> None:
        self.number_frames = animations["number_frames"]
        self.animations_list = [
            AnimationData(**animation) for animation in animations["list"]
        ]
        self.current_animation = 0
        self.current_animation_time = self.animations_list[0].framerate
        self.current_frame = self.animations_list[0].start
        self.finished = False

    def set_animation(self, name: str):
        index = next(
            i
            for i, animation in enumerate(self.animations_list)
            if animation.name == name
        )

        if self.current_animation == index:
            return

        self.current_animation = index
        self.current_animation_time = self.animations_list[index].framerate
        self.current_frame = self.animations_list[index].start
        self.finished = False


class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate
