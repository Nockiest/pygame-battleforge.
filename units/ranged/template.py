from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from animations.shooting_animation import ShootingAnimation
from animations.basic_animations import AmmoExpendedAnimation
import re

class Ranged(Unit):
    def __init__(self, hp, attack_range, attack_resistance, base_actions, ammo, base_movement, size, x, y, icon, color, cost):
        super().__init__(hp, attack_range, attack_resistance, base_actions,
                         base_movement, size, x, y, ammo, icon, color, cost)
       

    
    def prevent_shhooting_through_forrest(self, line_pixel_colors, line_points):
        if FORREST_GREEN in line_pixel_colors:
            print("Ranged unit can't attack through forests")
            print("Pixel with forest green color:",
                  line_pixel_colors[line_pixel_colors.index(FORREST_GREEN)])
            
            return True
        return False
        
    def calculate_self_enemy_center_line(self, attacked_unit_center):
        defender_x = attacked_unit_center[0]
        defender_y = attacked_unit_center[1]

        line_points = bresenham_line(
            self.center[0], self.center[1], defender_x,    defender_y
        )
        return line_points
    def attack(self):
        super().attack()
        animations.append(AmmoExpendedAnimation(self.x,self.y - self.size//2))
    
    def render_attack_circle(self):
        self.check_if_observer_in_range( )
        return super().render_attack_circle()
    

    def try_attack(self, click_pos, attacked_unit):
        self.check_if_observer_in_range( )
         
        if attacked_unit in self.enemies_in_range:
            self.attack()
            res = "UNIT ATTACKS"
        else:
           return "Attack not possible"

        
        # Calculate the line between unit's center and click position
        line_points = self.calculate_self_enemy_center_line(
            attacked_unit.center)

        line_pixel_colors = get_pixel_colors(
            line_points, background_screen)
        prevented = self.prevent_shhooting_through_forrest(
            line_pixel_colors, line_points)
        # if not prevented:
        #     self.create_shoot_animation(line_points)
        if prevented:
            return "Attack not possible"
            
               
            # Check if FORREST_GREEN is present in pixel colors

        return "UNIT ATTACKS"

    def get_attackable_units(self):
        super().get_attackable_units()
        units_to_remove = []  # Create a list to store units to be removed

        for unit in self.enemies_in_range:
            center_x, center_y = self.center[0], self.center[1]
            enemy_center_x, enemy_center_y = unit.start_turn_position[0], unit.start_turn_position[1]
            line_points = bresenham_line(
                center_x, center_y, enemy_center_x, enemy_center_y)
            line_pixel_colors = get_pixel_colors(
                line_points, background_screen)

            # Check if any point in the line has the color RIVER_BLUE
            if any(color == FORREST_GREEN for color in line_pixel_colors):
                # Add the unit to the removal list
                units_to_remove.append(unit)
                line_index = next((j for j, line in enumerate(
                    self.lines_to_enemies_in_range) if line["enemy"] == unit), None)
                if line_index is not None:
                    # Add an interference point to the line
                    interference_point = next(
                        (point for point, color in zip(line_points, line_pixel_colors) if color == FORREST_GREEN), None)
                    self.lines_to_enemies_in_range[line_index]["interference_point"] = interference_point

        # Remove units that need to be removed from enemies_in_range
        for unit in units_to_remove:
            self.enemies_in_range.remove(unit)

    def check_if_observer_in_range(self):
        observer_units = []
        for unit in  living_units.array:
            if unit.color == self.color:
                if re.search("observer", repr(unit), re.IGNORECASE):
                    
                    observer_units.append(unit)
        range_provided = False
        for observer in observer_units:
            res = observer.provide_attack_range(self)
          
            if res:
                range_provided = True
        if range_provided == False:
             
            self.attack_range_modifiers["in_observer_range"] = 0
         
    def move_in_game_field(self, click_pos):
        super().move_in_game_field(click_pos)
        
         
        
        ## get all the firendly observers
        # game_state.players[game_state.cur_player].sorted_by_class_units:
  

    # def render_attack
