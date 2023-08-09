import random
import pygame
import math
from config import *
from utils import *
square_size = 10  # Adjust the size range as needed

def do_lines_intersect(p1, p2, p3, p4):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)

    if o1 != o2 and o3 != o4:
        if min(p1[0], p2[0]) <= max(p3[0], p4[0]) and min(p3[0], p4[0]) <= max(p1[0], p2[0]) and \
           min(p1[1], p2[1]) <= max(p3[1], p4[1]) and min(p3[1], p4[1]) <= max(p1[1], p2[1]):
            # Calculate the point of intersection
            intersect_x = (o1 * p3[0] - o2 * p4[0]) / (o1 - o2)
            intersect_y = (o1 * p3[1] - o2 * p4[1]) / (o1 - o2)
            return intersect_x, intersect_y

    return False

class BattleGround:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.forests = []
        self.rivers = []# [(0, 0), (400, 300)]#[(0,0),(100, 200),(300,300), (350, 200)]
        self.river_intersection_points = []
        self.towns = []
        self.roads = []
        self.supply_depots = []
        
        # Define quantities of each element to generate
        self.num_forests = 6
        self.num_rivers = 3
        self.num_towns = 4
        self.num_roads = 9
        self.num_supply_depots = 2

    def place_forrests(self):
          for _ in range(self.num_forests):
            x = round(random.randint(0, self.width))
            y = round(random.randint(0, self.height - BUTTON_BAR_HEIGHT))

         
            forest_size = 4500 # round(random.randint(20, 50))
            forest_from_squares = self.create_forest_squares(x, y, square_size, 0.2, forest_size)
            forest_shape = self.find_edge_points(forest_from_squares)
            if len(forest_shape) >= 3:
             self.forests.append(forest_shape)
    
    def create_forest_squares(self, x, y, size, regularity, forest_size):
        points = [(x, y)]  # Start with the initial square's center
        num_squares = 1
        last_points = points[-4:]  # Get the last 4 points
        new_points = []
        while num_squares < forest_size:
            new_points = []

            # Generate new points with a probability based on regularity
            for px, py in last_points:
                if random.random() < regularity:
                    new_points.append((px + size, py))  # Right
                    new_points.append((px - size, py))  # Left
                    new_points.append((px, py + size))  # Down
                    new_points.append((px, py - size))  # Up
                else:
                    new_points.append((px, py))

            # Filter out points that are duplicates or outside the bounds
            new_points = [
                (x, min(max(y, 0), self.height)) for x, y in new_points
            ]  
            new_points = list(set(new_points))  # Remove duplicates
            last_points = new_points  # Update last_points with new points
            points.extend(new_points)
            num_squares = len(points)
            
        return points
    
    def find_edge_points(self,points):
        leftmost_point = min(points, key=lambda p: p[0])
        rightmost_point = max(points, key=lambda p: p[0])
        edge_points = [leftmost_point, rightmost_point]
        leftmost_x, rightmost_x = edge_points[0][0], edge_points[1][0]
        result = []

        for x_axis in range(leftmost_x, rightmost_x + 1, square_size):
            same_x_points = [(x, y) for x, y in points if x == x_axis]
            if same_x_points:
                # print(f"Points with x-coordinate {x_axis}: {same_x_points}")

                # Find points with lowest and highest y-values in the same_x_points array
                lowest_y_point = min(same_x_points, key=lambda p: p[1])
                highest_y_point = max(same_x_points, key=lambda p: p[1])
                # print(f"Lowest y-value: {lowest_y_point}, Highest y-value: {highest_y_point}")

                # Add lowest and highest points to the result array
                result.insert(0,lowest_y_point)
                result.append(highest_y_point)

    

        return result
    
    def place_rivers(self):
        for _ in range(self.num_rivers):
            start_x = random.choice([0, self.width])
            start_y = random.randint(0, self.height)
            end_x = self.width - start_x
            end_y = random.randint(0, self.height)

            control_x1 = random.randint(0, self.width)
            control_y1 = random.randint(0, self.height)
            control_x2 = random.randint(0, self.width)
            control_y2 = random.randint(0, self.height)

            points = []
            num_segments = 10
            convergence_point = None  # Initialize the intersection point as None

            for i in range(num_segments + 1):
                t = i / num_segments
                point = calculate_bezier_curve(t, (start_x, start_y), (control_x1, control_y1), (control_x2, control_y2), (end_x, end_y))
                rounded_point = (round(point[0]), round(point[1]))
                intersects = False  # Initialize the intersection flag as False
                points.append(rounded_point)

                for existing in self.rivers:
                    for j in range(len(existing) - 1):
                        intersection = do_lines_intersect(points[len(points) - 2], rounded_point, existing[j], existing[j+1])
                        if intersection:
                            intersects = True  # Set the intersection flag to True
                            convergence_point = existing[j+1]  # Store the intersection point
                            self.river_intersection_points.append(intersection)
                            break  # Break the inner loop once an intersection is found

                    if intersects:  # If an intersection is found, break the outer loop
                        break

                if intersects:  # If an intersection is found, break the loop and do not add the river
                    break

            if convergence_point:
                points[-1] = convergence_point  # Replace the last point with the intersection point

            # Only add the river if there were no intersections
            self.rivers.append(points)
            # print(self.river_intersection_points)
                 
    

    def place_towns(self):
        #  choose a random point on the map, that it at least 300px from other starting town points

        # create a rectangle with a height and width AROUND 60x30 px



        # for _ in range(self.num_towns):
        #     x = random.randint(0, self.width)
        #     y = random.randint(0, self.height)
        #     self.towns.append((x, y))

    def place_roads(self):
        for _ in range(self.num_roads):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            self.roads.append(((x1, y1), (x2, y2)))

    def place_supply_depots(self):
    # Place supply depots on the left side
        for _ in range(self.num_supply_depots // 2):
            x_left = random.randint(50, self.width // 2 - 50)  # Ensure at least 50 pixels from the left edge
            y = random.randint(50, self.height - 50)  # Ensure at least 50 pixels from top and bottom edges
            self.supply_depots.append((x_left, y))

        # Place supply depots on the right side
        for _ in range(self.num_supply_depots // 2):
            x_right = random.randint(self.width // 2 + 50, self.width - 50)  # Ensure at least 50 pixels from the right edge
            y = random.randint(50, self.height - 50)  # Ensure at least 50 pixels from top and bottom edges
            self.supply_depots.append((x_right, y))

    def draw_bezier_curve(self, screen, points):
            num_segments = 100
            curve_points = []
            for t in range(num_segments + 1):
                t_normalized = t / num_segments
                x = int((1 - t_normalized)**3 * points[0][0] +
                        3 * (1 - t_normalized)**2 * t_normalized * points[2][0] +
                        3 * (1 - t_normalized) * t_normalized**2 * points[3][0] +
                        t_normalized**3 * points[1][0])
                y = int((1 - t_normalized)**3 * points[0][1] +
                        3 * (1 - t_normalized)**2 * t_normalized * points[2][1] +
                        3 * (1 - t_normalized) * t_normalized**2 * points[3][1] +
                        t_normalized**3 * points[1][1])
                curve_points.append((x, y))
            
            pygame.draw.lines(screen, (128, 128, 128), False, curve_points, 2)

    def draw(self, screen):
        dot_radius = 10

        # Draw forrests 
        for forest in self.forests:
           
            pygame.draw.polygon(screen, (0, 255, 0), forest)
            # create a polygon out of the edge pointa
                
        for points in self.rivers:
            pygame.draw.lines(screen, (128, 128, 128), False, points, 2)
        # Draw towns
        for x, y in self.towns:
            pygame.draw.circle(screen, (255, 0, 0), (x, y), dot_radius)  # Red

        # Draw roads
        for (x1, y1), (x2, y2) in self.roads:
            pygame.draw.circle(screen, (139, 69, 19), (x1, y1), dot_radius)  # Saddle Brown
            pygame.draw.circle(screen, (139, 69, 19), (x2, y2), dot_radius)  # Saddle Brown
            pygame.draw.line(screen, (139, 69, 19), (x1, y1), (x2, y2), 2)  # Saddle Brown

        # Draw supply depots
        for x, y in self.supply_depots:
            pygame.draw.circle(screen, (255, 255, 0), (x, y), dot_radius)  # Yellow

def find_river_segments_for_crossing(rivers):
    river_segments = []

    for river in rivers:
        if not river:
            continue

        river_segment_start = river[0]  # Start the river segment from the first point
        river_segment_end = None

        for point in river:
            point_in_other_river = False
            for other_river in rivers:
                if other_river != river and point in other_river:
                    point_in_other_river = True
                    river_segment_end = point
                    break

            if point_in_other_river:
                if river_segment_start != river_segment_end:  # Check if it's a line segment and not a dot
                    river_segments.append((river_segment_start, river_segment_end))
                river_segment_start = river_segment_end
                river_segment_end = None

        # Add the last river segment if needed
        if river_segment_end is None and river_segment_start != river[-1]:
            river_segments.append((river_segment_start, river[-1]))

    return river_segments

 
# # Example usage:
# points = [(1, 3), (4, 2), (2, 6), (7, 1), (5, 5)]
# sample_points=[(70, 110), (95, 75), (80, 120), (135, 120), (75, 115), (130, 115), (110, 75), (105, 125), (115, 105), (105, 70), (90, 115), (120, 95), (80, 95), (100, 110), (75, 90), (130, 90), (50, 100), (105, 100), (115, 80), (90, 90), (65, 100), (125, 
# 130), (70, 75), (125, 75), (100, 85), (85, 130), (110, 95), (120, 115), (95, 125), (95, 70), (80, 115), (135, 115), (130, 110), (110, 125), (110, 70), (105, 120), (105, 65), (90, 110), (120, 90), (65, 120), (95, 100), (80, 90), (100, 105), 
# (75, 85), (55, 100), (50, 95), (115, 130), (105, 95), (115, 75), (60, 105), (90, 85), (70, 125), (70, 70), (125, 125), (125, 70), (100, 80), (60, 80), (120, 110), (95, 120), (70, 100), (95, 65), (110, 120), (110, 65), (85, 100), (105, 115), (90, 105), (120, 85), (95, 95), (80, 85), (135, 85), (55, 95), (75, 80), (130, 80), (50, 90), (115, 125), (105, 90), (115, 70), (90, 135), (65, 90), (125, 120), (100, 130), (75, 110), (100, 75), (85, 120), (115, 100), (95, 115), (70, 95), 
# (125, 95), (80, 105), (110, 115), (85, 95), (65, 110), (120, 80), (80, 80), (55, 90), (130, 130), (110, 90), (50, 85), (105, 85), (115, 65), (90, 130), (90, 75), (65, 85), (70, 115), (125, 115), (100, 125), (75, 105), (85, 115), (95, 110), 
# (70, 90), (125, 90), (100, 100), (55, 110), (110, 110), (105, 105), (65, 105), (120, 75), (95, 85), (80, 75), (55, 85), (75, 70), (110, 85), (130, 125), (115, 115), (90, 125), (125, 110), (100, 65), (85, 110), (115, 90), (95, 105), (70, 85), (125, 85), (45, 95), (100, 95), (55, 105), (110, 105), (85, 85), (60, 95), (120, 125), (120, 70), (95, 135), (95, 80), (80, 125), (135, 125), (75, 120), (130, 120), (110, 80), (115, 110), (105, 75), (90, 120), (120, 100), (65, 75), (125, 
# 105), (80, 100), (100, 115), (75, 95), (100, 60), (85, 105), (60, 115), (115, 85), (90, 95), (70, 80), (125, 80), (45, 90), (100, 90), (110, 100), (85, 80), (60, 90), (120, 120), (120, 65), (95, 130)] 
 
# edge_points = find_edge_points(sample_points)
# print(edge_points)
# # print(edge_points)  # Output: [(1, 3), (7, 1)]