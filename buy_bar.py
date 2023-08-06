import pygame
from config import *
# Define the buy_unit function
def buy_unit(unit_type):
    # Add your logic here to handle the purchase of the unit_type
    print(f"Bought {unit_type}!")

class BuyButton:
    def __init__(self, icon, unit_type, description):
         
        self.icon = icon
        self.unit_type = unit_type
        self.description = description
        self.button_width = 60  # Increased button width to add padding
        self.button_height = 60  # Increased button height to add padding
        self.button_surface = pygame.Surface((self.button_width, self.button_height))
        self.button_surface.fill((255, 255, 255))  # Fill with white color

        # Calculate padding for the icon
        icon_padding_x = (self.button_width - icon.get_width()) // 2
        icon_padding_y = (self.button_height - icon.get_height()) // 2

        # Blit the icon with padding onto the button surface
        self.button_surface.blit(icon, (icon_padding_x, icon_padding_y))

        self.hovered = False  # Track whether the button is currently being hovered over


    def draw(self, screen, x, y):
        if self.hovered:
            # Darken the button when hovered
            dark_surface = pygame.Surface((self.button_width, self.button_height))
            dark_surface.fill((100, 100, 100))  # Dark gray color
            dark_surface.set_alpha(100)  # Set transparency to achieve the hover effect
            screen.blit(dark_surface, (x, y))
        screen.blit(self.button_surface, (x, y))

        # Create a surface for the description text
        font = pygame.font.Font(None, 20)  # You can adjust the font size as needed
        text_surface = font.render(self.description, True, (0, 0, 0))  # Black color for the text

        # Center the description text horizontally within the button
        text_x = x + (self.button_width - text_surface.get_width()) // 2
        text_y = y + self.button_height + 5  # Place the text below the button
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

class ButtonBar:
    def __init__(self, screen_width, buttons):
        self.screen_width = screen_width
        self.buttons = buttons
        self.button_spacing = (screen_width - sum(button.button_width for button in buttons)) // (len(buttons) + 1)
        self.background_color = (192, 192, 192)  # Gray color

    def draw(self, screen, y):
        # Draw the background rectangle for the button bar
        button_bar_rect = pygame.Rect(0, y, self.screen_width, BUTTON_BAR_HEIGHT)
        pygame.draw.rect(screen, self.background_color, button_bar_rect)

        x = self.button_spacing
        for button in self.buttons:
            button.draw(screen, x, y)
            button.set_position(x, y)  # Set the position of the button within the game window
            x += button.button_width + self.button_spacing

    def get_clicked_button(self, mouse_pos):
        for button in self.buttons:
            
            if button.is_clicked(mouse_pos):
                return button
        return None


# Assuming you have icons for the buttons, load them here (replace with actual icons)
knight_buy_bt = pygame.image.load("img/knight.png")
shield_buy_bt = pygame.image.load("img/armor.png")
canon_buy_bt = pygame.image.load("img/canon.png")
medic_buy_bt = pygame.image.load("img/medic.png")
pike_buy_bt = pygame.image.load("img/pike.png")
musket_buy_bt = pygame.image.load("img/musket.png")
 
 
# Create instances of BuyButton for each unit type
buy_buttons = [
    BuyButton(knight_buy_bt, "Knight", "Buy Knight"),  # Add descriptions for each button
    BuyButton(shield_buy_bt, "Shield", "Buy Shield"),
    BuyButton(canon_buy_bt, "Canon", "Buy Canon"),
    BuyButton(medic_buy_bt, "Medic", "Buy Medic"),
    BuyButton(pike_buy_bt, "Pikeman", "Buy Pike"),
    BuyButton(musket_buy_bt, "Musketeer", "Buy Musket"),
]
