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

def create_unit( unit_params,   living_units):
    # Create the unit object
    unit_class, x, y,   color, = unit_params
    unit = unit_class(x=x, y=y,  color=color)
 
    living_units.append(unit)
    # Update the teams dictionary to store the unit in the corresponding color's list
    

    return unit