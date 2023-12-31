import random
import pygame
import math
from config import *
from utils.utils import *
from buildings.supply_depo import SupplyDepo
from buildings.bridge import Bridge
from buildings.town import Town, is_far_enough, get_town_distances
from buildings.road import *
from buildings.river import River
from utils.generation_utils import find_river_segments_for_crossing
import game_state

class BattleGround:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Define quantities of each element to generate
        self.num_forests = game_state.num_forests
        self.num_rivers = game_state. num_rivers
        self.num_towns = game_state.num_towns
        self.max_roads = 9
        self.num_supply_depots = 2
# self.place_forrests()#
        self.forests = self.place_forrests()  # [[(378, 10), (368, 0), (358, 0), (348, 0), (338, 0), (328, 0), (318, 0), (308, 0), (298, 0), (288, 0), (278, 0), (268, 0), (258, 0), (248, 0), (238, 0), (228, 0), (218, 0), (208, 0), (198, 0), (188, 0), (178, 0), (168, 0), (158, 0), (148, 0), (138, 0), (128, 0), (118, 0), (108, 0), (98, 10), (88, 10), (78, 20), (68, 30), (68, 30), (78, 40), (88, 50), (98, 70), (108, 100), (118, 110), (128, 140), (138, 150), (148, 150), (158, 150), (168, 140), (178, 140), (188, 140), (198, 130), (208, 150), (218, 160), (228, 170), (238, 160), (248, 160), (258, 150), (268, 110), (278, 100), (288, 100), (298, 90), (308, 70), (318, 70), (328, 80), (338, 70), (348, 60), (358, 40), (368, 30), (378, 10)]]#self.place_forrests( ) #[[(1260, 240), (1250, 230), (1240, 210), (1230, 200), (1220, 200), (1210, 190), (1200, 180), (1190, 180), (1180, 150), (1170, 140), (1160, 140), (1150, 150), (1140, 140), (1130, 150), (1120, 150), (1110, 160), (1100, 170), (1090, 180), (1080, 170), (1070, 180),
# (1060, 190), (1050, 190), (1040, 200), (1030, 210), (1020, 230), (1010, 250), (1010, 260), (1020, 270), (1030, 270), (1040, 300), (1050, 330), (1060, 340), (1070, 360), (1080, 370), (1090, 360), (1100, 370), (1110, 380), (1120, 370), (1130, 370), (1140, 360), (1150, 350), (1160, 350), (1170, 350), (1180, 360), (1190, 350), (1200, 360), (1210, 350), (1220, 330), (1230, 320), (1240, 290), (1250, 280), (1260, 250)]]#
        # [(0, 0), (400, 300)]#[(0,0),(100, 200),(300,300), (350, 200)]
        self.rivers = self.place_rivers()
        # self.convergence_points = []
        self.towns = self.place_towns()
        self.roads = self.place_roads()
        self.bridges = self.place_bridges()
        self.supply_depots = self.place_supply_depots()

        self.river_segments = None

    def __del__(self):
        print("BATTLEGROUND DELETED")

    def place_forrests(self):
        forests = []
        for _ in range(self.num_forests):
            x = round(random.randint(0, self.width))
            y = round(random.randint(0, self.height - BUTTON_BAR_HEIGHT))

            forest_size = 4500  # round(random.randint(20, 50))
            forest_from_squares = self.create_forest_squares(
                x, y, square_size, 0.2, forest_size)
            forest_shape = find_edge_points(forest_from_squares)
            if len(forest_shape) >= 3:
                forests.append(forest_shape)

        return forests

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
        rivers = []
        for _ in range(self.num_rivers):
            start_x = random.choice([0, self.width])
            start_y = random.randint(0, self.height)
            end_x = self.width - start_x
            end_y = random.randint(0, self.height)

            control_x1 = random.randint(0, self.width)
            control_y1 = random.randint(0, self.height)
            control_x2 = random.randint(0, self.width)
            control_y2 = random.randint(0, self.height)

            new_river = River((start_x, start_y), (end_x, end_y), [
                              (control_x1, control_y1), (control_x2, control_y2)])
            new_river.generate_chunks(rivers)
            rivers.append(new_river)
        self.river_segments = (find_river_segments_for_crossing(rivers))
         
        return rivers

    def place_towns(self):
        towns = []
        min_distance = 300
        max_attempts = 10

        for town_index in range(self.num_towns):
            for _ in range(max_attempts):
                x = random.randint(0, self.width - 60)
                y = random.randint(0, self.height - 60)
                town_coors = (x, y)
                # town_params = []

                if is_far_enough(town_coors, min_distance,  towns):
                    town_size = (random.randint(40, 60), random.randint(
                        40, 60))  # Random size for the rectangles
                    town_topleft = (x, y)
                    house_rectangles = []
                    num_houses = random.randint(3, 6)
                    new_town = Town(x, y, town_size, TOWN_RED, num_houses)

                    new_town.place_houses(self.rivers)
                    towns.append(new_town)

                    break
            else:
                print(f"Failed to place town after {max_attempts} attempts.")
                break
        return towns

    def place_roads(self):
        roads = []
        connected_towns = set()  # Keep track of connected towns to prevent duplicated roads
        screen_sides_starts = [
            ((0, random.randint(100, self.height - 100)), (self.width,
                                                           random.randint(100, self.height - 100))),  # Top side
            ((random.randint(100, self.width - 100), 0),
             (random.randint(100, self.width - 100), self.height)),  # Left side
            ((self.width, random.randint(100, self.height - 100)),
             (0, random.randint(100, self.height - 100))),  # Bottom side
            ((random.randint(100, self.width - 100), self.height),
             (random.randint(100, self.width - 100), 0))   # Right side
        ]
        for index, town in enumerate(self.towns):
            # List to store distances and corresponding town indices
            distances = get_town_distances(
                self.towns, town.center, town.rect, index)
            # Sort distances in ascending order
            distances.sort()
            # Get the indices of the two closest towns
            closest_indices = [i for _, i in distances[:2]]
            # Get the rectangles of the two closest towns
            closest_town_rects = [self.towns[i] for i in closest_indices]

            for i, nearby_town in zip(closest_indices, closest_town_rects):
                # Check if a road connection already exists between these towns
                if (index, i) in connected_towns or (i, index) in connected_towns:
                    continue

                new_road = Road(nearby_town, town)
                new_road.generate_road_points(roads, screen_sides_starts)

            # if not new_road.intersects:
            connected_towns.add((index, i))
            connected_towns.add((i, index))
            roads.append(new_road)

        edge_roads = generate_from_edge_roads(
            screen_sides_starts, self.towns, roads)

        for road in edge_roads:
            # Save the road path to self.roads
            roads.append(road)
        return roads

    def place_bridges(self):
        bridges = []
       
        # print("here are the river segments", self.river_segments)
        # print("here are the rivers", [river.points for river in self.rivers])

        # for every river segment
        for segment in self.river_segments:
            # if the segment doesnt have two points continue
            if len(segment) < 2:
                continue
           # for part in all_river_parts:
            river_part_intersects = False
      
            for i in range(len(segment) - 1):
                point1 = segment[i ]
                point2 = segment[i +1]
                line_segment = (point1, point2)

                # print(point1, point2, "points")
                for road in self.roads:
                    start_point, mid_point, end_point = road.points

                    if do_lines_intersect(point1, point2,  start_point, mid_point):
                        # print(f"River segment {line_segment} intersects with road segment ({start_point}, {mid_point})")
                        river_part_intersects = True
                    elif do_lines_intersect(point1, point2, mid_point, end_point):
                        # print(f"River segment {line_segment} intersects with road segment ({mid_point}, {end_point})")
                        river_part_intersects = True
            if river_part_intersects:
                continue
         
            start_point = random.choice(segment[:-1])
            end_point_index = segment.index(start_point) + 1
            end_point = segment[end_point_index]
            print("start end", start_point, end_point, segment)
            # get the a random point on a line between that point and a point next to that
            t = random.uniform(0, 1)
            bridge_point = (
                int(start_point[0] + t *
                    (end_point[0] - start_point[0])),
                int(start_point[1] + t *
                    (end_point[1] - start_point[1]))
            )
            # create a bridge on that point
            dx = end_point[0] - start_point[0]
            dy = end_point[1] - start_point[1]
            angle = math.atan2(dy, dx)

            new_bridge = Bridge(
                bridge_point[0], bridge_point[1], angle, (40, 30), BRIDGE_COLOR)

            print(
                f"River segment doesn't intersect with any road. Bridge declared at {bridge_point}, angle: {angle}")
            bridges.append(new_bridge)
            # append it
 
        return bridges

    def place_supply_depots(self):
        supply_depots = []
        DEPO_SIZE = 50
        AMMO_RANGE = 100
        AMMO_PER_UNIT = 1
    # Place supply depots on the left side
        for _ in range(self.num_supply_depots // 2):
            # Ensure at least 50 pixels from the left edge
            x_left = random.randint(50, self.width // 2 - 50)
            # Ensure at least 50 pixels from top and bottom edges
            y = random.randint(50, self.height - 50)
            supply_depots.append(SupplyDepo(
                x_left, y,  DEPO_SIZE, AMMO_RANGE, AMMO_PER_UNIT))

        # Place supply depots on the right side
        for _ in range(self.num_supply_depots // 2):
            # Ensure at least 50 pixels from the right edge
            x_right = random.randint(self.width // 2 + 50, self.width - 50)
            # Ensure at least 50 pixels from top and bottom edges
            y = random.randint(50, self.height - 50)
            supply_depots.append(SupplyDepo(
                x_right, y, DEPO_SIZE, AMMO_RANGE, AMMO_PER_UNIT))
        return supply_depots

    def draw(self, screen):
        dot_radius = 10

        # Draw forrests
        for forest in self.forests:

            pygame.draw.polygon(screen, FORREST_GREEN, forest)
        # Draw towns
        for town in self.towns:
            town.draw_self(screen)

          # Draw rivers
        for river in self.rivers:

            pygame.draw.lines(screen, RIVER_BLUE, False, river.points, 10)
         # Draw roads
        for road in self.roads:
            road.draw(screen)
        for bridge in self.bridges:
            bridge.draw(screen)
        for town in self.towns:

            town.draw_houses(screen)
        # Draw bridges

        bridge_width = 25
        bridge_height = 50

     
        # Draw supply depots
        for depo in self.supply_depots:
            depo.draw(screen)
