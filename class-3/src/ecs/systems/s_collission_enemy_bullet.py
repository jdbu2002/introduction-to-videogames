from esper import World

from src.ecs.components import CSurface, CTransform
from src.ecs.components.tags import CTagBullet, CTagEnemy


def system_collission_enemy_bullet(world: World):
    enemy_components = world.get_components(CTransform, CSurface, CTagEnemy)
    bullet_components = world.get_components(CTransform, CSurface, CTagBullet)

    for enemy_entity, (e_c_t, e_c_s, _) in enemy_components:
        for bullet_entity, (b_c_t, b_c_s, _) in bullet_components:
            enemy_rect = e_c_s.surf.get_rect(topleft=e_c_t.pos)
            bullet_rect = b_c_s.surf.get_rect(topleft=b_c_t.pos)

            if enemy_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
