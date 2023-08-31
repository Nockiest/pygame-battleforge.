from units.unit import Unit
import math
from utils.utils import *
from config import *
from game_state import *
from .template import Ranged
from animations.shooting_animation import ShootingAnimation
from pygame.locals import *
from music_player import play_sound_file
class Musketeer(Ranged):
    size=20
    cost = 15
    def __init__(self,   x, y,  color):
        
        super().__init__(hp=2, attack_range=200,attack_resistance=0.05,base_actions=1, base_movement=125,
                         size=self.size, x=x, y=y, ammo=10, icon="musketeer.png",   color=color, cost=self.cost)
        
    def try_attack(self, click_pos, attacked_unit):

        res = super().try_attack(click_pos, attacked_unit)

        if res !=  "Attack not possible":
            # Calculate the line between unit's center and click position
            line_points = self.calculate_self_enemy_center_line(
                attacked_unit.center)
            animations.append(ShootingAnimation(self.x, self.y, line_points, self,[attacked_unit]))
            
            line_pixel_colors = get_pixel_colors(
                line_points, background_screen)
            prevented = self.prevent_shhooting_through_forrest(
                line_pixel_colors, line_points)
            if prevented:
                 
                res = "Attack not possible"
            else:
                play_sound_file("_media/musketshot.wav")
                # play_sound_file("_media/reload1.wav")
            # Check if FORREST_GREEN is present in pixel colors

        return res


 