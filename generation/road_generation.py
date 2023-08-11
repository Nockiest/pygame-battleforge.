import math

def get_town_distances(all_towns, town_center, town_rect, town_index):
    distances = []  # Compare the center of the current town with the centers of other towns
    for i, other_town_tuple in enumerate(all_towns):
        if i == town_index:
            continue  # Skip comparing with itself
            
        other_town_center = other_town_tuple[0].center
        distance = math.dist(town_center, other_town_center)
        distances.append((distance, i))
    return distances

def calculate_mid_point_pos(town_rect,town_center):
    if abs(town_center[1] - town_rect.center[1]) <= 150:
       return town_center[0], town_center[1] 
    if town_center[1] < town_rect.center[1]:
       return town_center[0], town_center[1] + town_rect.height // 2 + 150 
    else:
       return town_rect.x + town_rect.width // 2, town_center[1] + town_rect.height // 2 - 150 

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
         