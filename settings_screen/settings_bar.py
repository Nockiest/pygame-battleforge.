import pygame
from .settings_globs import *
from .slider import Slider
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

 