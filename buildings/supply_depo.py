import pygame

from .structure import Structure
from units.ranged.template import Ranged  # Import Ranged from units folder
from units.support.supply_cart import SupplyCart  # Import SupplyCart from units folder
 
 
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
            print(isinstance(unit, Ranged), isinstance(unit, SupplyCart)) ,  distance(self.center, unit.center)
            if (isinstance(unit, Ranged) or isinstance(unit, SupplyCart)) and  distance(self.center, unit.center) < RESUPPLY_RANGE:
                unit.ammo +=  self.ammo_per_unit
                self.ammo_count -=  self.ammo_per_unit
                print(f"Dispensing { self.ammo_per_unit} ammo. ")

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.dot_radius )  # Draw a yellow dot at the depot's position

 