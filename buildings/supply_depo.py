import pygame

from .structure import Structure
from units.ranged.template import Ranged  # Import Ranged from units folder
# Import SupplyCart from units folder
from units.support.supply_cart import SupplyCart
import game_state
from utils.utils import *
from config import *
from animations.basic_animations import ResupplyAnimation
RESUPPLY_RANGE = 300


class SupplyDepo(Structure):
     
    def __init__(self, x, y, size, ammo_range, ammo_per_unit):
        super().__init__(x, y, (size,size), color=YELLOW)
        self.ammo_range = ammo_range
        self.ammo_per_unit = ammo_per_unit
        self.center = (x, y)
        self.dot_radius = 20
        self.ammo_count = 100
        
        self.image = pygame.image.load("img/block-house.png")
        self.image = pygame.transform.scale(self.image, (self.dot_radius*2, self.dot_radius*2))
        self.rect = pygame.Rect(x-self.dot_radius, y-self.dot_radius, self.dot_radius*2, self.dot_radius*2)
    def dispense_ammo(self):

        for unit in game_state.living_units:

            if (isinstance(unit, Ranged) or isinstance(unit, SupplyCart)) and distance(self.center, unit.center) < RESUPPLY_RANGE:
                game_state.animations.append(ResupplyAnimation(unit.x, unit.y))
                unit.ammo += self.ammo_per_unit
                self.ammo_count -= self.ammo_per_unit
                print(f"Dispensing { self.ammo_per_unit} ammo. ")

    def draw(self, screen):
        # Draw a yellow dot at the depot's position
        pygame.draw.circle(screen, (255, 255, 0),
                           (self.x, self.y), self.dot_radius)
          
        screen.blit(self.image, self.rect)
