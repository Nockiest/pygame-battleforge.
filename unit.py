import pygame
from config import *
from utils import *
import math
import random


GREEN, WHITE, BLACK, RED, BLUE, YELLOW = colors_tuple


def render_attack_cross(screen, x, y):
    cross_color = (255, 165, 0)  # Orange color
    cross_thickness = 2
    cross_length = 20

    pygame.draw.line(screen, cross_color, (x - cross_length, y),
                     (x + cross_length, y), cross_thickness)
    pygame.draw.line(screen, cross_color, (x, y - cross_length),
                     (x, y + cross_length), cross_thickness)


class Unit:
    def __init__(self, hp, attack_range, base_actions, base_movement, size, x, y, ammo, icon, color, cost):
        self.hp = hp
        self.base_hp = hp
        self.attack_range = attack_range
        self.attack_range_modifiers = 1
        self.remain_actions = 0 #base_actions
        self.base_actions = base_actions
        self.base_movement = base_movement
        self.x = x
        self.y = y
        self.size = size
        self.start_turn_position = (
            self.x + self.size//2, self.y + self.size//2)

        self.ammo = ammo
        self.cost = cost
        self.icon = icon
        self.rect = pygame.Rect(x, y, size, size)
        self.selected = False
        self.able_to_move = self.remain_actions > 0
        self.color = color

    def move_in_game_field(self, click_pos, living_units):
        # Calculate the distance between the new position and the starting position in both x and y directions
        delta_x = click_pos[0] - self.start_turn_position[0]
        delta_y = click_pos[1] - self.start_turn_position[1]

        # Calculate the distance from the starting position to the new position
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
           
        if distance > self.base_movement:
            # Calculate the new position based on the line connecting the two points
            scale_factor = (self.base_movement) / distance
            new_x = int(
                self.start_turn_position[0] + delta_x * scale_factor - self.size // 2)
            new_y = int(
                self.start_turn_position[1] + delta_y * scale_factor - self.size // 2)

        else:
            # The movement is within the allowed range, so set the position directly
            new_x = click_pos[0] - self.size // 2
            new_y = click_pos[1] - self.size // 2

        new_rect =  pygame.Rect(new_x, new_y, self.size, self.size)
        res = self.check_for_direct_overlap(living_units,new_rect)
        if res:
            return print("unit overlaps")
        res = self.control_interference(living_units,new_x,new_y)
        if res == "corrected":
            print("corrected")
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
            return
        else:
            self.x = max(0, min(new_x, WIDTH - self.size))
            self.y = max(0, min(new_y, HEIGHT - BUTTON_BAR_HEIGHT - self.size))     
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
  
    def check_for_direct_overlap(self, living_units,new_rect):
        for unit in living_units:
        # Skip units of the same color, units that cannot be moved, and the unit itself      
            if unit is self:
                continue
            
            res = unit.rect.colliderect(new_rect)
            if res and unit.color == self.color:
                return "collision_with_team_member"
            elif res and unit.color != self.color:
                return "collision_with_enemy"
        return False


    def control_interference(self, living_units,new_x,new_y):
        
        center_x = new_x + self.size // 2
        center_y = new_y + self.size // 2
        # print(center_x,center_y,new_x,new_y)
        for unit in living_units:           
            if unit.color == self.color or unit is self:
                continue

            point_x, point_y, line_points = check_square_line_interference(
                unit, self.start_turn_position[0], self.start_turn_position[1], center_x, center_y)
  
            # print( point_x  , point_y, line_points   )
            if  point_x != None and point_y  != None:
                
                move_unit_along_line(line_points, (point_x, point_y), self)
                return "corrected"
        return None

         
    def draw_as_active(self, screen):
        outline_rect = pygame.Rect(
            self.x - 2, self.y - 2, self.size + 4, self.size + 4)
        pygame.draw.rect(screen, BLACK, outline_rect)
        pygame.draw.circle(
            screen, YELLOW, self.start_turn_position, self.base_movement, 1)

        # Draw a line from self.start_turn_position to the center of the unit in red
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        pygame.draw.line(screen, BLACK, self.start_turn_position,
                         (center_x, center_y), 2)

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
        final_hit_probability = base_hit_chance
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
        warrior_img = pygame.transform.scale(warrior_img, (max_image_size, max_image_size))

        warrior_img_rect = warrior_img.get_rect()
        # Center the image within the allocated space with padding
        warrior_img_rect.center = (self.x + self.size // 2, self.y + self.size // 2)

        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(warrior_img, warrior_img_rect)

        # Render remaining attacks and ammo below the unit
        font = pygame.font.Font(None, 20)
        text_color = (255, 255, 255)  # White color
        text_pos = (self.x, self.y + self.size + padding)  # Adjust the text position with padding
        text_surface = font.render(
            f"Attacks: {self.remain_actions}   Ammo: {self.ammo} Hp: {self.hp}", True, text_color)
        screen.blit(text_surface, text_pos)