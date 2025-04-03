import heapq
import itertools
from typing import List, Dict, Set, Optional
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

def parse_clauses(filename: str) -> List[List[int]]:
    with open(filename, "r") as f:
        lines = f.readlines()
    clauses = [list(map(int, line.strip().split())) for line in lines]
    return clauses


def check_clause_satisfaction(clause: List[int], assignment: Dict[int, bool]) -> bool:
    for literal in clause:
        var = abs(literal)
        value = assignment.get(var)
        if value is not None:
            if (literal > 0 and value) or (literal < 0 and not value):
                return True
    return False


def count_unsatisfied_clauses(
    assignment: Dict[int, bool], formula: List[List[int]], cache: Dict[frozenset, int]
) -> int:
    key = frozenset(assignment.items())
    if key in cache:
        return cache[key]
    unsatisfied_count = sum(
        1 for clause in formula if not check_clause_satisfaction(clause, assignment)
    )
    cache[key] = unsatisfied_count
    return unsatisfied_count


def calculate_heuristic(
    assignment: Dict[int, bool],
    formula: List[List[int]],
    all_variables: Set[int],
    cache: Dict[frozenset, int],
) -> int:
    remaining_vars = len(all_variables - set(assignment.keys()))
    unsatisfied = count_unsatisfied_clauses(assignment, formula, cache)
    return remaining_vars + 2 * unsatisfied


def verify_assignment_validity(
    assignment: Dict[int, bool], formula: List[List[int]]
) -> bool:
    for clause in formula:
        if all(abs(literal) in assignment for literal in clause):
            if not any(
                (literal > 0 and assignment[abs(literal)] == True)
                or (literal < 0 and assignment[abs(literal)] == False)
                for literal in clause
            ):
                return False
    return True


def next_literal(
    assignment: Dict[int, bool], formula: List[List[int]], all_vars: Set[int]
) -> Optional[int]:
    literal_counts = {}
    for clause in formula:
        if not check_clause_satisfaction(clause, assignment):
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    literal_counts[var] = literal_counts.get(var, 0) + 1
    if literal_counts:
        return max(literal_counts, key=literal_counts.get)
    unassigned = all_vars - set(assignment.keys())
    return min(unassigned) if unassigned else None


def unit_propagation(
    assignment: Dict[int, bool], formula: List[List[int]]
) -> Dict[int, bool]:
    new_assignment = assignment.copy()
    changed = True
    while changed:
        changed = False
        for clause in formula:
            if check_clause_satisfaction(clause, new_assignment):
                continue
            unassigned_literals = [
                lit for lit in clause if abs(lit) not in new_assignment
            ]
            if len(unassigned_literals) == 1:
                forced_literal = unassigned_literals[0]
                forced_var = abs(forced_literal)
                forced_value = True if forced_literal > 0 else False
                if forced_var not in new_assignment:
                    new_assignment[forced_var] = forced_value
                    changed = True
    return new_assignment


def pure_literal_elimination(
    assignment: Dict[int, bool], formula: List[List[int]]
) -> Dict[int, bool]:
    new_assignment = assignment.copy()
    literal_occurrences = {}
    for clause in formula:
        if check_clause_satisfaction(clause, new_assignment):
            continue
        for literal in clause:
            var = abs(literal)
            if var not in new_assignment:
                literal_occurrences.setdefault(var, set()).add(1 if literal > 0 else -1)
    for var, signs in literal_occurrences.items():
        if len(signs) == 1:
            new_assignment[var] = True if 1 in signs else False
    return new_assignment


def conflict_analysis(
    assignment: Dict[int, bool], formula: List[List[int]]
) -> List[int]:
    """
    A very naive conflict analysis: returns the first fully-assigned clause that is unsatisfied.
    In a full CDCL, this would analyze an implication graph.
    """
    for clause in formula:
        if all(
            abs(lit) in assignment for lit in clause
        ) and not check_clause_satisfaction(clause, assignment):
            return clause
    return []


def astar(input_file, file_condition, file_dict, file_output, analysis_file):
    formula = parse_clauses(file_condition)
    all_variables = {abs(literal) for clause in formula for literal in clause}
    priority_queue = []
    closed_set = set()
    unsatisfied_cache = {}
    tie_breaker = itertools.count()

    clauses = []
    islands = find_islands(read_matrix(input_file))
    with open(file_condition, "r") as f:
        clauses = [list(map(int, line.strip().split())) for line in f]
    variable_map = load_variable_mapping(file_dict)
    start_time = time.perf_counter()
    initial_assignment = {}
    initial_assignment = unit_propagation(initial_assignment, formula)
    initial_assignment = pure_literal_elimination(initial_assignment, formula)
    initial_h = calculate_heuristic(
        initial_assignment, formula, all_variables, unsatisfied_cache
    )
    heapq.heappush(
        priority_queue, (initial_h, 0, next(tie_breaker), initial_assignment)
    )

    while priority_queue:
        f_score, g_score, _, assignment = heapq.heappop(priority_queue)

        if all(
            check_clause_satisfaction(clause, assignment) for clause in formula
        ) and all(var in assignment for var in all_variables):
            positive_vars = [
                var for var in range(1, len(variable_map) + 1) if assignment[var]
            ]
            edges = [
                variable_map[var]
                for var in positive_vars
                if variable_map[var][-2] == ")"
            ]
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
                return True

        state_key = frozenset(assignment.items())
        if state_key in closed_set:
            continue
        closed_set.add(state_key)

        next_var = next_literal(assignment, formula, all_variables)
        if next_var is None:
            continue

        for decision in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[next_var] = decision
            new_assignment = unit_propagation(new_assignment, formula)
            new_assignment = pure_literal_elimination(new_assignment, formula)

            if not verify_assignment_validity(new_assignment, formula):
                learned_clause = conflict_analysis(new_assignment, formula)
                if learned_clause:
                    formula.append(learned_clause)
                    unsatisfied_cache.clear()
                continue

            new_g = g_score + 1
            new_h = calculate_heuristic(
                new_assignment, formula, all_variables, unsatisfied_cache
            )
            new_f = new_g + new_h

            heapq.heappush(
                priority_queue, (new_f, new_g, next(tie_breaker), new_assignment)
            )

    with open(file_output, "w") as f:
        f.write("UNSAT\n")
    with open(analysis_file, "w") as f:
        f.write(f"Time: {(time.perf_counter() - start_time)*1000:.4f} miliseconds\n")
    return False
