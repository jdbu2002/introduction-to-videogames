from esper import World
from pygame import Vector2

from src.create.prefabs import create_explosion
from src.ecs.components import CSurface, CTransform
from src.ecs.components.tags import CTagBullet, CTagEnemy
from src.types import Explosion


def system_collission_enemy_bullet(world: World, explosion_cfg: Explosion):
    enemy_components = world.get_components(CTransform, CSurface, CTagEnemy)
    bullet_components = world.get_components(CTransform, CSurface, CTagBullet)

    for enemy_entity, (e_c_t, e_c_s, _) in enemy_components:
        enemy_rect = CSurface.get_relative_area(e_c_s.area, e_c_t.pos)

        for bullet_entity, (b_c_t, b_c_s, _) in bullet_components:
            bullet_rect = CSurface.get_relative_area(b_c_s.area, b_c_t.pos)

            if enemy_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)

                create_explosion(world, Vector2(enemy_rect.center), explosion_cfg)
