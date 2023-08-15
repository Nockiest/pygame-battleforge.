import pygame
import random
from .structure import Structure
from config import *
from utils.utils import *
 
def get_town_distances(all_towns, town_center, town_rect, town_index):
    distances = []  # Compare the center of the current town with the centers of other towns
    for i, other_town  in enumerate(all_towns):
        if i == town_index:
            continue  # Skip comparing with itself
            
   
        distance = math.dist(town_center,  other_town.center)
        distances.append((distance, i))
    return distances

def is_far_enough(  new_coors, min_distance, towns):
        for town in towns:
           
            if  distance(new_coors, town.center) < min_distance:
                return False
        return True


def check_river_collision(new_house, rivers, screen):
    for river in rivers:
        
        for i in range(len(river.points) - 1):
            segment_start = river.points[i]
            segment_end = river.points[i + 1]
           
            # Create a rectangle representing the river segment
            segment_rect = pygame.Rect(segment_start, (segment_end[0] - segment_start[0], segment_end[1] - segment_start[1]))
           
            if pygame.draw.line(screen, (0, 0, 0, 0), segment_start, segment_end).colliderect(new_house):
                # print("TOWN COLLIDES", new_house, segment_rect)
                return True  # House collides with river segment
    return False  # No collision with any river segment

class Town(Structure):
    def __init__(self, x, y, size, color, num_houses  ):
        super().__init__(x, y, size,color)
        self.num_houses = num_houses
        self.houses = []
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.center = (self.x + self.size[0] // 2, self.y +  self.size[1] // 2) 


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, (0, 0, 0), (self.x + 10, self.y + 10, self.size - 20, self.size - 20))

    def place_houses(self, rivers):
        for _ in range(self.num_houses):
                    placed_house = False
                    for _ in range(50):  # Attempt at most 50 times to place a house
                        house_x = random.randint(self.x, self.x + self.size[0] - square_size)
                        house_y = random.randint(self.y, self.y + self.size[1] - square_size)
                        new_house = pygame.Rect(house_x, house_y, square_size, square_size) # square size is the default size of a square
                        
                        # Check for interference with other town rectangles
                        interferes_with_town = any(rect.colliderect(new_house) for rect in self.houses)
                        
                        if not interferes_with_town:
                            interferes_with_river = check_river_collision(new_house,  rivers, screen)                      
                            if not interferes_with_river:
                                self.houses.append(new_house)
                                placed_house = True
                                break
                    
                    if not placed_house:
                        break  # If failed to place a house 50 times or if it interferes with rivers, break the loop
                   
    def draw_self(self, screen):
          pygame.draw.rect(screen, TOWN_RED  , self.rect)  # Red rectangle for town center with reduced opacity

    def draw_houses(self, screen):
        for house_rect in self.houses:
            pygame.draw.rect(screen, HOUSE_PURPLE , house_rect, 2)  # Magenta rectangle for each house
         
