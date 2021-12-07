import os

import pygame
import pygame.freetype
from pygame.locals import *

from .character import Character
from .colors import COLORS
from .sprite import Sprite
from .ui import *


class CharacterDesigner:
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

        self.component_group = ComponentGroup()
        self.component_group.components = [
            Select('hair style:', ['long', 'short'], self.font),
            Select('hair color:', ['black', 'red', 'brown', 'yellow'], self.font),
            Select('skin tone:', ['brown', 'yellow'], self.font),
            Select('shirt color:', ['blue', 'red', 'cyan'], self.font),
            Select('pants color:', ['blue', 'red', 'cyan'], self.font),
            Button('START', self.font)
        ]
        self.component_group.pack()
        self.component_group.x = 640 // 2 - self.component_group.width // 2 + 128
        self.component_group.y = 448 // 2 - self.component_group.height // 2
        self.make_character()

    def start_game(self):
        self.gameapplication.state = 'game'

    def make_character(self):
        kwargs = {
            'hair_style': self.component_group.components[0].get_option(),
            'hair_color': self.component_group.components[1].get_option(),
            'skin_tone': self.component_group.components[2].get_option(),
            'shirt_color': self.component_group.components[3].get_option(),
            'pants_color': self.component_group.components[4].get_option()
        }
        self.character = Character(os.path.join(self.path, 'assets', 'characters'), **kwargs)

    def update(self):
        def select(action):
            if action == 'START':
                self.gameapplication.game.player.set_character(self.character)
                self.gameapplication.state = 'game'

        while self.events:
            event = self.events.pop()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.component_group.on_up()
                elif event.key == K_DOWN:
                    self.component_group.on_down()
                elif event.key == K_LEFT:
                    self.component_group.on_left()
                    self.make_character()
                elif event.key == K_RIGHT:
                    self.component_group.on_right()
                    self.make_character()
                elif event.key == K_SPACE:
                    select(self.component_group.on_activate())
            elif event.type == JOYAXISMOTION:
                if event.axis == 1:
                    if event.value < -0.1:
                        self.component_group.on_up()
                    elif event.value > 0.1:
                        self.component_group.on_down()
            elif event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    select(self.component_group.on_activate())

    def display(self, screen):
        screen.fill(COLORS['cyan'])
        screen.blit(self.background, (0, 0))
        self.component_group.display(screen)
        sprite = Sprite(self.character.surface, 4)
        sprite.x = 16 * 2
        sprite.y = 16 * 3
        sprite.frame_w = 9
        sprite.frame_h = 26
        sprite.display(screen)
