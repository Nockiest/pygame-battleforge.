import pygame
import game_state
from config import *
from utils.render_utils import *
from utils.utils import *
from utils.debug import *
from utils.text_utils import *
import json
def save_game_state(game_state, filename):
    data = {
        'animations': game_state.animations,
        # 'all_buttons': game_state.all_buttons,
        'players': game_state.players,
        'cur_player': game_state.cur_player,
        'living_units': game_state.living_units,
        'state': game_state.state,
        'selected_for_movement_unit': game_state.selected_for_movement_unit,
        'selected_attacking_unit': game_state.selected_attacking_unit,
        'unit_placement_mode': game_state.unit_placement_mode,
        'battle_ground': game_state.battle_ground,
        # 'button_bar': game_state.button_bar,
        # 'next_turn_button': game_state.next_turn_button,
        # 'end_screen_button': game_state.end_screen_button,
        # 'start_game_button': game_state.start_game_button,
        # 'settings_button': game_state.settings_button,
        'game': game_state.game,
        'num_turns': game_state.num_turns,
        'num_attacks': game_state.num_attacks,
        'killed_units': game_state.killed_units,
        'enemies_killed': game_state.enemies_killed,
        'money_spent': game_state.money_spent,
        'shots_fired': game_state.shots_fired,
        'movement_costs': game_state.movement_costs,
        'pixel_colors': game_state.pixel_colors,
        'num_towns': game_state.num_towns,
        'num_rivers': game_state.num_rivers,
        'num_forests': game_state.num_forests,
        'blue_player': game_state.blue_player,
        'red_player': game_state.red_player,
        'starting_money': game_state.starting_money,
        'money_per_turn': game_state.money_per_turn
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

def handle_game_running_state(game):
   
    if game == None:
        return

    cursor_x, cursor_y = pygame.mouse.get_pos()
    # get_hovered_element(cursor_x, cursor_y)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            print(event)
            save_game_state(game_state, "game_state.json")
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
    # text = "game" + (" ended  " if game_state.game_won else "  is running ")

    # render_text(screen, text,
    #             WIDTH // 2, 10, color=(255, 255, 255),   font_size=24)

    # Render everything on the display
    mouse_x,mouse_y = pygame.mouse.get_pos()
    pixel_color=game_state.pixel_colors[mouse_x][mouse_y]
    debug(pygame.mouse.get_pos(),mouse_y, mouse_x)
    debug(pixel_color  )
    pygame.display.update()

    # RENDER ELEMENTS ON THE BACKGROUND SCREEN
    draw_ui(background_screen,)
 
def handle_left_mouse_clk(click_pos, game):
    # Check if any button in the button bar is clicked
    if game_state.hovered_button and game_state.hovered_button.hovered:
        game_state.hovered_button.callback()
 
    if game_state.unit_placement_mode and game_state.players[game_state.cur_player].preview_unit != None:
        game.buy_unit(click_pos)
    else:
        game.select_unit(click_pos)

def handle_right_mouse_clk(click_pos, game):
    
    player =  game_state.players[game_state.cur_player]
     
    if  player.preview_unit != None:
        abort_placement_mode(player, player.preview_unit)
    elif  game_state.hovered_button:
        game_state.hovered_button.callback(  ) 
    elif game_state.selected_attacking_unit:
        game.process_attack(
            game_state.selected_attacking_unit, click_pos)
    else:
        game.activate_attack_mode(click_pos)

def handle_mouse_motion(click_pos):
    if game_state.players == []:
        return
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
   