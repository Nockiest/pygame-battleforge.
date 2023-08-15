from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *

class Support(Unit):
    def __init__(self, hp, attack_range,attack_resistance, base_actions, base_movement, size, x, y, icon, color, cost, custom_ammo=None):
        # Call the constructor of the parent class (Unit) without specifying the 'ammo' parameter
        ammo = custom_ammo if custom_ammo is not None else None
        super().__init__(hp, attack_range, attack_resistance, base_actions,
                         base_movement, size, x, y, ammo, icon, color, cost)
        
        
    def try_attack(self, click_pos, living_units):
        return  ("SUPPORTS DONT ATTACK") 