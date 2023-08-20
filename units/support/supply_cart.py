from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Support
from units.ranged.template import Ranged
 

class SupplyCart(Support):
    size = 30
    cost = 500
    def __init__(self,   x, y,  color):
        
        super().__init__(hp=1, attack_range=50,attack_resistance=0.05, base_actions=1, base_movement=150,
                         size=self.size, x=x, y=y, icon="supplycart.png", color=color, cost=self.cost, custom_ammo=20)
        self.size = 30
    def dispense_ammo(self, amount, living_units):
        
        for unit in living_units:
            if self.ammo <= 0:
                print("no ammo left")
                break

            if unit.color != self.color:
                continue
 

            if isinstance(unit, Ranged) and distance(self.center, unit.center) <= RESUPPLY_RANGE:
                print(self.ammo)
                unit.ammo += amount
                self.ammo -= amount
                print(f"Dispensing {amount} ammo. Remaining ammo: {self.ammo} to {unit}vv")
