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
    create_buttons()
    # settings_btn.back_button.visible = True
    # settings_btn.apply_button.visible = True
    # fill the screen with white color
    screen.fill(WHITE)
    change_cursor()
    # draw the back button
     
    settings_btn.back_button.draw(screen)  
    settings_btn.apply_button.draw(screen)
    structures_bar.draw(screen)
    red_player_bar.draw(screen)
    blue_player_bar.draw(screen)
    money_bar.draw(screen)
     # draw the structures settings bar
    # print("units",game_state.red_player_units)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False
        handle_screen_click(event )

    pygame.display.update()

 
def create_buttons():
    settings_btn.back_button.visible = True
    settings_btn.apply_button.visible = True
   

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
 

# create a new SettingsBar object for structures
 
structures_bar = SettingsBar("Structures", 50, 100)
structures_bar.add_slider("Towns", 0, 10, game_state.num_towns, update_num_towns)
structures_bar.add_slider("Rivers", 0, 5, game_state.num_rivers, update_num_rivers)
structures_bar.add_slider("Forests", 0, 10, game_state.num_forests, update_num_forests)
 
money_bar = SettingsBar("Money", 50, 400)
money_bar.add_slider("Start Money", 0, 1000, game_state.num_forests, update_start_money)
money_bar.add_slider("Turn Income", 0, 100, game_state.num_forests, update_income)
# create a new SettingsBar object for units
blue_player_bar = SettingsBar("Blue Player", 700, 100) 
blue_player_bar.add_slider("Medics", 0, 10, game_state. blue_num_Medics  , lambda new_value:  update_blue_num_Medics(new_value))
blue_player_bar.add_slider("Observers", 0, 10, game_state. blue_num_Observers , lambda new_value:  update_blue_num_Observers(new_value))
blue_player_bar.add_slider("Supply Carts", 0, 10,game_state. blue_num_Supply_carts , lambda new_value:  updateblue_num_Supply_carts(new_value))
blue_player_bar.add_slider("Cannons", 0, 10, game_state. blue_num_Cannons  , lambda new_value: update_blue_num_Cannons(new_value))
blue_player_bar.add_slider("Musketeers", 0, 10, game_state. blue_num_Musketeers , lambda new_value:  update_blue_num_Musketeers(new_value))
blue_player_bar.add_slider("Pikemen", 0, 10, game_state. blue_num_Pikemen  , lambda new_value:  update_blue_num_Pikemen(new_value))
blue_player_bar.add_slider("Shields", 0, 10, game_state. blue_num_Shields  , lambda new_value:  update_blue_num_Shields(new_value))
blue_player_bar.add_slider("Knights", 0, 10, game_state. blue_num_Knights  , lambda new_value:  update_blue_num_Knights(new_value))

red_player_bar = SettingsBar("Red Player", 300, 100)
red_player_bar.add_slider("Medics", 0, 10,  game_state. red_num_Medics , lambda new_value: update_red_num_Medics(new_value)) 
red_player_bar.add_slider("Observers", 0, 10,  game_state. red_num_Observers , lambda new_value:  update_red_num_Observers(new_value))
red_player_bar.add_slider("Supply Carts", 0, 10, game_state. red_num_Supply_carts , lambda new_value:  updatered_num_Supply_carts(new_value))
red_player_bar.add_slider("Cannons", 0, 10,  game_state. red_num_Cannons , lambda new_value: update_red_num_Cannons(new_value))
red_player_bar.add_slider("Musketeers", 0, 10, game_state. red_num_Musketeers , lambda new_value: update_red_num_Musketeers(new_value))
red_player_bar.add_slider("Pikemen", 0, 10,game_state. red_num_Pikemen  , lambda new_value:  update_red_num_Pikemen(new_value))
red_player_bar.add_slider("Shields", 0, 10, game_state. red_num_Shields ,  lambda new_value:  update_red_num_Shields(new_value))
red_player_bar.add_slider("Knights", 0, 10,game_state. red_num_Knights  , lambda new_value:  update_red_num_Knights(new_value))
 
 