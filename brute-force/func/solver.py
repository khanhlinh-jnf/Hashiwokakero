from itertools import combinations
import time


def parse_string_to_tuple_list(string_list):
    tuple_list = []
    for item in string_list:
        tuple_list.append(eval(item))  # Chuyển đổi chuỗi thành tuple
    return tuple_list


def read_matrix(file_path):
    with open(file_path, "r") as filein:
        return [[int(col) for col in line.split(",")] for line in filein]


def find_islands(matrix):
    return [
        (r, c, matrix[r][c])
        for r in range(len(matrix))
        for c in range(len(matrix[0]))
        if matrix[r][c] != 0
    ]


def load_variable_mapping(dict_file):
    variable_map = {}
    with open(dict_file, "r") as f:
        for line in f:
            key, value = line.strip().split(":", 1)
            variable_map[int(key)] = value.strip()
    return variable_map


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

    return len({find(node[:2]) for node in nodes}) == 1


def is_complete(clauses, value_bool_of_literal):
    return heuristic(clauses, value_bool_of_literal) == 0


def heuristic(clauses, value_bool_of_literal):
    sum = 0
    for clause in clauses:
        tmp = 0
        for literal in clause:
            tmp += value_bool_of_literal[literal]
        if tmp == 0:
            sum += 1
    return sum


def update_value_bool_of_literal(value_bool_of_literal, index, value):
    value_bool_of_literal[index] = value
    value_bool_of_literal[-index] = 1 - value


def brute_force(input_file, file_condition, file_dict, file_output, analysis_file):
    clauses = []
    islands = find_islands(read_matrix(input_file))

    with open(file_condition, "r") as f:
        clauses = [list(map(int, line.strip().split())) for line in f]

    variable_map = load_variable_mapping(file_dict)
    num_variables = len(variable_map)
    arr = [i for i in range(1, num_variables+1)]
    value_bool_of_literal = {}
    for i in range(-num_variables, num_variables + 1):
        value_bool_of_literal[i] = 0
    for i in range(1, num_variables + 1):
        update_value_bool_of_literal(value_bool_of_literal, i, 1)
        
    start_time = time.time()

    for i in range(1, num_variables + 1):
        for j in combinations(arr, i):
            for k in j:
                update_value_bool_of_literal(value_bool_of_literal, k, 0)
            if is_complete(clauses, value_bool_of_literal):
                positive_vars = [var for var in range(1, num_variables+1) if value_bool_of_literal[var]]
                edges = [variable_map[var] for var in positive_vars if variable_map[var][-2] == ")"]
                edges = parse_string_to_tuple_list(edges)
                if is_connected(edges, islands):
                    with open(file_output, "w") as f:
                        for result in positive_vars:
                            if variable_map[result][-2] != ")":
                                f.write(f"{variable_map[result]}\n")
                    with open(analysis_file, "w") as f:
                        f.write(f"Time: {round(time.time() - start_time,2)} seconds\n")
                        for result in positive_vars:
                            f.write(f"{result} ")
                    return
            for k in j:
                update_value_bool_of_literal(value_bool_of_literal, k, 1)
    with open(file_output, "w") as f:
        f.write("UNSAT\n")
    with open(analysis_file, "w") as f:
        f.write(f"Time: {time.time() - start_time}")
