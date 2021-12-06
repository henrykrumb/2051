import os

import pygame
from pygame.locals import *

from .game import Game
from .room import Room


class GameApplication:
    def __init__(self):
        self.sprites = []
        pygame.init()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.screen = pygame.display.set_mode((640, 448))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.state = 'menu'

    def run(self, menu, gamepath):
        game = Game(gamepath)
        pygame.display.set_caption(game.settings.get('title', 'Adventure'))

        icon = None
        try:
            icon = pygame.image.load(os.path.join(os.dirname(__file__), '..', 'twentyfiftyone.png'))
        except:
            try:
                icon = pygame.image.load('/usr/share/icons/twentyfiftyone.png')
            except:
                pass
        if icon:
            pygame.display.set_icon(icon)

        while self.state != 'quit':
            pygame.display.update()

            if self.state == 'menu':
                receiver = menu
            elif self.state == 'game':
                receiver = game

            events = []
            for event in pygame.event.get():
                if event.type == QUIT:
                    if self.state == 'game':
                        self.state = 'menu'
                    else:
                        self.state = 'quit'
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.state == 'game':
                            self.state = 'menu'
                        else:
                            self.state = 'quit'
                    else:
                        events.append(event)
                elif event.type == KEYUP:
                    events.append(event)
                elif event.type == JOYBUTTONDOWN:
                    events.append(event)
                elif event.type == JOYBUTTONUP:
                    events.append(event)
                elif event.type == JOYAXISMOTION:
                    events.append(event)
            receiver.events = events
            new_state = receiver.update()
            receiver.display(self.screen)
            self.clock.tick()
        pygame.quit()
        exit(0)

