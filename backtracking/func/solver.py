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


def find_max(count):
    max = 0
    for i in range(1, len(count)):
        if count[i] > count[max]:
            max = i
    return max


def update_value_bool_of_literal(value_bool_of_literal, index, value):
    value_bool_of_literal[index] = value
    value_bool_of_literal[-index] = 1 - value


def unit_propagate(cnf, assignment):
    """Lan truyền giá trị đơn (Unit Propagation)"""
    while True:
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if not unit_clauses:
            break

        for literal in unit_clauses:
            cnf = [clause for clause in cnf if literal not in clause]
            for clause in cnf:
                if -literal in clause:
                    clause.remove(-literal)
            assignment[abs(literal)] = literal > 0

    return cnf, assignment


def pure_literal_elimination(cnf, assignment):
    """Loại bỏ biến đơn thuần (Pure Literal Elimination)"""
    literals = {lit for clause in cnf for lit in clause}
    pure_literals = {lit for lit in literals if -lit not in literals}

    for literal in pure_literals:
        cnf = [clause for clause in cnf if literal not in clause]
        assignment[abs(literal)] = literal > 0

    return cnf, assignment


def dpll(cnf, variable_map, island, assignment={}):
    """Thuật toán DPLL"""
    cnf, assignment = unit_propagate(cnf, assignment)
    cnf, assignment = pure_literal_elimination(cnf, assignment)

    if not cnf:  # Nếu CNF rỗng -> thỏa mãn
        return True, assignment
    if any(not clause for clause in cnf):  # Nếu có mệnh đề rỗng -> mâu thuẫn
        return False, None

    # Chọn biến chưa gán
    variable = abs(next(iter(cnf[0])))

    # Thử gán True
    sat, result = dpll(
        [
            [lit for lit in clause if lit != -variable]
            for clause in cnf
            if variable not in clause
        ],
        variable_map,
        island,
        {**assignment, variable: True},
    )
    if sat:
        positive_vars = [var for var in range(1, len(variable_map) + 1) if result[var]]
        edges = [
            variable_map[var] for var in positive_vars if variable_map[var][-2] == ")"
        ]
        edges = parse_string_to_tuple_list(edges)
        if is_connected(edges, island):
            return True, result

    # Thử gán False
    sat, result = dpll(
        [
            [lit for lit in clause if lit != variable]
            for clause in cnf
            if -variable not in clause
        ],
        variable_map,
        island,
        {**assignment, variable: False},
    )
    if sat:
        positive_vars = [var for var in range(1, len(variable_map) + 1) if result[var]]
        edges = [
            variable_map[var] for var in positive_vars if variable_map[var][-2] == ")"
        ]
        edges = parse_string_to_tuple_list(edges)
        if is_connected(edges, island):
            return True, result

    return False, None


def solve_cnf(input_file, file_condition, file_dict, file_output, analysis_file):
    clauses = []
    islands = find_islands(read_matrix(input_file))

    with open(file_condition, "r") as f:
        clauses = [list(map(int, line.strip().split())) for line in f]

    variable_map = load_variable_mapping(file_dict)
    num_variables = len(variable_map)
    arr = [i for i in range(1, num_variables + 1)]
    value_bool_of_literal = {}
    for i in range(-num_variables, num_variables + 1):
        value_bool_of_literal[i] = 0
    for i in range(1, num_variables + 1):
        update_value_bool_of_literal(value_bool_of_literal, i, 1)

    start_time = time.time()
    sat, result = dpll(clauses, variable_map, islands)
    end_time = time.time()
    if sat:
        positive_vars = [var for var in range(1, num_variables + 1) if result[var]]
        with open(file_output, "w") as f:
            for result in positive_vars:
                if variable_map[result][-2] != ")":
                    f.write(f"{variable_map[result]}\n")
        with open(analysis_file, "w") as f:
            f.write(f"Time: {round(end_time - start_time,2)} seconds\n")
            for result in positive_vars:
                f.write(f"{result} ")
    else:
        with open(file_output, "w") as f:
            f.write("UNSAT\n")
        with open(analysis_file, "w") as f:
            f.write(f"Time: {time.time() - start_time}")
