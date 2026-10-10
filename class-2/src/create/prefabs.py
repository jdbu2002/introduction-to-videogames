import math
import random

from esper import World
from pygame import Color, Vector2

from src.ecs.components import CEnemySpawner, CSurface, CTransform, CVelocity
from src.types import Enemy, Level, Player, PlayerSpawn, Position


def create_square(
    world: World, size: Vector2, pos: Vector2, vel: Vector2, color: Color
):
    entity = world.create_entity()

    components: list[CSurface | CVelocity | CTransform] = [
        CTransform(pos),
        CVelocity(vel),
        CSurface(size, color),
    ]

    for component in components:
        world.add_component(entity, component)


def create_enemy_spawner(world: World, enemy_cfg: dict[str, Enemy], level_cgf: Level):
    spawner = world.create_entity()

    world.add_component(spawner, CEnemySpawner(enemy_cfg, level_cgf))


def create_enemy_square(world: World, type: Enemy, position: Position):
    pos = Vector2(position["x"], position["y"])
    color = Color(type["color"]["r"], type["color"]["g"], type["color"]["b"])
    size = Vector2(type["size"]["x"], type["size"]["y"])

    random_angle = math.radians(random.uniform(0, 360))
    random_speed = random.uniform(type["velocity_min"], type["velocity_max"])

    vel = Vector2(
        random_speed * math.cos(random_angle),
        random_speed * math.sin(random_angle),
    )

    create_square(world, size, pos, vel, color)


def create_player_square(world: World, cfg: Player, player_spawn: PlayerSpawn):
    size = Vector2(cfg["size"]["x"], cfg["size"]["y"])

    pos_x = player_spawn["position"]["x"] - size.x / 2
    pos_y = player_spawn["position"]["y"] - size.y / 2

    pos = Vector2(pos_x, pos_y)
    color = Color(cfg["color"]["r"], cfg["color"]["g"], cfg["color"]["b"])
    vel = Vector2(0, 0)

    create_square(world, size, pos, vel, color)
