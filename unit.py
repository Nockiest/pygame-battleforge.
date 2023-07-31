import pygame

class Unit:
    def __init__(self, hp, attack_range, base_movement,size, x, y, ammo, icon  ):
        self.hp = hp
        self.attack_range = attack_range
        self.base_movement = base_movement
        self.x = x
        self.y = y
        self.size = size
        self.ammo = ammo
        self.icon = icon
        self.rect = pygame.Rect(x, y, size, size)
       

    def move(self, new_x, new_y):
        # Implement the logic to move the unit to new coordinates (new_x, new_y)
        # Check if the movement is valid based on the base_movement attribute
        self.x = new_x
        self.y = new_y

    def attack(self, target_unit):
        pass
        # Implement the logic for the unit to attack the target_unit
        # Check if the target_unit is within attack_range
        # Reduce the target_unit's HP based on the unit's attack power

    def check_if_hit(self):
        pass
        # Implement the logic to check if the unit is hit by the enemy
        # You can use random numbers to simulate the chance of being hit

    def capture(self, target_building):
        pass
        # Implement the logic for the unit to capture the target_building
        # Check if the target_building is within the capture range of the unit
        # Reduce the capture progress of the building until it is captured

    def die(self):
        # Implement the logic for the unit to die
        # Remove the unit from the game or set its HP to 0
        pass
