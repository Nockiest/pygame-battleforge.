import pygame
import os
from  config import *
from .def_animation import Animation

 
# here I will add shared code between animation classes later on
class ShootingAnimation(Animation):
    def __init__(self, x, y, path, switch_speed=50 ):
        super().__init__(x, y, "img/anime/bullet_shot", switch_speed)
        self.path = path
        self.current_pos_index = 0

    def render(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= self.switch_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.start_time = current_time

        frame = self.images[self.current_frame]
        screen.blit(frame, (self.x, self.y))

        if self.current_frame == len(self.images) - 1:
            if self.current_pos_index < len(self.path) - 4:
                self.current_pos_index += 4
            else:
                self.animation_ended = True  # Set the flag when animation ends
                return "ENDED"

        # Update the sprite's position to the next position in the path
        self.x, self.y = self.path[self.current_pos_index]

        # Draw a red dot at the current position
        dot_radius = 5
        dot_color = (255, 0, 0)  # Red color
        pygame.draw.circle(screen, dot_color, (self.x, self.y), dot_radius)

        return "STILL RUNNING"