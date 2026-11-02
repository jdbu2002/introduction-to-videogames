from pygame import Color, Vector2


class CShockwave:
    def __init__(
        self,
        center: Vector2,
        max_radius: float,
        duration: float,
        thickness: int,
        color: Color,
    ) -> None:
        self.center = center.copy()
        self.max_radius = max_radius
        self.duration = duration
        self.thickness = thickness
        self.color = color
        self.elapsed: float = 0
        self.radius: float = 0
