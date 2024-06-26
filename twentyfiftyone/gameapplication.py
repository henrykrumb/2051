import os

import pygame
from pygame.locals import *

from .character_designer import CharacterDesigner
from .game import Game


class GameApplication:
    def __init__(self):
        self.width = 640
        self.height = 448
        self.sprites = []
        pygame.init()
        pygame.joystick.init()
        joysticks = [
            pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())
        ]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.state = "menu"

    def run(self, menu, gamepath):
        self.game = Game(gamepath)
        designer = CharacterDesigner(gamepath, self)
        pygame.display.set_caption(self.game.settings.get("title", "Adventure"))

        icon = None
        try:
            icon = pygame.image.load(
                os.path.join(os.dirname(__file__), "..", "twentyfiftyone.png")
            )
        except:
            try:
                icon = pygame.image.load("/usr/share/icons/twentyfiftyone.png")
            except:
                pass
        if icon:
            pygame.display.set_icon(icon)

        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.mouse.set_visible(False)
        while self.state != "quit":
            pygame.display.update()

            if self.state == "menu":
                receiver = menu
            elif self.state == "designer":
                receiver = designer
            elif self.state == "game":
                receiver = self.game

            events = []
            for event in pygame.event.get():
                if event.type == QUIT:
                    if self.state == "game":
                        self.state = "menu"
                    elif self.state == "designer":
                        self.state = "menu"
                    else:
                        self.state = "quit"
                elif event.type == KEYDOWN:
                    if event.key in (K_ESCAPE, K_q):
                        if self.state == "game":
                            self.state = "menu"
                        elif self.state == "designer":
                            self.state = "menu"
                        else:
                            self.state = "quit"
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
