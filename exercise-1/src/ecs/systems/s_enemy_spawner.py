import math
import random

from esper import World
from pygame import Color, Vector2

from src.create.prefabs import create_square
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
                type = c_es.enemy_types[enemy["enemy_type"]]
                pos = Vector2(enemy["position"]["x"], enemy["position"]["y"])
                color = Color(
                    type["color"]["r"], type["color"]["g"], type["color"]["b"]
                )

                size = Vector2(type["size"]["x"], type["size"]["y"])

                random_angle = math.radians(random.uniform(0, 360))
                random_speed = random.uniform(
                    type["velocity_min"], type["velocity_max"]
                )

                vel = Vector2(
                    random_speed * math.cos(random_angle),
                    random_speed * math.sin(random_angle),
                )

                create_square(world, size, pos, vel, color)
            except KeyError as e:
                print("El enemigo", e, "no existe. Saltando...")
            finally:
                c_es.spawned_indexes.add(i)
