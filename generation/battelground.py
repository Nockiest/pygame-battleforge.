import random
import pygame
import math
from config import *
from utils import *
from generation.town_generation import *
from generation.road_generation import *
 
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


 
 
class BattleGround:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.forests = []
        self.rivers =   []# [(0, 0), (400, 300)]#[(0,0),(100, 200),(300,300), (350, 200)]
        self.convergence_points = []
        self.towns = []
        self.roads = []
        self.supply_depots = []
        self.bridges= []
        # Define quantities of each element to generate
        self.num_forests = 6
        self.num_rivers = 2
        self.num_towns = 2
        self.num_roads = 9
        self.num_supply_depots = 2


    def place_forrests(self):
          for _ in range(self.num_forests):
            x = round(random.randint(0, self.width))
            y = round(random.randint(0, self.height - BUTTON_BAR_HEIGHT))
     
            forest_size = 4500 # round(random.randint(20, 50))
            forest_from_squares = self.create_forest_squares(x, y, square_size, 0.2, forest_size)
            forest_shape = find_edge_points(forest_from_squares)
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
                        # print(intersection, existing[j], existing[j+1] )
                        if intersection:
                            intersects = True  # Set the intersection flag to True
                            # print(intersection)
                            convergence_point = existing[j+1]  # Store the intersection point
                            self.convergence_points.append(convergence_point)
                            break  # Break the inner loop once an intersection is found


                    if intersects:  # If an intersection is found, break the outer loop
                        break


                if intersects:  # If an intersection is found, break the loop and do not add the river
                    break


            if convergence_point:
                points[-1] = convergence_point  # Replace the last point with the intersection point


            # Only add the river if there were no intersections
           
            self.rivers.append(points)

    def place_towns(self, screen):
        min_distance = 200
        max_attempts = 10


        for _ in range(self.num_towns):
            for _ in range(max_attempts):
                x =random.randint(0, self.width - 60)
                y =random.randint(0, self.height- 60)
                town_coors = (x, y)
                town_params = []
             
                if  is_far_enough(town_coors, min_distance, self.towns):
                    town_size = (random.randint(40, 60), random.randint(40, 60))  # Random size for the rectangles
                    town_topleft = (x, y)
                    house_rectangles = []
                    num_houses = random.randint(3, 6)
                    for _ in range(num_houses):
                        placed_house = False
                        for _ in range(50):  # Attempt at most 50 times to place a house
                            house_x = random.randint(x, x + town_size[0] - square_size)
                            house_y = random.randint(y, y + town_size[1] - square_size)
                            new_house = pygame.Rect(house_x, house_y, square_size, square_size) # square size is the default size of a square
                           
                            # Check for interference with other town rectangles
                            interferes_with_town = any(rect.colliderect(new_house) for rect in house_rectangles)
                           
                            if not interferes_with_town:
                                interferes_with_river = check_river_collision(new_house, self.rivers, screen)                      
                                if not interferes_with_river:
                                    house_rectangles.append(new_house)
                                    placed_house = True
                                    break
                       
                        if not placed_house:
                            break  # If failed to place a house 50 times or if it interferes with rivers, break the loop
                   
                    town_rect = pygame.Rect(town_coors[0], town_coors[1], town_size[0], town_size[1])
                    town_params.append(town_rect )
                    town_params.append(house_rectangles)
                    self.towns.append(town_params)
            else:
                print(f"Failed to place town after {max_attempts} attempts.")
                break
   
       
 
    def place_roads(self):
        connected_towns = set()  # Keep track of connected towns to prevent duplicated roads
   
        for index, town_tuple in enumerate(self.towns):
            town_rect = town_tuple[0]  # Get the rectangle representing the town
            town_center = town_rect.center
           
            # List to store distances and corresponding town indices
            distances = get_town_distances(self.towns, town_center, town_rect, index)
                      
            # Sort distances in ascending order
            distances.sort()         
            # Get the indices of the two closest towns
            closest_indices = [i for _, i in distances[:2]]
            # Get the rectangles of the two closest towns
            closest_town_rects = [self.towns[i][0] for i in closest_indices]
           
            for i, rect in zip(closest_indices, closest_town_rects):
                # Check if a road connection already exists between these towns
                if (index, i) in connected_towns or (i, index) in connected_towns:
                    continue
               
                # Mark these towns as connected
                connected_towns.add((index, i))
                connected_towns.add((i, index))
               
                # Calculate the point along the x or y axis to move first
                mid_point = calculate_mid_point_pos(rect,town_center)
                      
                # Calculate the direction of the road (angle towards the other town)
                angle = math.atan2(rect.center[1] - mid_point[1], rect.center[0] - mid_point[0])
               
                # Calculate the endpoint of the road
                road_length = math.dist(mid_point, rect.center)
                endpoint = (
                    int(mid_point[0] + road_length * math.cos(angle)),
                    int(mid_point[1] + road_length * math.sin(angle))
                )
               
                # Check for road intersections
                for road in self.roads:
                    _, road_start_point, road_end_point = road                
                    mid_point, road_end_point = augment_mid_point(road_end_point, road_start_point, mid_point)

                    # Check if the road intersects with any existing road segments
            intersects_existing = False
            for existing_road in self.roads:
                _, existing_mid_point, _ = existing_road
                if do_lines_intersect(mid_point, endpoint, existing_road[0], existing_mid_point):
                    intersects_existing = True
                    endpoint = existing_mid_point
                    break
                
            # If the road doesn't intersect with any existing road, add it to the roads list
            if not intersects_existing:
                connected_towns.add((index, i))
                connected_towns.add((i, index))
                self.roads.append((town_center, mid_point, endpoint))

               
                # Save the road path to self.roads
                # self.roads.append((town_center, mid_point, endpoint))
        # Iterate through each side of the screen
        screen_sides = [
            ((0, random.randint(100, self.height - 100)), (self.width, random.randint(100, self.height - 100))),  # Top side
            ((random.randint(100, self.width - 100), 0), (random.randint(100, self.width - 100), self.height)),  # Left side
            ((self.width, random.randint(100, self.height - 100)), (0, random.randint(100, self.height - 100))),  # Bottom side
            ((random.randint(100, self.width - 100), self.height), (random.randint(100, self.width - 100), 0))   # Right side
        ]
       
        for index, town_tuple in enumerate(self.towns):
            town_rect = town_tuple[0]  # Get the rectangle representing the town
            town_center = town_rect.center
           
            # Iterate through each screen side and find the closest town
            closest_town_index = None
            min_distance = float('inf')
            for i, (side_start, side_end) in enumerate(screen_sides):
                distance = math.dist(town_center, side_start)
                if distance < min_distance:
                    min_distance = distance
                    closest_town_index = i
           
            # Get the point on the selected screen side
            selected_point = screen_sides[closest_town_index][0]
           
            # Calculate the direction of the road (angle towards the selected point)
            angle = math.atan2(selected_point[1] - town_center[1], selected_point[0] - town_center[0])
           
            # Calculate the endpoint of the road
            road_length = math.dist(town_center, selected_point)
            endpoint = (int(town_center[0] + road_length * math.cos(angle)),
                        int(town_center[1] + road_length * math.sin(angle)))
           
            # Save the road path to self.roads
            self.roads.append((town_center, selected_point, selected_point))

    def place_bridges(self):
        # print(self.convergence_points, "segments")
        # print(self.rivers, "rivers")
        all_river_parts = []
        for river in self.rivers:
            river_parts = []  # Initialize the list to hold current river segment
           
            for point in river:
                # Check if the point matches any convergence point
                if point in self.convergence_points:
                    # if len(river_parts) > 1:
                    river_parts.append(point)
                    all_river_parts.append(river_parts)  # Append the current segment to the list
                    river_parts = [point]  # Start a new segment with the convergence point
                else:
                    river_parts.append(point)  # Append the point to the current segment
           
            if len(river_parts) > 1:
                all_river_parts.append(river_parts)  # Append the last segment if it has more than one point


            # vím, že tato funkce neappenduje convergence point k oběma částem rozdělené řeky, ale je mi to asi jedno
               
        for part in all_river_parts:
            river_part_intersects = False
            # print(part, "river part")
            # print(len(part))
            if len(part) <= 3:
                continue
            for i in range(len(part) - 2):
                point1 = part[i +1 ]
                point2 = part[i +2]
                line_segment = (point1, point2)
               
                # print(point1, point2, "points")
                for road in self.roads:
                    start_point, mid_point, end_point = road
                   


                    if do_lines_intersect(point1, point2,  start_point, mid_point) :
                        # print(f"River segment {line_segment} intersects with road segment ({start_point}, {mid_point})")
                        river_part_intersects = True
                    elif do_lines_intersect(point1, point2, mid_point, end_point):
                        # print(f"River segment {line_segment} intersects with road segment ({mid_point}, {end_point})")
                        river_part_intersects = True
                     
           
            if not river_part_intersects:
                # Choose a random index from the river part
                random_index = random.randint(0, len(part) - 2)
                random_point = part[random_index]
                next_point = part[random_index + 1]


                # Calculate a random point on the line between random_point and next_point
                t = random.uniform(0, 1)
                bridge_point = (
                    int(random_point[0] + t * (next_point[0] - random_point[0])),
                    int(random_point[1] + t * (next_point[1] - random_point[1]))
                )


                # Calculate the angle between the line segment and the x-axis
                dx = next_point[0] - random_point[0]
                dy = next_point[1] - random_point[1]
                angle = math.atan2(dy, dx)


                print(f"River segment doesn't intersect with any road. Bridge declared at {bridge_point}, angle: {angle}")
                self.bridges.append((bridge_point, angle))

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
            pygame.draw.polygon(screen, (128, 255, 128), forest)

        # Draw rivers
        for points in self.rivers:
            pygame.draw.lines(screen, (173, 216, 230), False, points, 10)


        # Draw roads
        for road in self.roads:
            points = road
            # pygame.draw.circle(screen,  (128, 128, 128), points[0], dot_radius)  # Saddle Brown
            # pygame.draw.circle(screen, (128, 128, 128), points[-1], dot_radius)  # Saddle Brown
            for i in range(len(points) - 1):
                pygame.draw.line(screen,  (128, 128, 128), points[i], points[i + 1], 15)  # Saddle Brown
               
                # Calculate the coordinates for the corners of the square
                x, y = points[i + 1]
                square_size = 15
                square_corners = [
                    (x - square_size / 2, y - square_size / 2),
                    (x + square_size / 2, y - square_size / 2),
                    (x + square_size / 2, y + square_size / 2),
                    (x - square_size / 2, y + square_size / 2)
                ]
               
                # Draw the square
                pygame.draw.polygon(screen, (128, 128, 128), square_corners)

        # Draw towns
        for town_rect in self.towns:
            pygame.draw.rect(screen, (255, 0, 0, 100), town_rect[0])  # Red rectangle for town center with reduced opacity
            for house_rect in town_rect[1]:
                pygame.draw.rect(screen, (255, 0, 255), house_rect, 2)  # Magenta rectangle for each house


        # Draw bridges
        bridge_color = (139, 69, 19)  # Saddle Brown
        bridge_width = 25
        bridge_height = 50


        for bridge_center, angle in self.bridges:
            # Calculate the position for the top-left corner of the rotated rectangle
            x = bridge_center[0] - bridge_width / 2
            y = bridge_center[1] - bridge_height / 2
           
            # Create a rotated surface for the rectangle
            bridge_surface = pygame.Surface((bridge_width, bridge_height), pygame.SRCALPHA)
            pygame.draw.rect(bridge_surface, bridge_color, (0, 0, bridge_width, bridge_height))
            rotated_surface = pygame.transform.rotate(bridge_surface, math.degrees(angle   ))
           
            # Calculate the position to blit the rotated rectangle
            blit_position = rotated_surface.get_rect(topleft=(x, y))
           
            # Draw the rotated rectangle onto the screen
            screen.blit(rotated_surface, blit_position)


        # Draw supply depots
        for x, y in self.supply_depots:
            pygame.draw.circle(screen, (255, 255, 0), (x, y), dot_radius)  # Yellow


        # # Update the display
        # pygame.display.flip()
 
