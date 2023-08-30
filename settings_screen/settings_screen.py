from config import *
import game_state
from buttons.button import Button
from .settings_bar import SettingsBar, Slider 
from .settings_globs import *
from .fc.update_game_state_fc import *
from .fc.handle_screen_click import handle_screen_click
import settings_screen.settings_buttons as settings_btn
def draw_settings_screen():  
    """Draw the settings screen."""
    # fill the screen with white color
    screen.fill(WHITE)
    change_cursor()
    # draw the back button
     
    settings_btn.back_button.draw(screen)  
    settings_btn.apply_button.draw(screen)
    structures_bar.draw(screen)
    units_bar.draw(screen)
     # draw the structures settings bar
    print("num forrrests",game_state.num_forests)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False
        handle_screen_click(event )

    pygame.display.update()

 

   

def change_cursor():
    global selected_slider
    pos = pygame.mouse.get_pos()
     # change the cursor to a pointer when selected_slider is not None
    if selected_slider is not None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    for button in game_state.all_buttons:
        button.hovered = False
        if button.rect.collidepoint(pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            button.hovered = True
            break
    # check if a button or input field was clicked
    # ...

 
        
    # update game variables based on the selected settings
    # ...

 

# create a new SettingsBar object for structures
selected_slider = None
structures_bar = SettingsBar("Structures", 50, 100)
structures_bar.add_slider("Towns", 0, 10, game_state.num_towns, update_num_towns)
structures_bar.add_slider("Rivers", 0, 5, game_state.num_rivers, update_num_rivers)
structures_bar.add_slider("Forests", 0, 10, game_state.num_forests, update_num_forests)
 
# create a new SettingsBar object for units
units_bar = SettingsBar("Units", 300, 100)
units_bar.add_slider("Medics", 0, 10, game_state.num_Medics, update_num_Medics)
units_bar.add_slider("Observers", 0, 10, game_state.num_Observers, update_num_Observers)
units_bar.add_slider("Supply Carts", 0, 10, game_state.num_Supply_carts, update_num_Supply_carts)
units_bar.add_slider("Cannons", 0, 10, game_state.num_Cannons, update_num_Cannons)
units_bar.add_slider("Musketeers", 0, 10, game_state.num_Musketeers, update_num_Musketeers)
units_bar.add_slider("Pikemen", 0, 10, game_state.num_Pikemen, update_num_Pikemen)
units_bar.add_slider("Shields", 0, 10, game_state.num_Shields, update_num_Shields)
units_bar.add_slider("Knights", 0, 10, game_state.num_Knights, update_num_Knights)

 