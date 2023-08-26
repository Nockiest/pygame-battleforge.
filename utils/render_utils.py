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
