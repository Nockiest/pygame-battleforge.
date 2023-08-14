from unit import Unit
import math
from utils import *
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
            print(line_pixel_colors)
            # Check if FORREST_GREEN is present in pixel colors
            if RIVER_BLUE   in line_pixel_colors:
                print("Ranged unit can't attack through forests")
                res = ("MELEE UNIT CAN'T ATTACK THROUGH RIVERS ", click_pos, None)

        return res

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
                res = ("RANGED UNIT CAN'T ATTACK THROUGH FORESTS", click_pos, None)

        return res
class Support(Unit):
    def __init__(self, hp, attack_range,attack_resistance, base_actions, base_movement, size, x, y, icon, color, cost, custom_ammo=None):
        # Call the constructor of the parent class (Unit) without specifying the 'ammo' parameter
        ammo = custom_ammo if custom_ammo is not None else None
        super().__init__(hp, attack_range, attack_resistance, base_actions,
                         base_movement, size, x, y, ammo, icon, color, cost)
        
        
    def try_attack(self, click_pos, living_units):
        return  ("SUPPORTS DONT ATTACK") 

class Knight(Melee):
    def __init__(self, x, y,   color):
        super().__init__(hp=2, attack_range=30, attack_resistance=0.1,base_actions=1, base_movement=200,
                         size=30, x=x, y=y,   icon="knight.png",   color=color, cost=20)

    # Additional methods or overrides for the Knight class


class Pikeman(Melee):
    def __init__(self, x, y,  color ):
        super().__init__(hp=3, attack_range=30,attack_resistance=0.1, base_actions=1, base_movement=100,
                         size=20, x=x, y=y,  icon="pikeman.png",   color=color, cost=10)

    # Additional methods or overrides for the Pikeman class



 
class Musketeer(Ranged):
    def __init__(self,   x, y,  color):
        super().__init__(hp=2, attack_range=200,attack_resistance=0.05,base_actions=1, base_movement=125,
                         size=20, x=x, y=y, ammo=10, icon="musketeer.png",   color=color, cost=15)

    # Additional methods or overrides for the Musketeer class


class Canon(Ranged):
    def __init__(self,  x, y,  color):
        super().__init__(hp=1, attack_range=300,attack_resistance=0.05, base_actions=1, base_movement=50,
                         size=40, x=x, y=y, ammo=5, icon="canon.png",  color=color, cost=30)

    # Additional methods or overrides for the Cannon class

class Commander(Melee):
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=40,attack_resistance=0.2, base_actions=1, base_movement=150,
                         size=20, x=x, y=y,    icon="commander.png", color=color, cost=10000)

    # Additional methods or overrides for the Commander class
    def support(self):
        # Implement support method for other units (e.g., buff their abilities)
        pass

 

class Medic(Support):
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=100,attack_resistance=0.05,base_actions=1, base_movement=75,
                         size=20, x=x, y=y,  icon="medic.png",   color=color, cost=50)

   
    # def reset_for_next_turn(self, living_units):
      
    #     super().reset_for_next_turn()  # Call the reset_for_next_turn method of the parent class (Support)
    #     self.heal(living_units)  # Call the heal method to heal nearby units

    def heal(self, unit):
        # for unit in units:
            # Check if the target unit is not a Medic and is within the range of base movement
            if not isinstance(unit, Medic):
                distance = get_two_units_center_distance(self,unit)
                if distance <= self.base_movement and unit.base_hp > unit.hp:
                    unit.hp += 1  # Heal the target unit by 1 HP

 
class SupplyCart(Support):
    def __init__(self,   x, y,  color):
        super().__init__(hp=1, attack_range=50,attack_resistance=0.05, base_actions=1, base_movement=150,
                         size=30, x=x, y=y, icon="supplycart.png", color=color, cost=500, custom_ammo=20)
         

    def dispense_ammo(self, amount, living_units):
        print("called")
        for unit in living_units:
            if self.ammo <= 0:
                print("no ammo left")
                break

            if unit.color != self.color:
                continue

            if isinstance(unit, Ranged) and distance(self.center, unit.center) < RESUPPLY_RANGE:
                print(self.ammo)
                unit.ammo += amount
                self.ammo -= amount
                print(f"Dispensing {amount} ammo. Remaining ammo: {self.ammo} to {unit}vv")

    # def provide_ammo(self,ammount, units):
    #     print("called")
    #     for unit in units:
    #         # Check if the target unit is not a Melee or Support unit
    #         if isinstance(unit,  Ranged ):
    #             distance = get_two_units_center_distance(self ,unit    )
    #             if distance <= self.base_movement:
    #                 unit.ammo += ammount  # Provide the target unit with 10 ammo
    #                 self.ammo -= ammount  # Provide the target unit with 10 ammo
                     


class Observer(Support):
    def __init__(self, x, y,  color):
        super().__init__(hp=1, attack_range=0,attack_resistance=0.05, base_actions=1,  base_movement=50,
                         icon="observer.png", size=20, x=x, y=y,  color=color, cost=500)
        
class Shield(Support):
    def __init__(self, x, y, color):
        super().__init__(hp=5, attack_range=0,attack_resistance=0.2,base_actions=1, base_movement=30,
                         size=30, x=x, y=y,   icon="shield.png",  color=color, cost=50)

    # Additional methods or overrides for the Shield class

 
