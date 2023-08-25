import pygame
import json
  
pygame.init()

screen = pygame.display.set_mode((500, 500), pygame.SRCALPHA)
class Spritesheet:
    def __init__(self, filename, switch_speed  ):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename)#.convert()
        self.meta_data = self.filename.replace('png', 'json')
        
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

        self.start_time = pygame.time.get_ticks()
        self.switch_speed = switch_speed  # Switch image every 'switch_speed' milliseconds
        self.current_frame = 0
        self.x = 100
        self.y = 100
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
    
    def render(self, screen):
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        print("running",current_time,elapsed_time,self.animation,len(self.animation), self.current_frame)
        if elapsed_time >= self.switch_speed:
            self.current_frame = (self.current_frame + 1) % len(self.animation)
            self.start_time = current_time
            frame = self.animation[self.current_frame]
            print("frame and cur frame",frame, self.current_frame)
            screen.blit(frame, (self.x, self.y))
            
        if self.current_frame == len(self.animation) - 1:
            self.animation_ended = True  # Set the flag when animation ends
            return "ENDED"
        else:
            return "STILL RUNNING"