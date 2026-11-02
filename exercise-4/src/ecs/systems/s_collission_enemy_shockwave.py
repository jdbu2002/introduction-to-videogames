from esper import World
from pygame import Vector2

from src.create.prefabs import create_explosion
from src.ecs.components import CShockwave, CSurface, CTransform
from src.ecs.components.tags import CTagEnemy
from src.types import Explosion


def system_collission_enemy_shockwave(world: World, explosion_cfg: Explosion):
    shockwaves = world.get_component(CShockwave)
    enemy_components = world.get_components(CTransform, CSurface, CTagEnemy)

    for _, c_sw in shockwaves:
        for enemy_entity, (c_t, c_s, _) in enemy_components:
            enemy_rect = CSurface.get_relative_area(c_s.area, c_t.pos)
            enemy_center = Vector2(enemy_rect.center)
            reach = c_sw.radius + max(enemy_rect.w, enemy_rect.h) / 2

            if enemy_center.distance_to(c_sw.center) <= reach:
                world.delete_entity(enemy_entity)
                create_explosion(world, enemy_center, explosion_cfg)
