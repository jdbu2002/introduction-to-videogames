from esper import World

from src.create.prefabs import create_enemy_square
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world: World, delta_time: float):
    components = world.get_component(CEnemySpawner)

    for _, c_es in components:
        c_es.current_time += delta_time

        to_spawn = [
            (i, event)
            for i, event in enumerate(c_es.events)
            if event["time"] <= c_es.current_time and i not in c_es.spawned_indexes
        ]

        for i, enemy in to_spawn:
            try:
                enemy_type = c_es.enemy_types[enemy["enemy_type"]]
                create_enemy_square(world, enemy_type, enemy["position"])
            except KeyError as e:
                print("El tipo de enemigo", e, "no existe. Saltando...")
            finally:
                c_es.spawned_indexes.add(i)
