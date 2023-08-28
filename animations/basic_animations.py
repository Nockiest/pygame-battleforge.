import pygame
import os
from  config import *
from .def_animation import Animation

 
# here I will add shared code between animation classes later on
class SlashAnimation(Animation):
    def __init__(self, x, y ,switch_speed=50):
        super().__init__(x,y,"img/anime/slash")
       
class ResupplyAnimation(Animation):
    def __init__(self, x, y ,switch_speed=25):
        super().__init__(x,y,"img/anime/resupply")
       
class MISSEDAnimation(Animation):
    def __init__(self, x, y , resize=None, switch_speed=100):
        super().__init__(x=x,y=y,animation_folder="img/anime/MISSED", switch_speed=switch_speed, resize=resize)
    
class AmmoExpendedAnimation(Animation):
    def __init__(self, x, y , resize=None, switch_speed=100):
        super().__init__(x=x,y=y,animation_folder="img/anime/bullet-minus", switch_speed=switch_speed,  )