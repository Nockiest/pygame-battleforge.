import pygame
import random
from config import *
from game_state import *
from utils.image_utils import render_image
from utils.utils import *
from units.support.observer import Observer
import end_screen.stats as stats
from units.unit import Unit
# import game_state
 

class Player:
    def __init__(self, color, tender_x):
        self.supplies = game_state.starting_money  # Initial supplies
        self.units = []  # List to store units (use 'list()' to create a copy)
        # i should use the sorteddict class for this
        self.sorted_by_class_units = {}
        self.color = color  # Player's color
        self.max_scroll = 0
        self.tender_x = tender_x  # X position for the tender rectangle
        self.scroll_position = 0
        self.preview_unit = None
        self.spawn_width = 200
        # stats
        self.num_attacks = 0
        self.num_bought_units = 0 
        self.occupied_towns = [] # unused


        self.side = 0 if self.color == RED else WIDTH - self.spawn_width
        self.buy_area = ( self.side, UPPER_BAR_HEIGHT, self.spawn_width, HEIGHT - TENDER_HEIGHT - UPPER_BAR_HEIGHT)
    
    
    def __repr_(self):
        return f'Player{self.color}, has {self.units} sorted {self.sorted_by_class_units} and a buy area{self.buy_area}'
    def to_dict(self):
        return {
            'supplies': self.supplies,
            # 'units': [unit.to_dict() for unit in self.units],
            'color': self.color,
            'tender_x': self.tender_x,
            'scroll_position': self.scroll_position,
            # 'preview_unit': self.preview_unit.to_dict() if self.preview_unit else None,
            'spawn_width': self.spawn_width,
            'num_attacks': self.num_attacks,
            'num_bought_units': self.num_bought_units,
            # 'occupied_towns': self.occupied_towns
        }

    @classmethod
    def from_dict(cls, data):
        player = cls.__new__(cls)
        player.supplies = data['supplies']
        # player.units = [Unit.from_dict(unit_data) for unit_data in data['units']]
        player.color = data['color']
        player.tender_x = data['tender_x']
        player.scroll_position = data['scroll_position']
        # player.preview_unit = Unit.from_dict(data['preview_unit']) if data['preview_unit'] else None
        player.spawn_width = data['spawn_width']
        player.num_attacks = data['num_attacks']
        player.num_bought_units = data['num_bought_units']
        player.occupied_towns = data['occupied_towns']
        return player

    def __del__(self):
        stats.num_bought_stats[str(self.color)] = self.num_bought_units
        stats.num_attacks_stats[str(self.color)] = self.num_attacks
        print("UNIT DELETED", stats.num_bought_stats,  stats.num_attacks_stats)


    def update_sorted_units(self):
        self.sorted_by_class_units = {}
        for unit in self.units:
            unit_type = unit.__class__.__name__
            self.sorted_by_class_units[unit_type] = self.sorted_by_class_units.get(
                unit_type, 0) + 1


    def create_unit(self, unit_params):
        # Create the unit object
        print(unit_params, "UNIT PARAMS")
        unit_class, x, y = unit_params
        unit = unit_class(x=x, y=y,  color=self.color)

        if self.supplies >= unit.cost:

            # game_state.living_units.array.append(unit)
            self.units.append(unit)
            print("created unit", unit, )
            self.supplies -= unit.cost
            print("player has :", self.supplies, "supplies")
            unit.remain_actions = 0
        else:
            print("you cant buy this unit")
            unit.__del__()  # Remove the unit from memory since it won't be added to the lists
            return None
        self.update_sorted_units()
        
        return unit
    

    def create_starting_unit(self, unit_params):
        # print("CALLED CREATE UNIT")
        unit_class, x, y,   = unit_params
        unit = unit_class(x=x, y=y,  color=self.color)
        # game_state.living_units.array.append(unit)
        self.units.append(unit)
        self.update_sorted_units()


    def create_preview_unit(self, unit_params):
        self.preview_unit = self.create_unit(unit_params)
   
   
    def pin_and_move_unit(self, unit):
  

        cursor_x, cursor_y = pygame.mouse.get_pos()
        unit.x = cursor_x - unit.size // 2
        unit.y = cursor_y - unit.size // 2
        unit.rect.x =cursor_x - unit.size // 2
        unit.rect.y =cursor_y -unit.size  // 2
        unit.center = (unit.x + unit.size // 2, unit.y + unit.size//2)
        
        unit.start_turn_position = (
            unit.x + unit.size  // 2, unit.y + unit.size  // 2)
        unit.rect = pygame.Rect(unit.x , unit.y, unit.size,unit.size)
   
   
    def show_buy_area(self):
        buy_area_rect = pygame.Rect(*self.buy_area)
        pygame.draw.rect(screen, ORANGE, buy_area_rect, 2) 
        for town in self.occupied_towns:
            # town_rect = pygame.Rect(*town)
            pygame.draw.rect(screen, ORANGE, town.rect, 2)

    def render_tender(self):
        # Render the tender rectangle on the screen at the specified position
        tender_rect = pygame.Rect(
            self.tender_x, HEIGHT-TENDER_HEIGHT, TENDER_WIDTH, TENDER_HEIGHT)
        pygame.draw.rect(screen, self.color, tender_rect)
        # Render the player's supplies on the tender
        supplies_text_line2 = default_font.render(
            f"Ammo {self.supplies}", True, (255, 255, 255))
        unit_head_text = default_font.render("Deployed", True, (255, 255, 255))

        # Adjust y-coordinate for the second line
        screen.blit(supplies_text_line2, (self.tender_x +
                    10, HEIGHT - TENDER_HEIGHT + 10))
        unit_head_text_y = HEIGHT - TENDER_HEIGHT + 30
        screen.blit(unit_head_text, (self.tender_x + 10, unit_head_text_y))

        total_text_height = supplies_text_line2.get_height() + unit_head_text.get_height()

        # Calculate unit_y based on the total text height
        unit_y = HEIGHT - TENDER_HEIGHT + total_text_height + 20  # Adjust 20 for spacing
        # + unit_head_text_y# - HEIGHT + TENDER_HEIGHT
        total_content_height = len(self.sorted_by_class_units) * 30

        # Adjust the scroll position based on total content height
        space_for_unit_list = TENDER_HEIGHT - unit_head_text_y

        # for the 4 rows of the unit table
        self.max_scroll = min(0, -total_content_height - (-30*4))

        # print(self.scroll_position , self.color,  self.max_scroll)
        for unit_type, count in self.sorted_by_class_units.items():
            unit_info = f"{count} "
            unit_text = default_font.render(unit_info, True, (255, 255, 255))

            # Calculate the y-coordinate for rendering
            render_y = unit_y + self.scroll_position

            if render_y  >= unit_head_text_y:
                # Render the unit count text
                screen.blit(unit_text, (self.tender_x + 10, render_y))
                # Load and render the unit image
                unit_img_path = f"img/{unit_type.lower()}.png"
                unit_size = (20, 20)
                render_position = (self.tender_x + 30, render_y)

                render_image(unit_img_path, unit_size, render_position, screen)

            unit_y += 30  # Move down for the next unit type

   
    def handle_input(self):
        #  # Check if there is hidden content below the visible are
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.scroll_position -= 5
            # Ensure scroll position doesn't go below 0
            self.scroll_position = max(self.scroll_position,   self.max_scroll)
        if keys[pygame.K_DOWN]:

            self.scroll_position += 5
            # Ensure scroll position doesn't exceed max
            self.scroll_position = min(self.scroll_position, 0)


    def get_boost(self):
        # Add logic to calculate and apply boost to the player's units
        # (e.g., increase attack, defense, or other attributes)
        pass

     
    def remove_self_unit(self,  unit):
        # Find the unit in the player's units list and remove it
        if unit in self.units:
            self.units.remove(unit)

        self.update_sorted_units()
        # update_sorted_units()
 
  
    def place_starting_units(self, unit_class_list):
        sides = {
            "(255, 0, 0)": 0,
            "(0, 0, 255)": WIDTH - self.spawn_width
        }
        for unit_class in unit_class_list:

           
            while True:
                # Random x on the left side
                x = random.randint(
                    self.side ,  self.side   +  self.spawn_width - unit_class.size  )
                # Random y anywhere on screen
                y = random.randint(
                    UPPER_BAR_HEIGHT, HEIGHT - TENDER_HEIGHT - unit_class.size)
                # Replace with your actual pixel color fetching function
                pixel_color =  pixel_colors[x+unit_class.size//2][ y+unit_class.size//2 ]
               
                # Check if the position is valid (not on river and not occupied)
                if pixel_color  != RIVER_BLUE and not self.is_position_occupied(x, y, ):
                    break

            unit_params = (unit_class, x, y)
            self.create_starting_unit(unit_params)

  
    def is_position_occupied(self, x, y,):
        for unit in living_units.array:
            if abs(unit.x - x) < unit.size and abs(unit.y - y) < unit.size:
                return True
        return False


# def announce_defeat(self):
#         print("Player ", self.color, " has been defeated")
