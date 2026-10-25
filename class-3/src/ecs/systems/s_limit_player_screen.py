from pygame import Surface

from src.engine.types import PlayerReference


def system_limit_player_in_screen(screen: Surface, player_reference: PlayerReference):
    screen_rect = screen.get_rect()
    player_rect = player_reference["c_s"].surf.get_rect(
        topleft=player_reference["c_t"].pos
    )

    if (
        player_rect.left < 0
        or player_rect.right > screen_rect.width
        or player_rect.top < 0
        or player_rect.bottom > screen_rect.height
    ):
        player_rect.clamp_ip(screen_rect)
        player_reference["c_t"].pos.x = player_rect.x
        player_reference["c_t"].pos.y = player_rect.y
