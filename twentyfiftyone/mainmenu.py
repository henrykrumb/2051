import os

import pygame
import pygame.freetype
from pygame.locals import *

from .colors import COLORS
from .ui import ComponentGroup, Button


class MainMenu:
    def __init__(self, path, gameapplication):
        self.running = True
        self.path = path
        background_path = os.path.join(self.path, "assets", "ui", "background.png")
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (640, 448))
        fontpath = os.path.join(self.path, "fonts")
        font = pygame.freetype.Font(os.path.join(fontpath, "default.ttf"), 8)
        self.events = []
        self.gameapplication = gameapplication

        self.button_group = ComponentGroup()
        self.button_group.components = [
            Button("START", font),
            Button("LOAD", font),
            Button("EXIT", font),
        ]
        self.button_group.pack()
        self.button_group.x = gameapplication.width // 2 - self.button_group.width // 2
        self.button_group.y = gameapplication.height // 2 - self.button_group.height // 2

    def start_game(self):
        self.gameapplication.state = "game"

    def update(self):
        def select(action):
            action = action.lower()
            if action == "start":
                self.gameapplication.state = "game"#"designer"
            elif action == "load":
                self.gameapplication.state = "load"
            elif action == "exit":
                self.gameapplication.state = "quit"

        while self.events:
            event = self.events.pop()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.button_group.on_up()
                elif event.key == K_DOWN:
                    self.button_group.on_down()
                elif event.key == K_SPACE:
                    select(self.button_group.on_activate())
            elif event.type == JOYAXISMOTION:
                if event.axis == 1:
                    if event.value < -0.1:
                        self.button_group.on_up()
                    elif event.value > 0.1:
                        self.button_group.on_down()
            elif event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    select(self.button_group.on_activate())

    def display(self, screen):
        screen.fill(COLORS["cyan"])
        screen.blit(self.background, (0, 0))
        self.button_group.display(screen)
