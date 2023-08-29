import math
import os
import sys
from units.unit import Unit
 
from utils.utils import *
from config import *
from game_state import *
from animations.basic_animations import SlashAnimation
 
class Melee(Unit):
    def __init__(self, hp, attack_range,attack_resistance,   base_actions,  base_movement, size, x, y, icon, color, cost):
        super().__init__(hp, attack_range,attack_resistance, base_actions,
                         base_movement, size, x, y, None, icon, color, cost)
       
    def try_attack(self, click_pos, attacked_unit    ):
        res = super().try_attack(click_pos, attacked_unit   )

        if res == "UNIT ATTACKS":
            # Calculate the line between unit's center and click position
            print("MELEE UNIT ATTACKS")
            line_points = bresenham_line(
                self.center[0], self.center[1], click_pos[0], click_pos[1]
            )

            # Get the pixel colors along the line
            # line_pixel_colors = get_pixel_colors(line_points, background_screen)
            # self.slash_animation.x, self.slash_animation.x = attacked_unit.x , attacked_unit.y
            print("rendering slash anim",attacked_unit.x,attacked_unit.y)
            animations.append(SlashAnimation(self.center[0], self.center[1]))
            # self.play_attack_animation( self.x, self.y)
            for point in line_points:
                color =  pixel_colors[point[0]][point[1]]
                if color == RIVER_BLUE :
                  res =  "MELEE UNIT CAN'T ATTACK THROUGH RIVERS " 

        return res
    
    def get_attackable_units(self):
        super().get_attackable_units()
        units_to_remove = []  # Create a list to store units to be removed

        for i, unit in enumerate(self.enemies_in_range):
            center_x, center_y = self.x, self.y
            enemy_center_x, enemy_center_y = unit.start_turn_position[0], unit.start_turn_position[1]
            line_points = bresenham_line(center_x, center_y, enemy_center_x, enemy_center_y)
            line_pixel_colors = get_pixel_colors(line_points, background_screen)

            # Check if any point in the line has the color RIVER_BLUE
            if any(color == RIVER_BLUE for color in line_pixel_colors):
                units_to_remove.append(unit)  # Add the unit to the removal list
                # Find the index of the line to the enemy in range
                line_index = next((j for j, line in enumerate(
                    self.lines_to_enemies_in_range) if line["enemy"] == unit), None)
                if line_index is not None:
                    # Add an interference point to the line
                    interference_point = next(
                        (point for point, color in zip(line_points, line_pixel_colors) if color == RIVER_BLUE), None)
                    self.lines_to_enemies_in_range[line_index]["interference_point"] = interference_point

    # Remove units that need to be removed from enemies_in_range
        for unit in units_to_remove:
            self.enemies_in_range.remove(unit)

    # def load_attack_animation(self):
    #     image_folder = "img/anime/slash"
    #     images = []
    #     for filename in os.listdir(image_folder):
    #         if filename.endswith(".png"):
    #             img = pygame.image.load(os.path.join(image_folder, filename))
    #             images.append(img)
    #     return images
    
    # def play_attack_animation(self, x, y):
    #     animation_duration = 50  # Duration of each frame in milliseconds
    #     start_time = pygame.time.get_ticks()
    #     current_frame = 0
        
    #     current_frame = 0

    #     while current_frame < len(self.slash_animation):
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()

    #         current_time = pygame.time.get_ticks()
    #         elapsed_time = current_time - start_time
    #         current_frame = elapsed_time // animation_duration

    #         # screen.fill((0, 0, 0))  # Clear the screen

    #         if current_frame < len(self.slash_animation):
    #             frame = self.slash_animation[current_frame]
    #             screen.blit(frame, (x, y))
            

    #         pygame.display.flip()
    #         clock.tick(60)  # Frame rate
