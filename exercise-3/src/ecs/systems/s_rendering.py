from esper import World
from pygame import Surface

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_rendering(world: World, screen: Surface):
    components = world.get_components(CTransform, CSurface)

    for _, (c_t, c_s) in components:
        screen.blit(c_s.surf, c_t.pos, c_s.area)
