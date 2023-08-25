from units.unit import Unit
import math
from utils.utils import *
from config import *
import game_state
from .template import Ranged


class Canon(Ranged):
    size = 40
    cost = 30

    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=300, attack_resistance=0.05, base_actions=1, base_movement=50,
                         size=self.size, x=x, y=y, ammo=5, icon="canon.png", color=color, cost=self.cost)
    
    def __repr__(self):
        return f"Musketeer(x={self.x}, y={self.y}, color={self.color!r})"

    def try_attack(self, click_pos, attacked_unit):
        # print("before calling the function",game_state.living_units, attacked_unit  )
        # # res = Unit.try_attack(self, click_pos, attacked_unit)
        # print("after calling the function",game_state.living_units,   attacked_unit)
        if attacked_unit not in self.enemies_in_range:
            return "Attack not possible"
        self.attack()

        # Calculate a line extending from the center of the unit towards the click position
        unit_center_x, unit_center_y = self.center
        attacked_center_x, attacked_center_y = attacked_unit.center
        dx = attacked_center_x - unit_center_x
        dy = attacked_center_y - unit_center_y
        # Calculate the distance between the attacker and the attacked unit
        distance = math.sqrt(dx ** 2 + dy ** 2)
        # Calculate the angle between the attacker and the attacked unit
        angle_radians = math.atan2(dy, dx)
        point_x = self.center[0] + self.attack_range * math.cos(angle_radians)
        point_y = self.center[1] + self.attack_range * math.sin(angle_radians)
        line_points = bresenham_line(
            self.center[0], self.center[1], int(point_x),    int(point_y)
        )
        line_pixel_colors = get_pixel_colors(
            line_points, background_screen)
        prevented = self.prevent_shhooting_through_forrest(
            line_pixel_colors, line_points)
        if not prevented:
            self.create_shoot_animation(line_points)
        # Check if FORREST_GREEN is present in pixel colors

        # print("Attacker Center:", unit_center_x, unit_center_y)
        # print("Attacked Center:", attacked_center_x, attacked_center_y)
        # print("line points", line_points)
        print("livng units before", game_state.living_units, attacked_unit)
        
        for unit in game_state.living_units.copy():
            print("x")
            print(unit)
            if unit.color == self.color:
                continue
            # elif unit == attacked_unit:
            #     continue

            print(game_state.living_units)
            # print(self.enemies_in_range)
            # print(unit)

            result = check_precalculated_line_square_interference(
                unit, line_points)
            print(result[0], result[1], unit.rect, unit)
            if result[0] != None:
                print(unit, unit.rect,  "interferes at", result[0], result[1])
                # self.try_attack( click_pos,unit)
                remain_hp = unit.take_damage(self)

                if remain_hp < 0:
                    game_state.living_units.remove(unit)
                    self.enemies_in_range.remove(unit)
                    print("Removed", unit, "from game_state.living_units")
            print("x")
            print("copy",  game_state.living_units. copy())

        return "UNIT ATTACKS"
        #     if distance < self.attack_range:
        #         # Extend the line by setting the new endpoint to the attack range distance from the unit center
        #         line_length = self.attack_range
        #         angle = math.atan2(dy, dx)
        #         new_end_x = unit_center_x + line_length * math.cos(angle)
        #         new_end_y = unit_center_y + line_length * math.sin(angle)
        #     print(unit_center_x, unit_center_y, new_end_x, new_end_y)
        #     line_points = bresenham_line(unit_center_x, unit_center_y, int(new_end_x), int(new_end_y))
        #     for unit in game_state.living_units.array:
        #         if unit.color == self.color:
        #             continue
        #         elif unit == attacked_unit:
        #             continue

        #         res = check_precalculated_line_square_interference(unit, line_points)
        #         print(res[0], res[1], unit.rect, unit)
        #         if res[0] != None:
        #             print(unit, unit.rect,  "interferes at" ,res[0], res[1])
        #             # self.try_attack( click_pos,unit)
        #             res = unit.take_damage(self)
        #             if res < 0:
        #                 self.enemies_in_range.remove(unit)

    # zatím je pravěpodobnost zásahu jednotek v cestě 100%, musím změnit
