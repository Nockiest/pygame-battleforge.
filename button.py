import pygame
from config import * 
 

class Button:
    def __init__(self, description, x, y, width, height, callback):
        self.description = description
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.button_surface = pygame.Surface(( width,  height))  # Create a button surface
        self.button_surface.fill((255, 255, 255))  # Fill with white color
        self.callback = callback
        self.hovered = False  # Track whether the button is currently being hovered over

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        my_font = pygame.font.Font(MAIN_FONT_URL, 15)
        text_surface = my_font.render(self.description, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)