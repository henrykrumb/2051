import os

import pygame

from .colors import replace_pair


class Character:
    def __init__(self, template_location, **kwargs):
        template = kwargs.pop("template", "human")
        skin_tone = kwargs.pop("skin_tone", "brown")
        hair_color = kwargs.pop("hair_color", "black")
        hair_style = kwargs.pop("hair_style", "long")
        shirt_color = kwargs.pop("shirt_color", "red")
        pants_color = kwargs.pop("pants_color", "blue")

        self.surface = pygame.image.load(
            os.path.join(template_location, f"{template}.png")
        )
        self.pants = pygame.image.load(os.path.join(template_location, "pants.png"))
        self.hair = pygame.image.load(
            os.path.join(template_location, f"hair_{hair_style}.png")
        )
        self.shirt = pygame.image.load(os.path.join(template_location, "shirt.png"))

        self.surface = replace_pair(self.surface, "yellow", skin_tone)
        self.pants = replace_pair(self.pants, "magenta", pants_color)
        self.shirt = replace_pair(self.shirt, "magenta", shirt_color)
        self.hair = replace_pair(self.hair, "black", hair_color)

        self.surface.blit(self.pants, (0, 0))
        self.surface.blit(self.shirt, (0, 0))
        self.surface.blit(self.hair, (0, 0))
