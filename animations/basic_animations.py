import pygame
import os
from  config import *
from .def_animation import Animation

 
# here I will add shared code between animation classes later on
class SlashAnimation(Animation):
    def __init__(self, x, y ,switch_speed=50):
        super().__init__(x,y,"img/anime/slash")
       
class ResupplyAnimation(Animation):
    def __init__(self, x, y ,switch_speed=100):
        super().__init__(x,y,"img/anime/resupply")
       