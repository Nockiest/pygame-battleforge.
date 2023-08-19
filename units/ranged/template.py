from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *


class Ranged(Unit):
    def __init__(self, hp, attack_range, attack_resistance, base_actions, ammo, base_movement, size, x, y, icon, color, cost):
        super().__init__(hp, attack_range, attack_resistance, base_actions,
                         base_movement, size, x, y, ammo, icon, color, cost)
 
    def try_attack(self, click_pos, living_units    ):
        res = super().try_attack(click_pos, living_units)
        print(res, "res")
        if res[0] == "UNIT ATTACKS":
            # Calculate the line between unit's center and click position
            attaacked_unit = res[2]
            line_points = bresenham_line(
                self.center[0], self.center[1], attaacked_unit.center[0], attaacked_unit.center[1]
            )
            # calculate a line to the center of the enemy unit

            # Get the pixel colors along the line
            line_pixel_colors = get_pixel_colors(line_points, background_screen)

            # Check if FORREST_GREEN is present in pixel colors
            if FORREST_GREEN in line_pixel_colors:
                print("Ranged unit can't attack through forests")
                print("Pixel with forest green color:", line_pixel_colors[line_pixel_colors.index(FORREST_GREEN)])
                res = ("RANGED UNIT CAN'T ATTACK THROUGH FORESTS", click_pos, None )

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
            if any(color == FORREST_GREEN for color in line_pixel_colors):
                units_to_remove.append(unit)  # Add the unit to the removal list
                
        # Remove units that need to be removed from enemies_in_range
        for unit in units_to_remove:
            self.enemies_in_range.remove(unit)

     
    def calculate_attack_circle(self, living_units):
        num_samples = 360  # Number of samples (angles) around the unit's center
        center_x, center_y = self.start_turn_position[0], self.start_turn_position[1]
        self.attack_circle = []
        total_attack_range_modifier = sum(self.attack_range_modifiers.values())
        attack_range_with_modifiers = self.attack_range * total_attack_range_modifier

       
        for angle in range(0, 360, 360   // num_samples   ):   
            # Convert angle to radians
            radians = math.radians(angle)
            current_line = []
            current_cost = 0
            base_chunk = WIDTH//2
            distance = base_chunk
            iteration = 2

            # it will create a line from start pos to the endline, it will check, wheter some pixel on 
            # that line is forrest, it will move the attack range to the pixel before the forrest
            # it will get the units enemy units indide the attack circle
             
            while base_chunk//iteration >= 1 and current_cost !=  self.base_movement :

                new_x = min(WIDTH, max( center_x + distance * math.cos(radians), 0)) 
                new_y = min(HEIGHT - BUTTON_BAR_HEIGHT, max( center_y + distance * math.sin(radians), UPPER_BAR_HEIGHT))   
                # print(new_x, new_y)
                line_points = bresenham_line(center_x, center_y, int(new_x), int(new_y))
                line_pixel_colors = get_pixel_colors(line_points, background_screen)
                movement_cost = calculate_movement_cost(line_pixel_colors)  
                current_cost = movement_cost[-1][0]
               
                if current_cost > self.base_movement:
                    # print(distance, iteration, "decrementing",  512//iteration)
                    distance -= base_chunk//iteration
                elif current_cost < self.base_movement: 
                    # print(distance, iteration, "incrementing")
                    distance += base_chunk//iteration          
                current_line = line_points
                iteration*=2


            new_line_points = []
            for point in line_points:
                if not self.new_point_interferes(living_units, point[0], point[1]):
                    new_line_points.append(point)
                else:
                    break  # Stop adding points if interference is detected
            line_points = new_line_points
            self.valid_movement_positions.append(line_points)
            self.valid_movement_positions_edges.append( line_points[len(line_points) - 1] )