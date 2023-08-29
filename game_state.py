 
import pygame
from classdict import SortedDict
from config import *
pygame.init()

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
battle_ground_structures = {}
input_allowed = True
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
num_towns = 5
num_rivers = 3
num_forests = 3
num_medics = 1
num_observers = 1
num_supply_carts = 1
num_cannons = 2
num_musketeers = 3
num_pikemen = 7
num_shields = 2
num_knights = 2