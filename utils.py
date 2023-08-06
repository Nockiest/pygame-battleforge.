import math

 

def  get_two_units_center_distance(unit1, unit2):
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


def create_unit( unit_params, living_units,     ):
    # Create the unit object
    unit_class, x, y,   color, = unit_params
    unit = unit_class(x=x, y=y,  color=color )
 
    living_units.append(unit)
    # Update the teams dictionary to store the unit in the corresponding color's list
    

    return unit
 
def bresenham_line(x0, y0, x1, y1, max_iterations=1000):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    iterations = 0

    while True:
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

        iterations += 1
        if iterations >= max_iterations:
            print("Maximum iterations exceeded. Terminating.")
            break

    return points

def check_square_line_interference(attacked_unit, line_start_x, line_start_y, line_end_x, line_end_y):
    # Calculate the center of the square

    # Generate all the points on the line segment using Bresenham's algorithm
    line_points = bresenham_line(line_start_x, line_start_y, line_end_x, line_end_y)
   
    for point_x, point_y in line_points:
        
        # print(attacked_unit.rect, point_x,point_y, attacked_unit.rect.collidepoint((point_x, point_y)))
        if attacked_unit.rect.collidepoint((point_x, point_y)):
            # print(f"Interfering point: ({point_x}, {point_y}  ) ")
            return (point_x, point_y, line_points)
    
    point_x = None
    point_y= None
    
    return (point_x, point_y, line_points)
        
def move_unit_along_line(line_points, interersecting_point, unit    ):
    # print(line_points, interersecting_point, unit)
  
    # Find the index of the intersecting point in the line_points list
    intersecting_index = line_points.index(interersecting_point)
    # print(intersecting_index)
   
  
    new_index = max(0, intersecting_index - unit.size // 2)
    # print(new_index)
    # Update the unit's x and y coordinates with the coordinates from the new index
    new_center_x, new_center_y = line_points[new_index]
    unit.x = new_center_x - unit.size // 2
    unit.y = new_center_y - unit.size // 2
    # print( new_center_x, new_center_y )
    return  

 