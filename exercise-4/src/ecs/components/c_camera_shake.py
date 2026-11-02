from pygame import Vector2


class CCameraShake:
    def __init__(self) -> None:
        self.duration: float = 0
        self.intensity: float = 0
        self.time_left: float = 0
        self.offset = Vector2(0, 0)

    def shake(self, duration: float, intensity: float):
        self.duration = duration
        self.intensity = intensity
        self.time_left = duration
