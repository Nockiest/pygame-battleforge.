 
import pygame
from classdict import SortedDict
from config import *
pygame.init()

## cokoliv sem přídáš bys měl přidat do reset_game_state v utils

all_buttons = []
players = []
cur_player = 0
game_won = False
living_units = SortedDict([])# pygame.sprite.Group()
state = "start_screen"
selected_for_movement_unit = None
selected_attacking_unit = None
unit_placement_mode = None
lets_continue = True
unit_to_be_placed = None
hovered_unit = None
hovered_button = None    
battle_ground = None
button_bar = None
next_turn_button = None
end_screen_button = None
 
 
game = None
num_attacks = 0
animations = []
# create a two-dimensional array to store the movement costs
movement_costs = []
pixel_colors = []
for X in range(WIDTH):
    row = []
    for Y in range(HEIGHT):
        row.append(0)
    movement_costs.append(row)
    pixel_colors.append(row[:]) # Create a copy of the row list before appending 
num_towns = 0
num_rivers = 5
num_forests = 0
num_Medics = 0
num_Observers = 0
num_Supply_carts = 0
num_Cannons = 0
num_Musketeers = 0
num_Pikemen = 0
num_Shields = 0
num_Knights = 0
num_Commanders = 0