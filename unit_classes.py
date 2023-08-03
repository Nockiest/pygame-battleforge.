from unit import Unit
import math
from utils import get_two_units_center_distance

class Melee(Unit):
    def __init__(self, hp, attack_range, base_actions, base_movement, size, x, y, icon, color):
        super().__init__(hp, attack_range, base_actions,
                         base_movement, size, x, y, None, icon, color)

    def try_attack(self, click_pos, living_units):
        dx = click_pos[0] - (self.x + self.size // 2)
        dy = click_pos[1] - (self.y + self.size // 2)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance <= self.attack_range:
            if self.rect.collidepoint(click_pos):
                return ("CANT ATTACK SELF", click_pos)
             
            for unit in living_units:
                if unit.rect.collidepoint(click_pos):
                    if unit.color == self.color:
                        return ("YOU CANT DO FRIENDLY FIRE",click_pos)
                        break
                    self.remain_actions -= 1
                     
                     
                    self.attack_square(click_pos)
                    hit_result = unit.check_if_hit(0.8)  # 80% hit chance
                    if hit_result:
                        unit.take_damage(living_units)
                        if unit.hp <= 0:
                            unit.remove_from_game(living_units)
                    print(f"{self} hit {unit}?", hit_result)
                    return ("UNIT ATTACKS", click_pos)

        return ("Attack not possible", click_pos)
    
class Support(Unit):
    def __init__(self, hp, attack_range, base_actions, base_movement, size, x, y, icon, color):
        # Call the constructor of the parent class (Unit) without specifying the 'ammo' parameter
        super().__init__(hp, attack_range, base_actions,
                         base_movement, size, x, y, None, icon, color)
        
    def try_attack(self, click_pos, living_units):
        return ("this is a support unit and cant attack")

class Knight(Melee):
    def __init__(self, x, y,   color):
        super().__init__(hp=2, attack_range=40, base_actions=1, base_movement=200,
                         size=30, x=x, y=y,   icon="knight.png",   color=color)

    # Additional methods or overrides for the Knight class


class Shield(Support):
    def __init__(self, x, y, color):
        super().__init__(hp=5, attack_range=0,base_actions=1, base_movement=30,
                         size=30, x=x, y=y,   icon="armor.png",  color=color)

    # Additional methods or overrides for the Shield class


class Pikeman(Melee):
    def __init__(self, x, y,  color):
        super().__init__(hp=3, attack_range=50, base_actions=1, base_movement=100,
                         size=20, x=x, y=y,  icon="pike.png",   color=color)

    # Additional methods or overrides for the Pikeman class


class Musketeer(Unit):
    def __init__(self,   x, y,  color):
        super().__init__(hp=2, attack_range=200,base_actions=1, base_movement=125,
                         size=20, x=x, y=y, ammo=50, icon="musket.png",   color=color)

    # Additional methods or overrides for the Musketeer class


class Cannon(Unit):
    def __init__(self,  x, y,  color):
        super().__init__(hp=1, attack_range=300, base_actions=1, base_movement=50,
                         size=40, x=x, y=y, ammo=10, icon="canon.png",  color=color)

    # Additional methods or overrides for the Cannon class


class Medic(Support):
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=100,base_actions=1, base_movement=75,
                         size=15, x=x, y=y,  icon="medic.png",   color=color)

   
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

class Commander(Unit):
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=40, base_actions=1, base_movement=150,
                         size=20, x=x, y=y, ammo=1, icon="commander.png", color=color)

    # Additional methods or overrides for the Commander class
    def support(self):
        # Implement support method for other units (e.g., buff their abilities)
        pass

    def take_damage(self, living_units):
    # Call the parent class's take_damage method first
        super().take_damage(living_units)
        # Perform additional actions or logic specific to the Commander class
        self.die()

    def die(self):
        # Example: Print a message when the Commander dies
        print("Player lost the game")



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
                         icon="spyglass.png", size=15, x=x, y=y,  color=color)

# Testing the classes:
# You can create instances of these classes and test their methods and behaviors in your game.
# For example:
# knight = Knight(100, 1, 30, 100, 100, False, (255, 0, 0))
# musketeer = Musketeer(80, 2, 30, 200, 200, False, (0, 255, 0))
# cannon = Cannon(120, 1, 40, 300, 300, False, (0, 0, 255))
# shield = Shield(200, 40, 400, 400, False, (255, 255, 0))
# medic = Medic(40, 1, 25, 500, 500, False, (255, 0, 255))
# commander = Commander(30, 600, 100, False, (0, 255, 255))
# pikeman = Pikeman(80, 1, 30, 700, 100, False, (128, 128, 128))
# supply_cart = SupplyCart(50, 100, 500, False, (0, 0,
