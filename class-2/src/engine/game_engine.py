import json
from os import path

import pygame
from esper import World
from pygame import Color

from src.create.prefabs import create_enemy_spawner, create_player_square
from src.ecs.systems import (
    system_enemy_spawner,
    system_movement,
    system_rendering,
    system_screen_bounce,
)
from src.types import Config, Enemy, Level, Player, Window


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

        self.clock = pygame.time.Clock()
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
        create_player_square(
            self.world, self.config["player"], self.config["level"]["player_spawn"]
        )
        create_enemy_spawner(self.world, self.config["enemies"], self.config["level"])

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.world, self.delta_time)
        system_movement(self.world, self.delta_time)
        system_screen_bounce(self.world, self.screen)

    def _draw(self):
        self.screen.fill(self.bg_color)

        system_rendering(self.world, self.screen)

        pygame.display.flip()

    def _clean(self):
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

        self.config = {
            "window": window,
            "enemies": enemies,
            "level": level,
            "player": player,
        }
