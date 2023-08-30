import game_state
from game_state import *
from config import *
 

def draw_ui(screen):
    if len(game_state.players) == 0:
        return
    try:
        if game_state.battle_ground is not None:
            game_state.battle_ground.draw(screen)
        
        if game_state.button_bar is not None and game_state.players:
            game_state.button_bar.draw(screen, HEIGHT - BUTTON_BAR_HEIGHT,
                        game_state.players[game_state.cur_player].color)
            
        for player in game_state.players:
            if player is not None:
                player.render_tender()

        if game_state.next_turn_button is not None:
            game_state.next_turn_button.draw(screen)

        if game_state.end_screen_button is not None:
            game_state.end_screen_button.draw(screen)
    except ValueError as e:
        print("Error in drawing ui",e)


def draw_units(screen):
    for unit in game_state.living_units.array:
        unit.render()
        if unit == game_state.selected_for_movement_unit:
            game_state.selected_for_movement_unit.draw_possible_movement_area()
            game_state.selected_for_movement_unit.draw_as_active()

        if unit == game_state.selected_attacking_unit:
            game_state.selected_attacking_unit.draw_as_active()

        if unit == game_state.hovered_unit:
            if unit.color ==  game_state.players[game_state.cur_player].color and unit.remain_actions <= 0:
                continue
            unit.draw_possible_movement_area()
            unit.render_attack_circle()
            unit.render_hovered_state()
    if game_state.selected_attacking_unit != None:
        game_state.selected_attacking_unit.highlight_attackable_units()
        game_state.selected_attacking_unit.draw_lines_to_enemies_in_range()
    if game_state.selected_attacking_unit:
        game_state.selected_attacking_unit.render_attack_circle()
    if game_state.unit_placement_mode:
        game_state.players[game_state.cur_player].show_unit_to_be_placed(
            (game_state.unit_to_be_placed, 0, 0))
