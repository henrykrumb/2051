import pygame
from pygame.locals import *

from .game import Game
from .room import Room

class GameApplication:
    def __init__(self):
        self.sprites = []

    def run(self, game_path):
        pygame.init()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        screen = pygame.display.set_mode((640, 448))
        screen.fill((0, 0, 0))
        clock = pygame.time.Clock()

        game = Game(game_path, parent=self)
        pygame.display.set_caption(game.settings.get('title', 'Adventure'))

        running = True
        while running:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    else:
                        game.events.append(event)
                elif event.type == KEYUP:
                    game.events.append(event)
                elif event.type == JOYBUTTONDOWN:
                    game.events.append(event)
                elif event.type == JOYBUTTONUP:
                    game.events.append(event)
                elif event.type == JOYAXISMOTION:
                    game.events.append(event)
            game.update()
            game.display(screen)
            clock.tick()
        pygame.quit()
        exit(0)

