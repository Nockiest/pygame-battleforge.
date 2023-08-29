import game_state
import pygame
from ..settings_globs import *
from ..settings_buttons import back_button, apply_button

def handle_screen_click(event):
    """Handle click events on the settings screen."""
    global selected_slider
    if event.type == pygame.QUIT:
        print(event)
        game_state.lets_continue = False
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        pos = pygame.mouse.get_pos()
        handle_buttons_click(pos)
    if event.type == pygame.MOUSEBUTTONUP:
        selected_slider = None
    
    if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
        for slider in settings_bars:
            if slider != selected_slider and selected_slider is not None:
                continue
            if slider.slider_rect.collidepoint(event.pos):
                slider.handle_click(event.pos)
                selected_slider = slider

def handle_buttons_click(pos):
    try:
        if   back_button.rect.collidepoint(pos):
            back_button.callback()
        elif  apply_button.rect.collidepoint(pos):
          apply_button.callback()
    except AttributeError as e:
        print("error in handle button click", e)
