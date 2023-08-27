import pygame
# from ..config import *
from .def_spritesheet import Spritesheet
 
 
# my_spritesheet = Spritesheet('img/spritesheets/heal_pulse/heal_pulse.png')


class Heal_animation(Spritesheet):
    def __init__(self, x, y):
        super().__init__(x, y, 'img/spritesheets/heal_pulse/heal_pulse.png', 100)
        for num in range(13):
            # Replace "frame" with the actual base name of your sprites
            sprite_name = f'frame-{num}.png'
            sprite = super().parse_sprite(sprite_name)
            self.animation.append(sprite)


# heal_animation = Heal_animation(100, 100)
# canvas = pygame.Surface((WIDTH, HEIGHT))
# window = pygame.display.set_mode(((WIDTH, HEIGHT)), pygame.SRCALPHA)
# running = True

# index = 0
# # heal_animation.render(canvas)
# while running:
#     ################################# CHECK PLAYER INPUT #################################
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     ################################# UPDATE WINDOW AND DISPLAY #################################
#     window.fill((255, 255, 255))
#     heal_animation.render(window)
#     # window.blit(canvas, (0, 0))
#     pygame.display.update()
