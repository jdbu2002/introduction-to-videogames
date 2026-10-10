import json
from os import path

import pygame
from esper import World
from pygame import Color

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.types.enemy import Enemy
from src.types.level import Level
from src.types.window import Window

file_path = path.dirname(path.abspath(__file__))
config_folder = path.join(file_path, "../../assets/cfg")


class GameEngine:
    def __init__(self) -> None:
        pygame.init()

        self.is_running = False

        self._load_screen_config()

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
        spawner = self.world.create_entity()

        with open(path.join(config_folder, "enemies.json")) as f:
            enemies: dict[str, Enemy] = json.load(f)

        with open(path.join(config_folder, "level_01.json")) as f:
            level: Level = json.load(f)

        self.world.add_component(spawner, CEnemySpawner(enemies, level))

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

    def _load_screen_config(self):
        with open(path.join(config_folder, "window.json")) as f:
            config: Window = json.load(f)

        pygame.display.set_caption(config["title"])

        size = (config["size"]["w"], config["size"]["h"])
        self.screen = pygame.display.set_mode(size)
        self.bg_color = Color(
            config["bg_color"]["r"], config["bg_color"]["g"], config["bg_color"]["b"]
        )

        self.framerate = config["framerate"]
