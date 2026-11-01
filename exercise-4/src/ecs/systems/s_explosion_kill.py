from esper import World

from src.ecs.components import CAnimation
from src.ecs.components.tags import CTagExplosion


def system_explosion_kill(world: World):
    components = world.get_components(CAnimation, CTagExplosion)

    for explosion_entity, (c_a, _) in components:
        if c_a.finished:
            world.delete_entity(explosion_entity)
