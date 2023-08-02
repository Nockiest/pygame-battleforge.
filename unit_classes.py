from unit import Unit

class Knight(Unit):
    def __init__(self, x, y,   color):
        super().__init__(hp=2, attack_range=50, remain_attacks=1, base_movement=200,
                         size=30, x=x, y=y, ammo=0, icon="knight.png",   color=color)

    # Additional methods or overrides for the Knight class


class Musketeer(Unit):
    def __init__(self,   x, y,  color):
        super().__init__(hp=2, attack_range=200, remain_attacks=1, base_movement=125,
                         size=20, x=x, y=y, ammo=50, icon="musket.png",   color=color)

    # Additional methods or overrides for the Musketeer class


class Cannon(Unit):
    def __init__(self,  x, y,  color):
        super().__init__(hp=1, attack_range=300, remain_attacks=1, base_movement=50,
                         size=50, x=x, y=y, ammo=10, icon="canon.png",  color=color)

    # Additional methods or overrides for the Cannon class


class Shield(Unit):
    def __init__(self, x, y, color):
        super().__init__(hp=5, attack_range=0, remain_attacks=0, base_movement=50,
                         size=30, x=x, y=y, ammo=0, icon="armor.png",  color=color)

    # Additional methods or overrides for the Shield class


class Medic(Unit):
    def __init__(self, x, y, color):
        super().__init__(hp = 1, attack_range=100, remain_attacks=3, base_movement=100,
                         size=15, x=x, y=y, ammo=100, icon="medic.png",   color=color)

    # Additional methods or overrides for the Medic class
    def heal(self, target_unit):
        target_unit.hp += 10  # Example: Heal the target unit by 10 HP


class Commander(Unit):
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=0, remain_attacks=0, base_movement=175,
                         size=20, x=x, y=y, ammo=0, icon="commander.png",   color=color)

    # Additional methods or overrides for the Commander class
    def support(self):
        # Implement support method for other units (e.g., buff their abilities)
        pass

    def die(self):
        print("Player lost the game")  # Example: Print a message when the Commander dies


class Pikeman(Unit):
    def __init__(self, x, y,  color):
        super().__init__(hp=3, attack_range=50, remain_attacks=1, base_movement=100,
                         size=20, x=x, y=y, ammo=100, icon="pike.png",   color=color)

    # Additional methods or overrides for the Pikeman class


class SupplyCart(Unit):
    def __init__(self,   x, y,  color):
        super().__init__(hp=1, attack_range=0, remain_attacks=3, base_movement=150,
                         size=30, x=x, y=y, ammo=200, icon="supply.png",   color=color)

    # Additional methods or overrides for the Supply Cart class
    def provide_ammo(self, target_unit):
        target_unit.ammo += 10  # Example: Provide the target unit with 10 ammo


class Observer(Unit):
    def __init__(self,   x, y,  color):
        super().__init__(hp=1, attack_range=0, remain_attacks=0, base_movement=50,
                         icon="spyglass.png", size=15, x=x,)

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