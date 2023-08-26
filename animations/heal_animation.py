import pygame
# from ..config import *
from def_spritesheet import Spritesheet
WIDTH = 500
HEIGHT = 500
pygame.init()
# my_spritesheet = Spritesheet('img/spritesheets/heal_pulse/heal_pulse.png')
 

class Heal_animation(Spritesheet):
    def __init__(self):
        super().__init__('img/spritesheets/heal_pulse/heal_pulse.png', 100  )
        
        for num in range(13):
            # Replace "frame" with the actual base name of your sprites
            sprite_name = f'frame-{num}.png'
            
            sprite = super().parse_sprite(sprite_name)
            self.animation.append(sprite)

         


heal_animation = Heal_animation()
canvas = pygame.Surface((WIDTH, HEIGHT))
window = pygame.display.set_mode(((WIDTH, HEIGHT)))
running = True

index = 0

while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############### UPDATE SPRITE IF SPACE IS PRESSED #################################
            if event.key == pygame.K_SPACE:
                heal_animation.render(canvas)
               
                # index = (index + 1) % len(heal_animation.animation)

    ################################# UPDATE WINDOW AND DISPLAY #################################
    # canvas.fill((255, 255, 255))
    # canvas.blit(heal_animation.animation[index], (0, WIDTH - 128))
     
    window.blit(canvas, (0, 0))
    
    pygame.display.update()
