import asyncio
from typing import cast, get_type_hints

import pygame
from esper import World
from pygame import Color, Vector2
from pygame.time import Clock

from src.create.prefabs import (
    create_bullet_from_player,
    create_camera,
    create_enemy_spawner,
    create_interface,
    create_pause_screen,
    create_player_input,
    create_player_square,
    create_shockwave,
    create_special,
)
from src.ecs.components import (
    CCameraShake,
    CInputCommand,
    CommandPhase,
    CSpecial,
    CSurface,
)
from src.ecs.components.tags import CTagBullet
from src.ecs.systems import (
    system_animation,
    system_camera_shake,
    system_collission_enemy_bullet,
    system_collission_enemy_shockwave,
    system_collission_player_enemy,
    system_delete_bullet_in_limit,
    system_enemy_spawner,
    system_explosion_kill,
    system_hunter_state,
    system_limit_player_in_screen,
    system_movement,
    system_player_input,
    system_player_state,
    system_rendering,
    system_rendering_ui,
    system_screen_bounce,
    system_shockwave,
    system_special_cooldown,
    system_special_hud,
)
from src.engine.service_locator import ServiceLocator
from src.types import Config, Hunter

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
        self.is_paused = False
        self._pause_entities: list[int] = []

        self.clock = Clock()
        self.delta_time: float = 0

        self.world = World()

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self._load_player_reference()

        create_enemy_spawner(self.world, self.config["enemies"], self.config["level"])

        create_player_input(self.world)

        create_interface(self.world, self.config["interface"])

        special_entity = create_special(
            self.world, self.config["special"], self.config["interface"]
        )
        self._special = self.world.component_for_entity(special_entity, CSpecial)

        camera_entity = create_camera(self.world)
        self._camera = self.world.component_for_entity(camera_entity, CCameraShake)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000

    def _process_events(self):
        for event in pygame.event.get():
            system_player_input(self.world, event, self._do_action)

            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        if self.is_paused:
            return

        system_enemy_spawner(self.world, self.delta_time)
        system_movement(self.world, self.delta_time)

        system_player_state(self.world, self.config["player"])
        system_hunter_state(
            self.world,
            self._player,
            self.delta_time,
            cast(Hunter, self.config["enemies"]["Hunter"]),
        )

        system_screen_bounce(self.world, self.screen)
        system_limit_player_in_screen(self.screen, self._player)

        system_collission_player_enemy(
            self.world,
            self._player["entity"],
            self.config["level"]["player_spawn"],
            self.config["explosion"],
        )
        system_collission_enemy_bullet(self.world, self.config["explosion"])
        system_collission_enemy_shockwave(self.world, self.config["explosion"])
        system_delete_bullet_in_limit(self.world, self.screen)

        system_shockwave(self.world, self.delta_time)
        system_special_cooldown(self.world, self.delta_time, self.config["special"])
        system_camera_shake(self.world, self.delta_time)

        system_animation(self.world, self.delta_time)
        system_explosion_kill(self.world)

        system_special_hud(self.world, self.config["interface"])

        self.world._clear_dead_entities()  # type: ignore

    def _draw(self):
        self.screen.fill(self.bg_color)

        system_rendering(self.world, self.screen, self._camera.offset)
        system_rendering_ui(self.world, self.screen)

        pygame.display.flip()

    def _clean(self):
        self.world.clear_database()
        pygame.quit()

    def _load_config_files(self):
        configs = ServiceLocator.configs_service

        self.config = {
            "window": configs.get("assets/cfg/window.json"),
            "enemies": configs.get("assets/cfg/enemies.json"),
            "level": configs.get("assets/cfg/level_01.json"),
            "player": configs.get("assets/cfg/player.json"),
            "bullet": configs.get("assets/cfg/bullet.json"),
            "explosion": configs.get("assets/cfg/explosion.json"),
            "interface": configs.get("assets/cfg/interface.json"),
            "special": configs.get("assets/cfg/special.json"),
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
                if c_input.phase == CommandPhase.START and not self.is_paused:
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

            case "PLAYER_SPECIAL":
                if c_input.phase == CommandPhase.START and not self.is_paused:
                    self._fire_special()

            case "PAUSE":
                if c_input.phase == CommandPhase.START:
                    self._toggle_pause()

            case _:
                pass

    def _fire_special(self):
        if not self._special.is_ready:
            self._special.denied_time = 0.25
            ServiceLocator.sounds_service.play(self.config["special"]["sound_denied"])
            return

        self._special.time_left = self._special.cooldown

        player_rect = CSurface.get_relative_area(
            self._player["c_s"].area, self._player["c_t"].pos
        )
        create_shockwave(
            self.world, Vector2(player_rect.center), self.config["special"]
        )

        shake = self.config["special"]["shake"]
        self._camera.shake(shake["duration"], shake["intensity"])

    def _toggle_pause(self):
        self.is_paused = not self.is_paused

        if self.is_paused:
            ServiceLocator.sounds_service.pause_all()
            self._pause_entities = create_pause_screen(
                self.world, self.config["interface"], Vector2(self.screen.get_size())
            )
        else:
            ServiceLocator.sounds_service.resume_all()
            for entity in self._pause_entities:
                self.world.delete_entity(entity, immediate=True)
            self._pause_entities = []
