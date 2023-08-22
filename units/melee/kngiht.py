from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Melee
 
 
 

class Knight(Melee):
    size=30
    cost = 30
    def __init__(self, x, y,   color):
        super().__init__(hp=2, attack_range=30, attack_resistance=0.1,base_actions=1, base_movement=200,
                         size=self.size, x=x, y=y,   icon="knight.png",   color=color, cost=self.cost)
        
    def get_boost_for_destroying_unit(self ):
        super().get_boost_for_destroying_unit( )
        self.dash(  )
        print("knight will get anotoher attack after killing a unit")

    def dash(self  ):
        self.remain_actions += 1
        self.able_to_move = True
        self.start_turn_position = (
            self.x + self.size // 2, self.y + self.size // 2)
        print(self.x, self.y, self.start_turn_position)
        self.get_units_movement_area( )
        print(self.able_to_move,"able to move")

    # Additional methods or overrides for the Knight class


 
