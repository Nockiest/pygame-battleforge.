import pygame
import os
from  config import *
from .def_animation import Animation
import game_state
from utils.text_utils import *
from utils.render_utils import draw_ui
# here I will add shared code between animation classes later on
class ShootingAnimation(Animation):
    def __init__(self, x, y, path, switch_speed=50 ):
        super().__init__(x, y, "img/anime/bullet_shot", switch_speed)
        self.path = path
        self.current_pos_index = 0

    def render(self  ):
        animation_delay = 1   # Delay in milliseconds (adjust as needed)

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

            screen.fill(GREEN)
            if not self.animation_ended:
                # Erase previous position by drawing a black circle
                # pygame.draw.circle(screen, (0, 0, 0), (prev_x, prev_y), 5)
                draw_ui(screen)
                for unit in game_state.living_units:
                  unit.render()
                  text = "game" + (" ended  " if game_state.game_won else "  is running ")

                  render_text(screen, text,
                            WIDTH // 2, 10, color=(255, 255, 255), font=None, font_size=24)
                # frame = self.images[self.current_frame]  # Get the current frame
                # screen.blit(frame, (self.x, self.y))  # Draw the current frame

            prev_x, prev_y = self.x, self.y  # Update the previous position

            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5)  # Draw a red dot

            pygame.display.flip()  # Update the display
            pygame.time.delay(animation_delay)  # Introduce the delay

        return "ENDED"
                # return "STILL RUNNING"
     
      
     

       

      