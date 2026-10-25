import json
from os import path
from typing import cast, get_type_hints

import pygame
from esper import World
from pygame import Color, Vector2
from pygame.time import Clock

from src.create.prefabs import (
    create_bullet_from_player,
    create_enemy_spawner,
    create_player_input,
    create_player_square,
)
from src.ecs.components import CInputCommand, CommandPhase
from src.ecs.components.tags import CTagBullet
from src.ecs.systems import (
    system_animation,
    system_collission_enemy_bullet,
    system_collission_player_enemy,
    system_delete_bullet_in_limit,
    system_enemy_spawner,
    system_limit_player_in_screen,
    system_movement,
    system_player_input,
    system_player_state,
    system_rendering,
    system_screen_bounce,
)
from src.types import Bullet, Config, Enemy, Level, Player, Window

from .types import PlayerReference


class GameEngine:
    def __init__(self) -> None:
        pygame.init()

        self.config: Config
        self._load_config_files()

        pygame.display.set_caption(self.config["window"]["title"])

        self.screen = pygame.display.set_mode(
            (self.config["window"]["size"]["w"], self.config["window"]["size"]["h"])
        )
        self.bg_color = Color(
            self.config["window"]["bg_color"]["r"],
            self.config["window"]["bg_color"]["g"],
            self.config["window"]["bg_color"]["b"],
        )

        self.framerate = self.config["window"]["framerate"]

        self.is_running = False

        self.clock = Clock()
        self.delta_time: float = 0

        self.world = World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._load_player_reference()

        create_enemy_spawner(self.world, self.config["enemies"], self.config["level"])

        create_player_input(self.world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000

    def _process_events(self):
        for event in pygame.event.get():
            system_player_input(self.world, event, self._do_action)

            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.world, self.delta_time)
        system_movement(self.world, self.delta_time)

        system_player_state(self.world)

        system_screen_bounce(self.world, self.screen)
        system_limit_player_in_screen(self.screen, self._player)

        system_collission_player_enemy(
            self.world, self._player["entity"], self.config["level"]["player_spawn"]
        )
        system_collission_enemy_bullet(self.world)
        system_delete_bullet_in_limit(self.world, self.screen)

        system_animation(self.world, self.delta_time)

        self.world._clear_dead_entities()  # type: ignore

    def _draw(self):
        self.screen.fill(self.bg_color)

        system_rendering(self.world, self.screen)

        pygame.display.flip()

    def _clean(self):
        self.world.clear_database()
        pygame.quit()

    def _load_config_files(self):
        file_path = path.dirname(path.abspath(__file__))
        config_folder = path.join(file_path, "../../assets/cfg")

        with open(path.join(config_folder, "window.json")) as f:
            window: Window = json.load(f)

        with open(path.join(config_folder, "enemies.json")) as f:
            enemies: dict[str, Enemy] = json.load(f)

        with open(path.join(config_folder, "level_01.json")) as f:
            level: Level = json.load(f)

        with open(path.join(config_folder, "player.json")) as f:
            player: Player = json.load(f)

        with open(path.join(config_folder, "bullet.json")) as f:
            bullet: Bullet = json.load(f)

        self.config = {
            "window": window,
            "enemies": enemies,
            "level": level,
            "player": player,
            "bullet": bullet,
        }

    def _load_player_reference(self):
        entity = create_player_square(
            self.world, self.config["player"], self.config["level"]["player_spawn"]
        )

        components = get_type_hints(PlayerReference)
        components.pop("entity")

        self._player = cast(
            PlayerReference,
            {
                "entity": entity,
                **{
                    name: self.world.component_for_entity(entity, component)
                    for name, component in components.items()
                },
            },
        )

    def _do_action(self, c_input: CInputCommand):
        match c_input.name:
            case "PLAYER_LEFT":
                self._player["c_v"].vel.x -= (
                    self.config["player"]["input_velocity"] * c_input.phase.value
                )

            case "PLAYER_RIGHT":
                self._player["c_v"].vel.x += (
                    self.config["player"]["input_velocity"] * c_input.phase.value
                )

            case "PLAYER_UP":
                self._player["c_v"].vel.y -= (
                    self.config["player"]["input_velocity"] * c_input.phase.value
                )

            case "PLAYER_DOWN":
                self._player["c_v"].vel.y += (
                    self.config["player"]["input_velocity"] * c_input.phase.value
                )

            case "PLAYER_FIRE":
                if c_input.phase == CommandPhase.START:
                    components = self.world.get_component(CTagBullet)
                    bullet_amount = len(components)

                    if (
                        bullet_amount
                        < self.config["level"]["player_spawn"]["max_bullets"]
                    ):
                        mouse_pos = Vector2(pygame.mouse.get_pos())
                        create_bullet_from_player(
                            self.world, self._player, self.config["bullet"], mouse_pos
                        )

            case _:
                pass
