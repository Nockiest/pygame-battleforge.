

import pygame
from config import *
from buttons.button import Button
from game_state import *
import game_state # you can use both versions at the same time!!

class BuyButton(Button):
    def __init__(self, icon, unit_type, description, x, enter_buy_mode):
        self.icon = icon
        self.unit_type = unit_type
        self.width = 60
        self.height = 60

        def custom_callback():
            # Pass unit_type to the original callback
            enter_buy_mode(self.unit_type)

        super().__init__(description=description, x=x, y=(HEIGHT - 100), width=self.width,
                         height=self.height, callback=custom_callback, game_state_screen="game_is_running")

        # Resize the icon to fit within the button
        new_width = self.width - 10  # Leave some padding around the icon
        new_height = self.height - 10
        resized_icon = pygame.transform.scale(icon, (new_width, new_height))

        # Center the icon within the button
        icon_x = (self.width - resized_icon.get_width()) // 2
        icon_y = (self.height - resized_icon.get_height()) // 2

        # Blit the resized icon onto the button surface
        self.button_surface.blit(resized_icon, (icon_x, icon_y))
        
    def draw(self, screen, x, y):
        if self == game_state.hovered_button:
            # Darken the button when hovered
            dark_surface = pygame.Surface((self.width, self.height))
            dark_surface.fill(50)  # Dark gray color
            # Set transparency to achieve the hover effect
            dark_surface.set_alpha(100)
            screen.blit(dark_surface, (x, y))
        screen.blit(self.button_surface, (x, y))

        # Create a surface for the description text
        # You can adjust the font size as needed
        font = pygame.font.Font(None, 20)
        # Black color for the text
        text_surface = font.render(self.description, True, (0, 0, 0))

        # Center the description text horizontally within the button
        text_x = x + (self.width - text_surface.get_width()) // 2
        text_y = y + self.height + 5  # Place the text below the button
        screen.blit(text_surface, (text_x, text_y))

        # Create a surface for the cost text
        cost_text = f"${self.unit_type.cost}"
        # Black color for the text
        cost_surface = font.render(cost_text, True, (0, 0, 0))

        # Position the cost text next to the button
        cost_x = x + self.width + 10  # Add some spacing between the button and the cost text
        # Center the cost text vertically within the button
        cost_y = y + (self.height - cost_surface.get_height()) // 2
        screen.blit(cost_surface, (cost_x, cost_y))

    def set_position(self, x, y):
        # Set the position of the button within the game window
        self.position = (x, y)

    def is_clicked(self, mouse_pos):
        x, y = mouse_pos
        button_rect = self.button_surface.get_rect(topleft=self.position)
        if button_rect.collidepoint(mouse_pos):
            self.callback(self.unit_type)
            return True

    def set_hovered(self, hovered):
        self.hovered = hovered
