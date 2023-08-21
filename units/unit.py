import pygame
from config import *
from utils.utils import *
import math
import random
import shapely.geometry
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
        pygame.sprite.Sprite.__init__(self)
        self.hp = hp
        self.base_hp = hp
        self.attack_range = attack_range
        self.attack_range_modifiers = {"base_modifier": 1}
        self.remain_actions = 1  # base_actions
        self.base_actions = base_actions
        self.base_movement = base_movement
        self.atttack_resistance = attack_resistance
        self.enemies_in_range = []
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
        self.able_to_move = self.remain_actions > 0
        self.color = color
        self.attack_circle = []
        self.valid_movement_positions = []
        self.valid_movement_positions_edges = []
        
        self.running_animations = []

        

    def move_in_game_field(self, click_pos, living_units):
        new_center_x, new_center_y = click_pos
        point1 = shapely.geometry.Point(new_center_x, new_center_y)
        movement_polygon = shapely.geometry.Polygon(
            self.valid_movement_positions_edges)

        # Check if the clicked position is a valid movement position
       
        if point1.within(movement_polygon):
            self.x = new_center_x - self.size // 2
            self.y = new_center_y - self.size // 2

        else:
            # Create a line between the click position and starting position
            movement_line = bresenham_line(
                new_center_x, new_center_y, self.start_turn_position[0], self.start_turn_position[1])

            # Find the first valid movement position along the line
            for pos in movement_line:
                point = shapely.geometry.Point(pos[0], pos[1])
                if point.within(movement_polygon):
                    self.x, self.y = pos[0] - \
                        self.size // 2, pos[1] - self.size // 2
                    break

        # Update the position of the unit in the living_units list
        index = living_units.index(self)
         

        self.rect = pygame.Rect(
            self.x, self.y, self.size, self.size)
        self.center = (self.x + self.size//2, self.y + self.size//2)
        living_units[index].x = self.x
        living_units[index].y = self.y
        living_units[index].size = self.size
        living_units[index].rect = self.rect



    def new_point_interferes(self, living_units, point_x, point_y):
        # Create a new rectangle for the unit's position
        new_rect = pygame.Rect(point_x - self.size // 2,
                               point_y - self.size // 2, self.size, self.size)

        for unit in living_units:
            if unit is self:
                continue
            res = unit.rect.colliderect(new_rect)
            if res:
                return True
        return False

    def get_units_movement_area(self, living_units):

        # Number of samples (angles) around the unit's center
        num_samples = 360
        center_x, center_y = self.start_turn_position[0], self.start_turn_position[1]
        self.valid_movement_positions = []
        self.valid_movement_positions_edges = []
        for angle in range(0, 360, 360 // num_samples):
            # Convert angle to radians

            # create line from start to the edge of the screen
            # get the costs of every pixel on the line
            # find river or enemy unit at the first index

            radians = math.radians(angle)
            line_points = []
            current_cost = 0
            base_chunk = WIDTH//2
            distance = base_chunk

            iteration = 2

            while base_chunk//iteration >= 1 and current_cost != self.base_movement:

                new_x = min(WIDTH, max(
                    center_x + distance * math.cos(radians), 0))
                new_y = min(HEIGHT - BUTTON_BAR_HEIGHT, max(center_y +
                            distance * math.sin(radians), UPPER_BAR_HEIGHT))
                 
                
                line_points = bresenham_line(
                    center_x, center_y, int(new_x), int(new_y))
                line_pixel_colors = get_pixel_colors(
                    line_points, background_screen)
                movement_cost = calculate_movement_cost(line_pixel_colors)
                current_cost = movement_cost[-1][0]

                if current_cost > self.base_movement:
                    # print(distance, iteration, "decrementing",  512//iteration)
                    distance -= base_chunk//iteration
                elif current_cost < self.base_movement:
                    # print(distance, iteration, "incrementing")
                    distance += base_chunk//iteration
                current_line = line_points

                iteration *= 2
            if current_cost < self.base_movement:
                while current_cost < self.base_movement:
                    new_x = min(WIDTH, max(
                        len(line_points)  +1 * math.cos(radians), 0))
                    new_y = min(HEIGHT - BUTTON_BAR_HEIGHT, max(center_y +
                                len(line_points)    +1 * math.sin(radians), UPPER_BAR_HEIGHT))

                    # line_points = bresenham_line(
                    #     center_x, center_y, int(new_x), int(new_y))
                    new_pixel_color = get_pixel_colors(
                        [(int(new_x), int(new_y))], background_screen)
                    pixel_cost = calculate_movement_cost([new_pixel_color])
                    current_cost += movement_cost[-1][0]

                    if current_cost >= self.base_movement:
                        break
            else:
                while current_cost > self.base_movement and line_points:
                    last_x, last_y = line_points[-1]
                    last_pixel_color =  line_pixel_colors[-1]
                    pixel_cost = calculate_movement_cost([last_pixel_color])
                    current_cost -= pixel_cost[-1][0]
                    line_points.pop()

            line_points = line_points[:-self.size//2]
            new_line_points = []
            for point in line_points:
                other_units = [
                    unit for unit in living_units if unit.color != self.color]
                if not self.new_point_interferes(other_units, point[0], point[1]):
                    new_line_points.append(point)
                else:
                    break  # Stop adding points if interference is detected
            line_points = new_line_points
            self.valid_movement_positions.append(line_points)

            if line_points:
                self.valid_movement_positions_edges.append(
                    line_points[len(line_points) - 1])
        if self.valid_movement_positions_edges:
         print("points", self.valid_movement_positions_edges[-1])

    def draw_possible_movement_area(self, screen):
        farthest_points = []
        for angle in self.valid_movement_positions:
            if len(angle) >= 2:
                farthest_points.append(angle[-1])
                farthest_points.append(angle[-2])

        # Draw the connected path using lines
        if len(farthest_points) > 1:
            pygame.draw.lines(screen, (0, 255, 0), False, farthest_points, 2)

    def get_attackable_units(self, living_units):
        self.enemies_in_range = []
        # for every living unit
        for unit in living_units:
            if unit.color == self.color:
                continue

            # nevím proč to nemám centrovat, abd to fungovalo
        
            center_x, center_y = self.center
          
            enemy_center_x, enemy_center_y = unit.center
            print(   enemy_center_x, enemy_center_y , center_x, center_y, unit.start_turn_position)
            distance = math.sqrt((enemy_center_x - center_x)**2 + (enemy_center_y - center_y)**2)
            print(distance, unit, unit.size//2, self.attack_range)
            if distance - unit.size//2 < self.attack_range:
                self.enemies_in_range.append(unit)

        print("in attack range are", self.enemies_in_range)

    def calculate_attack_circle(self, battelground, living_units):
        pass

    def get_attack_circle(self, living_units):
        pass

    def render_attack_circle(self ):

        total_attack_range_modifier = sum(self.attack_range_modifiers.values())
        attack_range_with_modifiers = self.attack_range * total_attack_range_modifier

        pygame.draw.circle(screen, RED, (self.x + self.size // 2,
                           self.y + self.size // 2), int(attack_range_with_modifiers), 1)

    def attack_square(self, click_pos):
        self.attack_cross_position = click_pos
        self.attack_cross_time = pygame.time.get_ticks()
        self.remain_actions -= 1
        if self.ammo != None:
            self.ammo -= 1

    def render_attack_cross(self ):
        if hasattr(self, 'attack_cross_position') and hasattr(self, 'attack_cross_time'):
            time_elapsed = pygame.time.get_ticks() - self.attack_cross_time
            # Render the cross for 1 second (1000 milliseconds)
            if time_elapsed <= 1000:
                render_attack_cross(screen, *self.attack_cross_position)
            else:
                del self.attack_cross_position
                del self.attack_cross_time

    def try_attack(self, click_pos, attacked_unit):
        if attacked_unit in self.enemies_in_range:
            # if attacked_unit.rect.collidepoint(click_pos):
            return ("UNIT ATTACKS", click_pos, attacked_unit)
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

        print(player.color, self.color, player.units, self, "removing unit")
        # Remove the unit from the 'cur_players' array
        player.units.remove(self)
        player.update_sorted_units()
        living_units.remove(self)
        # Set the unit's x, y, and rect attributes to None to remove it from the game field
        self.x = None
        self.y = None
        self.rect = None

        print("Unit is dead")

    def reset_for_next_turn(self, living_units):
        self.start_turn_position = (
            self.x + self.size//2, self.y + self.size//2)

        self.remain_actions = 1
        self.able_to_move = True
        self.remain_actions = self.base_actions

    def highlight_attackable_units(self):
        for unit in self.enemies_in_range:
            # Calculate the center coordinates of self and the target unit
            self_center = self.center
            target_center = unit.center

            # Calculate the midpoint of the line
            midpoint = ((self_center[0] + target_center[0]) // 2, (self_center[1] + target_center[1]) // 2)

            # Calculate the distance between self and the target unit
            distance = math.sqrt((self_center[0] - target_center[0]) ** 2 + (self_center[1] - target_center[1]) ** 2)

            # Draw a line from self's center to the target unit's center
            unit.draw_as_active()
            pygame.draw.line(screen, DARK_RED, self_center, target_center, 2)

            # Render the distance as text at the midpoint
            font = pygame.font.Font(None, 20)
            text_surface = font.render(f"{int(distance)}/{self.attack_range} units", True, WHITE)
            text_rect = text_surface.get_rect(center=midpoint)
            screen.blit(text_surface, text_rect)
    def render_hovered_state(self):
        padding = 2  # Adjust the padding size as needed
        font = pygame.font.Font(None, 20)
        text_color = (255, 255, 255)  # White color

        # Determine the width of the rectangle based on the longest text line
        text_lines = [
            f"Attacks: {self.remain_actions}",
            f"Ammo: {self.ammo}",
            f"Hp: {self.hp}"
        ]
        max_line_width = max(font.size(line)[0] for line in text_lines)
        rect_width = max_line_width + 2 * padding

        # Create a transparent background for the text with the adjusted width
        text_surface = pygame.Surface((rect_width, 80), pygame.SRCALPHA)
        pygame.draw.rect(text_surface, (0, 0, 0, 100), (0, 0, text_surface.get_width(), text_surface.get_height()))

        # Render remaining attacks, ammo, and HP in the formatted rectangle
        for i, line in enumerate(text_lines):
            text_rendered = font.render(line, True, text_color)
            text_surface.blit(text_rendered, (padding, i * 20 + padding))

        # Position the rectangle below the unit
        text_pos = (self.x, self.y + self.size + padding)

        # Blit the formatted rectangle onto the screen
        screen.blit(text_surface, text_pos)

 
    def render_on_screen(self):
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
        outline_color = BLACK  # self.outline_color  # Use the unit's color for the outline

        # Draw the filled rectangle for the unit
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, outline_color, self.rect, 1)  # Outline

        # Draw the unit image
        screen.blit(warrior_img, warrior_img_rect)

     

    def draw_as_active(self):
        outline_rect = pygame.Rect(
            self.x - 2, self.y - 2, self.size + 4, self.size + 4)
        pygame.draw.rect(screen,  BLACK, outline_rect, 2)

        # Draw a line from self.start_turn_position to the center of the unit in red
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        pygame.draw.line(screen, self.color, self.start_turn_position,
                         (center_x, center_y), 2)
