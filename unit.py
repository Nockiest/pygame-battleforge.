import pygame
from globalVars import width, height
import math


class Unit:
    def __init__(self, hp, attack_range, base_movement, size, x, y, ammo, icon, selected):
        self.hp = hp
        self.attack_range = attack_range
        self.base_movement = base_movement

        self.x = x
        self.y = y
        self.size = size
        self.start_turn_position = (
            self.x + self.size//2, self.y + self.size//2)
        self.ammo = ammo
        self.icon = icon
        self.rect = pygame.Rect(x, y, size, size)
        self.selected = selected

    def move_in_game_field(self, click_pos):
        top_left_x = click_pos[0] - self.size // 2
        top_left_y = click_pos[1] - self.size // 2
        new_top_left_x_in_window = max(0, min(top_left_x, width - self.size))
        new_top_left_y_in_window = max(0, min(top_left_y, height - self.size))

        # Calculate the distance between the new position and the starting position in both x and y directions
        centered_new_top_left_x_in_window = new_top_left_x_in_window + self.size // 2
        centered_new_top_left_y_in_window = new_top_left_y_in_window + self.size // 2
        delta_x = centered_new_top_left_x_in_window - self.start_turn_position[0]
        delta_y = centered_new_top_left_y_in_window - self.start_turn_position[1]

        # Calculate the distance from the starting position to the new position
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        # Check if the distance exceeds the limit of base_movement
        if distance > self.base_movement:
            # The move is not allowed, so return without changing the position
            return "Unit can't move that far"

        self.x = new_top_left_x_in_window
        self.y = new_top_left_y_in_window

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

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

    def render(self):
        pass
