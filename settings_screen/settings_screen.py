from config import *
import game_state
from buttons.button import Button
from .settings_bar import SettingsBar, Slider
def draw_settings_screen():
    """Draw the settings screen."""
    # fill the screen with white color
    screen.fill(WHITE)

    # draw the back button
    back_button = Button("BACK", WIDTH//2-50, HEIGHT//2-50, 100, 100, go_back)
    back_button.draw(screen)
    
     # draw the structures settings bar
    structures_bar = SettingsBar("Structures", 50, 100)
    structures_bar.add_slider("Towns", 0, 10, game_state.num_towns)
    structures_bar.add_slider("Rivers", 0, 5, game_state.num_rivers)
    structures_bar.add_slider("Forests", 0, 10, game_state.num_forests)
    structures_bar.draw(screen)

    # draw the units settings bar
    units_bar = SettingsBar("Units", 300, 100)
    units_bar.add_slider("Medics", 0, 10, game_state.num_medics)
    units_bar.add_slider("Observers", 0, 10, game_state.num_observers)
    units_bar.add_slider("Supply Carts", 0, 10, game_state.num_supply_carts)
    units_bar.add_slider("Cannons", 0, 10, game_state.num_cannons)
    units_bar.add_slider("Musketeers", 0, 10, game_state.num_musketeers)
    units_bar.add_slider("Pikemen", 0, 10, game_state.num_pikemen)
    units_bar.add_slider("Shields", 0, 10, game_state.num_shields)
    units_bar.add_slider("Knights", 0, 10, game_state.num_knights)
    units_bar.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if back_button.rect.collidepoint(pos):
                back_button.callback()

       
        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            for slider in structures_bar.sliders + units_bar.sliders:
                slider.handle_click(event.pos)


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