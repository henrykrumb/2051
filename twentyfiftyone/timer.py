import pygame


class Timer:
    def __init__(self, delay):
        self.delay = delay
        self.t = pygame.time.get_ticks()

    def reset(self):
        self.t = pygame.time.get_ticks()

    def done(self):
        t = pygame.time.get_ticks()
        return t >= self.t + self.delay
