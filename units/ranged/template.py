from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *


class Ranged(Unit):
    def __init__(self, hp, attack_range, attack_resistance, base_actions, ammo, base_movement, size, x, y, icon, color, cost):
        super().__init__(hp, attack_range, attack_resistance, base_actions,
                         base_movement, size, x, y, ammo, icon, color, cost)
 
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
            if FORREST_GREEN in line_pixel_colors:
                print("Ranged unit can't attack through forests")
                print("Pixel with forest green color:", line_pixel_colors[line_pixel_colors.index(FORREST_GREEN)])
                res = ("RANGED UNIT CAN'T ATTACK THROUGH FORESTS", click_pos, None )

        return res