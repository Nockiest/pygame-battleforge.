#define the width and height of the battlefield
from battelground import BattleGround
from player_actions import Player
from config import *
import game_state
from utils.render_utils import *
from utils.utils import *
from game import *

# create a BattleGround object
battle_ground = BattleGround(WIDTH, HEIGHT)

# place forests on the battlefield
battle_ground.place_forrests()

# place rivers on the battlefield
battle_ground.place_rivers()

# place supply depots on the battlefield
battle_ground.place_supply_depots()

# place towns on the battlefield
battle_ground.place_towns()

# place bridges on the battlefield
battle_ground.place_bridges()

# place roads on the battlefield
battle_ground.place_roads()

# create Player objects for the red and blue players
red_player = Player(RED, 0)
blue_player = Player(BLUE, WIDTH - TENDER_WIDTH)

# add the players to the game state
game_state.players.append(red_player)
game_state.players.append(blue_player)

# set the battle_ground attribute of the game_state object
game_state.battle_ground = battle_ground

# draw the UI elements on the screen
draw_ui(screen)
draw_ui(background_screen)

# place starting units for each player
place_starting_units(red_player, blue_player)

# initialize movement costs for each pixel
try:
    for x in range(WIDTH):
        for y in range(HEIGHT):
            # set the movement cost for pixel (x, y)
            color = get_pixel_colors([(x,y)], background_screen)
            arr = calculate_movement_cost(color)
            cost, _, color = arr[0]
            game_state.movement_costs[x][y] = cost
            game_state.pixel_colors[x][y] = color
except Exception as e:
    print(f"An error occurred: {e}")