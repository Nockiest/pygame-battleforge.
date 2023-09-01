 
import pygame
from utils.classdict import SortedDict
from config import *
pygame.init()

## cokoliv sem přídáš bys měl přidat do reset_game_state v utils
animations = []
all_buttons = []
players = []
cur_player = 0
game_won = False
living_units = SortedDict([])# pygame.sprite.Group()
state = "start_screen"
selected_for_movement_unit = None
selected_attacking_unit = None
unit_placement_mode = False
lets_continue = True

hovered_unit = None
hovered_button = None    

battle_ground = None
button_bar = None
next_turn_button = None
end_screen_button = None
start_game_button = None
settings_button = None
game = None

## game stats
num_turns =  0  
num_attacks =  0, 0 
killed_units = 0
enemies_killed = 0
money_spent = 0
shots_fired = 0
# create a two-dimensional array to store the movement costs
movement_costs = []
pixel_colors = []
for X in range(WIDTH):
    row = []
    for Y in range(HEIGHT):
        row.append(0)
    movement_costs.append(row)
    pixel_colors.append(row[:]) # Create a copy of the row list before appending 

# settings config
num_towns = 7
num_rivers = 2
num_forests = 10
blue_player = {
    'num_Medics': 0,
    'num_Observers': 0,
    'num_Supply_carts': 0,
    'num_Cannons': 0,
    'num_Musketeers': 0,
    'num_Pikemen': 0,
    'num_Shields': 0,
    'num_Knights': 0,
    'num_Commanders': 0,
}
red_player = {
    'num_Medics': 0,
    'num_Observers': 0,
    'num_Supply_carts': 0,
    'num_Cannons': 0,
    'num_Musketeers': 0,
    'num_Pikemen': 0,
    'num_Shields': 0,
    'num_Knights': 0,
    'num_Commanders': 1
}
starting_money = 100
money_per_turn = 10