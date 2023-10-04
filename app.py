import game_state
from utils.utils import *
from utils.render_utils import *
from utils.text_utils import *
from start_screen.start_screen import *
from settings_screen.settings_screen import *
from end_screen.end_screen import *
from game_screen.handle_game_running_state import handle_game_running_state
  
 
pygame.init()
pygame.display.set_caption('BattleForge')
 
while  lets_continue:
    # get_hovered_element( )
    # set_cursor()
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # display the current position of the mouse on the screen
    
  
    if game_state.state == "game_is_running":

        handle_game_running_state(game_state.game)

    elif game_state.state == "start_screen":

        handle_start_screen()
    elif game_state.state == "end_screen":

        draw_end_screen()
    elif game_state.state == "settings_screen":

        draw_settings_screen()
    else:
        print("this game screen doesnt exist", game_state.state) 
     
    clock.tick(fps)

    # # Add more game states and handling logic here
pygame.quit()
# import sys
# import glob
 # modules = glob.glob(join(dirname(__file__), "*.py"))
# __all__ = [basename(f)[:-3] for f in modules if isfile(f)
#            and not f.endswith('__init__.py')]
# this allows you to import entire folders
# mixer.init()
# mixer.music.load('_media/background-life.wav')
# mixer.music.play()
 