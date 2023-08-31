import pygame
import game_state
from config import *
from utils.render_utils import *
from utils.utils import *
from utils.text_utils import *
def handle_game_running_state(game):
   
    if game == None:
        return

    cursor_x, cursor_y = pygame.mouse.get_pos()
    get_hovered_element(cursor_x, cursor_y)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            handle_left_mouse_clk(event.pos, game)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            handle_right_mouse_clk(event.pos, game)
        if event.type == pygame.MOUSEMOTION:
            handle_mouse_motion(event.pos)

    for player in game_state.players:
        player.handle_input()
    
    screen.fill(GREEN)
    # RENDER ELEMENTS ON THE MAIN SCREEN
    # render the game game_state.state information
    draw_ui(screen,)
    draw_units(screen)
    for animation in game_state.animations:
        animation.render()
    text = "game" + (" ended  " if game_state.game_won else "  is running ")

    render_text(screen, text,
                WIDTH // 2, 10, color=(255, 255, 255), font=None, font_size=24)

    # Render everything on the display
    pygame.display.update()

    # RENDER ELEMENTS ON THE BACKGROUND SCREEN
    draw_ui(background_screen,)

    clock.tick(fps)

def handle_left_mouse_clk(click_pos, game):
    # Check if any button in the button bar is clicked
    if game_state.hovered_button and game_state.hovered_button.hovered:
        game_state.hovered_button.callback()
        ## enter unit placement mode
        ## new players unit is created
        ## new unit is pinned to the playeers cursor
        ## he moves it around 
        ## unit gets placed on a valid position
        ## money is subtracted
        ## units gets unpinned
    if game_state.unit_placement_mode and game_state.players[game_state.cur_player].preview_unit != None:
        game.buy_unit(click_pos)
    else:
        game.select_unit(click_pos)

def handle_right_mouse_clk(click_pos, game):
    
    player =  game_state.players[game_state.cur_player]
    if game_state.hovered_button:
        game_state.hovered_button.callback()
    elif player.preview_unit != None:
        player.remove_self_unit( player.preview_unit )
        player.preview_unit.__del__()

        player.preview_unit = None
        game_state.unit_placement_mode = False
    elif game_state.selected_attacking_unit:
        game.process_attack(
            game_state.selected_attacking_unit, click_pos)
    else:
        game.activate_attack_mode(click_pos)

def handle_mouse_motion(click_pos):
    player =  game_state.players[game_state.cur_player]
    if game_state.selected_for_movement_unit:
        game_state.selected_for_movement_unit.move_in_game_field(
            click_pos)
    elif game_state.unit_placement_mode:
        player.pin_and_move_unit(player.preview_unit)

def get_hovered_element(cursor_x, cursor_y):
    cursor_hovers_over_unit = False
    cursor_hovers_over_button = False
    for unit in game_state.living_units.array:
        if unit.rect.collidepoint((cursor_x, cursor_y)):
            game_state.hovered_unit = unit
            cursor_hovers_over_unit = True
    for button in game_state.all_buttons:
        if button.is_hovered((cursor_x, cursor_y)):
            game_state.hovered_button = button
            game_state.hovered_button.hovered = True
            cursor_hovers_over_button = True
        else:
            button.hovered = False

    if not cursor_hovers_over_unit:
        game_state.hovered_unit = None
    if not cursor_hovers_over_button:
        game_state.hovered_button = None
   