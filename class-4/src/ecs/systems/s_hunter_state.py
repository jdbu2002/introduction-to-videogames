from esper import World
from pygame import Vector2

from src.ecs.components import CAnimation, CHunterState, CSurface, CTransform, CVelocity
from src.ecs.components.c_hunter_state import HunterState
from src.engine.types import PlayerReference


def system_hunter_state(
    world: World, player_reference: PlayerReference, delta_time: float
):
    components = world.get_components(CTransform, CVelocity, CAnimation, CHunterState)

    player_rect = CSurface.get_relative_area(
        player_reference["c_s"].area, player_reference["c_t"].pos
    )
    player_center = Vector2(player_rect.center)

    for hunter_entity, (c_t, c_v, c_a, c_hs) in components:
        c_s = world.component_for_entity(hunter_entity, CSurface)
        hunter_center = c_t.pos + Vector2(c_s.area.size) / 2

        match c_hs.state:
            case HunterState.IDLE:
                _do_idle_state(c_v, c_a, c_hs, hunter_center, player_center)

            case HunterState.CHASE:
                _do_chase_state(c_t, c_v, c_a, c_hs, hunter_center, player_center)

            case HunterState.RETURN:
                _do_return_state(c_t, c_v, c_a, c_hs, delta_time)


def _do_idle_state(
    c_v: CVelocity,
    c_a: CAnimation,
    c_hs: CHunterState,
    hunter_center: Vector2,
    player_center: Vector2,
):
    c_a.set_animation("IDLE")
    c_v.vel = Vector2(0, 0)

    if hunter_center.distance_to(player_center) <= c_hs.distance_start_chase:
        c_hs.state = HunterState.CHASE


def _do_chase_state(
    c_t: CTransform,
    c_v: CVelocity,
    c_a: CAnimation,
    c_hs: CHunterState,
    hunter_center: Vector2,
    player_center: Vector2,
):
    c_a.set_animation("MOVE")

    if c_t.pos.distance_to(c_hs.origin) >= c_hs.distance_start_return:
        c_hs.state = HunterState.RETURN
        return

    difference = player_center - hunter_center
    if difference.length_squared() == 0:
        c_v.vel = Vector2(0, 0)
        return

    c_v.vel = difference.normalize() * c_hs.velocity_chase


def _do_return_state(
    c_t: CTransform,
    c_v: CVelocity,
    c_a: CAnimation,
    c_hs: CHunterState,
    delta_time: float,
):
    c_a.set_animation("MOVE")

    difference = c_hs.origin - c_t.pos

    if difference.length() <= c_hs.velocity_return * delta_time:
        c_t.pos.update(c_hs.origin)
        c_v.vel = Vector2(0, 0)
        c_hs.state = HunterState.IDLE
        return

    c_v.vel = difference.normalize() * c_hs.velocity_return
