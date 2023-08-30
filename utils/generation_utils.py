def find_river_segments_for_crossing(rivers):
    river_segments = []

    for river in rivers:
        index = 0
        last_point = river.points[index]
        river_segment = [last_point]

        while index < len(river.points) - 1:

            new_point = river.points[index + 1]
            river_segment.append(new_point)

            intersects = compare_to_other_rivers(
                rivers, new_point, river,  river_segment, river_segments)

            if intersects:
                reset_segment(new_point, river_segment, river_segments)
                break

            index += 1

    return river_segments


def compare_to_other_rivers(other_rivers, point, river,  river_segment, river_segments):
    for other_river in other_rivers:
        if other_river == river:
            continue
        if point in other_river.points:
            return True
    return False


def reset_segment(point, river_segment, river_segments):
    river_segments.append(river_segment)
    river_segment = [point]