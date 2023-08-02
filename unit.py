import pygame
from config import WIDTH, HEIGHT, colors_tuple
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
    def __init__(self, hp, attack_range, remain_attacks, base_movement, size, x, y, ammo, icon, color):
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
        self.selected = False
        self.ableToMove = True
        self.color = color

    def move_in_game_field(self, click_pos):
    # Calculate the distance between the new position and the starting position in both x and y directions
         
        delta_x = click_pos[0] - self.start_turn_position[0]  
        delta_y = click_pos[1] - self.start_turn_position[1]   
        print(click_pos, self.start_turn_position,delta_x,delta_y)
        # Calculate the distance from the starting position to the new position
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        print(distance, self.base_movement + self.size // 2, self.base_movement, self.size // 2)
        # Check if the distance exceeds the limit of base_movement + size/2
        if distance > self.base_movement:
            # Calculate the new position based on the line connecting the two points
            scale_factor = (self.base_movement  ) / distance
            new_x = int(self.start_turn_position[0] + delta_x * scale_factor  - self.size // 2 )
            new_y = int(self.start_turn_position[1] + delta_y * scale_factor - self.size // 2)
            print(new_x, "new x", new_y , "new_y")
        else:
            # The movement is within the allowed range, so set the position directly
            new_x = click_pos[0]  - self.size // 2
            new_y = click_pos[1]  - self.size // 2

            print(new_x, "new x", new_y , "new_y as centered_click_pos")

        # Ensure that the unit stays within the game window boundaries
        self.x = max(0, min(new_x, WIDTH - self.size))
        self.y = max(0, min(new_y, HEIGHT - self.size))

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
            # Render the cross for 1 second (1000 milliseconds)
            if time_elapsed <= 1000:
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
               
                self.remain_attacks -= 1
                self.ammo -= 1 
                self.ableToMove = self.ammo > 0 and self.remain_attacks > 0
                print(self.ableToMove)
                self.attack_square(click_pos)

                return ("UNIT ATTACKS" ,click_pos)
            
           
        return ("Attack not possible",click_pos)

    def check_if_hit(self, base_hit_chance):
         
        final_hit_probability= base_hit_chance #i will augment base_hit_chance by some variables
        # Generate a random float between 0 and 1
        hit_treshold_value = random.random()

        # Calculate the actual hit chance considering the base_hit_chance and random factor
    
        print( final_hit_probability,  hit_treshold_value )
        # Check if the unit is hit based on the actual hit chance
        if   final_hit_probability >= hit_treshold_value:
            return True  # Unit is hit
        else:
            return False  # Unit is not hi
        
    def take_damage(self):
        self.hp -= 1
        print(self.hp)
        
        
    def capture(self, target_building):
        pass
        # Implement the logic for the unit to capture the target_building
        # Check if the target_building is within the capture range of the unit
        # Reduce the capture progress of the building until it is captured

    def remove_from_game(self, units):
         units.remove(self)
         print("unit is dead")
         print(units)
         self.x = None
         self.y = None
         self.rect = None
     

    def reset_for_next_turn(self):
        self.start_turn_position = (
            self.x + self.size//2, self.y + self.size//2)
         
        self.remain_attacks = 1   
        self.ammo += 2
        self.ableToMove = True
        print(self.ammo,self.remain_attacks)

    def render_on_screen(self, screen):
        warrior_img = pygame.image.load(f"img/{self.icon}")
        warrior_img = pygame.transform.scale(warrior_img, (self.size, self.size))
        warrior_img_rect = warrior_img.get_rect()
        warrior_img_rect.topleft = (self.x, self.y)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(warrior_img, warrior_img_rect)



    