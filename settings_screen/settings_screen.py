from config import *
import game_state
from buttons.button import Button
from .settings_bar import SettingsBar, Slider 
 
 
def draw_settings_screen():
    global selected_slider
    """Draw the settings screen."""
    # fill the screen with white color
    screen.fill(WHITE)

    # draw the back button
    back_button = Button("BACK", WIDTH//2-50, HEIGHT//2-50, 100, 100, go_back)
    back_button.draw(screen)
    structures_bar.draw(screen)
    units_bar.draw(screen)
     # draw the structures settings bar
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if back_button.rect.collidepoint(pos):
                back_button.callback()
        if event.type == pygame.MOUSEBUTTONUP   :
            selected_slider = None
       
        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            for slider in structures_bar.sliders + units_bar.sliders:
                if slider != selected_slider and selected_slider is not None:
                    continue
                # if event.pos[0] >=  slider.slider_start and event.pos[0] <= slider.x +   slider.slider_end and event.pos[1] >= slider.y - 15 and event.pos[1] <= slider.y + 15:
                if slider.slider_rect.collidepoint(event.pos):
                  slider.handle_click(event.pos)
                  selected_slider = slider
                


    # draw buttons and input fields for each setting
    # ...
    pygame.display.update()

def go_back():
    game_state.state = "start_screen"

def handle_settings_screen_click(pos):
    """Handle click events on the settings screen."""
    

    # check if a button or input field was clicked
    # ...

def apply_settings():
    """Apply the selected settings."""
    # update game variables based on the selected settings
    # ...

# define update functions for each connected variable in your game state
def update_num_towns(new_value):
    game_state.num_towns = new_value
    print("num towns",game_state.num_towns)
def update_num_rivers(new_value):
    game_state.num_rivers = new_value

def update_num_forests(new_value):
    game_state.num_forests = new_value

def update_num_medics(new_value):
    game_state.num_medics = new_value

def update_num_observers(new_value):
    game_state.num_observers = new_value

def update_num_supply_carts(new_value):
    game_state.num_supply_carts = new_value

def update_num_cannons(new_value):
    game_state.num_cannons = new_value

def update_num_musketeers(new_value):
    game_state.num_musketeers = new_value

def update_num_pikemen(new_value):
    game_state.num_pikemen = new_value

def update_num_shields(new_value):
    game_state.num_shields = new_value

def update_num_knights(new_value):
    game_state.num_knights = new_value

# create a new SettingsBar object for structures
selected_slider = None
structures_bar = SettingsBar("Structures", 50, 100)
structures_bar.add_slider("Towns", 0, 10, game_state.num_towns, update_num_towns)
structures_bar.add_slider("Rivers", 0, 5, game_state.num_rivers, update_num_rivers)
structures_bar.add_slider("Forests", 0, 10, game_state.num_forests, update_num_forests)

# create a new SettingsBar object for units
units_bar = SettingsBar("Units", 300, 100)
units_bar.add_slider("Medics", 0, 10, game_state.num_medics, update_num_medics)
units_bar.add_slider("Observers", 0, 10, game_state.num_observers, update_num_observers)
units_bar.add_slider("Supply Carts", 0, 10, game_state.num_supply_carts, update_num_supply_carts)
units_bar.add_slider("Cannons", 0, 10, game_state.num_cannons, update_num_cannons)
units_bar.add_slider("Musketeers", 0, 10, game_state.num_musketeers, update_num_musketeers)
units_bar.add_slider("Pikemen", 0, 10, game_state.num_pikemen, update_num_pikemen)
units_bar.add_slider("Shields", 0, 10, game_state.num_shields, update_num_shields)
units_bar.add_slider("Knights", 0, 10, game_state.num_knights, update_num_knights)