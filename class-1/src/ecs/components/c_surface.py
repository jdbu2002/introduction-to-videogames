from pygame import Vector2, Color, Surface

class CSurface:
    def __init__(self, size: Vector2, color: Color) -> None:
        self.surf = Surface(size)
        self.surf.fill(color)
    