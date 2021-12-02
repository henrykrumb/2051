class Screen:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale
        self.screen = pygame.display.set_mode((width, height))


    def display(self):
        pygame.display.update()

    def blit(self, surface, coords):
        self.screen.blit(surface, coords)

    def fill(self, color):
        self.screen.fill(color)
