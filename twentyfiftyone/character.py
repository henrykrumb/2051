import os

import pygame

from .colors import COLORS, make_pair


def replace_color(image, color_old, color_new):
    if isinstance(color_old, str):
        color_old = COLORS[color_old]
    if isinstance(color_new, str):
        color_new = COLORS[color_new]
    w, h = image.get_size()
    for x in range(w):
        for y in range(h):
            if image.get_at((x, y)) == color_old:
                image.set_at((x, y), pygame.Color(color_new))
    return image


def replace_pair(image, color_old, color_new):
    color_old_dark, color_old_light = make_pair(color_old)
    color_new_dark, color_new_light = make_pair(color_new)
    image = replace_color(image, color_old_dark, color_new_dark)
    image = replace_color(image, color_old_light, color_new_light)
    return image


class Character:
    def __init__(self, template_location, **kwargs):
        hair_color = kwargs.pop('hair_color', 'black')
        hair_style = kwargs.pop('hair_style', 'long')
        shirt_color = kwargs.pop('shirt_color', 'cyan')
        pants_color = kwargs.pop('pants_color', 'blue')

        self.surface = pygame.image.load(os.path.join(template_location, 'human.png'))
        self.pants = pygame.image.load(os.path.join(template_location, 'pants.png'))
        self.hair = pygame.image.load(os.path.join(template_location, f'hair_{hair_style}.png'))
        self.shirt = pygame.image.load(os.path.join(template_location, 'shirt.png'))

        self.pants = replace_pair(self.pants, 'magenta', pants_color)
        self.shirt = replace_pair(self.shirt, 'magenta', shirt_color)
        self.hair = replace_pair(self.hair, 'black', hair_color)

        self.surface.blit(self.pants, (0, 0))
        self.surface.blit(self.shirt, (0, 0))
        self.surface.blit(self.hair, (0, 0))

