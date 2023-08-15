from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Melee
 

class Commander(Melee):
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=40,attack_resistance=0.2, base_actions=1, base_movement=150,
                         size=20, x=x, y=y,    icon="commander.png", color=color, cost=10000)

    # Additional methods or overrides for the Commander class
    def support(self):
        # Implement support method for other units (e.g., buff their abilities)
        pass
