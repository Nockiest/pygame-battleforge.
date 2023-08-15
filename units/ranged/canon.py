from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Ranged
 


class Canon(Ranged):
    def __init__(self,  x, y,  color):
        super().__init__(hp=1, attack_range=300,attack_resistance=0.05, base_actions=1, base_movement=50,
                         size=40, x=x, y=y, ammo=5, icon="canon.png",  color=color, cost=30)

    # Additional methods or overrides for the Cannon class