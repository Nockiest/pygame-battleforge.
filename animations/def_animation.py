import pygame
import os
from config import *
from utils.render_utils import draw_ui, draw_units
import game_state

class Animation:
    def __init__(self, x, y, animation_folder, switch_speed=50, resize=None):
        self.resize = resize
        self.images = self.load_animation(animation_folder)
        self.start_time = pygame.time.get_ticks()
        self.switch_speed = switch_speed  # Switch image every 'switch_speed' milliseconds
        self.current_frame = 0
        self.x = x
        self.y = y
        self.animation_ended = False

    def __repr__(self):
        return f'{type(self).__name__} '

    def load_animation(self, animation_folder):
        images = []
        for filename in os.listdir(animation_folder):
            if filename.endswith(".png"):
                img = pygame.image.load(
                    os.path.join(animation_folder, filename))
                if self.resize:
                    img = pygame.transform.scale(img, self.resize)
                images.append(img)
        return images

    def render(self):
      
        
        # Update animation
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= self.switch_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.start_time = current_time

        # Render current frame
        frame = self.images[self.current_frame]
       
        screen.blit(frame, (self.x, self.y))

        # Check if animation has ended
        if self.current_frame == len(self.images) - 1:
            self.animation_ended = True
            
            game_state.animations.remove(self)
            del self

#   screen.fill(GREEN)
#         draw_ui(screen)
#         draw_units(screen)