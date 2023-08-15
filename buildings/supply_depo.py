import pygame

from .structure import Structure
from unit_classes import *
from utils.utils import *
from config import *

RESUPPLY_RANGE = 300
class SupplyDepo(Structure):
    def __init__(self, x, y, size, ammo_range, ammo_per_unit):
        super().__init__(x, y, size, color=YELLOW)
        self.ammo_range = ammo_range
        self.ammo_per_unit = ammo_per_unit
        self.center = (x,y)
        self.dot_radius = 10
        self.ammo_count = 100
    def dispense_ammo(self,   living_units):
       
        for unit in living_units:
           
            if (isinstance(unit, Ranged) or isinstance(unit, SupplyCart)) and  distance(self.center, unit.center) < RESUPPLY_RANGE:
                unit.ammo +=  self.ammo_per_unit
                self.ammo_count -=  self.ammo_per_unit
                print(f"Dispensing { self.ammo_per_unit} ammo. ")

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.dot_radius )  # Draw a yellow dot at the depot's position

#         import pygame
# from config import *
# from utils.utils import *
# from unit_classes import *
# dot_radius = 10

# class SupplyDepo:
#     def __init__(self, center_x, center_y   ):
#         self.center_x = center_x
#         self.center_y = center_y
#         self.center = (  self.center_x, self.center_y )
#         self.ammo_count = 100  # Initial ammo count

#     def dispense_ammo(self, amount, living_units):
       
#         for unit in living_units:
#             if self.ammo_count <= 0:
#                 print("no ammo left")
#                 break
#             if (isinstance(unit, Ranged) or isinstance(unit, SupplyCart)) and distance(self.center, unit.center) < RESUPPLY_RANGE:
#                 unit.ammo += amount
#                 self.ammo_count -= amount
#                 print(f"Dispensing {amount} ammo. Remaining ammo: {self.ammo_count}")
   
#     def resuply_depo(self,ammount):
#         self.ammo_count += ammount

#     def draw(self):
#         pygame.draw.circle(screen, (255, 255, 0), (self.center_x, self.center_y), dot_radius)  # Yellow

 