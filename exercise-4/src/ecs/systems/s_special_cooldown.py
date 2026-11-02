from esper import World

from src.ecs.components import CSpecial
from src.engine.service_locator import ServiceLocator
from src.types import Special


def system_special_cooldown(world: World, delta_time: float, special_cfg: Special):
    components = world.get_component(CSpecial)

    for _, c_sp in components:
        c_sp.elapsed += delta_time
        c_sp.denied_time = max(0, c_sp.denied_time - delta_time)
        c_sp.ready_flash_time = max(0, c_sp.ready_flash_time - delta_time)

        if c_sp.is_ready:
            continue

        c_sp.time_left -= delta_time
        if c_sp.is_ready:
            c_sp.time_left = 0
            c_sp.ready_flash_time = 0.3
            ServiceLocator.sounds_service.play(special_cfg["sound_ready"])
