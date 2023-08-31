from units.unit import Unit
import math
from utils.utils import *
from config import *
import game_state
from .template import Ranged
from animations.shooting_animation import ShootingAnimation

class Cannon(Ranged):
    size = 40
    cost = 30

    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=300, attack_resistance=0.05, base_actions=1, base_movement=50,
                         size=self.size, x=x, y=y, ammo=5, icon="Cannon.png", color=color, cost=self.cost)
    
     

    def try_attack(self, click_pos, attacked_unit):
        res = super().try_attack( click_pos, attacked_unit)
      
        if res == "Attack not possible":
            return res
      
         
        # self.attack()
        total_attack_range_modifier = sum(self.attack_range_modifiers.values())
        # Calculate a line extending from the center of the unit towards the click position
        unit_center_x, unit_center_y = self.center
        attacked_center_x, attacked_center_y = attacked_unit.center
        dx = attacked_center_x - unit_center_x
        dy = attacked_center_y - unit_center_y
        # Calculate the distance between the attacker and the attacked unit
        # distance = math.sqrt(dx ** 2 + dy ** 2)
        # Calculate the angle between the attacker and the attacked unit
        angle_radians = math.atan2(dy, dx)
        point_x = self.center[0] + self.attack_range*total_attack_range_modifier * math.cos(angle_radians)
        point_y = self.center[1] + self.attack_range*total_attack_range_modifier * math.sin(angle_radians)
        line_points = bresenham_line(
            self.center[0], self.center[1], int(point_x),    int(point_y)
        )
        line_pixel_colors = get_pixel_colors(
            line_points, background_screen)
        prevented = self.prevent_shhooting_through_forrest(
            line_pixel_colors, line_points)
        units_in_attack_path = []
        if not prevented:
            for unit in game_state.living_units.array.copy():
                if unit.color == self.color:
                    continue
               
                point_x, point_y, interferes = check_precalculated_line_square_interference(
                    unit, line_points)
                
                if interferes :
                    print(unit, unit.rect,  "interferes at", point_x, point_y)
                    # self.try_attack( click_pos,unit)
                    units_in_attack_path.append(unit   )
                    # remain_hp = unit.take_damage(self)

                    # if remain_hp < 0:
                    #     game_state.living_units.array.remove(unit)
                    #     self.enemies_in_range.remove(unit)
                    #     print("Removed", unit, "from game_state.living_units.array")
            game_state.animations.append(ShootingAnimation(self.x, self.y, line_points,self, units_in_attack_path) )
 
             
 
       
            
        return "UNIT ATTACKS"
     