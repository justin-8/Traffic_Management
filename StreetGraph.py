import sys

# Initialize an empty graph
graph = {"adj_list": {}, "edges": set()}

def do_lines_intersect(p1, q1, p2, q2):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or counterclockwise

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and is_point_on_segment(p1, p2, q1):
        return True
    if o2 == 0 and is_point_on_segment(p1, q2, q1):
        return True
    if o3 == 0 and is_point_on_segment(p2, p1, q2):
        return True
    if o4 == 0 and is_point_on_segment(p2, q1, q2):
        return True

    return False

def is_point_on_segment(p, q, r):
    if (
        q[0] <= max(p[0], r[0])
        and q[0] >= min(p[0], r[0])
        and q[1] <= max(p[1], r[1])
        and q[1] >= min(p[1], r[1])
    ):
        return True
    return False

def calculate_intersection(street1, street2):
    intersections = []
    for i in range(len(street1) - 1):
        for j in range(len(street2) - 1):
            p1, q1 = street1[i], street1[i + 1]
            p2, q2 = street2[j], street2[j + 1]
            if do_lines_intersect(p1, q1, p2, q2):
                intersection = find_intersection(p1, q1, p2, q2)
                intersections.append(intersection)
    return intersections

def find_intersection(p1, q1, p2, q2):
    A1 = q1[1] - p1[1]
    B1 = p1[0] - q1[0]
    C1 = A1 * p1[0] + B1 * p1[1]

    A2 = q2[1] - p2[1]
    B2 = p2[0] - q2[0]
    C2 = A2 * p2[0] + B2 * p2[1]

    determinant = A1 * B2 - A2 * B1

    x = (B2 * C1 - B1 * C2) / determinant
    y = (A1 * C2 - A2 * C1) / determinant

    return (x, y)

def add_street(name, coordinates):
    graph["adj_list"][name] = {"coord": coordinates, "intersections": set()}

    for street_name, street_data in graph["adj_list"].items():
        if street_name != name:
            intersections = calculate_intersection(
                coordinates, street_data["coord"]
            )
            for intersection in intersections:
                street_data["intersections"].add(intersection)
                graph["adj_list"][street_name]["intersections"].add(intersection)

def modify_street(name, coordinates):
    if name not in graph["adj_list"]:
        raise Exception(f"Street name does not exist: {name}")

    old_coordinates = graph["adj_list"][name]["coord"]
    for street_name, street_data in graph["adj_list"].items():
        if street_name != name:
            street_data["intersections"] -= set(
                calculate_intersection(old_coordinates, street_data["coord"])
            )

    graph["adj_list"][name]["coord"] = coordinates

    for street_name, street_data in graph["adj_list"].items():
        if street_name != name:
            intersections = calculate_intersection(
                coordinates, street_data["coord"]
            )
            for intersection in intersections:
                street_data["intersections"].add(intersection)
                graph["adj_list"][street_name]["intersections"].add(intersection)

def remove_street(name):
    if name not in graph["adj_list"]:
        raise Exception(f"Street name does not exist: {name}")

    del graph["adj_list"][name]

    for street_name, street_data in graph["adj_list"].items():
        street_data["intersections"] -= set(
    (intersection for intersection in street_data["intersections"] if name in intersection)
)

def generate_graph():
    print("V = {")
    for i, (street_name, street_data) in enumerate(graph["adj_list"].items(), start=1):
        print(f"{i}: {street_data['coord']}")
    print("}")

    print("E = {")
    edge_set = set()
    for street_name, street_data in graph["adj_list"].items():
        for intersection in street_data["intersections"]:
            other_street = next(
                name for name, data in graph["adj_list"].items() if intersection in data["intersections"]
            )
            if street_name < other_street:
                edge_set.add((street_name, other_street))
    for i, (u, v) in enumerate(edge_set, start=1):
        print(f"<{i},{u},{v}>")
    print("}")

def main():
    while True:
        try:
            line = input().strip()
            if not line:
                continue
            elif line == "gg":
                generate_graph()
            else:
                parts = line.split()
                command = parts[0]
                if command == "add":
                    street_name = ' '.join(parts[1:parts.index('(')])
                    coordinates = [(int(parts[i]), int(parts[i + 1])) for i in range(parts.index('(') + 1, len(parts), 2)]
                    add_street(street_name, coordinates)
                elif command == "mod":
                    street_name = ' '.join(parts[1:parts.index('(')])
                    coordinates = [(int(parts[i]), int(parts[i + 1])) for i in range(parts.index('(') + 1, len(parts), 2)]
                    modify_street(street_name, coordinates)
                elif command == "rm":
                    street_name = ' '.join(parts[1:]).strip('"')
                    remove_street(street_name)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
