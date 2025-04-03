import time

def parse_string_to_tuple_list(string_list):
    tuple_list = []
    for item in string_list:
        tuple_list.append(eval(item))
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

def unit_propagate(cnf, assignment):
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
    literals = {lit for clause in cnf for lit in clause}
    pure_literals = {lit for lit in literals if -lit not in literals}

    for literal in pure_literals:
        cnf = [clause for clause in cnf if literal not in clause]
        assignment[abs(literal)] = literal > 0

    return cnf, assignment

def dpll(cnf, variable_map, island, assignment={}):
    cnf, assignment = unit_propagate(cnf, assignment)
    cnf, assignment = pure_literal_elimination(cnf, assignment)
    if not cnf: 
        return True, assignment
    for clause in cnf:
        if len(clause) == 0:
            return False, None
    
    variable = abs(cnf[0][0])
    
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
            f.write(f"Time: {round((end_time - start_time)*1000)} miliseconds\n")
            for result in positive_vars:
                f.write(f"{result} ")
        return True
    else:
        with open(file_output, "w") as f:
            f.write("UNSAT\n")
        with open(analysis_file, "w") as f:
            f.write(f"Time: {round((end_time - start_time)*1000)} miliseconds\n")
        return False
