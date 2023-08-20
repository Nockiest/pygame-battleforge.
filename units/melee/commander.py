from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Melee
 

class Commander(Melee):
    size = 20  # Set the size attribute at the class level
    cost = 100000
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=40,attack_resistance=0.2, base_actions=1, base_movement=150,
                         size=self.size, x=x, y=y,    icon="commander.png", color=color, cost=self.cost)
 