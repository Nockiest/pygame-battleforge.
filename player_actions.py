import pygame
from config import *
# Define the width and height of the tender rectangle
TENDER_WIDTH = 40
TENDER_HEIGHT = 100

class Player:
    def __init__(self, color, tender_x, tender_y):
        self.supplies = 100  # Initial supplies
        self.units = []  # List to store units (use 'list()' to create a copy)
        self.color = color  # Player's color
        self.tender_x = tender_x  # X position for the tender rectangle
        self.tender_y = tender_y  # Y position for the tender rectangle

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
        print("created starting unit")

    def show_unit_to_be_placed(self, unit_params ):
        print("i have been called")
        unit_class_name, _, _ = unit_params
        print(unit_class_name)
        unit_class = unit_class_name # globals().get(unit_class_name)  # Retrieve class object based on string
        print(unit_class)
        cursor_x, cursor_y = pygame.mouse.get_pos()
        dummy_unit = unit_class(x=-100, y=-100, color=BLACK)
        unit_x = cursor_x - dummy_unit.size // 2
        unit_y = cursor_y - dummy_unit.size // 2
        unit = unit_class(x=unit_x, y=unit_y, color=self.color)
        unit.render_on_screen(screen)
       
    
    def render_tender(self, screen):
        # Render the tender rectangle on the screen at the specified position
        tender_rect = pygame.Rect(self.tender_x, self.tender_y, TENDER_WIDTH, TENDER_HEIGHT)
        pygame.draw.rect(screen, self.color, tender_rect)

        # Create a font object for rendering text
        font = pygame.font.Font(None, 20)

        # Render the player's supplies on the tender
        supplies_text = font.render(f"Supplies: {self.supplies}", True, (255, 255, 255))
        screen.blit(supplies_text, (self.tender_x + 10, self.tender_y + 10))

        # Render the units' information on the tender
        unit_y = self.tender_y + 40
        for unit in self.units:
            unit_info = f"{unit.__class__.__name__} at ({unit.x}, {unit.y})"
            unit_text = font.render(unit_info, True, (255, 255, 255))
            screen.blit(unit_text, (self.tender_x + 10, unit_y))
            unit_y += 20


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
            
     