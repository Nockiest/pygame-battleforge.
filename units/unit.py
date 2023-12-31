import pygame
import math
from math import sqrt, ceil
import random
import shapely.geometry

import game_state
from animations.basic_animations import MISSEDAnimation
from config import *
from utils.utils import *
from utils.image_utils import *
# from game_state import num_attacks

class Unit(pygame.sprite.Sprite):
    def __init__(self, hp, attack_range, attack_resistance, base_actions, base_movement, size, x, y, ammo, icon, color, cost):
        super().__init__()
        self.hp = hp
        self.base_hp = hp
        self.attack_range = attack_range 
        self.attack_range_modifiers = {"base_modifier": 1}
        self.remain_actions = 1  # base_actions
        self.base_actions = base_actions
        self.base_movement = base_movement   
        self.attack_resistances =  {"base_resistance":  attack_resistance  }  
        self.enemies_in_range = []
        self.lines_to_enemies_in_range = []
        self.x = x
        self.y = y
        self.rect = pygame.Rect(
            self.x, self.y, self.size, self.size)
        self.size = size
        self.center = (self.x + self.size//2, self.y + self.size//2)
        self.start_turn_position = (
            self.x + self.size // 2, self.y + self.size // 2)
        self.color = color
        self.ammo = ammo
        self.cost = cost

        self.icon = icon
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.attack_circle = []
        self.valid_movement_positions = []
        self.valid_movement_positions_edges = []
        self.lines_to_enemies_in_range = []
        self.apply_modifiers()
        game_state.living_units.append(self)
 
    def update(self):
        # Add any necessary update logic here
        pass

    def __repr__(self):
        return f'{type(self).__name__}(hp={self.hp},x={self.x}, y={self.y}, ammo={self.ammo}, actions={ self.remain_actions } , '

    def __del__(self):
        game_state.living_units.remove(self) ## možníá smazat
        print("DELETING", self )
   
    def move_in_game_field(self, click_pos):
     
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

        self.rect = pygame.Rect(
            self.x, self.y, self.size, self.size)
        self.center = (self.x + self.size//2, self.y + self.size//2)
        self.apply_modifiers( )
 

  
    def apply_modifiers(self):
        self.attack_resistances =  {"base_resistance":  1 }  
        new_pos_color = game_state.pixel_colors[self.center[0]][self.center[1]]
        if new_pos_color == FORREST_GREEN:
            self.attack_resistances["IN FORREST" ] = 0.3
        

        for town in game_state.battle_ground.towns:
            if town.rect.collidepoint(self.center):
                print("IN TOWN RECT", self)
                self.attack_resistances["IN TOWN" ] = 0.1
                break
    
        for commander in game_state.living_units.dict["Commanders"]:
            if commander.color == self.color and commander != self:
                commander.give_deffense_boost(self)
      
    def get_units_movement_area(self):
        num_samples = 180
        center_x, center_y = self.start_turn_position[0], self.start_turn_position[1]
        self.valid_movement_positions = []
        self.valid_movement_positions_edges = []


        ## create a large circle around the unit
        def get_circle_points(center_x, center_y, radius, num_samples):
            points = []
            for i in range(num_samples):
                angle = math.radians(i * (360 / num_samples))
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                points.append((x, y))
            return points
         
        ## take out all of the unique points the circle crosses
        far_points = get_circle_points(center_x, center_y, self.base_movement*2.1, 180)
        ## for each point get a path from that point to the unit center
        movement_outline = []
        for edge in far_points:
            # Check if edge coordinates are within bounds
            edge_x = max(0, min(edge[0], WIDTH - 1))
            edge_y = max(UPPER_BAR_HEIGHT, min(edge[1], HEIGHT - 1))
             
            line_to_center = bresenham_line(center_x, center_y, edge_x, edge_y)
            points_in_reach = []
            cost = 0
            for point in line_to_center:
                if cost > self.base_movement:
                    break
                # get the background movement cost
                # add it to cost
                try:
                    cost += game_state.movement_costs[point[0]][point[1]]
                except Exception as e:
                    print(f"An error occurred: {e}", point[0], point[1])
                       
                

                ## append it to the points in reach 
                points_in_reach.append(point)
           
            farthest_valid_point =  points_in_reach[-1] 
            other_units = [
                unit for unit in game_state.living_units.array if unit.color != self.color]
            
            for unit in other_units:
                point_x, point_y, interferes = check_precalculated_line_square_interference(unit, points_in_reach)
                if interferes:
                    
                    if points_in_reach.index((point_x,point_y)) <  points_in_reach.index(farthest_valid_point):
                        farthest_valid_point = (point_x,point_y)
                        
          
            points_in_reach = points_in_reach[:points_in_reach.index(farthest_valid_point)   ]
         
          
            if len(points_in_reach) > 0:
                movement_outline.append(points_in_reach[-1])
                self.valid_movement_positions.append(points_in_reach)
                self.valid_movement_positions_edges.append(points_in_reach[-1])

        def check_for_obstacles(point1, point2, i):
            line = bresenham_line(point1[0], point1[1], point2[0], point2[1])
            if len(line) <= 2:
                return
            line_is_without_obstacles = True
            
            for point in line:       
                color = game_state.pixel_colors[point[0]][point[1]]
                
                if color == RIVER_BLUE:
                    line_is_without_obstacles = False
                    break
               
            
            if not line_is_without_obstacles:
                mid_point = line[len(line)//2]
                check_for_obstacles(point1, mid_point, i)
                check_for_obstacles(mid_point, point2, i+1)
                
                line_to_center = bresenham_line(center_x, center_y, mid_point[0], mid_point[1])
                cost = 0
                farthest_valid_point = (center_x, center_y)
                for point in line_to_center:
                    if cost > self.base_movement:
                        break
                    
                    try:
                        cost += game_state.movement_costs[point[0]][point[1]]
                        farthest_valid_point = point
                    except Exception as e:
                        print(f"An error occurred: {e}", point[0], point[1])
                
                self.valid_movement_positions_edges.insert(i , farthest_valid_point)

        for i in range(len(movement_outline)):
            point1 = movement_outline[i]
            point2 = movement_outline[(i + 1) % len(movement_outline)]
            
            check_for_obstacles(point1, point2, i)     
   
        #         self.valid_movement_positions_edges.insert(i, farthest_valid_point)
            ## make a calcuation from the units center to this point and find the farthest point on this vertecy
            ## insert the point into the movement outline
            ## from the farthest point you found, create a line to point i and i+1
            ## if the line is without obstacles do nothing
            ## otherwise take the middle of the new line, and do the same calculation
            ## repeat until condition is fullfilled
                        

    def draw_possible_movement_area(self):
        farthest_points = []
        for angle in self.valid_movement_positions:
            if len(angle) >= 2:
                farthest_points.append(angle[-1])

        if len(self.valid_movement_positions) > 2:

            farthest_points.append(self.valid_movement_positions[0][-1])
            # farthest_points.append(angle[-2])

        # Draw the connected path using lines
        if len(farthest_points) > 1:
            pygame.draw.lines(screen, self.color, False, farthest_points, 2)

    def find_obstacles_in_line_to_enemies(self, enemy, line_points):
        # I could only reset the line to that specific unit instead of deleting the whole array
        ######################### x FIND BLOCKING UNITS ##############
        blocked = False
        for unit in game_state.living_units.array:
            if unit == enemy:
                continue
            elif unit.color == self.color:
                continue
            point_x, point_y, interferes = check_precalculated_line_square_interference(
                unit, line_points)
            distance_between_units = get_two_units_center_distance(unit  , enemy )
            
            if interferes and abs(distance_between_units )> max(enemy.size//2, unit.size//2):
                print("this unit is blocking the way", unit, enemy)
                blocked = True
                self.lines_to_enemies_in_range.append({
                    "enemy": enemy,
                    "start": self.center,
                    "interference_point": (point_x, point_y),
                    "end": enemy.center})

                break
        if not blocked:
            self.lines_to_enemies_in_range.append({
                "enemy": enemy,
                "start": self.center,
                "interference_point": None,
                "end": enemy.center})

        return blocked

    def get_attackable_units(self):
        self.enemies_in_range = []
        self.lines_to_enemies_in_range = []
        total_attack_range_modifier = sum(self.attack_range_modifiers.values())
        # for every living unit
        for enemy in game_state.living_units.array:
            if enemy.color == self.color:
                continue
            center_x, center_y = self.center
            enemy_center_x, enemy_center_y = enemy.center
            distance = math.sqrt((enemy_center_x - center_x)
                                 ** 2 + (enemy_center_y - center_y)**2)
            line_points = bresenham_line(
                center_x, center_y, enemy_center_x, enemy_center_y)
            if distance - enemy.size//2 < self.attack_range  * total_attack_range_modifier:
                blocked = self.find_obstacles_in_line_to_enemies(
                    enemy, line_points)

                if not blocked:
                    self.enemies_in_range.append(enemy)

        print("in attack range are", self.enemies_in_range)

    def render_attack_circle(self):
        total_attack_range_modifier = sum(self.attack_range_modifiers.values())
       
        attack_range_with_modifiers = self.attack_range * total_attack_range_modifier

        pygame.draw.circle(screen, BLACK, (self.x + self.size // 2,
                           self.y + self.size // 2), int(attack_range_with_modifiers), 2)

    def attack(self):
        self.remain_actions -= 1
        if self.ammo != None:
            self.ammo -= 1

    def try_attack(self, click_pos, attacked_unit):
        ####!!!RANGED UNITS ARNET CONNECTED O THIS FUNCTION!!!#####
        if attacked_unit in self.enemies_in_range:
            self.attack()
            hit_result = attacked_unit.check_if_hit()  # 80% hit chance
            # num_attacks += 1
            if hit_result:
                remaining_hp = attacked_unit.take_damage(self)
                print("remaining enemy hp", remaining_hp)

                return "UNIT ATTACKS"
            else:
                return "UNIT MISSED"
        return "Attack not possible"

    def check_if_hit(self):
        attack_resistance =   sum(self.attack_resistances.values())
      
       
        final_hit_probability = 1 - attack_resistance
        
        # Generate a random float between 0 and 1
        hit_treshold_value = random.random()

        # Calculate the actual hit chance considering the base_hit_chance and random factor

        print("comparing", final_hit_probability,  hit_treshold_value,
              final_hit_probability >= hit_treshold_value)

        if final_hit_probability >= hit_treshold_value:
            print("UNIT WAS HIT")
            return True  # Unit is hit
        else:
            # Unit is not hit
            print("UNIT WASNT HIT")
            game_state.animations.append(MISSEDAnimation(
                x=self.x - self.size//2, y=self.y - self.size//2, resize=(self.size * 2, self.size*2)))

            return False

    def take_damage(self, attacker):
      
        self.hp -= 1
        if self.hp <= 0:
            game_state.living_units.array.remove(self)
            # players[cur_player].remove_from_game(self)
            attacker.get_boost_for_destroying_unit()
            game_state.killed_units += 1
            update_players_unit()
            print("Removing unit:", self)
            print("Units in living_units:", game_state.living_units.array)
             
            return self.hp
            del self
         
        return self.hp

    
    def reset_for_next_turn(self):
       
        self.start_turn_position = (
            self.x + self.size//2, self.y + self.size//2)
        self.remain_actions = self.base_actions
        self.get_units_movement_area()
        self.apply_modifiers()

    def draw_lines_to_enemies_in_range(self):
        for line in self.lines_to_enemies_in_range:
            start = line["start"]
            end = line["end"]
            interference_point = line["interference_point"]

            if interference_point is not None:
                pygame.draw.line(screen, DARK_RED, start,
                                 interference_point, 3)
                pygame.draw.line(screen, (HOUSE_PURPLE),
                                 interference_point, end, 3)
            else:
                pygame.draw.line(screen, DARK_RED, start, end, 3)
                midpoint = ((start[0] + end[0]) // 2,
                            (start[1] + end[1]) // 2)
                distance = math.sqrt(
                    (start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
                font = pygame.font.Font(None, 20)
                text_surface = font.render(
                    f"{int(distance)} meters", True, WHITE)
                text_rect = text_surface.get_rect(center=midpoint)
                screen.blit(text_surface, text_rect)

    def highlight_attackable_units(self):
        for unit in self.enemies_in_range:
            # Calculate the center coordinates of self and the target unit
            self_center = self.center
            target_center = unit.center
            # Draw a line from self's center to the target unit's center
            unit.draw_as_active()

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
        pygame.draw.rect(text_surface, (0, 0, 0, 100), (0, 0,
                         text_surface.get_width(), text_surface.get_height()))

        # Render remaining attacks, ammo, and HP in the formatted rectangle
        for i, line in enumerate(text_lines):
            text_rendered = font.render(line, True, text_color)
            text_surface.blit(text_rendered, (padding, i * 20 + padding))

        # Position the rectangle below the unit
        text_pos = (self.x, self.y + self.size + padding)

        # Blit the formatted rectangle onto the screen
        screen.blit(text_surface, text_pos)

    def render(self):
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

    def get_boost_for_destroying_unit(self):
        print("unit killed an enemy, and could get a boost now")

    def draw_as_active(self):
        # Try to execute the following block of code
        try:
            # Check if the attack_range_modifiers attribute contains "in_observers_range"
            
            if "in_observer_range" in self.attack_range_modifiers   :
                if self.attack_range_modifiers[ "in_observer_range"] > 0:
                    outline_rect = pygame.Rect(
                    self.x+self.size//2, self.y-10  , 20 , 20)
                    pygame.draw.rect(screen,  GRAY, outline_rect, 0)

                    render_image("img/observer.png", (15, 15), (self.x+self.size//2, self.y-10 ), screen)

            # Create a rectangle outline around the unit
            outline_rect = pygame.Rect(
                int(self.x) - 2, int(self.y) - 2, self.size + 4, self.size + 4)
            # Draw the rectangle outline on the screen in black color with a width of 2 pixels
            pygame.draw.rect(screen, BLACK, outline_rect, 2)

            # Calculate the center coordinates of the unit
           
            center_x = self.center[0]
            center_y = self.center[1]
            # Draw a line from the start_turn_position attribute to the center of the unit in red color with a width of 2 pixels
            pygame.draw.line(screen, self.color, self.start_turn_position,
                            (center_x, center_y), 2)
        # If an exception occurs
        except Exception as e:
            # Print an error message with the exception details
            print("An error occurred in draw as active:", e)

    def to_dict(self):
        return {
            'hp': self.hp,
            'base_hp': self.base_hp,
            'attack_range': self.attack_range,
            'attack_range_modifiers': self.attack_range_modifiers,
            'remain_actions': self.remain_actions,
            'base_actions': self.base_actions,
            'base_movement': self.base_movement,
            'attack_resistance': self.attack_resistance,
            'enemies_in_range': [enemy.to_dict() for enemy in self.enemies_in_range],
            'x': self.x,
            'y': self.y,
            'size': self.size,
            'center': self.center,
            'start_turn_position': self.start_turn_position,
            'color': self.color,
            'ammo': self.ammo,
            'cost': self.cost
        }

    @classmethod
    def from_dict(cls, data):
        unit = cls.__new__(cls)
        unit.hp = data['hp']
        unit.base_hp = data['base_hp']
        unit.attack_range = data['attack_range']
        unit.attack_range_modifiers = data['attack_range_modifiers']
        unit.remain_actions = data['remain_actions']
        unit.base_actions = data['base_actions']
        unit.base_movement = data['base_movement']
        unit.attack_resistance = data['attack_resistance']
        unit.enemies_in_range = [Unit.from_dict(enemy_data) for enemy_data in data['enemies_in_range']]
        unit.x = data['x']
        unit.y = data['y']
        unit.size = data['size']
        unit.center = data['center']
        unit.start_turn_position = data['start_turn_position']
        unit.color = data['color']
        unit.ammo = data['ammo']
        unit.cost = data['cost']
        return unit


























       ## ensure that the point doesnt interfere with enemies

            
                # 
                
                
                
                 ## scan from the units center and find the farthest point, that has lower movement than movement cost

        ## append the farthest point 


        # for angle in range(0, 360, 360 // num_samples):
            # Convert angle to radians

            # create line from start to the edge of the screen
            # get the costs of every pixel on the line
            # find river or enemy unit at the first index

            # radians = math.radians(angle)
            # line_points = []
            # current_cost = 0
            # base_chunk = WIDTH//2
            # distance = base_chunk

            # iteration = 2

            # while base_chunk//iteration >= 1 and current_cost != self.base_movement:

            #     new_x = min(WIDTH, max(
            #         center_x + distance * math.cos(radians), 0))
            #     new_y = min(HEIGHT - BUTTON_BAR_HEIGHT, max(center_y +
            #                 distance * math.sin(radians), UPPER_BAR_HEIGHT))

            #     line_points = bresenham_line(center_x, center_y, int(new_x), int(new_y))
            #     movement_cost = []
            #     try:
            #         for point in line_points:
            #             x, y = point
            #             cost = movement_costs[x][y]
            #             movement_cost.append(cost)
            #     except Exception as e:
            #         print(f"An error occurred: {e}")

            #     current_cost = movement_cost[-1]


            #     if current_cost > self.base_movement:
            #         # print(distance, iteration, "decrementing",  512//iteration)
            #         distance -= base_chunk//iteration
            #     elif current_cost < self.base_movement:
            #         # print(distance, iteration, "incrementing")
            #         distance += base_chunk//iteration
            #     current_line = line_points

            #     iteration *= 2
            # if current_cost < self.base_movement:
            #     while current_cost < self.base_movement:
            #         new_x = min(WIDTH, max(
            #             len(line_points) + 1 * math.cos(radians), 0))
            #         new_y = min(HEIGHT - BUTTON_BAR_HEIGHT, max(center_y +
            #                     len(line_points) + 1 * math.sin(radians), UPPER_BAR_HEIGHT))
            #         new_pixel_color = get_pixel_colors(
            #             [(int(new_x), int(new_y))], background_screen)
            #         pixel_cost=10000
            #         try:
            #          pixel_cost =   movement_costs[int(new_x)][int(new_y)]
            #         except Exception as e:
            #             print(f"An error occurred: {e}{int(new_x) }{ int(new_y)}")
                    
            #         current_cost += pixel_cost 

            #         if current_cost >= self.base_movement:
            #             break
            # else:
            #     while current_cost > self.base_movement and line_points:
            #         last_x, last_y = line_points[-1]
                    
            #         # check if the indices are within the valid range
            #         if 0 <= last_x < len(movement_costs) and 0 <= last_y < len(movement_costs[0]):
            #             pixel_cost = movement_costs[last_x][last_y]
            #             current_cost -= pixel_cost
            #         else:
            #             # subtract a large value from current_cost if the indices are out of range
            #             current_cost -= 10000000000
                    
            #         # pop the last point from line_points
            #         line_points.pop()
            # line_points = line_points[:-self.size//2]
            # new_line_points = []
            # for point in line_points:
            #     other_units = [
            #         unit for unit in living_units.array if unit.color != self.color]

            #     if not new_point_interferes_with_unit(self, point[0], point[1], other_units,):
            #         new_line_points.append(point)
            #     else:
            #         break  # Stop adding points if interference is detected
            # line_points = new_line_points
            # self.valid_movement_positions.append(line_points)

            # if line_points:
            #     self.valid_movement_positions_edges.append(
            #         line_points[len(line_points) - 1])


      # for i, point in enumerate(movement_outline.copy()):
        #     def return_next_point():
        #         if i + 1 >= len(movement_outline):
        #             return 0
        #         else:
        #             return  i + 1 
        #     next_point = return_next_point()
        #     def get_line_between_points():
        #         if i == len(movement_outline) -1:
        #             return  bresenham_line(point[0], point[1], movement_outline[0][0], movement_outline[0][1])
        #         else:
        #             return  bresenham_line(point[0], point[1], movement_outline[next_point][0], movement_outline[next_point][1])
            
            
        #     line_to_next_point = get_line_between_points()  
        #     line_is_without_obstacles = True
        #     for point in line_to_next_point:
        #         try:
        #             color = game_state.pixel_colors[point[0]][point[1]]
        #             if color == RIVER_BLUE:
        #                 line_is_without_obstacles = False
        #         except Exception as e:
        #             print(f"An error occurred: {e}", point[0], point[1])
        #     if not line_is_without_obstacles:
                    
            
        #        ## if there is an obstacle in the line, take the middle point of the line
        #         mid_point = line_to_next_point[len(line_to_next_point)//2]
        #         line_to_center =  bresenham_line(center_x, center_y, mid_point[0], mid_point[1])
        #         cost = 0
        #         farthest_valid_point = (center_x, center_y)
        #         for point in line_to_center:
        #             if cost > self.base_movement:
        #                 break
                    
        #             try:
        #                 cost += game_state.movement_costs[point[0]][point[1]]
        #                 farthest_valid_point = point
        #             except Exception as e:
        #                 print(f"An error occurred: {e}", point[0], point[1])

        #         line1 =  bresenham_line(farthest_valid_point[0], farthest_valid_point[1], movement_outline[i][0], movement_outline[i][1])
        #         line2 =  bresenham_line(farthest_valid_point[0], farthest_valid_point[1], movement_outline[next_point][0], movement_outline[next_point][1])