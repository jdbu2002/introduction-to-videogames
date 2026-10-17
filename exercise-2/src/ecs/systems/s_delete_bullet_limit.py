from esper import World
from pygame import Surface

from src.ecs.components import CSurface, CTransform
from src.ecs.components.tags import CTagBullet


def system_delete_bullet_in_limit(world: World, screen: Surface):
    screen_rect = screen.get_rect()

    components = world.get_components(CTransform, CSurface, CTagBullet)

    for bullet_entity, (c_t, c_s, _) in components:
        bullet_rect = c_s.surf.get_rect(topleft=c_t.pos)

        if (
            bullet_rect.left < 0
            or bullet_rect.right > screen_rect.width
            or bullet_rect.top < 0
            or bullet_rect.bottom > screen_rect.height
        ):
            world.delete_entity(bullet_entity)
