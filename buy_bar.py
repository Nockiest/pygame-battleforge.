import pygame
from config import *
from button import Button

BUTTON_BAR_Y = HEIGHT - 100
# Define the buy_unit function
def buy_unit(unit_type):
    # Add your logic here to handle the purchase of the unit_type
    print(f"Bought {unit_type}!")

class BuyButton(Button):
    def __init__(self, icon, unit_type, description, x  ):
        super().__init__(description, x, y=(HEIGHT - 100), width=60, height=60, callback=buy_unit)
        self.icon = icon
        self.unit_type = unit_type
        
        
        # Calculate padding for the icon
        icon_padding_x = (self.width - icon.get_width()) // 2
        icon_padding_y = (self.height - icon.get_height()) // 2
        # Blit the icon with padding onto the button surface
        self.button_surface.blit(icon, (icon_padding_x, icon_padding_y))
         

    def draw(self, screen, x, y ):
        if self.hovered:
            # Darken the button when hovered
            dark_surface = pygame.Surface((self.button_width, self.button_height))
            dark_surface.fill(0,0,50)  # Dark gray color
            dark_surface.set_alpha(100)  # Set transparency to achieve the hover effect
            screen.blit(dark_surface, (x, y))
        screen.blit(self.button_surface, (x, y))

        # Create a surface for the description text
        font = pygame.font.Font(None, 20)  # You can adjust the font size as needed
        text_surface = font.render(self.description, True, (0, 0, 0))  # Black color for the text

        # Center the description text horizontally within the button
        text_x = x + (self.width - text_surface.get_width()) // 2
        text_y = y + self.height + 5  # Place the text below the button
        screen.blit(text_surface, (text_x, text_y))
    def set_position(self, x, y):
        # Set the position of the button within the game window
        self.position = (x, y)

    def is_clicked(self, mouse_pos):
        x, y = mouse_pos
        button_rect = self.button_surface.get_rect(topleft=self.position)
        return button_rect.collidepoint(mouse_pos)

    def set_hovered(self, hovered):
        self.hovered = hovered

# Assuming you have icons for the buttons, load them here (replace with actual icons)
knight_buy_img = pygame.image.load("img/knight.png")
shield_buy_img = pygame.image.load("img/armor.png")
canon_buy_img = pygame.image.load("img/canon.png")
medic_buy_img = pygame.image.load("img/medic.png")
pike_buy_img = pygame.image.load("img/pike.png")
musket_buy_img = pygame.image.load("img/musket.png")
button_instances = [
    BuyButton(knight_buy_img, "Knight", "Buy Knight", 100),
    BuyButton(shield_buy_img, "Shield", "Buy Shield", 600),
    BuyButton(canon_buy_img, "Canon", "Buy Canon", 200),
    BuyButton(medic_buy_img, "Medic", "Buy Medic",300),
    BuyButton(pike_buy_img, "Pikeman", "Buy Pike", 400),
    BuyButton(musket_buy_img, "Musketeer", "Buy Musket", 500)
]
class ButtonBar:
    def __init__(self, buttons):
        self.button_width = 60
        self.buttons = buttons
        
        # Calculate the total width of all buttons
        total_button_width = self.button_width * len(buttons)
        
        # Calculate the remaining space for spacing
        remaining_space = WIDTH - total_button_width
        
        # Calculate the button spacing
        self.button_spacing = remaining_space // (len(buttons) + 1)
        
        self.background_color = (192, 192, 192)  # Gray color
        def add_button(self, button):
            self.buttons.append(button)
            self.update_button_positions()

    def update_button_positions(self):
        total_button_width = sum(self.button_width for button in self.buttons) + (len(self.buttons) - 1) * self.button_spacing
        start_x = (WIDTH - total_button_width) // 2
        x_position = start_x
        for button in self.buttons:
            button.set_position(x_position, BUTTON_BAR_Y)
            x_position += self.button_width + self.button_spacing

    def draw(self, screen, y, current_player_color):
        # Draw the background rectangle for the button bar
        button_bar_rect = pygame.Rect(0, y,WIDTH, BUTTON_BAR_HEIGHT)
        pygame.draw.rect(screen, self.background_color, button_bar_rect)

        # Draw the narrow strip with the current player's color at the bottom
        current_player_strip_rect = pygame.Rect(0, y + BUTTON_BAR_HEIGHT - 10, WIDTH, 10)
        pygame.draw.rect(screen, current_player_color, current_player_strip_rect)

        x = self.button_spacing
        for button in self.buttons:
            button.draw(screen, x, y)
            button.set_position(x, y)  # Set the position of the button within the game window
            x += button.width + self.button_spacing

    def get_clicked_button(self, mouse_pos):
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                return button
        return None

 