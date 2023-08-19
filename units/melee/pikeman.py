from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Melee
 
 
 
 
 
 
class Pikeman(Melee):
    size=20
    def __init__(self, x, y,  color ):
        
        super().__init__(hp=3, attack_range=30,attack_resistance=0.1, base_actions=1, base_movement=100,
                         size=self.size, x=x, y=y,  icon="pikeman.png",   color=color, cost=10)

    # Additional methods or overrides for the Pikeman class
