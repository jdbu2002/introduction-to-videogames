import math
import random

import pygame
from esper import World
from pygame import Color, Surface, Vector2

from src.ecs.components import (
    CEnemySpawner,
    CInputCommand,
    CSurface,
    CTransform,
    CVelocity,
)
from src.ecs.components.tags import CTagBullet, CTagEnemy, CTagPlayer
from src.engine.types import PlayerReference
from src.types import (
    Bullet,
    Enemy,
    Level,
    Player,
    PlayerSpawn,
    Position,
)
from src.utils.load_image import load_image


def create_square(
    world: World, size: Vector2, pos: Vector2, vel: Vector2, color: Color
):
    return world.create_entity(CTransform(pos), CVelocity(vel), CSurface(size, color))


def create_enemy_spawner(world: World, enemy_cfg: dict[str, Enemy], level_cgf: Level):
    return world.create_entity(CEnemySpawner(enemy_cfg, level_cgf))


def create_enemy_square(world: World, type: Enemy, position: Position):
    pos = Vector2(position["x"], position["y"])

    surface = load_image(type["image"])

    random_angle = math.radians(random.uniform(0, 360))
    random_speed = random.uniform(type["velocity_min"], type["velocity_max"])

    vel = Vector2(math.cos(random_angle), math.sin(random_angle)) * random_speed

    entity = create_sprite(world, pos, vel, surface)
    world.add_component(entity, CTagEnemy())

    return entity


def create_sprite(world: World, pos: Vector2, vel: Vector2, surf: Surface):
    return world.create_entity(
        CTransform(pos), CVelocity(vel), CSurface.from_surface(surf)
    )


def create_player_square(world: World, cfg: Player, player_spawn: PlayerSpawn):
    surf = load_image(cfg["image"])
    size = Vector2(surf.size)

    pos = (
        Vector2(player_spawn["position"]["x"], player_spawn["position"]["y"]) - size / 2
    )
    vel = Vector2(0, 0)

    entity = create_sprite(world, pos, vel, surf)
    world.add_component(entity, CTagPlayer())

    return entity


def create_player_input(world: World):
    inputs = [
        ("PLAYER_UP", pygame.K_UP),
        ("PLAYER_RIGHT", pygame.K_RIGHT),
        ("PLAYER_DOWN", pygame.K_DOWN),
        ("PLAYER_LEFT", pygame.K_LEFT),
        ("PLAYER_FIRE", pygame.BUTTON_LEFT),
    ]

    for input in inputs:
        world.create_entity(CInputCommand(*input))


def create_bullet_from_player(
    world: World, player_ref: PlayerReference, bullet_conf: Bullet, mouse_pos: Vector2
):
    player_rect = player_ref["c_s"].surf.get_rect(topleft=player_ref["c_t"].pos)

    surf = load_image(bullet_conf["image"])
    size = Vector2(surf.size)
    player_center = Vector2(player_rect.center)

    difference = mouse_pos - player_center
    if difference.length_squared() == 0:
        return

    vel = difference.normalize() * bullet_conf["velocity"]

    pos = player_center - size / 2

    entity = create_sprite(world, pos, vel, surf)
    world.add_component(entity, CTagBullet())

    return entity
