from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Ranged


class Canon(Ranged):
    size = 40
    cost = 30

    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=300, attack_resistance=0.05, base_actions=1, base_movement=50,
                         size=self.size, x=x, y=y, ammo=5, icon="canon.png", color=color, cost=self.cost)

    def try_attack(self, click_pos, attacked_unit):
        

        # Calculate a line extending from the center of the unit towards the click position
        unit_center_x, unit_center_y = self.center
        click_x, click_y = click_pos
        dx = click_x - unit_center_x
        dy = click_y - unit_center_y
        distance = math.sqrt(dx ** 2 + dy ** 2)  # Calculate the distance between the unit and the click position
        print("checkpoint")
         
        if distance < self.attack_range:
            # Extend the line by setting the new endpoint to the attack range distance from the unit center
            line_length = self.attack_range
            angle = math.atan2(dy, dx)
            new_end_x = unit_center_x + line_length * math.cos(angle)
            new_end_y = unit_center_y + line_length * math.sin(angle)
        print(unit_center_x, unit_center_y, new_end_x, new_end_y)
        line_points = bresenham_line(unit_center_x, unit_center_y, int(new_end_x), int(new_end_y))
        print("checkpoint")
        for unit in living_units:
            if unit.color == self.color:
                continue
            elif unit == attacked_unit:
                continue
            
            res = check_precalculated_line_square_interference(unit, line_points)
            print(res)
            if res[0] != None:
                print(unit, unit.rect, res, "interferes at" ,res[0], res[1])
                unit.take_damage(self)
      
        res = super().try_attack(click_pos, attacked_unit)
        print("result of canon attacking is", res)
        return res
    
    # zatím je pravěpodobnost zásahu jednotek v cestě 100%, musím změnit