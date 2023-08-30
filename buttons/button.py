import pygame
from config import * 
from game_state import *
 
class Button:
    def __init__(self, description, x, y, width, height, callback    ):
        self.description = description
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.button_surface = pygame.Surface((width, height))  # Create a button surface
        self.button_surface.fill((255, 255, 255))  # Fill with white color
        self.callback = callback
        self.hovered = False  # Track whether the button is currently being hovered over
        self.color = RED if self.hovered else BLACK
        self.visible = False
        # game.all_buttons.append(self)
        all_buttons.append(self)
    def __repr__(self):
         return f'{type(self).__name__}, rect: {self.rect},description: {self.description}, callback:{self.callback} '
   
    def draw(self, screen):
        # Draw the outline of the button
         
        self.color = RED if self.hovered else BLACK
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
        # Draw the text inside the button
        my_font = pygame.font.Font(MAIN_FONT_URL, 15)
        text_surface = my_font.render(self.description, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def hide_button(self):
        self.visible = False

    def is_clicked(self, pos):
        if not self.visible:
            return False
        return self.rect.collidepoint(pos)
    
    def is_hovered(self, pos):
        if not self.visible:
            return False
        return self.rect.collidepoint(pos)
