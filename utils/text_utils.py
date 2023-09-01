import pygame
from config import *

def render_text(screen, text, x, y, color=(255, 255, 255), font=None, font_size=36, align='center'):
    if font is None:
        # Change the font size as needed
        font = pygame.font.Font(None, font_size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == 'center':
        text_rect.center = (x, y)
    elif align == 'topleft':
        text_rect.topleft = (x, y)
    elif align == 'topright':
        text_rect.topright = (x, y)
    elif align == 'bottomleft':
        text_rect.bottomleft = (x, y)
    elif align == 'bottomright':
        text_rect.bottomright = (x, y)

    screen.blit(text_surface, text_rect)
