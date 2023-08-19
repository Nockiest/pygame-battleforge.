from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Melee
 
 
 

class Knight(Melee):
    size=30
    def __init__(self, x, y,   color):
        super().__init__(hp=2, attack_range=30, attack_resistance=0.1,base_actions=1, base_movement=200,
                         size=self.size, x=x, y=y,   icon="knight.png",   color=color, cost=20)

    # Additional methods or overrides for the Knight class


 
