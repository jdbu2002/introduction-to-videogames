from pygame import Color, Surface, Vector2


class CSurface:
    def __init__(self, size: Vector2, color: Color) -> None:
        self.surf = Surface(size)
        self.surf.fill(color)

    @classmethod
    def from_surface(cls, surf: Surface):
        c_surf = cls(Vector2(surf.size), Color(0, 0, 0))
        c_surf.surf = surf
        return c_surf
