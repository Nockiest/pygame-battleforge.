import pygame
class Structure(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        
        self.image = pygame.Surface((size[0], size[1]))
        self.image.fill(color)
        self.rect = self.image.get_rect()
         
        self.rect.x = x
        self.rect.y = y