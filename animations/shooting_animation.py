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

    def render(self  ):
        animation_delay = 10   # Delay in milliseconds (adjust as needed)

        # Store the initial position
        prev_x, prev_y = self.path[0]

        while self.current_pos_index < len(self.path) - 1:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time

            if elapsed_time >= self.switch_speed:
                self.current_frame = (self.current_frame + 1) % len(self.images)
                self.start_time = current_time
                frame = self.images[self.current_frame]

            if self.current_frame == len(self.images) - 1:
                if self.current_pos_index < len(self.path) - 1:
                    self.current_pos_index += min(4, len(self.path) - self.current_pos_index - 1)
                else:
                    self.animation_ended = True

            self.x, self.y = self.path[self.current_pos_index]

            if not self.animation_ended:
                # Erase previous position by drawing a black circle
                # pygame.draw.circle(screen, (0, 0, 0), (prev_x, prev_y), 5)
                screen.blit(background_screen, (prev_x, prev_y), pygame.Rect(prev_x, prev_y, 20, 20))
                # frame = self.images[self.current_frame]  # Get the current frame
                # screen.blit(frame, (self.x, self.y))  # Draw the current frame

            prev_x, prev_y = self.x, self.y  # Update the previous position

            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5)  # Draw a red dot

            pygame.display.flip()  # Update the display
            pygame.time.delay(animation_delay)  # Introduce the delay

        return "ENDED"
                # return "STILL RUNNING"
     
      
     

       

      