
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
from pygame.locals import *
from pygame import mixer
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith('__init__.py')]
# this allows you to import entire folders
# mixer.init()
# mixer.music.load('_media/background-life.wav')
# mixer.music.play()

pygame.init()
pygame.display.set_caption('BattleForge')


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
