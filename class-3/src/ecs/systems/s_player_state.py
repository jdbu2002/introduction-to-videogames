from esper import World

from src.ecs.components import CAnimation, CPlayerState, CVelocity
from src.ecs.components.c_player_state import PlayerState


def system_player_state(world: World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)

    for _, (c_v, c_a, c_ps) in components:
        match c_ps.state:
            case PlayerState.IDLE:
                _do_idle_state(c_v, c_a, c_ps)

            case PlayerState.MOVE:
                _do_move_state(c_v, c_a, c_ps)


def _do_idle_state(c_v: CVelocity, c_a: CAnimation, c_ps: CPlayerState):
    _set_animation(c_a, 1)

    if c_v.vel.magnitude_squared() > 0:
        c_ps.state = PlayerState.MOVE


def _do_move_state(c_v: CVelocity, c_a: CAnimation, c_ps: CPlayerState):
    _set_animation(c_a, 0)

    if c_v.vel.magnitude_squared() <= 0:
        c_ps.state = PlayerState.IDLE


def _set_animation(c_a: CAnimation, index: int):
    if c_a.current_animation == index:
        return

    c_a.current_animation = index
    c_a.current_animation_time = 0
    c_a.current_frame = c_a.animations_list[index].start
