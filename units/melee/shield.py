from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Melee


class Shield(Melee):
    size = 30
    def __init__(self, x, y, color):
        
        super().__init__(hp=5, attack_range=20,attack_resistance=0.2,base_actions=1, base_movement=30,
                         size=self.size, x=x, y=y,   icon="shield.png",  color=color, cost=50)
 
 
 