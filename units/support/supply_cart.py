from units.unit import Unit
import math
from utils.utils import *
from config import *
import game_state
from .template import Support
from units.ranged.template import Ranged
from animations.basic_animations import ResupplyAnimation, AmmoExpendedAnimation
from ammo_dispenser import Ammo_dispenser
class SupplyCart(Support, Ammo_dispenser):
    size = 30
    cost = 500
    def __init__(self,   x, y,  color):
        
        super().__init__(hp=1, attack_range=50,attack_resistance=0.05, base_actions=1, base_movement=150,
                         size=self.size, x=x, y=y, icon="supplycart.png", color=color, cost=self.cost, custom_ammo=20)
        self.size = 30
   
    def reset_for_next_turn(self,  ):
        super().reset_for_next_turn( )
        
        depleted_ammo = super().dispense_ammo(1)
        print(depleted_ammo)
        self.ammo -= depleted_ammo