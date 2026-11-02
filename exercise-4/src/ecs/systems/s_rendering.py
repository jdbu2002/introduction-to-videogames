from esper import World
from pygame import Surface, Vector2

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags import CTagUI


def system_rendering(world: World, screen: Surface, offset: Vector2):
    components = world.get_components(CTransform, CSurface)

    for entity, (c_t, c_s) in components:
        if not world.has_component(entity, CTagUI):
            screen.blit(c_s.surf, c_t.pos + offset, c_s.area)


def system_rendering_ui(world: World, screen: Surface):
    components = sorted(world.get_components(CTransform, CSurface, CTagUI))

    for _, (c_t, c_s, _) in components:
        screen.blit(c_s.surf, c_t.pos, c_s.area)
