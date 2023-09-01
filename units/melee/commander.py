from units.unit import Unit
import math
from utils.utils import *
from config import *
import game_state
from .template import Melee


class Commander(Melee):
    size = 20  # Set the size attribute at the class level
    cost = 100000
    
    def __init__(self, x, y, color):
        super().__init__(hp=1, attack_range=40, attack_resistance=0.2, base_actions=1, base_movement=150,
                         size=self.size, x=x, y=y,    icon="commander.png", color=color, cost=self.cost)
        self.boost_range = 150
    
    def move_in_game_field(self, click_pos):
        super().move_in_game_field(click_pos)
        for unit in game_state.living_units.array:
            if unit.color == self.color:
                self.give_deffense_boost(unit)

    def take_damage(self, attacker):
        hp = super().take_damage(attacker)
       # print(hp,game_state.game_won = True, "game won is")
        if hp <= 0:
            game_state.game.go_to_end_screen() 
        return hp
    
    def give_deffense_boost(self, unit):
        distance = get_two_units_center_distance(self, unit)
        if distance < self.boost_range:
            unit.attack_resistances["NEAR COMMANDER"] = 0.2
        else:
            unit.attack_resistances["NEAR COMMANDER"] = 0