from buttons.button import Button
from config import *
from .settings_globs import *
import game_state
 

def apply_settings():
    """Apply the selected settings."""
    for slider in settings_sliders:
        slider.alter_original_value()
    print(
        game_state.blue_player,
        game_state.red_player,
        "THOSE ARE THE PLAYERS VALUES NOW"
    )
def go_back():
    game_state.state = "start_screen"
 

back_button = Button("BACK", WIDTH//2-50, HEIGHT//2-50, 100, 100, go_back, "settings_screen")
apply_button =  Button("APPLY", WIDTH - 100, 50, 100, 50, apply_settings,"settings_screen" )


 