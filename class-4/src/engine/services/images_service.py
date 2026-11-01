from pygame import Surface
from pygame.image import load

from src.utils.parse_path import parse_path


class ImagesService:
    def __init__(self) -> None:
        self._images: dict[str, Surface] = {}

    def get(self, path: str) -> Surface:
        if path not in self._images:
            self._images[path] = load(parse_path(path)).convert_alpha()
        return self._images[path]
