from pygame.mixer import Sound

from src.utils.parse_path import parse_path


class SoundsService:
    def __init__(self) -> None:
        self._sounds: dict[str, Sound] = {}

    def play(self, path: str):
        try:
            if path not in self._sounds:
                self._sounds[path] = Sound(parse_path(path))
            self._sounds[path].play()
        except FileNotFoundError:
            print("Sound not found. Skipping!")
