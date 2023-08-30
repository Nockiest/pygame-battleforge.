import pygame
import game_state
from config import *
from buttons.button import Button
from .start_scree_state import *
from game_screen.game_object import Game
def set_up_game_screen():
     

    game_state.start_game_button = Button("BEGIN GAME", WIDTH//2-50,
                                      HEIGHT//2-50, 100, 100, start_game)
    game_state.settings_button = Button("SETTINGS", WIDTH//2-50,
                                      HEIGHT//2+50, 100, 100, open_settings)
    screen_set_up = True

def open_settings():
     
    game_state.state = "settings"
def start_game(): 
    global start_game_button
    global settings_button
    for button in game_state.all_buttons:
        if button == game_state.start_game_button:
            button.visible = False
        if button == game_state.settings_button:
            button.visible = False
    
    print("BUTTONS",game_state.start_game_button.visible, game_state.settings_button.visible)
    # this function gets actually called multiple times
    if game_state.game is   None: 
      game_state.game = Game()
    game_state.state = "game_is_running"

def handle_start_screen():
    if not screen_set_up:
        set_up_game_screen()
    screen.fill(BRIDGE_COLOR)
    game_state.start_game_button.draw(screen)
    game_state.settings_button.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state.start_game_button.rect.collidepoint(event.pos):
                game_state.start_game_button.callback()
            elif game_state.settings_button.rect.collidepoint(event.pos):
                game_state.settings_button.callback()

 

    # Render everything on the display
    pygame.display.update()
    game_state.start_game_button.visible = False
    game_state.settings_button.visible = False
  

    clock.tick(fps)