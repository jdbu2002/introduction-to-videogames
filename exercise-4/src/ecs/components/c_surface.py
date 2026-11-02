from pygame import Color, Rect, Surface, Vector2
from pygame.font import Font


class CSurface:
    def __init__(self, size: Vector2, color: Color) -> None:
        self.surf = Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()

    @classmethod
    def from_surface(cls, surf: Surface):
        c_surf = cls(Vector2(surf.size), Color(0, 0, 0))
        c_surf.surf = surf
        c_surf.area = surf.get_rect()
        return c_surf

    @classmethod
    def from_text(cls, text: str, font: Font, color: Color):
        return cls.from_surface(font.render(text, False, color))

    @staticmethod
    def get_relative_area(area: Rect, topleft: Vector2):
        rect = area.copy()
        rect.topleft = topleft
        return rect
