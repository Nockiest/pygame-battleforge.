import pygame
from config import default_font, BLACK


def debug(info, y=10,   x=10):
    display_surf = pygame.display.get_surface()
    debug_surf = default_font.render(str(info), True, BLACK )
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    display_surf.blit(debug_surf, debug_rect)
