import heapq
import itertools
from typing import List, Dict, Set, Optional

def parse_clauses(filename: str) -> List[List[int]]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    clauses = []
    for line in lines:
        clause = list(map(int, line.strip().split()))
        clauses.append(clause)
    return clauses

def is_clause_satisfied(clause: List[int], assignment: Dict[int, bool]) -> bool:
    for literal in clause:
        var = abs(literal)
        value = assignment.get(var, None)
        if value is not None:
            if (literal > 0 and value) or (literal < 0 and not value):
                return True
    return False

def count_unsatisfied_clauses(cnf: List[List[int]], assignment: Dict[int, bool]) -> int:
    unsatisfied_count = 0
    for clause in cnf:
        if not is_clause_satisfied(clause, assignment):
            unsatisfied_count += 1
    return unsatisfied_count

def heuristic(assignment: Dict[int, bool], cnf: List[List[int]], all_vars: Set[int]) -> int:
    unassigned = len(all_vars - set(assignment.keys()))  # Convert keys to set
    unsatisfied = count_unsatisfied_clauses(cnf, assignment)
    return unassigned + 2 * unsatisfied

def next_literal(assignment: Dict[int, bool], cnf: List[List[int]], all_vars: Set[int]) -> Optional[int]:
    literal_exist = {}
    for clause in cnf:
        if not is_clause_satisfied(clause, assignment):
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    literal_exist[var] = literal_exist.get(var, 0) + 1
    
    if literal_exist:
        return max(literal_exist, key=literal_exist.get)
    unassigned = all_vars - set(assignment.keys())  # Convert keys to set
    return min(unassigned) if unassigned else None



def astar(cnf: List[List[int]], all_vars: Set[int]) -> Optional[Dict[int, bool]]:
    open_list = []
    closed_set = set()
    counter = itertools.count()

    initial_state = {}
    initial_h = heuristic(initial_state, cnf, all_vars)
    heapq.heappush(open_list, (initial_h, 0, next(counter), initial_state))

    while open_list:
        f_score, g_score, _, state = heapq.heappop(open_list)
    
        if all(is_clause_satisfied(clause, state) for clause in cnf):
            return state
        
        state_key = frozenset(state.items())
        if state_key in closed_set:
            continue
        closed_set.add(state_key)
        
        next_var = next_literal(state, cnf, all_vars)
        if next_var is None:
            continue

        for value in [True, False]:
            new_state = state.copy()
            new_state[next_var] = value

            new_g = g_score + 1
            new_h = heuristic(new_state, cnf, all_vars)
            new_f = new_g + new_h

            heapq.heappush(open_list, (new_f, new_g, next(counter), new_state))

    return None


if __name__ == "__main__":
    filename = "..//data//test.txt"  
    clauses = parse_clauses(filename)
    all_vars = {abs(literal) for clause in clauses for literal in clause}

    result = astar(clauses, all_vars)
    
    if result is None:
        print("No satisfying assignment found.")
    else:
        print("Available assignment:")
        for var, value in sorted(result.items()):
            print(f"{'-' if not value else ''}{var} ", end="")
