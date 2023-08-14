from config import *
from player_actions import Player
from generation.battleground import *
game_state = "game-is-running"
selected_unit = None
render_units_attack_screen = False
unit_placement_mode = None
game_won = False
living_units = []
unit_to_be_placed = None
red_player = Player(RED, 0) 
blue_player = Player(BLUE, WIDTH -TENDER_WIDTH)
players = [red_player, blue_player]
battle_ground = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
cur_player = 0
unit_to_be_placed = None
all_buttons = []