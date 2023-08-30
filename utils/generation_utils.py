def find_river_segments_for_crossing(rivers):
    river_segments = []
    for river in rivers:
        index = 0
        last_point = river.points[index]
        river_segment = [last_point]

        while index < len(river.points) - 1:
             
            new_point = river.points[index + 1]
            last_point = new_point
            # print("river_segment" , river_segment)
            # print("last_point" , last_point)
            river_segment.append(new_point)

            intersects = compare_to_other_rivers(
                rivers, new_point, river,  river_segment, river_segments)

            if intersects:
               
                river_segments.append(river_segment)
                river_segment = [last_point]
                # print("INTERSECTS", river_segments, river_segment)
                #reset_segment(last_point, river_segment, river_segments)
                

            index += 1
        river_segments.append(river_segment)
            

    return river_segments


def compare_to_other_rivers(other_rivers, point, river,  river_segment, river_segments):
    for other_river in other_rivers:
        if other_river == river:
            continue
        # print("POINt in other river", point in other_river.points)
        # print("other river points", other_river.points)
        if point in other_river.points:
            return True
    return False


# def reset_segment(last_point, river_segment, river_segments):
#     river_segments.append(river_segment)
#     river_segment = [last_point]
#     # print("reseted river segment")
    