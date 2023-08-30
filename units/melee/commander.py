from units.unit import Unit
import math
from utils.utils import *
from config import *
import game_state
from .template import Melee


class Commander(Melee):
    size = 20  # Set the size attribute at the class level
    cost = 100000

    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=40, attack_resistance=0.2, base_actions=1, base_movement=150,
                         size=self.size, x=x, y=y,    icon="commander.png", color=color, cost=self.cost)

    def take_damage(self, attacker):
         
        hp = super().take_damage(attacker)
       # print(hp,game_state.game_won = True, "game won is")
        if hp <= 0:
       
            game_state.state = "end_screen"
          
     
        return hp
