
import game_state
# define update functions for each connected variable in your game state
def update_game_state(attribute, new_value):
    setattr(game_state, attribute, new_value)


def update_num_towns(new_value):
    game_state.num_towns = new_value
     
def update_num_rivers(new_value):
    game_state.num_rivers = new_value

def update_num_forests(new_value):
    game_state.num_forests = new_value

# def update_game_state(name_of_object, name_of_parameter, new_value):
#     param = getattr(game_state, name_of_object)
#     setattr(param, name_of_parameter, new_value)
#     print("param",game_state.red_player_units)
def update_start_money(new_value):
    game_state.starting_money = new_value
def update_income(new_value):
    game_state.money_per_turn = new_value
 
 
def update_blue_num_Medics(new_value):
    game_state.blue_num_Medics = new_value

def update_blue_num_Observers(new_value):
    game_state.blue_num_Observers = new_value

def updateblue_num_Supply_carts(new_value):
    game_state.blue_num_Supply_carts = new_value

def update_blue_num_Cannons(new_value):
    game_state.blue_num_Cannons = new_value

def update_blue_num_Musketeers(new_value):
    game_state.blue_num_Musketeers = new_value

def update_blue_num_Pikemen(new_value):
    game_state.blue_num_Pikemen = new_value

def update_blue_num_Shields(new_value):
    game_state.blue_num_Shields = new_value

def update_blue_num_Knights(new_value):
    game_state.blue_num_Knights = new_value

def update_red_num_Medics(new_value):
    game_state.red_num_Medics = new_value

def update_red_num_Observers(new_value):
    game_state.red_num_Observers = new_value

def updatered_num_Supply_carts(new_value):
    game_state.red_num_Supply_carts = new_value

def update_red_num_Cannons(new_value):
    game_state.red_num_Cannons = new_value

def update_red_num_Musketeers(new_value):
    game_state.red_num_Musketeers = new_value

def update_red_num_Pikemen(new_value):
    game_state.red_num_Pikemen = new_value

def update_red_num_Shields(new_value):
    game_state.red_num_Shields = new_value
  
def update_red_num_Knights(new_value):
    game_state.red_num_Knights = new_value