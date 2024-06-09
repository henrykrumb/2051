import pygame


class Sprite:
    def __init__(self, image, scale: int = 1):
        self.x = 0
        self.y = 0
        self.xframe = 0
        self.yframe = 0
        self.frame_w = image.get_width()
        self.frame_h = image.get_height()
        self.scale = scale
        self.image = pygame.transform.scale(
            image, (scale * image.get_width(), scale * image.get_height())
        )

    def display(self, screen):
        if self.frame_w != 0 and self.frame_h != 0:
            cliprect = (
                self.xframe * self.frame_w * self.scale,
                self.yframe * self.frame_h * self.scale,
                self.frame_w * self.scale,
                self.frame_h * self.scale,
            )
            screen.blit(
                self.image, (self.x * self.scale, self.y * self.scale), cliprect
            )
        else:
            screen.blit(self.image, (self.x * self.scale, self.y * self.scale))
