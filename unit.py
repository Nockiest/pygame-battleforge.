import pygame
from config import WIDTH, HEIGHT, colors_tuple
import math
GREEN, WHITE, BLACK, RED, BLUE, YELLOW = colors_tuple

def render_attack_cross(screen, x, y):
    cross_color = (255, 165, 0)  # Orange color
    cross_thickness = 2
    cross_length = 20
    print("function called")
    pygame.draw.line(screen, cross_color, (x - cross_length, y), (x + cross_length, y), cross_thickness)
    pygame.draw.line(screen, cross_color, (x, y - cross_length), (x, y + cross_length), cross_thickness)
class Unit:
    def __init__(self, hp, attack_range, remain_attacks, base_movement, size, x, y, ammo, icon, selected):
        self.hp = hp
        self.attack_range = attack_range
        self.remain_attacks = remain_attacks
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
        new_top_left_x_in_window = max(0, min(top_left_x, WIDTH - self.size))
        new_top_left_y_in_window = max(0, min(top_left_y, HEIGHT - self.size))

        # Calculate the distance between the new position and the starting position in both x and y directions
        centered_new_top_left_x_in_window = new_top_left_x_in_window + self.size // 2
        centered_new_top_left_y_in_window = new_top_left_y_in_window + self.size // 2
        delta_x = centered_new_top_left_x_in_window - \
            self.start_turn_position[0]
        delta_y = centered_new_top_left_y_in_window - \
            self.start_turn_position[1]

        # Calculate the distance from the starting position to the new position
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        # Check if the distance exceeds the limit of base_movement
        if distance > self.base_movement:
            # The move is not allowed, so return without changing the position
            return "Unit can't move that far"

        self.x = new_top_left_x_in_window
        self.y = new_top_left_y_in_window

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw_as_active(self, screen):
        # print(self.x, self.y, self.start_turn_position)
        outline_rect = pygame.Rect(
            self.x - 2, self.y - 2, self.size + 4, self.size + 4)
        pygame.draw.rect(screen, BLACK, outline_rect)
        pygame.draw.circle(
            screen, YELLOW, self.start_turn_position, self.base_movement, 1)

    def render_attack_circle(self, screen):
        pygame.draw.circle(screen, RED, (self.x + self.size //
                           2, self.y + self.size//2), self.attack_range, 1)
    def attack_square(self, click_pos):
        self.attack_cross_position = click_pos
        self.attack_cross_time = pygame.time.get_ticks()

    def render_attack_cross(self, screen):
        if hasattr(self, 'attack_cross_position') and hasattr(self, 'attack_cross_time'):
            time_elapsed = pygame.time.get_ticks() - self.attack_cross_time
            if time_elapsed <= 1000:  # Render the cross for 1 second (1000 milliseconds)
                render_attack_cross(screen, *self.attack_cross_position)
            else:
                del self.attack_cross_position
                del self.attack_cross_time
    def attack(self, click_pos):
        # Check if the click position is within the attack range of the unit
        dx = click_pos[0] - (self.x + self.size // 2)
        dy = click_pos[1] - (self.y + self.size // 2)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance <= self.attack_range:
            # Check if the click position does not collide with the unit's rectangle
            if not self.rect.collidepoint(click_pos):
                self.attack_square(click_pos)
                return "UNIT ATTACKS " + str(click_pos)

        return "Attack not possible"

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

    def reset_for_next_turn(self):
        self.start_turn_position = (
            self.x + self.size//2, self.y + self.size//2)
