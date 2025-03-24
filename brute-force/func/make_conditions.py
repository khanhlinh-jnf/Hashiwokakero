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


def find_subsets_with_greater_k(data, k):
    n = len(data)
    valid_subsets = []
    for size in range(1, n + 1):
        for subset in combinations(data, size):
            total_weight = sum(item[1] for item in subset)
            info_set = set(item[0] for item in subset)
            if len(info_set) == len(subset) and total_weight > k:
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


def generate_conditions_of_sum_bridge_unvalid_of_island(list_of_island, list_of_bridge):
    res = {}
    for island in list_of_island:
        res[island] = {}
        list_case = find_subsets_with_greater_k(list_of_bridge[island], island[2])
        i = 0
        for case in list_case:
            res[island][i] = {}
            for bridge in case:
                res[island][i][bridge] = False
            i += 1
    return res


def find_list_of_variables(
    condition_of_island_sum_bridge,
    condition_of_same_brige,
    condition_of_intersection_bridge,
    connections,
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
    for connection in connections:
        list_of_variables.add(connection)
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


def creat_conditions_file(input_file, conditions_file, dict_of_variables_file):
    matrix = read_matrix(input_file)
    list_of_islands = find_islands(matrix)
    connections = find_connections(list_of_islands)
    intersections = find_intersections(list_of_islands)
    set_edges_of_island = find_set_edges_of_island(list_of_islands, connections)
    conditions_of_island, conditions_of_same_brige, list_bridge_of_island = (
        generate_conditions_of_island_and_same_bridge(
            list_of_islands, set_edges_of_island
        )
    )
    conditions_of_intersection_bridge = generate_conditions_of_intersection_bridge(
        intersections
    )
    conditions_of_island_sum_bridge = generate_conditions_of_sum_bridge_of_island(
        list_of_islands, list_bridge_of_island
    )
    conditions_of_island_sum_bridge_unvalid = (
        generate_conditions_of_sum_bridge_unvalid_of_island(
            list_of_islands, list_bridge_of_island
        )
    )
    conditions_of_bridge_equivalent = generate_conditions_of_bridge_equivalent(
        connections
    )

    cout = open(conditions_file, "w")
    dict_of_variables, convert_dict_of_variables, set_of_variables = (
        find_list_of_variables(
            conditions_of_island_sum_bridge,
            conditions_of_same_brige,
            conditions_of_intersection_bridge,
            connections,
        )
    )
    dout = open(dict_of_variables_file, "w")
    for x in convert_dict_of_variables:
        dout.write(str(x) + " : " + str(convert_dict_of_variables[x]) + "\n")
    dout.close()

    for x in list_of_islands:
        for y in conditions_of_island_sum_bridge[x]:
            cout.write("(")
            for z in conditions_of_island_sum_bridge[x][y]:
                cout.write(str(dict_of_variables[z]))
                if z != list(conditions_of_island_sum_bridge[x][y].keys())[-1]:
                    cout.write("& ")
            cout.write(")")
            if y != list(conditions_of_island_sum_bridge[x].keys())[-1]:
                cout.write("| ")
            else:
                cout.write("\n")

    for x in list_of_islands:
        for y in conditions_of_island_sum_bridge_unvalid[x]:
            for z in conditions_of_island_sum_bridge_unvalid[x][y]:
                cout.write("-" + str(dict_of_variables[z]))
                if z != list(conditions_of_island_sum_bridge_unvalid[x][y].keys())[-1]:
                    cout.write("| ")
                else:
                    cout.write("\n")

    for x in conditions_of_same_brige:
        for y in conditions_of_same_brige[x]:
            cout.write("-" + str(dict_of_variables[y]))
            if y != list(conditions_of_same_brige[x].keys())[-1]:
                cout.write("| ")
            else:
                cout.write("\n")

    for x in conditions_of_intersection_bridge:
        for y in conditions_of_intersection_bridge[x]:
            cout.write("-" + str(dict_of_variables[y]))
            if y != list(conditions_of_intersection_bridge[x].keys())[-1]:
                cout.write("| ")
            else:
                cout.write("\n")

    for x in conditions_of_bridge_equivalent:
        for y in conditions_of_bridge_equivalent[x]:
            for z in conditions_of_bridge_equivalent[x][y]:
                if not conditions_of_bridge_equivalent[x][y][z]:
                    cout.write(str(dict_of_variables[z]))
                else:
                    cout.write("-" + str(dict_of_variables[z]))
                if z != list(conditions_of_bridge_equivalent[x][y].keys())[-1]:
                    cout.write("| ")
            cout.write("\n")
    cout.close()
    dout.close()
