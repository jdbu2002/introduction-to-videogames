from esper import World

from src.ecs.components import CSurface, CTransform
from src.ecs.components.tags import CTagEnemy
from src.types import PlayerSpawn


def system_collission_player_enemy(
    world: World, player_entity: int, player_spawn: PlayerSpawn
):
    components = world.get_components(CTransform, CSurface, CTagEnemy)

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = pl_s.surf.get_rect(topleft=pl_t.pos)

    for enemy_entity, (c_t, c_s, _) in components:
        enemy_rect = c_s.surf.get_rect(topleft=c_t.pos)

        if enemy_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            pl_t.pos.x = player_spawn["position"]["x"] - pl_rect.width / 2
            pl_t.pos.y = player_spawn["position"]["y"] - pl_rect.height / 2
