import pygame
from config import *
from utils.utils import *
from unit_classes import *
dot_radius = 10

class SupplyDepo:
    def __init__(self, center_x, center_y   ):
        self.center_x = center_x
        self.center_y = center_y
        self.center = (  self.center_x, self.center_y )
        self.ammo_count = 100  # Initial ammo count

    def dispense_ammo(self, amount, living_units):
       
        for unit in living_units:
            if self.ammo_count <= 0:
                print("no ammo left")
                break
            if (isinstance(unit, Ranged) or isinstance(unit, SupplyCart)) and distance(self.center, unit.center) < RESUPPLY_RANGE:
                unit.ammo += amount
                self.ammo_count -= amount
                print(f"Dispensing {amount} ammo. Remaining ammo: {self.ammo_count}")
   
    def resuply_depo(self,ammount):
        self.ammo_count += ammount

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (self.center_x, self.center_y), dot_radius)  # Yellow

 