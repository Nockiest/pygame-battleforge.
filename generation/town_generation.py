from utils import *
from config import *
import pygame
def is_far_enough(  new_town, min_distance, towns):
        for town in towns:
           
            if  distance(new_town, town[0]) < min_distance:
                return False
        return True


def check_river_collision(new_house, rivers, screen):
    for river in rivers:
        for i in range(len(river) - 1):
            segment_start = river[i]
            segment_end = river[i + 1]
           
            # Create a rectangle representing the river segment
            segment_rect = pygame.Rect(segment_start, (segment_end[0] - segment_start[0], segment_end[1] - segment_start[1]))
           
            if pygame.draw.line(screen, (0, 0, 0, 0), segment_start, segment_end).colliderect(new_house):
                # print("TOWN COLLIDES", new_house, segment_rect)
                return True  # House collides with river segment
    return False  # No collision with any river segment


