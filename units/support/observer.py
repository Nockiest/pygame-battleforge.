from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Support
from units.ranged.template import Ranged
class Observer(Support):
    def __init__(self, x, y,  color):
        super().__init__(hp=1, attack_range=0,attack_resistance=0.05, base_actions=1,  base_movement=50,
                         icon="observer.png", size=20, x=x, y=y,  color=color, cost=500)
        
    def provide_attack_range(self, selected_unit):
        
        if issubclass(selected_unit.__class__, Ranged)   and self.color == selected_unit.color:
            distance = get_two_units_center_distance(selected_unit, self)
            if distance <= 75:
                selected_unit.attack_range_modifiers["in_observer_range"] = 0.5
                return True
            else:
                return False
        
 