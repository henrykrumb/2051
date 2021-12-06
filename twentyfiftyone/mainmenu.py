import os

import pygame
import pygame.freetype
from pygame.locals import *

from .colors import COLORS


class MainMenu:
    def __init__(self, path, gameapplication):
        self.running = True
        self.path = path
        background_path = os.path.join(self.path, 'assets', 'ui', 'background.png')
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (640, 448))
        fontpath = os.path.join(self.path, 'fonts')
        self.font = pygame.freetype.Font(os.path.join(fontpath, 'default.ttf'), 8)
        self.events = []
        self.gameapplication = gameapplication
        self.actions = ['start', 'load', 'exit']
        self.action = 0
        self.texts = [
            self.font.render(action.upper(), COLORS['blue'])[0] for action in self.actions
        ]
        self.texts_select = [
            self.font.render(action.upper(), COLORS['white'])[0] for action in self.actions
        ]
        self.texts = [pygame.transform.scale(t, (t.get_width() * 4, t.get_height() * 4)) for t in self.texts]
        self.texts_select = [pygame.transform.scale(t, (t.get_width() * 4, t.get_height() * 4)) for t in self.texts_select]

    def start_game(self):
        self.gameapplication.state = 'game'

    def update(self):
        def up():
            self.action -= 1
            if self.action < 0:
                self.action = 0

        def down():
            self.action += 1
            if self.action >= len(self.actions):
                self.action = len(self.actions) - 1

        def select():
            if self.actions[self.action] == 'start':
                self.gameapplication.state = 'game'
            elif self.actions[self.action] == 'load':
                self.gameapplication.state = 'load'
            elif self.actions[self.action] == 'exit':
                self.gameapplication.state = 'quit'

        while self.events:
            event = self.events.pop()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    up()
                elif event.key == K_DOWN:
                    down()
                elif event.key == K_SPACE:
                    select()
            elif event.type == JOYAXISMOTION:
                if event.axis == 1:
                    if event.value < -0.1:
                        up()
                    elif event.value > 0.1:
                        down()
            elif event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    select()

    def display(self, screen):
        screen.fill(COLORS['cyan'])
        screen.blit(self.background, (0, 0))
        for i, text in enumerate(self.texts):
            surface = text
            if i == self.action:
                surface = self.texts_select[i]
            x = 640 // 2 - surface.get_width() // 2
            y = 480 // 2 + i * 48 - len(self.texts) * 48 // 2
            screen.blit(surface, (x, y))
