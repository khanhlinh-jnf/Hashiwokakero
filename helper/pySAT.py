from pysat.solvers import Solver
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
    return [(r, c, matrix[r][c]) for r in range(len(matrix)) for c in range(len(matrix[0])) if matrix[r][c] != 0]

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


def solve_cnf(input_file, file_condition, file_dict, file_output, analysis_file):
    clauses = []
    islands = find_islands(read_matrix(input_file))

    with open(file_condition, "r") as f:
        clauses = [list(map(int, line.strip().split())) for line in f]

    variable_map = load_variable_mapping(file_dict)
    solver = Solver(name="g3")

    for clause in clauses:
        solver.add_clause(clause)

    start_time = time.perf_counter()
    while solver.solve():
        model = solver.get_model()
        positive_vars = [var for var in model if var > 0]
        edges = [variable_map[var] for var in positive_vars if variable_map[var][-2] == ")"]
        edges = parse_string_to_tuple_list(edges)

        if is_connected(edges, islands):
            with open(file_output, "w") as f:
                for result in positive_vars:
                    if variable_map[result][-2] != ")":
                        f.write(f"{variable_map[result]}\n")
            with open(analysis_file, "w") as f:
                f.write(
                    f"Time: {(time.perf_counter() - start_time)*1000:.4f} miliseconds\n"
                )
                for result in positive_vars:
                    f.write(f"{result} ")
            solver.delete()
            return True

        solver.add_clause([-var for var in model]) 

    with open(file_output, "w") as f:
        f.write("UNSAT\n")
    with open(analysis_file, "w") as f:
        f.write(f"Time: {(time.perf_counter() - start_time)*1000:.4f} miliseconds\n")

    solver.delete()
    return False
