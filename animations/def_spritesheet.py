import pygame
import json
from utils.render_utils import draw_units, draw_ui
from config import *
 
 
class Spritesheet:
    def __init__(self, x,y,filename, switch_speed  ):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename)#.convert()
        self.meta_data = self.filename.replace('png', 'json')
        self.animation_ended = False

        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

        self.start_time = pygame.time.get_ticks()
        self.switch_speed = switch_speed  # Switch image every 'switch_speed' milliseconds
        self.current_frame = 0
        self.x = x
        self.y = y
        self.animation = []



    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image
    
    def render(self,  ):
      
        while not self.animation_ended:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time
            
            if elapsed_time >= self.switch_speed:
                self.current_frame = (self.current_frame + 1) % len(self.animation)
                self.start_time = current_time
                frame = self.animation[self.current_frame]
                
                screen.fill(GREEN)
                draw_ui(screen)
                draw_units(screen)
                screen.blit(frame, (self.x, self.y))
                pygame.display.update()
                
            if self.current_frame == len(self.animation) - 1:
                self.animation_ended = True  # Set the flag when animation ends
                screen.fill(GREEN)
                draw_ui(screen)
                draw_units(screen)
                pygame.display.update()
   
               

                
               

 