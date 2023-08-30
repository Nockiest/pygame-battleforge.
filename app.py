
from battelground import *
from player_actions import Player
from config import *
from buttons.buy_bar import *
from utils import *
import game_state
from utils.render_utils import *
from units import *
from utils.text_utils import *
import sys
from os.path import dirname, basename, isfile, join
import glob
from animations.basic_animations import *
from start_screen.start_screen import *
from settings_screen.settings_screen import *
from end_screen.end_screen import *
from game_screen.game_object import Game
from game_screen.handle_game_running_state import handle_game_running_state
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith('__init__.py')]
# this allows you to import entire folders
 

# def place_starting_units(red_player, blue_player):
#     # blue_player.create_starting_unit(
#     #     (Musketeer, 0, 100))
#     red_player.create_starting_unit(
#         (Musketeer, 200, 200))
#     red_player.create_starting_unit(
#         (Pikeman, 175, 175))
#     red_player.create_starting_unit(
#         (Canon, 250, 250))
#     red_player.create_starting_unit(
#         (Canon, 120, 100))
#     red_player.create_starting_unit(
#         (Shield, 400, 300))
#     blue_player.create_starting_unit(
#         (Medic, 125, 160))
#     blue_player.create_starting_unit(
#         (Medic, 500, 400))
#     blue_player.create_starting_unit(
#         (Commander, 550, 100))
#     red_player.create_starting_unit(
#         (Commander, 500, 70))
#     red_player.create_starting_unit(
#         (Pikeman, 700, 100))
#     blue_player.create_starting_unit(
#         (SupplyCart, 300, 300))
#     blue_player.create_starting_unit(
#         (Musketeer, 340, 300))
#     blue_player.create_starting_unit(
#         (Observer, 200, 150))
#     blue_player.create_starting_unit(
#         (Observer, 250, 150))
#     blue_player.create_starting_unit(
#         (Knight, 450, 500))
#     blue_player.create_starting_unit(
#         (Knight, 50, 100))
#     blue_player.create_starting_unit(
#         (Knight, 80, 100))
#     # # # blue_player.create_starting_unit(
#     # #     (Knight, 50, 500)s)


pygame.init()
pygame.display.set_caption('BattleForge')

 
def go_to_end_screen():
    game_state.state = "end_screen"
 
game_state.end_screen_button = Button(
    "GIVE UP", WIDTH-100, 0, 100, UPPER_BAR_HEIGHT, go_to_end_screen)

while game_state.lets_continue:
    if game_state.state == "game_is_running":
        handle_game_running_state(game_state.game)

    elif game_state.state == "start_screen":
       
        handle_start_screen()
    elif game_state.state == "end_screen":
        
        draw_end_screen()
    elif game_state.state == "settings":
        
        draw_settings_screen() 
    else:
        print("this game screen doesnt exist", game_state.state)

    

    # Add more game states and handling logic here
pygame.quit()
