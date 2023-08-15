import pygame
from config import *
from utils.utils import *
import math
import random
# from game_state import *
 
def render_attack_cross(screen, x, y):
    cross_color = (255, 165, 0)  # Orange color
    cross_thickness = 2
    cross_length = 20

    pygame.draw.line(screen, cross_color, (x - cross_length, y),
                     (x + cross_length, y), cross_thickness)
    pygame.draw.line(screen, cross_color, (x, y - cross_length),
                     (x, y + cross_length), cross_thickness)

 
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
        self.center = (self.x + self.size//2, self.y + self.size//2)
        self.start_turn_position = (
            self.x + self.size // 2, self.y + self.size // 2)

        self.ammo = ammo
        self.cost = cost
        self.icon = icon
        self.rect = pygame.Rect(x, y, size, size)
        self.selected = False
        self.able_to_move = self.remain_actions > 0
        self.color = color
        
       
        # if self.color == BLUE:
        #     self.outline_color = BLUE_OUTLINE_COLOR
        # else:
        #     self.outline_color = RED_OUTLINE_COLOR
            
        self.valid_movement_positions = []

    def move_in_game_field(self, click_pos, living_units):
        new_center_x, new_center_y = click_pos

        # Check if the clicked position is a valid movement position
        if any((new_center_x, new_center_y) in valid_pos for valid_pos in self.valid_movement_positions):
            self.x = new_center_x - self.size // 2
            self.y = new_center_y - self.size // 2
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        else:
            # Create a line between the click position and starting position
            movement_line = bresenham_line( new_center_x, new_center_y, self.start_turn_position[0], self.start_turn_position[1]  )

            # Find the first valid movement position along the line
            for pos in movement_line:
               
                if any(pos in valid_pos for valid_pos in self.valid_movement_positions):
                    self.x, self.y = pos[0] - self.size // 2, pos[1] - self.size // 2
                    self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
                    break

    def new_point_interferes(self, living_units, point_x, point_y  ):   
        # Create a new rectangle for the unit's position
        new_rect = pygame.Rect(point_x - self.size // 2, point_y - self.size // 2, self.size, self.size)

        for unit in living_units:
            if unit is self:
                    continue   
            res = unit.rect.colliderect(new_rect)
            if res :
                return True              
        return False
      

    def get_units_movement_area(self, screen,living_units):
        max_distance = self.base_movement  # Maximum distance to check from the unit's center
        num_samples = 360  # Number of samples (angles) around the unit's center

        center_x, center_y = self.start_turn_position[0], self.start_turn_position[1]
        self.valid_movement_positions = []
 

        for angle in range(0, 360, 360 // num_samples):
            # Convert angle to radians
            radians = math.radians(angle)

            valid_movement_positions = []
            current_cost = 0
            distance = 0
            while current_cost  < self.base_movement:
                new_x = center_x + distance * math.cos(radians)
                new_y = center_y + distance * math.sin(radians)
                distance += 1
                # Check if the new position is within the screen boundaries
                if 0 <= new_x < WIDTH and UPPER_BAR_HEIGHT <= new_y < HEIGHT - BUTTON_BAR_HEIGHT:
                    pixel_color = screen.get_at((int(new_x), int(new_y)))

                    # Check for obstacles (river, enemy units, black)
                    if pixel_color in [RIVER_BLUE ]:                      
                        break

                    if self.new_point_interferes(  living_units, new_x, new_y  ):
                        break
                    valid_movement_positions.append((int(new_x), int(new_y)),)
                    

                # Calculate movement cost
                line_pixel_colors=  get_pixel_colors(valid_movement_positions, background_screen)
                movement_cost  = calculate_movement_cost([pixel_color])
                
                current_cost += movement_cost[-1][0]
                 
                
                # Check if total cost exceeds base movement
                if current_cost  >= self.base_movement:
                    
                    break
                 

            self.valid_movement_positions.append(valid_movement_positions)
            
    def draw_possible_movement_area(self, screen):
    # Find the common valid movement positions for all angles
        farthest_points = []
        for angle in self.valid_movement_positions:
            if len(angle) >= 2:
                farthest_points.append(angle[-1])
                farthest_points.append(angle[-2])
            
        # Draw the connected path using lines
        if len(farthest_points) > 1:
            pygame.draw.lines(screen, (0, 255, 0), False, farthest_points, 2)

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
                return ("CANT ATTACK SELF", click_pos, [])

            # Calculate the line between unit's center and click position
            line_points = bresenham_line(
                self.start_turn_position[0], self.start_turn_position[1], click_pos[0], click_pos[1]
            )
            print(line_points)
            # points_on_line = []
            # for point in line_points:
            #     points_on_line.append(point)

            for unit in living_units:
                if unit.rect.collidepoint(click_pos):
                    if unit.color == self.color:
                        return ("YOU CANT DO FRIENDLY FIRE", click_pos, line_points)
                        break

                    return ("UNIT ATTACKS", click_pos, unit, line_points)

        return ("Attack not possible", click_pos, [])

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
      
        print(player.color, self.color, player.units, self)
        # Remove the unit from the 'cur_players' array
        player.units.remove(self)
        player.update_sorted_units()
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
        outline_color = BLACK# self.outline_color  # Use the unit's color for the outline

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
        pygame.draw.rect(screen,  BLACK, outline_rect, 2)
     

        # Draw a line from self.start_turn_position to the center of the unit in red
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        pygame.draw.line(screen, self.color, self.start_turn_position,
                         (center_x, center_y), 2)