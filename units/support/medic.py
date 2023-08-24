
from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Support
 


class Medic(Support):
    size = 20
    cost = 50

    def __init__(self, x, y, color):

        super().__init__(hp=1, attack_range=100, attack_resistance=0.05, base_actions=1, base_movement=75,
                         size=self.size, x=x, y=y,  icon="medic.png",   color=color, cost=self.cost)

    def heal(self):
        # for unit in units:
        # Check if the target unit is not a Medic and is within the range of base movement
        for unit in living_units:
            if unit.color != self.color:
                continue
            if unit == self:
                continue
            if not isinstance(unit, Medic):
                distance = get_two_units_center_distance(self, unit)
                if distance <= self.base_movement and unit.base_hp > unit.hp:
                    unit.hp += 1  # Heal the target unit by 1 HP

    def reset_for_next_turn(self):
        super().reset_for_next_turn()

        self.heal()
