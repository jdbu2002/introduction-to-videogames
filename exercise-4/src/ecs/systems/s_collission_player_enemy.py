from esper import World
from pygame import Vector2

from src.create.prefabs import create_explosion
from src.ecs.components import CSurface, CTransform
from src.ecs.components.tags import CTagEnemy
from src.types import Explosion, PlayerSpawn


def system_collission_player_enemy(
    world: World,
    player_entity: int,
    player_spawn: PlayerSpawn,
    explosion_cfg: Explosion,
):
    components = world.get_components(CTransform, CSurface, CTagEnemy)

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = CSurface.get_relative_area(pl_s.area, pl_t.pos)

    for enemy_entity, (c_t, c_s, _) in components:
        enemy_rect = CSurface.get_relative_area(c_s.area, c_t.pos)

        if enemy_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            pl_t.pos.x = player_spawn["position"]["x"] - pl_rect.width / 2
            pl_t.pos.y = player_spawn["position"]["y"] - pl_rect.height / 2

            create_explosion(world, Vector2(enemy_rect.center), explosion_cfg)
