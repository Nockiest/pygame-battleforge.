import math

from config import *


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
    line_points = bresenham_line(
        line_start_x, line_start_y, line_end_x, line_end_y)

    for point_x, point_y in line_points:

        # print(attacked_unit.rect, point_x,point_y, attacked_unit.rect.collidepoint((point_x, point_y)))
        if attacked_unit.rect.collidepoint((point_x, point_y)):
            # print(f"Interfering point: ({point_x}, {point_y}  ) ")
            return (point_x, point_y, line_points)

    point_x = None
    point_y = None

    return (point_x, point_y, line_points)


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
            # print(f"Points with x-coordinate {x_axis}: {same_x_points}")

            # Find points with lowest and highest y-values in the same_x_points array
            lowest_y_point = min(same_x_points, key=lambda p: p[1])
            highest_y_point = max(same_x_points, key=lambda p: p[1])
            # print(f"Lowest y-value: {lowest_y_point}, Highest y-value: {highest_y_point}")

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
        if point[0] >= 0 and point[0] < surface.get_width() and point[1] >= 0 and point[1] < surface.get_height():
            pixel_color = surface.get_at(point)
            points_colors.append(pixel_color)
        else:
            # Append a placeholder color (you can modify this as needed)
            points_colors.append((1,1,1 ))  # terminate color
            # Alternatively, you can use None to indicate that the pixel doesn't exist
            # points_colors.append(None)
    return points_colors