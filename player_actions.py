import pygame
from config import *
from game_state import *
SCROLL_SPEED = 5
class Player:
    def __init__(self, color, tender_x  ):
        self.supplies = 100  # Initial supplies
        self.units = []  # List to store units (use 'list()' to create a copy)
        self.color = color  # Player's color
        self.tender_x = tender_x  # X position for the tender rectangle
        self.scroll_position = 0
        

    def create_unit( self, unit_params, living_units ):
        # Create the unit object
        unit_class, x, y = unit_params
        unit = unit_class(x=x, y=y,  color=self.color )
        print(unit.color)
        if self.supplies >= unit.cost:
            
            living_units.append(unit)
            self.units.append(unit)
            print("hello",unit)
            self.supplies -= unit.cost
            print("player has :", self.supplies)
        else: 
            print("you cant buy this unit")
            del unit  # Remove the unit from memory since it won't be added to the lists
            return None

        return unit

    def create_starting_unit(self, unit_params, living_units):
        unit_class, x, y,   = unit_params
        unit = unit_class(x=x, y=y,  color=self.color )
        living_units.append(unit)
        self.units.append(unit) 

    def show_unit_to_be_placed(self, unit_params ):   
           
        unit_class_name, _, _ = unit_params
        print(unit_class_name, "x")
        cursor_x, cursor_y = pygame.mouse.get_pos()
        try:
            dummy_unit = unit_class_name(x=-100, y=-100, color=BLACK)
            unit_x = cursor_x - dummy_unit.size // 2
            unit_y = cursor_y - dummy_unit.size // 2
            unit = unit_class_name(x=unit_x, y=unit_y, color=self.color)
            unit.render_on_screen(screen)
        except Exception as e:
            print(f"An error occurred: {e}")

    
    def render_tender(self, screen):
        # Render the tender rectangle on the screen at the specified position
        tender_rect = pygame.Rect(self.tender_x, HEIGHT-TENDER_HEIGHT, TENDER_WIDTH, TENDER_HEIGHT)
        pygame.draw.rect(screen, self.color, tender_rect)
        # Render the player's supplies on the tender
        supplies_text_line2 = default_font.render(f"Ammo {self.supplies}" , True, (255, 255, 255))
        unit_head_text =  default_font.render("Deployed" , True, (255, 255, 255))
        
        screen.blit(supplies_text_line2, (self.tender_x + 10, HEIGHT - TENDER_HEIGHT + 10))  # Adjust y-coordinate for the second line
        unit_head_text_y =  HEIGHT - TENDER_HEIGHT + 30
        screen.blit(unit_head_text, (self.tender_x + 10, unit_head_text_y))
       
        # Create a dictionary to store unit type counts
        unit_count = {}  
        for unit in self.units:
            unit_type = unit.__class__.__name__
            unit_count[unit_type] = unit_count.get(unit_type, 0) + 1

        unit_y = HEIGHT - TENDER_HEIGHT + 60  # Starting y-coordinate for printing
        total_content_height = len(self.units) * 30 + unit_head_text_y - HEIGHT + TENDER_HEIGHT

        # Adjust the scroll position based on total content height
        space_for_unit_list =  TENDER_HEIGHT - unit_head_text_y
        self.max_scroll = max(0, total_content_height  - space_for_unit_list )
        
        # Check if there is hidden content below the visible area
        if total_content_height > TENDER_HEIGHT and self.scroll_position <  self.max_scroll:
            self.scroll_position += SCROLL_SPEED

        # Check if there is hidden content above the visible area
        if total_content_height > TENDER_HEIGHT and self.scroll_position > 0:
           self.scroll_position -= SCROLL_SPEED
        # print(self.scroll_position , self.color,  self.max_scroll)
        for unit_type, count in unit_count.items():
            unit_info = f"{count} "
            unit_text = default_font.render(unit_info, True, (255, 255, 255))
            
            # Calculate the y-coordinate for rendering
            render_y = unit_y + self.scroll_position
            if render_y >= unit_head_text_y:
                # Render the unit count text
                screen.blit(unit_text, (self.tender_x + 10, render_y))
                
                # Load and render the unit image
                unit_img_path = f"img/{unit_type.lower()}.png"  # Assuming lowercase filenames
                unit_img = pygame.image.load(unit_img_path)
                unit_img = pygame.transform.scale(unit_img, (20, 20))
                screen.blit(unit_img, (self.tender_x + 30, render_y))
            
            unit_y += 30  # Move down for the next unit type

    def handle_input(self):
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.scroll_position -= 5
            self.scroll_position = max(self.scroll_position, self.max_scroll)  # Ensure scroll position doesn't go below 0
        if keys[pygame.K_DOWN]:
            # print(self.scroll_position)
            self.scroll_position += 5
            self.scroll_position = max(self.scroll_position, 0)  # Ensure scroll position doesn't exceed max
    def get_boost(self):
        # Add logic to calculate and apply boost to the player's units
        # (e.g., increase attack, defense, or other attributes)
        pass

    def announce_defeat(self):
        print("Player ", self.color, " has been defeated")


    def end_game(self, game):
        game = True
        return game

    def remove_from_game(self, living_units, unit):
    # Find the unit in the living_units list and remove it
        if unit in living_units:
            living_units.remove(unit)

        # Find the unit in the player's units list and remove it
        if unit in self.units:
            self.units.remove(unit)

        # Reset the unit's position and rect to None to indicate it's no longer in the game
        unit.x = None
        unit.y = None
        unit.rect = None
            
     