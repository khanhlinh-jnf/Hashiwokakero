import heapq
import itertools
from typing import List, Dict, Optional, Set

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

def update_clause_status(clause: List[int], assignment: Dict[int, bool]) -> (bool, bool):
    satisfied = False
    undecided = False
    for literal in clause:
        var = abs(literal)
        value = assignment.get(var, None)
        if value is not None:
            if (literal > 0 and value) or (literal < 0 and not value):
                satisfied = True
                break
        else:
            undecided = True
    return satisfied, undecided

def is_satisfied(clause_status: Dict[int, bool], assignment: Dict[int, bool], clauses: List[List[int]]) -> bool:
    if not all(clause_status.values()):
        return False
    all_vars = {abs(literal) for clause in clauses for literal in clause}
    return all(var in assignment for var in all_vars)

def get_related_clauses(clauses: List[List[int]], var: int) -> List[int]:
    related = []
    for idx, clause in enumerate(clauses):
        if any(abs(literal) == var for literal in clause):
            related.append(idx)
    return related

def heuristic(clauses: List[List[int]], assignment: Dict[int, bool]) -> int:
    unsat = 0
    for clause in clauses:
        if not is_clause_satisfied(clause, assignment):
            unsat += 1
    return unsat

def astar_sat(clauses: List[List[int]]) -> Optional[Dict[int, bool]]:
    all_vars: Set[int] = {abs(literal) for clause in clauses for literal in clause}
    initial_assignment: Dict[int, bool] = {}
    clause_status = {}
    for idx, clause in enumerate(clauses):
        sat, und = update_clause_status(clause, initial_assignment)
        clause_status[idx] = sat or und

    h = heuristic(clauses, initial_assignment)
    g = len(initial_assignment)
    f = g + h

    counter = itertools.count()
    heap = []
    heapq.heappush(heap, (f, g, next(counter), initial_assignment, clause_status))

    while heap:
        current_f, current_g, _, assignment, clause_status = heapq.heappop(heap)

        if is_satisfied(clause_status, assignment, clauses):
            return assignment

        var = next((v for v in all_vars if v not in assignment), None)
        if var is None:
            continue

        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = value

            new_clause_status = clause_status.copy()
            related = get_related_clauses(clauses, var)
            for idx in related:
                sat, und = update_clause_status(clauses[idx], new_assignment)
                new_clause_status[idx] = sat or und

            new_g = len(new_assignment)
            new_h = heuristic(clauses, new_assignment)
            new_f = new_g + new_h

            heapq.heappush(heap, (new_f, new_g, next(counter), new_assignment, new_clause_status))

    return None

def solve_sat(filename: str) -> Optional[Dict[int, bool]]:
    clauses = parse_clauses(filename)
    return astar_sat(clauses)

if __name__ == "__main__":
    filename = "..//data//cnf-01.txt"  
    result = solve_sat(filename)
    
    if result is None:
        print("No satisfying assignment found.")
    else:
        print("Satisfying assignment:")
        for var, value in result.items():
            print(f"{'-' if not value else ''}{var} ", end="")
