import game_state
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
    except ValueError as e:
        print(e)


def draw_units(screen):
    for unit in game_state.living_units:
        unit.render()
        if unit == game_state.selected_for_movement_unit:
            game_state.selected_for_movement_unit.draw_possible_movement_area()
        elif unit == game_state.selected_attacking_unit:
            game_state.selected_attacking_unit.draw_as_active()

        if unit == game_state.hovered_unit:
            unit.render_hovered_state()

    if game_state.selected_attacking_unit != None:
        game_state.selected_attacking_unit.highlight_attackable_units()
        game_state.selected_attacking_unit.draw_lines_to_enemies_in_range()
    if game_state.selected_attacking_unit:
        attack_range_provided = False
        # for unit in game_state.living_units:
        #     if isinstance(unit, Observer) and unit.color == game_state.selected_attacking_unit.color:
        #         attack_range_provided = unit.provide_attack_range(
        #             game_state.selected_for_movement_unit)
        if attack_range_provided is False:
            game_state.selected_attacking_unit.attack_range_modifiers["in_observer_range"] = 0

        game_state.selected_attacking_unit.render_attack_circle()
    if game_state.unit_placement_mode:
        game_state.players[game_state.cur_player].show_unit_to_be_placed(
            (game_state.unit_to_be_placed, 0, 0))
