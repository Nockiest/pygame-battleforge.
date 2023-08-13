import pygame
from config import * 
 

class Button:
    def __init__(self, description, x, y, width, height, callback):
        self.description = description
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.button_surface = pygame.Surface((width, height))  # Create a button surface
        self.default_color = (255, 255, 255)
        self.hover_color = (200, 200, 200)  # Darker color for hover effect
        self.button_surface.fill(self.default_color)  # Fill with default color
        self.callback = callback
        self.hovered = False  # Track whether the button is currently being hovered over

    def draw(self, screen):
        # Update button color based on hover state
        if self.hovered:
            color = self.hover_color
        else:
            color = self.default_color

        pygame.draw.rect(self.button_surface, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        my_font = pygame.font.Font(MAIN_FONT_URL, 15)
        text_surface = my_font.render(self.description, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.button_surface.blit(text_surface, text_rect)
        
        screen.blit(self.button_surface, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def set_hovered(self, hovered):
        self.hovered = hovered