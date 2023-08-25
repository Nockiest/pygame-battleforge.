from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Ranged


class Musketeer(Ranged):
    size=20
    cost = 15
    def __init__(self,   x, y,  color):
        
        super().__init__(hp=2, attack_range=200,attack_resistance=0.05,base_actions=1, base_movement=125,
                         size=self.size, x=x, y=y, ammo=10, icon="musketeer.png",   color=color, cost=self.cost)
        
    def __repr__(self):
        return f"Musketeer(x={self.x}, y={self.y}, color={self.color!r})"

    # Additional methods or overrides for the Musketeer class


 