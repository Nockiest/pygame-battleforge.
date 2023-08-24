from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from animations.shooting_animation import ShootingAnimation


class Ranged(Unit):
    def __init__(self, hp, attack_range, attack_resistance, base_actions, ammo, base_movement, size, x, y, icon, color, cost):
        super().__init__(hp, attack_range, attack_resistance, base_actions,
                         base_movement, size, x, y, ammo, icon, color, cost)

    def create_shoot_animation(self, line_points):
        print("creating animation")
        self.running_animations.append(
                ShootingAnimation(self.x, self.y, line_points, 10))

    
    def prevent_shhooting_through_forrest(self, line_pixel_colors, line_points):
        if FORREST_GREEN in line_pixel_colors:
            print("Ranged unit can't attack through forests")
            print("Pixel with forest green color:",
                  line_pixel_colors[line_pixel_colors.index(FORREST_GREEN)])
            
            return True
        return False
        # else:
        #     self.running_animations.append(
        #         ShootingAnimation(self.x, self.y, line_points, 10))

    def calculate_self_enemy_center_line(self, attacked_unit_center):
        defender_x = attacked_unit_center[0]
        defender_y = attacked_unit_center[1]

        line_points = bresenham_line(
            self.center[0], self.center[1], defender_x,    defender_y
        )
        return line_points

    def try_attack(self, click_pos, attacked_unit):

        res = super().try_attack(click_pos, attacked_unit)

        if res == "UNIT ATTACKS":
            # Calculate the line between unit's center and click position
            line_points = self.calculate_self_enemy_center_line(
                attacked_unit.center)

            line_pixel_colors = get_pixel_colors(
                line_points, background_screen)
            prevented = self.prevent_shhooting_through_forrest(
                line_pixel_colors, line_points)
            if not prevented:
                self.create_shoot_animation(line_points)
            else:
                res = "Attack not possible"
            # Check if FORREST_GREEN is present in pixel colors

        return res

    def get_attackable_units(self):
        super().get_attackable_units()
        units_to_remove = []  # Create a list to store units to be removed

        for unit in self.enemies_in_range:
            center_x, center_y = self.x, self.y
            enemy_center_x, enemy_center_y = unit.start_turn_position[0], unit.start_turn_position[1]
            line_points = bresenham_line(
                center_x, center_y, enemy_center_x, enemy_center_y)
            line_pixel_colors = get_pixel_colors(
                line_points, background_screen)

            # Check if any point in the line has the color RIVER_BLUE
            if any(color == FORREST_GREEN for color in line_pixel_colors):
                # Add the unit to the removal list
                units_to_remove.append(unit)

        # Remove units that need to be removed from enemies_in_range
        for unit in units_to_remove:
            self.enemies_in_range.remove(unit)

    # def render_attack
