from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
 
class Melee(Unit):
    def __init__(self, hp, attack_range,attack_resistance,   base_actions,  base_movement, size, x, y, icon, color, cost):
        super().__init__(hp, attack_range,attack_resistance, base_actions,
                         base_movement, size, x, y, None, icon, color, cost)
    def try_attack(self, click_pos, living_units   ):
        res = super().try_attack(click_pos, living_units)

        if res[0] == "UNIT ATTACKS":
            # Calculate the line between unit's center and click position
            
            line_points = bresenham_line(
                self.center[0], self.center[1], click_pos[0], click_pos[1]
            )

            # Get the pixel colors along the line
            line_pixel_colors = get_pixel_colors(line_points, background_screen)
           
            # Check if FORREST_GREEN is present in pixel colors
            if RIVER_BLUE   in line_pixel_colors:
                print("Ranged unit can't attack through forests")
                res = ("MELEE UNIT CAN'T ATTACK THROUGH RIVERS ", click_pos, None)

        return res
    
    def get_attackable_units(self,  living_units):
        super().get_attackable_units(living_units)
        units_to_remove = []  # Create a list to store units to be removed

        for unit in self.enemies_in_range:
            center_x, center_y = self.x, self.y
            enemy_center_x, enemy_center_y = unit.start_turn_position[0], unit.start_turn_position[1]
            line_points = bresenham_line(center_x, center_y, enemy_center_x, enemy_center_y)
            line_pixel_colors = get_pixel_colors(line_points, background_screen)
            
            # Check if any point in the line has the color RIVER_BLUE
            if any(color == RIVER_BLUE for color in line_pixel_colors):
                units_to_remove.append(unit)  # Add the unit to the removal list
                
        # Remove units that need to be removed from enemies_in_range
        for unit in units_to_remove:
            self.enemies_in_range.remove(unit)