import math
import random

from esper import World
from pygame import Color, Vector2

from src.create.prefabs import create_square
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world: World, total_time: float):
    components = world.get_component(CEnemySpawner)

    for _, c_es in components:
        to_spawn = [
            (i, event)
            for i, event in enumerate(c_es.events)
            if event["time"] <= total_time and i not in c_es.spawned_indexes
        ]

        for i, enemy in to_spawn:
            type = c_es.enemy_types[enemy["enemy_type"]]
            pos = Vector2(enemy["position"]["x"], enemy["position"]["y"])
            color = Color(type["color"]["r"], type["color"]["g"], type["color"]["b"])

            size = Vector2(type["size"]["x"], type["size"]["y"])

            random_angle = random.uniform(0, 360)
            random_speed = random.uniform(type["velocity_min"], type["velocity_max"])

            vel = Vector2(
                random_speed * math.cos(random_angle),
                random_speed * math.sin(random_angle),
            )

            create_square(world, size, pos, vel, color)
            c_es.spawned_indexes.add(i)
