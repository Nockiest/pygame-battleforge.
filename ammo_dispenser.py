from units.unit import Unit
import math
from utils.utils import *
from config import *
import game_state
 
from units.ranged.template import Ranged
from animations.basic_animations import ResupplyAnimation, AmmoExpendedAnimation
class Ammo_dispenser():
    def __init__(self):
        pass
    
    def dispense_ammo(self, amount ):
        if game_state.players[game_state.cur_player].color != self.color:
            return 0
        depleted_ammo = 0
        for unit in game_state.living_units.array:
            if self.ammo <= 0:
                print("no ammo left")
                break

            if unit.color != self.color:
                continue


            if isinstance(unit, Ranged) and distance(self.center, unit.center) <= RESUPPLY_RANGE:
                
                game_state.animations.append(AmmoExpendedAnimation(self.x, self.y ))
                game_state.animations.append(ResupplyAnimation(unit.x, unit.y))
                unit.ammo += amount
                depleted_ammo += amount
                
                print(f"Dispensing {amount} ammo. Remaining ammo: {self.ammo} to {unit}vv")
        # print("depleted ammo", depleted_ammo)
        return depleted_ammo

