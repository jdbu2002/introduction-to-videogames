from esper import World

from src.ecs.components import CAnimation, CPlayerState, CVelocity
from src.ecs.components.c_player_state import PlayerState
from src.engine.service_locator import ServiceLocator
from src.types import Player


def system_player_state(world: World, player_cfg: Player):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)

    for _, (c_v, c_a, c_ps) in components:
        match c_ps.state:
            case PlayerState.IDLE:
                _do_idle_state(c_v, c_a, c_ps, player_cfg)

            case PlayerState.MOVE:
                _do_move_state(c_v, c_a, c_ps)


def _do_idle_state(
    c_v: CVelocity, c_a: CAnimation, c_ps: CPlayerState, player_cfg: Player
):
    c_a.set_animation("IDLE")

    if c_v.vel.magnitude_squared() > 0:
        ServiceLocator.sounds_service.play(player_cfg["sound_move"])
        c_ps.state = PlayerState.MOVE


def _do_move_state(c_v: CVelocity, c_a: CAnimation, c_ps: CPlayerState):
    c_a.set_animation("MOVE")

    if c_v.vel.magnitude_squared() <= 0:
        c_ps.state = PlayerState.IDLE
