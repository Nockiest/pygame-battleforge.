import pygame
from .settings_globs import *
from config import *

class SettingsBar:
    def __init__(self, heading, x, y):
        """Initialize the settings bar."""
        self.heading = heading
        self.x = x
        self.y = y
        self.sliders = []

    def add_slider(self, label, min_value, max_value, initial_value, update_fc):
        """Add a slider to the settings bar."""
        slider = Slider(label, min_value, max_value, initial_value,update_fc, self.x,  self.y + 50 * (len(self.sliders)+1))
        self.sliders.append(slider)

    def draw(self, screen):
        """Draw the settings bar on the screen."""
        # draw the heading
        text = default_font.render(self.heading, True, BLACK)
        text_rect = text.get_rect(center=(self.x + 100, self.y))
        screen.blit(text, text_rect)

        # draw the sliders
        for i, slider in enumerate(self.sliders):
            slider.draw(screen)

class Slider:
    def __init__(self, label, min_value, max_value, connected_value, update_function, x, y):
        """Initialize the slider."""
        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.value = connected_value
        self.update_function = update_function
        self.x = x
        self.y = y
        self.slider_start = self.x + 100
        self.slider_end = self.slider_start + 100
        self.slider_rect = pygame.Rect(self.slider_start,self.y -15,  self.slider_end - self.slider_start +10, 30)
        settings_bars.append(self)
    def draw(self, screen):
        """Draw the slider on the screen."""
      
        # draw the label
        text = default_font.render(self.label, True, BLACK)
        text_rect = text.get_rect(center=(self.x + 50, self.y))
        screen.blit(text, text_rect)

        # draw the slider
        pygame.draw.rect(screen, BLACK, (self.slider_start, self.y - 10, 100, 20), 1)
        pygame.draw.rect(screen, BLACK,
                        (self.x + 100 + int(100 * (self.value - self.min_value) / (self.max_value - self.min_value)) - 5,
                        self.y - 15,
                        10,
                        30))

        # draw the current value of the slider
        value_text = default_font.render(str(self.value), True, BLACK)
        value_text_rect = value_text.get_rect(center=(self.slider_start + 50, self.y - 25))
        screen.blit(value_text, value_text_rect)

    def handle_click(self, pos):
        """Handle click events on the slider."""
    
        # update the value of the slider based on the click position
        new_value = int((pos[0] - self.x - 100) * (self.max_value - self.min_value) / 100) + self.min_value
        # ensure that the new value is within the valid range
        new_value = max(self.min_value, min(new_value, self.max_value))
        if new_value != self.value:
            # update the value of the connected variable using the update function
            # self.update_function(new_value)
            # update the value of the slider
            self.value = new_value

    def alter_original_value(self   ):
        """Alter the original value of the connected variable."""
        # update the value of the connected variable using the update function
        self.update_function(self.value)
        # update the value of the slider
        