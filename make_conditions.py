from itertools import combinations


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
                connections.append((points[i], points[j]))
                flagRow = False
            if c1 == c2 and flagCol:
                connections.append((points[i], points[j]))
                flagCol = False
    return connections


def find_intersections(points):
    connections = find_connections(points)
    intersections = []
    for i in range(len(connections)):
        for j in range(i + 1, len(connections)):
            (r1, c1, v1), (r2, c2, v2) = connections[i]
            (r3, c3, v3), (r4, c4, v4) = connections[j]
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
        res[point] = []
        for connection in connections:
            if point in connection:
                res[point].append(connection)
    return res


def generate_conditions_of_island_and_same_bridge(list_island, set_edges_of_island):
    res_cdt_island = {}
    res_cdt_bridge = {}
    list_of_bridge = {}
    for island in list_island:
        res_cdt_island[island] = {}
        list_of_bridge[island] = []
        for edge in set_edges_of_island[island]:
            condition1 = (edge, 1)
            res_cdt_island[island][condition1] = False
            list_of_bridge[island].append(condition1)
            if edge[0][2] != 1 and edge[1][2] != 1:
                condition2 = (edge, 2)
                res_cdt_island[island][condition2] = False
                list_of_bridge[island].append(condition2)
                res_cdt_bridge[edge] = {}
                res_cdt_bridge[edge][condition1] = False
                res_cdt_bridge[edge][condition2] = False
    return res_cdt_island, res_cdt_bridge, list_of_bridge


def generate_conditions_of_intersection_bridge(list_intersections):
    res_cdt_bridge = {}
    for intersection in list_intersections:
        res_cdt_bridge[intersection] = {}
        res_cdt_bridge[intersection][(intersection[0])] = False
        res_cdt_bridge[intersection][(intersection[1])] = False
    return res_cdt_bridge


def find_subsets_with_sum_k(data, k):
    n = len(data)
    valid_subsets = []
    for size in range(1, n + 1):
        for subset in combinations(data, size):
            total_weight = sum(item[1] for item in subset)
            info_set = set(item[0] for item in subset)
            if len(info_set) == len(subset) and total_weight == k:
                valid_subsets.append(subset)
    return valid_subsets


def generate_conditions_of_sum_bridge_of_island(list_of_island, list_of_bridge):
    res = {}
    for island in list_of_island:
        res[island] = {}
        list_case = find_subsets_with_sum_k(list_of_bridge[island], island[2])
        i = 0
        for case in list_case:
            res[island][i] = {}
            for bridge in case:
                res[island][i][bridge] = False
            i += 1
    return res


def is_valid(edges, intersections):
    for edge1, edge2 in intersections:
        if edge1 in edges and edge2 in edges:
            return False
    return True


def is_connected(edges, nodes):
    parent = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    for node in nodes:
        parent[node[:2]] = node[:2]

    for edge in edges:
        union(edge[0][:2], edge[1][:2])

    roots = {find(node[:2]) for node in nodes}
    return len(roots) == 1


def find_valid_connections(islands, connections, intersections):
    valid_connections = []
    for r in range(1, len(connections) + 1):
        for edges in combinations(connections, r):
            if is_connected(edges, islands) and is_valid(edges, intersections):
                valid_connections.append(edges)
    return valid_connections


def generate_conditions_of_valid_connection(valid_connections):
    res = {}
    i = 0
    for connection in valid_connections:
        res[i] = {}
        for edge in connection:
            res[i][edge] = False
        i += 1
    return res


def find_list_of_variables(
    condition_of_island_sum_bridge,
    condition_of_same_brige,
    condition_of_intersection_bridge,
    condition_of_valid_connection,
):
    list_of_variables = set()
    res1 = {}
    res2 = {}
    i = 1
    for island in condition_of_island_sum_bridge:
        for case in condition_of_island_sum_bridge[island]:
            for bridge in condition_of_island_sum_bridge[island][case]:
                list_of_variables.add(bridge)
    for bridge in condition_of_same_brige:
        for case in condition_of_same_brige[bridge]:
            list_of_variables.add(case)
    for intersection in condition_of_intersection_bridge:
        for case in condition_of_intersection_bridge[intersection]:
            list_of_variables.add(case)
    for connection in condition_of_valid_connection:
        for case in condition_of_valid_connection[connection]:
            list_of_variables.add(case)
    for variable in list_of_variables:
        res1[variable] = i
        res2[i] = variable
        i += 1
    return res1, res2, list_of_variables


def generate_conditions_of_bridge_equivalent(list_of_bridge):
    res = {}
    for bridge in list_of_bridge:
        res[bridge] = {}
        v1, v2 = bridge[0][2], bridge[1][2]
        name1 = (bridge, 1)
        name2 = (bridge, 2)
        if v1 != 1 and v2 != 1:
            res[bridge][0] = {bridge: True, name1: False, name2: False}
            res[bridge][1] = {bridge: False, name1: True}
            res[bridge][2] = {bridge: False, name2: True}
        else:
            res[bridge][0] = {bridge: True, name1: False}
            res[bridge][1] = {bridge: False, name1: True}
    return res

def main():
    matrix = read_matrix("input.txt")
    list_of_islands = find_islands(matrix)
    connections = find_connections(list_of_islands)
    intersections = find_intersections(list_of_islands)
    set_edges_of_island = find_set_edges_of_island(list_of_islands, connections)
    conditions_of_island, conditions_of_same_brige, list_bridge_of_island = (
        generate_conditions_of_island_and_same_bridge(list_of_islands, set_edges_of_island)
    )
    conditions_of_intersection_bridge = generate_conditions_of_intersection_bridge(
        intersections
    )
    conditions_of_island_sum_bridge = generate_conditions_of_sum_bridge_of_island(
        list_of_islands, list_bridge_of_island
    )
    valid_connections = find_valid_connections(list_of_islands, connections, intersections)
    conditions_of_valid_connection = generate_conditions_of_valid_connection(
        valid_connections
    )
    conditions_of_bridge_equivalent = generate_conditions_of_bridge_equivalent(connections)

    fout = open("output.txt", "w")
    cout = open("conditions.txt", "w")
    fout.write("List of variables: \n")
    dict_of_variables,convert_dict_of_variables, set_of_variables = find_list_of_variables(
        conditions_of_island_sum_bridge,
        conditions_of_same_brige,
        conditions_of_intersection_bridge,
        conditions_of_valid_connection,
    )

    dout = open("dict_of_variables.txt", "w")
    for x in convert_dict_of_variables:
        dout.write(str(x) + " : " + str(convert_dict_of_variables[x]) + "\n")
    dout.close()

    for x in dict_of_variables:
        fout.write(str(x) + " : " + str(dict_of_variables[x]) + "\n")
    fout.write("\n")

    fout.write("List of condition of islands: DNF \n")
    for x in list_of_islands:
        fout.write(str(x) + " :\n")
        for y in conditions_of_island_sum_bridge[x]:
            fout.write("(")
            cout.write("(")
            for z in conditions_of_island_sum_bridge[x][y]:
                fout.write(str(dict_of_variables[z]))
                cout.write(str(dict_of_variables[z]))
                if z != list(conditions_of_island_sum_bridge[x][y].keys())[-1]:
                    fout.write(" and ")
                    cout.write("&")
            fout.write(")")
            cout.write(")")
            if y != list(conditions_of_island_sum_bridge[x].keys())[-1]:
                fout.write(" or ")
                cout.write("| ")
            else:
                fout.write("\n")
                cout.write("\n")
        fout.write("\n")

    fout.write("List of condition of islands (only one sum): \n")
    for x in conditions_of_island_sum_bridge:
        fout.write(str(x) + " :\n")
        for i in range(len(conditions_of_island_sum_bridge[x])):
            for j in range(i+1, len(conditions_of_island_sum_bridge[x])):
                fout.write("(")
                for y in conditions_of_island_sum_bridge[x][i]:
                    fout.write(f"-{str(dict_of_variables[y])}")
                    cout.write(f"-{str(dict_of_variables[y])}")
                    if y != list(conditions_of_island_sum_bridge[x][i].keys())[-1]:
                        fout.write(" or ")
                        cout.write("| ")
                fout.write(")")
                fout.write(" or ")
                cout.write("| ")
                fout.write("(")
                for y in conditions_of_island_sum_bridge[x][j]:
                    fout.write(f"-{str(dict_of_variables[y])}")
                    cout.write(f"-{str(dict_of_variables[y])}")
                    if y != list(conditions_of_island_sum_bridge[x][j].keys())[-1]:
                        fout.write(" or ")
                        cout.write("| ")
                    else:
                        cout.write("\n")
                fout.write(")\n")
        fout.write("\n")
    fout.write("\n")

    fout.write("List of condition limit bridge: Not A or Not B \n")
    for x in conditions_of_same_brige:
        fout.write(str(x) + " :\n")
        for y in conditions_of_same_brige[x]:
            fout.write("-" + str(dict_of_variables[y]))
            cout.write("-" + str(dict_of_variables[y]))
            if y != list(conditions_of_same_brige[x].keys())[-1]:
                fout.write(" or ")
                cout.write("| ")
            else:
                fout.write("\n")
                cout.write("\n")
        fout.write("\n")

    fout.write("List of condition of intersections: Not A or Not B \n")
    for x in conditions_of_intersection_bridge:
        fout.write(str(x) + " :\n")
        for y in conditions_of_intersection_bridge[x]:
            fout.write("-" + str(dict_of_variables[y]))
            cout.write("-" + str(dict_of_variables[y]))
            if y != list(conditions_of_intersection_bridge[x].keys())[-1]:
                fout.write(" or ")
                cout.write("| ")
            else:
                fout.write("\n")
                cout.write("\n")
        fout.write("\n")

    fout.write("List of condition of bridge equivalent: CNF \n")
    for x in conditions_of_bridge_equivalent:
        fout.write(str(x) + " :\n")
        for y in conditions_of_bridge_equivalent[x]:
            fout.write("(")
            for z in conditions_of_bridge_equivalent[x][y]:
                if not conditions_of_bridge_equivalent[x][y][z]:
                    fout.write(str(dict_of_variables[z]))
                    cout.write(str(dict_of_variables[z]))
                else:
                    fout.write("-" + str(dict_of_variables[z]))
                    cout.write("-" + str(dict_of_variables[z]))
                if z != list(conditions_of_bridge_equivalent[x][y].keys())[-1]:
                    fout.write(" or ")
                    cout.write("| ")
            fout.write(")")
            cout.write("\n")
            if y != list(conditions_of_bridge_equivalent[x].keys())[-1]:
                fout.write(" and ")
            else:
                fout.write("\n")
        fout.write("\n")

    fout.write("List of valid connections: DNF \n")
    for x in conditions_of_valid_connection:
        fout.write("(")
        cout.write("(")
        for y in conditions_of_valid_connection[x]:
            fout.write(str(dict_of_variables[y]))
            cout.write(str(dict_of_variables[y]))
            if y != list(conditions_of_valid_connection[x].keys())[-1]:
                fout.write(" and ")
                cout.write("&")
        fout.write(")")
        cout.write(")")
        if x != list(conditions_of_valid_connection.keys())[-1]:
            fout.write(" or ")
            cout.write("| ")
        else:
            fout.write("\n")
            cout.write("\n")

    fout.close()

main()
