import pygame
from config import *
from buttons.button import Button
from game_state import *
from units.melee.commander import Commander
from units.melee.kngiht import Knight
from units.melee.pikeman import Pikeman
from units.melee.shield import Shield
from units.melee.template import Melee
from units.ranged.cannon import Cannon
from units.ranged.musketeer import Musketeer
from units.ranged.template import Ranged
from units.support.medic import Medic
from units.support.observer import Observer
from units.support.supply_cart import SupplyCart
from units.support.template import Support
import game_state
BUTTON_BAR_Y = HEIGHT - 100


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
        all_buttons.append(self)

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


class ButtonBar:
    def __init__(self, callback):
        self.button_instances = [
            BuyButton(knight_buy_img, Knight, "Buy Knight",
                      x=220,  enter_buy_mode=callback),
            BuyButton(shield_buy_img, Shield, "Buy Shield",
                      x=280, enter_buy_mode=callback),
            BuyButton(Cannon_buy_img, Cannon, "Buy Cannon",
                      x=340, enter_buy_mode=callback, ),
            BuyButton(medic_buy_img, Medic, "Buy Medic",
                      x=400, enter_buy_mode=callback, ),
            BuyButton(pike_buy_img, Pikeman, "Buy Pike",
                      x=460, enter_buy_mode=callback, ),
            BuyButton(musket_buy_img, Musketeer, "Buy Musket",
                      x=600, enter_buy_mode=callback, )
        ]
        self.button_width = 60

        self.width = WIDTH  # 400
        # Calculate the total width of all buttonst
        total_button_width = self.button_width * len(self.button_instances)

        # Calculate the remaining space for spacing
        remaining_space = WIDTH - total_button_width

        # Calculate the button spacing
        self.button_spacing = remaining_space // (
            len(self.button_instances) + 1)

        self.background_color = (192, 192, 192)  # Gray color

        def add_button(self, button):
            self.button_instances(button)
            self.update_button_positions()

    def update_button_positions(self):
        total_button_width = sum(self.button_width for button in self.button_instances) + (
            len(self.button_instances) - 1) * self.button_spacing
        start_x = (self.width - total_button_width) // 2

        # Check if the total button width exceeds the maximum width (500 pixels)
        if total_button_width > 500:
            scaling_factor = 1  # 500 / total_button_width
            self.button_width = int(self.button_width * scaling_factor)
            total_button_width = sum(self.button_width for button in self.button_instances) + (
                len(self.button_instances) - 1) * self.button_spacing
            start_x = (self.width - total_button_width) // 2

        x_position = start_x
        for button in self.button_instances:
            button.set_position(x_position, BUTTON_BAR_Y)
            x_position += self.button_width + self.button_spacing + TENDER_WIDTH

    def draw(self, screen, y, current_player_color):
        # Draw the background rectangle for the button bar
        button_bar_rect = pygame.Rect(
            TENDER_WIDTH, y, TENDER_WIDTH + self.width, BUTTON_BAR_HEIGHT)
        pygame.draw.rect(screen, self.background_color, button_bar_rect)

        # Draw the narrow strip with the current player's color at the bottom
        current_player_strip_rect = pygame.Rect(
            0, y + BUTTON_BAR_HEIGHT - 10, self.width, 10)
        pygame.draw.rect(screen, current_player_color,
                         current_player_strip_rect)

        x = self.button_spacing
        for button in self.button_instances:
            button.x = x
            button.y = y
            # Corrected the order of width and height
            button.rect = pygame.Rect(
                button.x, button.y, button.width, button.height)
            # pygame.draw.rect(screen, ROAD_GRAY, button.rect)
            button.draw(screen, button.x, button.y)
            # # Draw the icon on the button surface (assuming button.icon is a surface)
            # icon_padding_x = (button.width - button.icon.get_width()) // 2
            # icon_padding_y = (button.height - button.icon.get_height()) // 2
            # button_surface = pygame.Surface((button.width, button.height))
            # button_surface.blit(button.icon, (icon_padding_x, icon_padding_y))
            # screen.blit(button_surface, (button.x, button.y))

            # button.rect.draw(screen, button.x, button.y)
            # button.set_position(x, y)  # Set the position of the button within the game window
            x += button.width + self.button_spacing

    def get_clicked_button(self, mouse_pos):
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                return button
        return None
