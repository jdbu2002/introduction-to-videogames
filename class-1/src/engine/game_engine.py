import pygame
from pygame import Vector2, Color
from esper import World

from src.create.prefabs import create_square

from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

class GameEngine:
    def __init__(self) -> None:
        pygame.init()

        self.is_running = False
        self.screen = pygame.display.set_mode((640, 360))
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.delta_time: float = 0

        self.ecs_world = World()

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
        create_square(
            world=self.ecs_world,
            size=Vector2(50, 50),
            color=Color(255, 255, 50),
            pos=Vector2(0, 0),
            vel=Vector2(75, 75),
        )

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill((43, 149, 214))

        system_rendering(self.ecs_world, self.screen)

        pygame.display.flip()

    def _clean(self):
        pygame.quit()
