 
import pygame
from classdict import SortedDict
pygame.init()

all_buttons = []
players = []
cur_player = 0
game_won = False
living_units = SortedDict([])# pygame.sprite.Group()
state = "game_is_running"
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
start_game_button = None
input_allowed = True
animations = []