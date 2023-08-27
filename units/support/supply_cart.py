from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Support
from units.ranged.template import Ranged
from animations.basic_animations import ResupplyAnimation
class SupplyCart(Support):
    size = 30
    cost = 500
    def __init__(self,   x, y,  color):
        
        super().__init__(hp=1, attack_range=50,attack_resistance=0.05, base_actions=1, base_movement=150,
                         size=self.size, x=x, y=y, icon="supplycart.png", color=color, cost=self.cost, custom_ammo=20)
        self.size = 30
    def dispense_ammo(self, amount ):
        
        for unit in living_units:
            if self.ammo <= 0:
                print("no ammo left")
                break

            if unit.color != self.color:
                continue
 

            if isinstance(unit, Ranged) and distance(self.center, unit.center) <= RESUPPLY_RANGE:
                resuuply_anim =   ResupplyAnimation(unit.x, unit.y)
                
                unit.ammo += amount
                self.ammo -= amount
                resuuply_anim.render( )
                print(f"Dispensing {amount} ammo. Remaining ammo: {self.ammo} to {unit}vv")

    def reset_for_next_turn(self,  ):
        super().reset_for_next_turn( )

        self.dispense_ammo(1   )
