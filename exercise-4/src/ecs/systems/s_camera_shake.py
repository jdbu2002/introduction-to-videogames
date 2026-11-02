import random

from esper import World

from src.ecs.components import CCameraShake


def system_camera_shake(world: World, delta_time: float):
    for _, c_cs in world.get_component(CCameraShake):
        if c_cs.time_left <= 0:
            c_cs.offset.update(0, 0)
            continue

        c_cs.time_left -= delta_time
        strength = c_cs.intensity * max(0, c_cs.time_left / c_cs.duration)
        c_cs.offset.update(
            random.uniform(-strength, strength), random.uniform(-strength, strength)
        )
