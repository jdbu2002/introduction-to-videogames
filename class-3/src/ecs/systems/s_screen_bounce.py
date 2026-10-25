from esper import World
from pygame import Rect, Surface

from src.ecs.components import CSurface, CTransform, CVelocity
from src.ecs.components.tags import CTagEnemy


def system_screen_bounce(world: World, screen: Surface):
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)
    screen_rect = screen.get_rect()

    def clamp_into_screen(rect: Rect, c_t: CTransform):
        rect.clamp_ip(screen_rect)
        c_t.pos.x = rect.x
        c_t.pos.y = rect.y

    for _, (c_t, c_v, c_s, _) in components:
        rect = CSurface.get_relative_area(c_s.area, c_t.pos)

        if rect.left < 0 or rect.right > screen_rect.width:
            c_v.vel.x *= -1
            clamp_into_screen(rect, c_t)

        if rect.top < 0 or rect.bottom > screen_rect.height:
            c_v.vel.y *= -1
            clamp_into_screen(rect, c_t)
