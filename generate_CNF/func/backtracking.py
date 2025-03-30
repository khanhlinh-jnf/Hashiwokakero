from typing import List, Dict, Optional, Set

def parse_clauses(filename: str) -> List[List[int]]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    clauses = []
    for line in lines:
        clause = list(map(int, line.strip().split()))
        clauses.append(clause)
    return clauses

def update_clause_status(clause: List[int], assignment: Dict[int, bool]) -> (bool, bool):
    satisfied = False
    undecided = False

    for literal in clause:
        var = abs(literal)
        value = assignment.get(var, None)

        if value is not None:
            if (literal > 0 and value is True) or (literal < 0 and value is False):
                satisfied = True
                break  
        else:
            undecided = True  
    
    return satisfied, undecided

def is_satisfied(clause_status: Dict[int, bool]) -> bool:
    return all(clause_status.values())

def get_related_clauses(clauses: List[List[int]], var: int) -> List[int]:
    related = []
    for idx, clause in enumerate(clauses):
        if any(abs(literal) == var for literal in clause):
            related.append(idx)
    return related

def backtrack(clauses: List[List[int]], assignment: Dict[int, bool], 
              clause_status: Dict[int, bool], all_vars: Set[int]) -> Optional[Dict[int, bool]]:
    if is_satisfied(clause_status) and all(var in assignment for var in all_vars):
        return assignment

    unassigned = sorted(var for var in all_vars if var not in assignment)
    if not unassigned:
        return None
    var = unassigned[0]

    for value in [True, False]:
        assignment[var] = value

        related_clauses = get_related_clauses(clauses, var)
        previous_status = {idx: clause_status[idx] for idx in related_clauses}
        for idx in related_clauses:
            satisfied, undecided = update_clause_status(clauses[idx], assignment)
            clause_status[idx] = satisfied or undecided

        result = backtrack(clauses, assignment, clause_status, all_vars)
        if result is not None:
            return result

        for idx, status in previous_status.items():
            clause_status[idx] = status
        assignment.pop(var)

    return None

def solve_sat(filename: str) -> Optional[Dict[int, bool]]:
    clauses = parse_clauses(filename)
    assignment = {}
    clause_status = {i: False for i in range(len(clauses))}
    all_vars = {abs(literal) for clause in clauses for literal in clause}
    
    for idx, clause in enumerate(clauses):
        satisfied, undecided = update_clause_status(clause, assignment)
        clause_status[idx] = satisfied or undecided

    return backtrack(clauses, assignment, clause_status, all_vars)

if __name__ == "__main__":
    filename = "..//data//test.txt"
    result = solve_sat(filename)
    
    if result is None:
        print("No satisfying assignment found.")
    else:
        print("Available assignment:")
        for var, value in result.items():
            print(f"{'-' if not value else ''}{var} ", end="")
