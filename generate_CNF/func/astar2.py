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

def check_clause_satisfaction(clause: List[int], assignment: Dict[int, bool]) -> bool:
    for literal in clause:
        var = abs(literal)
        value = assignment.get(var, None)
        if value is not None:
            if (literal > 0 and value) or (literal < 0 and not value):
                return True
    return False

def count_unsatisfied_clauses(assignment: Dict[int, bool], formula: List[List[int]], cache: Dict[frozenset, int]) -> int:
    key = frozenset(assignment.items())
    if key in cache:
        return cache[key]
    
    unsatisfied_count = sum(1 for clause in formula if not check_clause_satisfaction(clause, assignment))
    cache[key] = unsatisfied_count
    return unsatisfied_count

def calculate_heuristic(assignment: Dict[int, bool], formula: List[List[int]], all_variables: Set[int], cache: Dict[frozenset, int]) -> int:
    remaining_vars = len(all_variables - set(assignment.keys()))
    unsatisfied_clauses = count_unsatisfied_clauses(assignment, formula, cache)
    return remaining_vars + 2 * unsatisfied_clauses

def verify_assignment_validity(assignment: Dict[int, bool], formula: List[List[int]]) -> bool:
    for clause in formula:
        if all(abs(literal) in assignment for literal in clause):
            if not any((literal > 0 and assignment[abs(literal)] == True) or (literal < 0 and assignment[abs(literal)] == False)
                       for literal in clause):
                return False
    return True

def next_literal(assignment: Dict[int, bool], cnf: List[List[int]], all_vars: Set[int]) -> Optional[int]:
    literal_exist = {}
    for clause in cnf:
        if not check_clause_satisfaction(clause, assignment):
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    literal_exist[var] = literal_exist.get(var, 0) + 1
    
    if literal_exist:
        return max(literal_exist, key=literal_exist.get)
    unassigned = all_vars - set(assignment.keys()) 
    return min(unassigned) if unassigned else None


def astar(formula: List[List[int]], all_variables: Set[int]) -> Optional[Dict[int, bool]]:
    priority_queue = []
    visited_states = set()
    unsatisfied_cache = {}
    tie_breaker = itertools.count()

    initial_assignment = {}
    initial_h = calculate_heuristic(initial_assignment, formula, all_variables, unsatisfied_cache)
    heapq.heappush(priority_queue, (initial_h, 0, next(tie_breaker), initial_assignment))

    while priority_queue:
        f_score, g_score, _, current_assignment = heapq.heappop(priority_queue)
        
        if all(check_clause_satisfaction(clause, current_assignment) for clause in formula):
            return current_assignment
        
        state_key = frozenset(current_assignment.items())
        if state_key in visited_states:
            continue
        visited_states.add(state_key)
        
        next_variable = next_literal(current_assignment, formula, all_variables)
        if next_variable is None:
            continue

        for decision in [True, False]:
            new_assignment = current_assignment.copy()
            new_assignment[next_variable] = decision
            
            if not verify_assignment_validity(new_assignment, formula):
                continue
            
            new_g = g_score + 1
            new_h = calculate_heuristic(new_assignment, formula, all_variables, unsatisfied_cache)
            new_f = new_g + new_h

            heapq.heappush(priority_queue, (new_f, new_g, next(tie_breaker), new_assignment))

    return None


if __name__ == "__main__":
    filename = "..//data//cnf-06.txt"  
    clauses = parse_clauses(filename)
    all_vars = {abs(literal) for clause in clauses for literal in clause}

    result = astar(clauses, all_vars)
    
    if result is None:
        print("No satisfying assignment found.")
    else:
        print("Available assignment:")
        for var, value in sorted(result.items()):
            print(f"{'-' if not value else ''}{var} ", end="")


