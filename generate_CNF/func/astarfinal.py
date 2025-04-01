import heapq
import itertools
from typing import List, Dict, Set, Optional

def parse_clauses(filename: str) -> List[List[int]]:
    with open(filename, 'r') as f:
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

def count_unsatisfied_clauses(assignment: Dict[int, bool], formula: List[List[int]], 
                               cache: Dict[frozenset, int]) -> int:
    key = frozenset(assignment.items())
    if key in cache:
        return cache[key]
    unsatisfied_count = sum(1 for clause in formula if not check_clause_satisfaction(clause, assignment))
    cache[key] = unsatisfied_count
    return unsatisfied_count

def calculate_heuristic(assignment: Dict[int, bool], formula: List[List[int]], 
                        all_variables: Set[int], cache: Dict[frozenset, int]) -> int:
    remaining_vars = len(all_variables - set(assignment.keys()))
    unsatisfied = count_unsatisfied_clauses(assignment, formula, cache)
    return remaining_vars + 2 * unsatisfied

def verify_assignment_validity(assignment: Dict[int, bool], formula: List[List[int]]) -> bool:
    for clause in formula:
        if all(abs(literal) in assignment for literal in clause):
            if not any((literal > 0 and assignment[abs(literal)] == True) or 
                       (literal < 0 and assignment[abs(literal)] == False)
                       for literal in clause):
                return False
    return True

def next_literal(assignment: Dict[int, bool], formula: List[List[int]], all_vars: Set[int]) -> Optional[int]:
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

def unit_propagation(assignment: Dict[int, bool], formula: List[List[int]]) -> Dict[int, bool]:
    new_assignment = assignment.copy()
    changed = True
    while changed:
        changed = False
        for clause in formula:
            if check_clause_satisfaction(clause, new_assignment):
                continue
            unassigned_literals = [lit for lit in clause if abs(lit) not in new_assignment]
            if len(unassigned_literals) == 1:
                forced_literal = unassigned_literals[0]
                forced_var = abs(forced_literal)
                forced_value = True if forced_literal > 0 else False
                if forced_var not in new_assignment:
                    new_assignment[forced_var] = forced_value
                    changed = True
    return new_assignment

def pure_literal_elimination(assignment: Dict[int, bool], formula: List[List[int]]) -> Dict[int, bool]:
    new_assignment = assignment.copy()
    literal_occurrences = {}
    # For each clause that is not yet satisfied, record the polarity of each unassigned literal.
    for clause in formula:
        if check_clause_satisfaction(clause, new_assignment):
            continue
        for literal in clause:
            var = abs(literal)
            if var not in new_assignment:
                literal_occurrences.setdefault(var, set()).add(1 if literal > 0 else -1)
    # If a variable appears only with one polarity, assign it accordingly.
    for var, signs in literal_occurrences.items():
        if len(signs) == 1:
            new_assignment[var] = True if 1 in signs else False
    return new_assignment

def conflict_analysis(assignment: Dict[int, bool], formula: List[List[int]]) -> List[int]:
    """
    A very naive conflict analysis: returns the first fully-assigned clause that is unsatisfied.
    In a full CDCL, this would analyze an implication graph.
    """
    for clause in formula:
        if all(abs(lit) in assignment for lit in clause) and not check_clause_satisfaction(clause, assignment):
            return clause
    return []

def astar(formula: List[List[int]], all_variables: Set[int]) -> Optional[Dict[int, bool]]:
    priority_queue = []
    closed_set = set()
    unsatisfied_cache = {}
    tie_breaker = itertools.count()

    initial_assignment = {}
    # Apply unit propagation and pure literal elimination on the initial state.
    initial_assignment = unit_propagation(initial_assignment, formula)
    initial_assignment = pure_literal_elimination(initial_assignment, formula)
    initial_h = calculate_heuristic(initial_assignment, formula, all_variables, unsatisfied_cache)
    heapq.heappush(priority_queue, (initial_h, 0, next(tie_breaker), initial_assignment))

    while priority_queue:
        f_score, g_score, _, assignment = heapq.heappop(priority_queue)
        
        # Goal test: if all clauses are satisfied and all variables assigned, return solution.
        if all(check_clause_satisfaction(clause, assignment) for clause in formula) and \
           all(var in assignment for var in all_variables):
            return assignment
        
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
            # Apply unit propagation and pure literal elimination after the decision.
            new_assignment = unit_propagation(new_assignment, formula)
            new_assignment = pure_literal_elimination(new_assignment, formula)
            
            if not verify_assignment_validity(new_assignment, formula):
                # Conflict encountered; perform conflict analysis and learn a clause.
                learned_clause = conflict_analysis(new_assignment, formula)
                if learned_clause:
                    # Add the learned clause to the formula.
                    formula.append(learned_clause)
                    # Clear cache as formula has changed.
                    unsatisfied_cache.clear()
                continue
            
            new_g = g_score + 1
            new_h = calculate_heuristic(new_assignment, formula, all_variables, unsatisfied_cache)
            new_f = new_g + new_h
            
            heapq.heappush(priority_queue, (new_f, new_g, next(tie_breaker), new_assignment))
    
    return None

def solve_sat(filename: str) -> Optional[Dict[int, bool]]:
    cnf = parse_clauses(filename)
    all_vars = {abs(literal) for clause in cnf for literal in clause}
    return astar(cnf, all_vars)

if __name__ == "__main__":
    filename = "..//data//cnf-09.txt" 
    result = solve_sat(filename)
    
    if result is None:
        print("No satisfying assignment found.")
    else:
        print("Available assignment:")
        for var, value in sorted(result.items()):
            print(f"{'-' if not value else ''}{var} ", end="")
