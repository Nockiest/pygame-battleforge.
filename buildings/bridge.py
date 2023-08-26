import pygame
import math
from .structure import Structure

class Bridge(Structure):
    def __init__(self, x, y, angle, size, color):
        super().__init__(x, y, size, color)
        self.color = color
        self.size = size
        self.angle = angle

    def draw(self, screen):
        bridge_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        pygame.draw.rect(bridge_surface, self.color, (0, 0, self.size[0], self.size[1]))
        rotated_surface = pygame.transform.rotate(bridge_surface, math.degrees(self.angle   ))
        
        # Calculate the position to blit the rotated rectangle
        blit_position = rotated_surface.get_rect(center=(self.x, self.y))
        
        # Draw the rotated rectangle onto the screen
        screen.blit(rotated_surface, blit_position)
