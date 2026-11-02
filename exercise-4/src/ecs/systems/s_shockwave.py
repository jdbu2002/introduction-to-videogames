import pygame
from esper import World
from pygame import Color, Surface, Vector2

from src.ecs.components import CShockwave, CSurface, CTransform


def system_shockwave(world: World, delta_time: float):
    components = world.get_components(CTransform, CSurface, CShockwave)

    for entity, (c_t, c_s, c_sw) in components:
        c_sw.elapsed += delta_time
        progress = c_sw.elapsed / c_sw.duration

        if progress >= 1:
            world.delete_entity(entity)
            continue

        c_sw.radius = c_sw.max_radius * (1 - (1 - progress) ** 3)
        alpha = int(255 * (1 - progress) ** 1.5)
        radius = int(c_sw.radius)
        thickness = max(1, int(c_sw.thickness * (1 - progress)) + 1)

        size = radius * 2 + 2
        surf = Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)

        c = c_sw.color
        pygame.draw.circle(surf, Color(c.r, c.g, c.b, alpha // 6), center, radius)
        pygame.draw.circle(surf, Color(c.r, c.g, c.b, alpha), center, radius, thickness)
        if radius > thickness + 3:
            pygame.draw.circle(
                surf, Color(255, 255, 255, alpha), center, radius - thickness - 2, 1
            )

        c_s.surf = surf
        c_s.area = surf.get_rect()
        c_t.pos = c_sw.center - Vector2(center)
