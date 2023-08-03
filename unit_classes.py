from unit import Unit
import math
from utils import get_two_units_center_distance

class Melee(Unit):
    def __init__(self, hp, attack_range, base_actions, base_movement, size, x, y, icon, color):
        super().__init__(hp, attack_range, base_actions,
                         base_movement, size, x, y, None, icon, color)

class Ranged(Unit):
      def __init__(self, hp, attack_range, base_actions, ammo, base_movement, size, x, y, icon, color):
        super().__init__(hp, attack_range, base_actions,
                         base_movement, size, x, y, ammo, icon, color)
 
class Support(Unit):
    def __init__(self, hp, attack_range, base_actions, base_movement, size, x, y, icon, color):
        # Call the constructor of the parent class (Unit) without specifying the 'ammo' parameter
        super().__init__(hp, attack_range, base_actions,
                         base_movement, size, x, y, None, icon, color)
        
    def try_attack(self, click_pos, living_units):
        return ("this is a support unit and cant attack")

class Knight(Melee):
    def __init__(self, x, y,   color):
        super().__init__(hp=2, attack_range=30, base_actions=1, base_movement=200,
                         size=30, x=x, y=y,   icon="knight.png",   color=color)

    # Additional methods or overrides for the Knight class


class Pikeman(Melee):
    def __init__(self, x, y,  color):
        super().__init__(hp=3, attack_range=30, base_actions=1, base_movement=100,
                         size=20, x=x, y=y,  icon="pike.png",   color=color)

    # Additional methods or overrides for the Pikeman class



 
class Musketeer(Ranged):
    def __init__(self,   x, y,  color):
        super().__init__(hp=2, attack_range=200,base_actions=1, base_movement=125,
                         size=20, x=x, y=y, ammo=50, icon="musket.png",   color=color)

    # Additional methods or overrides for the Musketeer class


class Cannon(Ranged):
    def __init__(self,  x, y,  color):
        super().__init__(hp=1, attack_range=300, base_actions=1, base_movement=50,
                         size=40, x=x, y=y, ammo=10, icon="canon.png",  color=color)

    # Additional methods or overrides for the Cannon class

class Commander(Ranged):
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=40, base_actions=1, base_movement=150,
                         size=20, x=x, y=y, ammo=1, icon="commander.png", color=color)

    # Additional methods or overrides for the Commander class
    def support(self):
        # Implement support method for other units (e.g., buff their abilities)
        pass

    def lose_game(self):
        print(self.color, " lost the game" )



class Medic(Support):
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=100,base_actions=1, base_movement=75,
                         size=20, x=x, y=y,  icon="medic.png",   color=color)

   
    def reset_for_next_turn(self, living_units):
      
        super().reset_for_next_turn()  # Call the reset_for_next_turn method of the parent class (Support)
        self.heal(living_units)  # Call the heal method to heal nearby units

    def heal(self, units):
        for unit in units:
            # Check if the target unit is not a Medic and is within the range of base movement
            if not isinstance(unit, Medic):
                distance = get_two_units_center_distance(self,unit)
                if distance <= self.base_movement and unit.base_hp > unit.hp:
                    unit.hp += 1  # Heal the target unit by 1 HP

 
class SupplyCart(Support):
    def __init__(self,   x, y,  color):
        super().__init__(hp=1, attack_range=0, base_actions=1, base_movement=150,
                         size=30, x=x, y=y,   icon="supply.png",   color=color)

    # Additional methods or overrides for the Supply Cart class
    def reset_for_next_turn(self, living_units):
      
        super().reset_for_next_turn()  # Call the reset_for_next_turn method of the parent class (Support)
        self.provide_ammo_to_units(living_units)  # Call the heal method to heal nearby units

     

    def provide_ammo_to_units(self, units):
        for unit in units:
            # Check if the target unit is not a Melee or Support unit
            if not isinstance(unit, (Melee, Support)):
                distance = get_two_units_center_distance(self,unit)
                if distance <= self.base_movement:
                    unit.ammo += 1  # Provide the target unit with 10 ammo


class Observer(Support):
    def __init__(self, x, y,  color):
        super().__init__(hp=1, attack_range=0, base_actions=1,  base_movement=50,
                         icon="spyglass.png", size=20, x=x, y=y,  color=color)
class Shield(Support):
    def __init__(self, x, y, color):
        super().__init__(hp=5, attack_range=0,base_actions=1, base_movement=30,
                         size=30, x=x, y=y,   icon="armor.png",  color=color)

    # Additional methods or overrides for the Shield class

 
