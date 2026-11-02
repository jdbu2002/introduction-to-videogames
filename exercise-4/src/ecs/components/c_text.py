from pygame import Color, Rect, Vector2
from pygame.font import Font


class CText:
    def __init__(self, font: Font, color: Color, anchor: str, position: Vector2):
        self.font = font
        self.color = color
        self.anchor = anchor
        self.position = position.copy()

    def get_anchored_pos(self, area: Rect):
        rect = area.copy()
        setattr(rect, self.anchor, (self.position.x, self.position.y))
        return Vector2(rect.topleft)
