from typing import TypedDict

from .animations import Animations


class Explosion(TypedDict):
    image: str
    animations: Animations
