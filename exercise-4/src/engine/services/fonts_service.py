from pygame.font import Font

from src.utils.parse_path import parse_path


class FontsService:
    def __init__(self) -> None:
        self._fonts: dict[tuple[str, int], Font] = {}

    def get(self, path: str, size: int) -> Font:
        key = (path, size)
        if key not in self._fonts:
            self._fonts[key] = Font(parse_path(path), size)
        return self._fonts[key]
