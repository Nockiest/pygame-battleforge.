import game_state
from config import *


def draw_ui(screen,    ):
    if len(game_state.players) == 0:
        return
    game_state.battle_ground.draw(screen)
    game_state.button_bar.draw(screen, HEIGHT - BUTTON_BAR_HEIGHT,
                    game_state.players[game_state.cur_player].color)
    for player in game_state.players:
        player.render_tender()

    game_state.next_turn_button.draw(screen)
