import math
from config import *
import game_state

def get_two_units_center_distance(unit1, unit2):
    # Calculate the distance between the center points of the units, considering their sizes
    dx = (unit1.x + unit1.size // 2) - (unit2.x + unit2.size // 2)
    dy = (unit1.y + unit1.size // 2) - (unit2.y + unit2.size // 2)
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance


def sum_values(obj):
    total_sum = 0
    for value in obj.values():
        total_sum += value
    return total_sum

def bresenham_line(x0, y0, x1, y1):
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    if x0 < x1:
        sx = 1
    else:
        sx = -1
    if y0 < y1:
        sy = 1
    else:
        sy = -1

    err = dx - dy

    while True:
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break
        if 0> x0 or x0 > WIDTH or 0 > y0 or y0 > HEIGHT- BUTTON_BAR_HEIGHT:
            
            return points 
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return points

def check_precalculated_line_square_interference(attacked_unit, line_points):
    for point_x, point_y in line_points:

       
        if attacked_unit.rect.collidepoint((point_x, point_y)):
            # print(f"Interfering point: ({point_x}, {point_y}  ) ")
            interferes = True
            return (point_x, point_y,  interferes)

    
    return (None, None, False)
################for when I already have the bersenham line

def check_square_line_interference(attacked_unit, line_start_x, line_start_y, line_end_x, line_end_y):
    # Calculate the center of the square

    # Generate all the points on the line segment using Bresenham's algorithm
    line_points = bresenham_line(
        line_start_x, line_start_y, line_end_x, line_end_y)

    for point_x, point_y in line_points:

        
        if attacked_unit.rect.collidepoint((point_x, point_y)):
            # print(f"Interfering point: ({point_x}, {point_y}  ) ")
            return (point_x, point_y, False)

  
    return  (None, None, False)

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
            
def move_unit_along_line(line_points, intersecting_point, unit, screen):
    # Find the index of the intersecting point in the line_points list
    intersecting_index = line_points.index(intersecting_point)

    # Calculate the new index for the unit's position
    new_index = max(0, intersecting_index - unit.size // 2)

    # Update the unit's x and y coordinates with the coordinates from the new index
    new_center_x, new_center_y = line_points[new_index]
    unit.x = new_center_x - unit.size // 2
    unit.y = new_center_y - unit.size // 2

    # Print the color of each pixel along the line_points
    for point in line_points:
        pixel_color = screen.get_at(point)
        print(f"Color at pixel {point}: {pixel_color}")

    return


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def find_edge_points(points):
    leftmost_point = min(points, key=lambda p: p[0])
    rightmost_point = max(points, key=lambda p: p[0])
    edge_points = [leftmost_point, rightmost_point]
    leftmost_x, rightmost_x = edge_points[0][0], edge_points[1][0]
    result = []

    for x_axis in range(leftmost_x, rightmost_x + 1, square_size):
        same_x_points = [(x, y) for x, y in points if x == x_axis]
        if same_x_points:
          

            # Find points with lowest and highest y-values in the same_x_points array
            lowest_y_point = min(same_x_points, key=lambda p: p[1])
            highest_y_point = max(same_x_points, key=lambda p: p[1])
            

            # Add lowest and highest points to the result array
            result.insert(0, lowest_y_point)
            result.append(highest_y_point)

    return result


def calculate_bezier_curve(t, p0, p1, p2, p3):
    u = 1 - t
    uu = u * u
    uuu = uu * u
    tt = t * t
    ttt = tt * t

    p = (
        u * uuu * p0[0] + 3 * uu * t * p1[0] +
        3 * u * tt * p2[0] + ttt * p3[0],
        u * uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    )
    return p


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

def get_pixel_colors(points, surface):
    points_colors = []
    for point in points:

        if is_inside_rectangle(point[0], point[1], 0, HEIGHT-TENDER_HEIGHT, TENDER_WIDTH, TENDER_HEIGHT ):
            points_colors.append(TERMINATE_COLOR)  # terminate color
        elif is_inside_rectangle(point[0], point[1], WIDTH - TENDER_WIDTH, HEIGHT-TENDER_HEIGHT, TENDER_WIDTH, TENDER_HEIGHT ):
            points_colors.append(TERMINATE_COLOR)  # terminate color
        elif point[0] >= 0 and point[0] < WIDTH and point[1] >= 0 and point[1] < HEIGHT:
            
            pixel_color = surface.get_at(point)
            points_colors.append(pixel_color)
        else:
            points_colors.append(TERMINATE_COLOR)  # terminate color
          
    return points_colors

def calculate_movement_cost(color_list):
    movement_costs = []
    total_cost = 0
    for i, color in enumerate(color_list):
        
        if color == FORREST_GREEN:
            total_cost += 2
        elif color == ROAD_GRAY:
            total_cost += 0.5
        elif color == RIVER_BLUE:
            total_cost += 1000000 # to prevent the unit from going over the river 
        elif color == BRIDGE_COLOR:
            total_cost += 1
        elif color == TOWN_RED or color == HOUSE_PURPLE:
            total_cost += 1
        elif color == TERMINATE_COLOR:
            total_cost += 10000000000
            movement_costs.append((total_cost, i, color))
            return movement_costs
        else:
            total_cost += 1  # Default movement cost
        
        movement_costs.append((total_cost, i, color))
    
    return movement_costs

def update_sorted_units(   ) :
        global sorted_living_units
        sorted_living_units = {}
        for unit in game_state.living_units.array:
            unit_type = unit.__class__.__name__
            sorted_living_units.setdefault(unit_type, []).append(unit)
 

def is_inside_rectangle(x, y, left, top, width, height):
    if left <= x <= left + width and top <= y <= top + height:
        return True
    else:
        return False

def update_players_unit():
    for player in game_state.players:
        for unit in player.units:
            if unit not in game_state.living_units.array:
                player.remove_self_unit(  unit)

def new_point_interferes_with_unit(self,  point_x, point_y, living_units=game_state.living_units.array):
        # Create a new rectangle for the unit's position

        new_rect = pygame.Rect(point_x - self.size // 2,
                               point_y - self.size // 2, self.size, self.size)

        for unit in living_units:
            if unit is self:
                continue
            res = unit.rect.colliderect(new_rect)
            if res:
                return True
        return False