import pygame

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file, size=(10,10)):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, surface):
        surface.blit(self.image, self.rect)