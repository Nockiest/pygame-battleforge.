import pygame
import random
from .structure import Structure
from config import *
from utils.utils import *
 

def calculate_mid_point_pos(nearby_town ,start_town ):
    if abs(start_town.center[1] - nearby_town.center[1]) <= 150:
       return start_town.center[0], start_town.center[1] 
    if start_town.center[1] < nearby_town.center[1]:
       return start_town.center[0], start_town.center[1] + nearby_town.size[1] // 2 + 150 
    else:
       return nearby_town.x + nearby_town.size[0]// 2, start_town.center[1] + nearby_town.size[1] // 2 - 150 

def augment_mid_point(road_end_point, road_start_point, mid_point):
        # Define the equation of the line using two-point form: y - y1 = m * (x - x1)
    if road_end_point[0] - road_start_point[0] == 0:
        m = float('inf')  # Handle division by zero
    else:
        m = (road_end_point[1] - road_start_point[1]) / (road_end_point[0] - road_start_point[0])
    b = road_start_point[1] - m * road_start_point[0]
    
    # Calculate the y-coordinate of the intersection point
    intersection_y = m * mid_point[0] + b
    
    # Check if the calculated intersection y-coordinate is close enough to the mid_point's y-coordinate
    if abs(mid_point[1] - intersection_y) < 50:  # Adjust threshold as needed
        road_end_point = mid_point
    return( mid_point , road_end_point)
         
def check_for_roads_intersection(roads, start_point, mid_point, end_point):
    for existing_road in roads:
       
        existaing_start_point, existing_mid_point, existing_endPoint = existing_road.points
        res1 = do_lines_intersect(mid_point, end_point, existaing_start_point, existing_mid_point)
        res2 = do_lines_intersect(start_point, mid_point, existing_mid_point, existing_endPoint)
        if res1 :          
            end_point = res1 
            return True
        elif res2: 
            # print("INTERSECT")         
            end_point =res2
            mid_point =res2
            return True
        
    return False


def generate_from_edge_roads(screen_sides, towns, roads):
    edge_roads = []
    for index, town in enumerate(towns):
         
        # Iterate through each screen side and find the closest town
        closest_town_index = None
        min_distance = float('inf')
        for i, (side_start, side_end) in enumerate(screen_sides):
            distance = math.dist(town.center, side_start)
            if distance < min_distance:
                min_distance = distance
                closest_town_index = i
        
        # Get the point on the selected screen side
        selected_point = screen_sides[closest_town_index][0]
        
        # Calculate the direction of the road (angle towards the selected point)
        angle = math.atan2(selected_point[1] - town.center[1], selected_point[0] - town.center[0])
        
        # Calculate the endpoint of the road
        road_length = math.dist(town.center, selected_point)
        end_point = (int(town.center[0] + road_length * math.cos(angle)),
                    int(town.center[1] + road_length * math.sin(angle)))
        new_edge_road = Road(town, selected_point)
        res = check_for_roads_intersection(roads, town.center, end_point, end_point)
        if not res:
            new_edge_road.points = (town.center, end_point, end_point)
            edge_roads.append(new_edge_road)
    return edge_roads


class Road(Structure):
    def __init__(self, nearby_town, start_town   ):

        super().__init__(0, 0, size = (1,1), color=ROAD_GRAY)
        self.points = [] 
        self.start_town = start_town
        self.end_town = nearby_town
        # self.intersects = False

    def __repr__(self) -> str:
        return f'{type(self).__name__}, points {self.points} '  
    def generate_road_points(self, roads, screen_sides):
        # Calculate the point along the x or y axis to move first
        mid_point = calculate_mid_point_pos(self.start_town  ,self.end_town)
                
        # Calculate the direction of the road (angle towards the other town)
        angle = math.atan2(self.end_town.center[1] - mid_point[1], self.end_town.center[0] - mid_point[0])
        
        # Calculate the endpoint of the road
        road_length = math.dist(mid_point, self.end_town.center)
        end_point = (
            int(mid_point[0] + road_length * math.cos(angle)),
            int(mid_point[1] + road_length * math.sin(angle))
        )
        
        # Check for road intersections
        for road in roads:
            print("road", road, self)
            _, road_start_point, road_end_point = road.points                
            mid_point,  _ = augment_mid_point(road_end_point, road_start_point, mid_point)

            # Check if the road intersects with any existing road segments
        check_for_roads_intersection( roads, self.start_town.center, mid_point, end_point)
    
        
    # If the road doesn't intersect with any existing road, add it to the roads list
        # if not self.intersects:
        #     roads.append((start_town.center, mid_point, end_point))
        self.points = (self.start_town.center, mid_point, end_point)

 

    def draw(self, screen):
          
            for i in range(len(self.points) - 1):
                pygame.draw.line(screen, ROAD_GRAY  , self.points[i], self.points[i + 1], 10)  # Saddle Brown
               
                # Calculate the coordinates for the corners of the square
                x, y = self.points[i + 1]
                square_size = 7
                square_corners = [
                    (x - square_size / 2, y - square_size / 2),
                    (x + square_size / 2, y - square_size / 2),
                    (x + square_size / 2, y + square_size / 2),
                    (x - square_size / 2, y + square_size / 2)
                ]
               
                # Draw the square
                pygame.draw.polygon(screen, ROAD_GRAY, square_corners)