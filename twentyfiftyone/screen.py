import pygame


class Screen:
    def __init__(self, width: int, height: int, scale: int):
        self.width = width
        self.height = height
        self.scale = scale
        self.screen = pygame.display.set_mode((width, height))

    def display(self):
        pygame.display.update()

    def blit(self, surface, coords: tuple):
        self.screen.blit(surface, coords)

    def fill(self, color: tuple):
        self.screen.fill(color)
