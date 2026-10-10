from esper import World
from pygame import Color, Vector2
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_square(
    world: World, size: Vector2, pos: Vector2, vel: Vector2, color: Color
):
    cuad_entity = world.create_entity()

    components: list[CSurface | CVelocity | CTransform] = [
        CTransform(pos),
        CVelocity(vel),
        CSurface(size, color),
    ]

    for component in components:
        world.add_component(cuad_entity, component)
