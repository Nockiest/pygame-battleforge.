import pygame
from config import *
from utils import *
import math
import random


def render_attack_cross(screen, x, y):
    cross_color = (255, 165, 0)  # Orange color
    cross_thickness = 2
    cross_length = 20

    pygame.draw.line(screen, cross_color, (x - cross_length, y),
                     (x + cross_length, y), cross_thickness)
    pygame.draw.line(screen, cross_color, (x, y - cross_length),
                     (x, y + cross_length), cross_thickness)

def calculate_movement_cost(color_list):
    movement_costs = []
    total_cost = 0
    
    for i, color in enumerate(color_list):
        if color == FORREST_GREEN:
            total_cost += 2
        elif color == ROAD_GRAY:
            total_cost += 0.5
        elif color == RIVER_BLUE:
            total_cost += 1000000 # to prevent the unit from going over the river 
        elif color == BRIDGE_COLOR:
            total_cost += 1
        elif color == TOWN_RED or color == HOUSE_PURPLE:
            total_cost += 1
        elif color == TERMINATE_COLOR:
            total_cost += 10000000000
            movement_costs.append((total_cost, i, color))
            return movement_costs
        else:
            total_cost += 1  # Default movement cost
        
        movement_costs.append((total_cost, i, color))
    
    return movement_costs
class Unit:
    def __init__(self, hp, attack_range, attack_resistance, base_actions, base_movement, size, x, y, ammo, icon, color, cost):
        self.hp = hp
        self.base_hp = hp
        self.attack_range = attack_range
        self.attack_range_modifiers = 1
        self.remain_actions = 0  # base_actions
        self.base_actions = base_actions
        self.base_movement = base_movement
        self.atttack_resistance = attack_resistance
        self.x = x
        self.y = y
        self.size = size
        self.start_turn_position = (
            self.x + self.size // 2, self.y + self.size // 2)

        self.ammo = ammo
        self.cost = cost
        self.icon = icon
        self.rect = pygame.Rect(x, y, size, size)
        self.selected = False
        self.able_to_move = self.remain_actions > 0
        self.color = color
        
        # Assign outline color based on unit's team color
        if self.color == BLUE:
            self.outline_color = BLUE_OUTLINE_COLOR
        else:
            self.outline_color = RED_OUTLINE_COLOR
            
        self.valid_movement_positions = None

    def move_in_game_field(self, click_pos, living_units):
    # Calculate the endpoint of the Bresenham line
        movement_line = bresenham_line(self.start_turn_position[0], self.start_turn_position[1],  click_pos[0],  click_pos[1])   
        line_point_colors = get_pixel_colors(movement_line, background_screen)
        # count the movement cost of every pixel based on its color
        movement_costs = calculate_movement_cost(line_point_colors)

        new_center_x, new_center_y = self.start_turn_position  # Initialize new_center_x and new_center_y

        # find the pixel that doesn't overshoot the movement cost
        print(movement_costs[-1][0])
        for cost, index, color in reversed(movement_costs):
            if cost < self.base_movement:
                # Update the new_center_x and new_center_y
                new_center_x, new_center_y = movement_line[index - 1]
                # Set the unit's position to the last point before the condition was applied
                self.x = new_center_x - self.size // 2
                self.y = new_center_y - self.size // 2
                self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
                break

        new_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        # check whether the unit interferes with another of enemy units

        # if yes set the position to be just before the enemy unit
        res = self.control_interference(living_units, new_center_x, new_center_y, new_rect)
        print(res)
        if res == "corrected":
            print("corrected")
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
            return
        else:
            self.x = max(0, min(new_center_x - self.size // 2, WIDTH - self.size))
            self.y = max(0, min(new_center_y - self.size // 2, HEIGHT - BUTTON_BAR_HEIGHT - self.size))
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # check wheter the unit interferes with another of enemy units

        # if yes set the position to be just before the enemy unit

        # if there is a friendly unit where you want to place the unit set the moved unit before or arfter 
        # that unit

    def control_interference(self, living_units, center_x, center_y, new_rect):
        # print(center_x,center_y,new_x,new_y)
        for unit in living_units:
            if unit is self:
                    continue
            if unit.color == self.color:
                res = unit.rect.colliderect(new_rect)
                if res and unit.color == self.color:
                    return "collision_with_team_member"
                 

            point_x, point_y, line_points = check_square_line_interference(
                unit, self.start_turn_position[0], self.start_turn_position[1], center_x, center_y)

            # print( point_x  , point_y, line_points   )
            if point_x != None and point_y != None:

                move_unit_along_line(
                    line_points, (point_x, point_y), self, screen)
                return "corrected"
        return None

    def get_units_movement_area(self, screen  ):
        max_distance = self.base_movement  # Maximum distance to check from the unit's center
        num_samples = 360  # Number of samples (angles) around the unit's center

        center_x, center_y = self.start_turn_position[0], self.start_turn_position[1]
        valid_movement_positions = []
        angles_with_obstacle = []

        # Determine enemy color based on unit's color
        if self.color == BLUE:
            enemy_color = RED
        else:
            enemy_color = BLUE

        for angle in range(0, 360, 360 // num_samples):
            # Convert angle to radians
            radians = math.radians(angle)

            for distance in range(1, max_distance + 1):
                new_x = center_x + distance * math.cos(radians)
                new_y = center_y + distance * math.sin(radians)

                # Check if the new position is within the screen boundaries
                if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT - BUTTON_BAR_HEIGHT:
                    pixel_color = screen.get_at((int(new_x), int(new_y)))

                    # Check for obstacles (river, enemy units, black)
                    if pixel_color == RIVER_BLUE or pixel_color in [BLACK, enemy_color]:
                        angles_with_obstacle.append(angle)
                    elif angle not in angles_with_obstacle:
                        valid_movement_positions.append((int(new_x), int(new_y)))

        self.valid_movement_positions = valid_movement_positions

    def draw_possible_movement_area(self, screen   ):
        
        # Draw valid movement positions on the screen
        for pos in self.valid_movement_positions:
            pygame.draw.circle(screen, (0, 255, 0), pos, 2)  # Draw a green circle at the valid position
 
    def render_attack_circle(self, screen):
        pygame.draw.circle(screen, RED, (self.x + self.size //
                           2, self.y + self.size//2), self.attack_range*self.attack_range_modifiers, 1)

    def attack_square(self, click_pos):
        self.attack_cross_position = click_pos
        self.attack_cross_time = pygame.time.get_ticks()
        self.remain_actions -= 1
        if self.ammo != None:
            self.ammo -= 1

    def render_attack_cross(self, screen):  
        if hasattr(self, 'attack_cross_position') and hasattr(self, 'attack_cross_time'):
            time_elapsed = pygame.time.get_ticks() - self.attack_cross_time
            # Render the cross for 1 second (1000 milliseconds)
            if time_elapsed <= 1000:
                render_attack_cross(screen, *self.attack_cross_position)
            else:
                del self.attack_cross_position
                del self.attack_cross_time

    def try_attack(self, click_pos, living_units):

        # Check if the click position is within the attack range of the unit
        dx = click_pos[0] - (self.x + self.size // 2)
        dy = click_pos[1] - (self.y + self.size // 2)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance <= self.attack_range:
            # Check if the click position does not collide with the unit's rectangle
            if self.rect.collidepoint(click_pos):
                return ("CANT ATTACK SELF", click_pos)

            for unit in living_units:
                if unit.rect.collidepoint(click_pos):
                    if unit.color == self.color:
                        return ("YOU CANT DO FRIENDLY FIRE", click_pos)
                        break

                    return ("UNIT ATTACKS", click_pos, unit)

        return ("Attack not possible", click_pos)

    def check_if_hit(self, base_hit_chance):

        # i will augment base_hit_chance by some variables
        final_hit_probability = base_hit_chance - self.atttack_resistance
        print(final_hit_probability, "final hit probability")
        # Generate a random float between 0 and 1
        hit_treshold_value = random.random()

        # Calculate the actual hit chance considering the base_hit_chance and random factor

        print(final_hit_probability,  hit_treshold_value, "comparing")
        # Check if the unit is hit based on the actual hit chance
        if final_hit_probability >= hit_treshold_value:
            return True  # Unit is hit
        else:
            return False  # Unit is not hi

    def take_damage(self):
        self.hp -= 1
        return self.hp

    def capture(self, target_building):
        pass
        # Implement the logic for the unit to capture the target_building
        # Check if the target_building is within the capture range of the unit
        # Reduce the capture progress of the building until it is captured

    def remove_from_game(self, living_units, player):
        # Remove the unit from the 'units' list of the player
        # self.player.units.remove(self)
        print(player.color, self.color, player.units, self)
        # Remove the unit from the 'cur_players' array
        player.units.remove(self)
        living_units.remove(self)
        # Set the unit's x, y, and rect attributes to None to remove it from the game field
        self.x = None
        self.y = None
        self.rect = None

        print("Unit is dead")

    def reset_for_next_turn(self):
        self.start_turn_position = (
            self.x + self.size//2, self.y + self.size//2)

        self.remain_actions = 1

        self.able_to_move = True
        self.remain_actions = self.base_actions

    def render_on_screen(self, screen):
        padding = 2  # Adjust the padding size as needed

        warrior_img = pygame.image.load(f"img/{self.icon}")
        # Scale down the image to fit within the allocated space with padding
        max_image_size = self.size - padding * 2
        warrior_img = pygame.transform.scale(
            warrior_img, (max_image_size, max_image_size))

        warrior_img_rect = warrior_img.get_rect()
        # Center the image within the allocated space with padding
        warrior_img_rect.center = (
            self.x + self.size // 2, self.y + self.size // 2)

        # Determine the outline color based on the unit's team color
        outline_color = self.outline_color  # Use the unit's color for the outline

        # Draw the filled rectangle for the unit
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, outline_color, self.rect, 1)  # Outline

        # Draw the unit image
        screen.blit(warrior_img, warrior_img_rect)

        # Render remaining attacks and ammo below the unit
        font = pygame.font.Font(None, 20)
        text_color = (255, 255, 255)  # White color
        # Adjust the text position with padding
        text_pos = (self.x, self.y + self.size + padding)
        text_surface = font.render(
            f"Attacks: {self.remain_actions}   Ammo: {self.ammo} Hp: {self.hp}", True, text_color)
        screen.blit(text_surface, text_pos)

    def draw_as_active(self, screen):
        outline_rect = pygame.Rect(
            self.x - 2, self.y - 2, self.size + 4, self.size + 4)
        pygame.draw.rect(screen, self.outline_color, outline_rect)
        pygame.draw.circle(
            screen, YELLOW, self.start_turn_position, self.base_movement, 1)

        # Draw a line from self.start_turn_position to the center of the unit in red
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        pygame.draw.line(screen, self.color, self.start_turn_position,
                         (center_x, center_y), 2)