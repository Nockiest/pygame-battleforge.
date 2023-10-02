from config import *
import game_state
from buttons.button import Button
from .settings_bar import SettingsBar 
from .slider import Slider
from .settings_globs import *
from .fc.update_game_state_fc import *
from .fc.handle_screen_click import handle_screen_click
import settings_screen.settings_buttons as settings_btn
def draw_settings_screen():  
    """Draw the settings screen."""
    # fill the screen with white color
    screen.fill(WHITE)
    # change_cursor()
    # draw the back button
     
    settings_btn.back_button.draw(screen)  
    settings_btn.apply_button.draw(screen)
    structures_bar.draw(screen)
    red_player_bar.draw(screen)
    blue_player_bar.draw(screen)
    money_bar.draw(screen)
     # draw the structures settings bar
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False
        handle_screen_click(event )

    pygame.display.update()

 
 

# create a new SettingsBar object for structures
structures_bar = SettingsBar("Structures", 50, 100)
structures_bar.add_slider("Towns", 0, 10, game_state.num_towns, lambda new_value: update_game_state('num_towns', new_value))
structures_bar.add_slider("Rivers", 0, 5, game_state.num_rivers, lambda new_value: update_game_state('num_rivers', new_value))
structures_bar.add_slider("Forests", 0, 10, game_state.num_forests, lambda new_value: update_game_state('num_forests', new_value))

money_bar = SettingsBar("Money", 50, 400)
money_bar.add_slider("Start Money", 0, 1000, game_state.starting_money, lambda new_value: update_game_state('starting_money', new_value))
money_bar.add_slider("Turn Income", 0, 100, game_state.money_per_turn, lambda new_value: update_game_state('money_per_turn', new_value))
money_bar.add_slider("City Revnue", 0, 100, game_state.city_turn_revenue, lambda new_value: update_game_state('city_turn_revenue', new_value))

blue_player_bar = SettingsBar("Blue Player", 700, 100)
blue_player_bar.add_slider("Medics", 0, 10, game_state.blue_player['num_Medics'], lambda new_value: update_game_state('blue_player.num_Medics', new_value))
blue_player_bar.add_slider("Observers", 0, 10, game_state.blue_player['num_Observers'], lambda new_value: update_game_state('blue_player.num_Observers', new_value))
blue_player_bar.add_slider("Supply Carts", 0, 10, game_state.blue_player['num_Supply_carts'], lambda new_value: update_game_state('blue_player.num_Supply_carts', new_value))
blue_player_bar.add_slider("Cannons", 0, 10, game_state.blue_player['num_Cannons'], lambda new_value: update_game_state('blue_player.num_Cannons', new_value))
blue_player_bar.add_slider("Musketeers", 0, 10, game_state.blue_player['num_Musketeers'], lambda new_value: update_game_state('blue_player.num_Musketeers', new_value))
blue_player_bar.add_slider("Pikemen", 0, 10, game_state.blue_player['num_Pikemen'], lambda new_value: update_game_state('blue_player.num_Pikemen', new_value))
blue_player_bar.add_slider("Shields", 0, 10, game_state.blue_player['num_Shields'], lambda new_value: update_game_state('blue_player.num_Shields', new_value))
blue_player_bar.add_slider("Knights", 0, 10, game_state.blue_player['num_Knights'], lambda new_value: update_game_state('blue_player.num_Knights', new_value))

red_player_bar = SettingsBar("Red Player", 300, 100)
red_player_bar.add_slider("Medics", 0, 10, game_state.red_player['num_Medics'] , lambda new_value: update_game_state('red_player.num_Medics', new_value))
red_player_bar.add_slider("Observers", 0, 10 , game_state.red_player['num_Observers'] , lambda new_value: update_game_state('red_player.num_Observers', new_value))
red_player_bar.add_slider("Supply Carts", 0 ,10 ,game_state.red_player['num_Supply_carts'] , lambda new_value: update_game_state('red_player.num_Supply_carts',new_value))
red_player_bar.add_slider("Cannons",0 ,10 ,game_state.red_player['num_Cannons'] ,lambda new_value:update_game_state('red_player.num_Cannons' ,new_value))
red_player_bar.add_slider("Musketeers" ,0 ,10 ,game_state.red_player['num_Musketeers'] ,lambda new_value:update_game_state('red_player.num_Musketeers' ,new_value))
red_player_bar.add_slider("Pikemen" ,0 ,10 ,game_state.red_player['num_Pikemen'] ,lambda new_value:update_game_state('red_player.num_Pikemen' ,new_value))
red_player_bar.add_slider("Shields" ,0 ,10 ,game_state.red_player['num_Shields'] ,lambda new_value:update_game_state('red_player.num_Shields' ,new_value))
red_player_bar.add_slider("Knights" ,0 ,10 ,game_state.red_player['num_Knights'] ,lambda new_value:update_game_state('red_player.num_Knights' ,new_value))