from typing import TypedDict

from src.ecs.components import CSurface, CTransform, CVelocity


class PlayerReference(TypedDict):
    entity: int
    c_v: CVelocity
    c_t: CTransform
    c_s: CSurface
