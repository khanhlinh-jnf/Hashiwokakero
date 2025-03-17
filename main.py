def read_matrix(file_path):
    filein = open(file_path, "r")
    matrix = []
    for line in filein:
        row = []
        for col in line.split(","):
            row.append(int(col))
        matrix.append(row)
    filein.close()
    return matrix


def find_islands(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    points = []
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] != 0:
                points.append((r, c, matrix[r][c]))
    return points


def find_connections(points):
    connections = []
    for i in range(len(points)):
        flagRow = True
        flagCol = True
        for j in range(i + 1, len(points)):
            if not flagCol and not flagRow:
                break
            (r1, c1, v1) = points[i]
            (r2, c2, v2) = points[j]
            if r1 == r2 and flagRow:
                connections.append(((r1, c1), (r2, c2)))
                flagRow = False
            if c1 == c2 and flagCol:
                connections.append(((r1, c1), (r2, c2)))
                flagCol = False
    return connections


def find_intersections(points):
    connections = find_connections(points)
    intersections = []
    for i in range(len(connections)):
        for j in range(i + 1, len(connections)):
            (r1, c1), (r2, c2) = connections[i]
            (r3, c3), (r4, c4) = connections[j]
            if r1 == r2 and c3 == c4:
                if r1 > r3 and r1 < r4 and c3 > c1 and c3 < c2:
                    intersections.append((connections[i], connections[j]))
            elif c1 == c2 and r3 == r4:
                if c1 > c3 and c1 < c4 and r3 > r1 and r3 < r2:
                    intersections.append((connections[i], connections[j]))
    return intersections


def find_set_edges_of_island(island, connections):
    res = {}
    for point in island:
        name = (point[0], point[1])
        res[name] = []
        for connection in connections:
            if name in connection:
                res[name].append(connection)
    return res


def generate_conditions_of_island(list_island, set_edges_of_island):
    res_cdt_island = {}
    res_cdt_bridge = {}
    for island in list_island:
        name = (island[0], island[1])
        value = island[2]
        res_cdt_island[name] = {}
        for edge in set_edges_of_island[name]:
            condition1 = (edge, 1)
            if value != 1:
                condition2 = (edge, 2)
            res_cdt_island[name][condition1] = False
            if value != 1:
                res_cdt_island[name][condition2] = False
            if value != 1 and edge not in res_cdt_bridge:
                res_cdt_bridge[edge] = {}
                res_cdt_bridge[edge][condition1] = False
                res_cdt_bridge[edge][condition2] = False
    return res_cdt_island, res_cdt_bridge


matrix = read_matrix("input.txt")
list_of_islands = find_islands(matrix)
connections = find_connections(list_of_islands)
intersections = find_intersections(list_of_islands)
set_edges_of_island = find_set_edges_of_island(list_of_islands, connections)
conditions_of_island, conditions_of_brige = generate_conditions_of_island(
    list_of_islands, set_edges_of_island
)
fout = open("output.txt", "w")
for island in list_of_islands:
    name = (island[0], island[1])
    fout.write(str(island) + " : " + str(conditions_of_island[name]) + "\n")
    fout.write("\n")
    
for bridge in connections:
    fout.write(str(bridge) + " : " + str(conditions_of_brige[bridge]) + "\n")
    fout.write("\n")
fout.close()
