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
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= self.switch_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.start_time = current_time
            frame = self.images[self.current_frame]

        # if self.current_frame == len(self.images) - 4:
        if self.current_pos_index < len(self.path) - 4:
            self.current_pos_index += min(4, len(self.path) - self.current_pos_index - 1)
        else:
            self.animation_ended = True
            game_state.animations.remove(self)
            del self
            return

        self.x, self.y = self.path[self.current_pos_index]
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5)  # Draw a red dot
     

       

      