import heapq
import itertools
from typing import List, Dict, Set, Optional, Tuple

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

def build_variable_to_clauses_map(formula: List[List[int]], all_variables: Set[int]) -> Dict[int, List[int]]:
    """Build a map from each variable to the indices of clauses it appears in."""
    var_to_clauses = {var: [] for var in all_variables}
    for i, clause in enumerate(formula):
        for literal in clause:
            var = abs(literal)
            var_to_clauses[var].append(i)
    return var_to_clauses

def initialize_clause_status(formula: List[List[int]], assignment: Dict[int, bool]) -> List[bool]:
    """Initialize the satisfaction status of all clauses."""
    return [check_clause_satisfaction(clause, assignment) for clause in formula]

def count_unsatisfied_clauses(clause_status: List[bool]) -> int:
    """Count unsatisfied clauses from the clause status list."""
    return sum(1 for status in clause_status if not status)

def update_clause_status(formula: List[List[int]], clause_status: List[bool], 
                         var: int, value: bool, var_to_clauses: Dict[int, List[int]]) -> None:
    """Update the clause status when a variable is assigned."""
    for clause_idx in var_to_clauses[var]:
        if not clause_status[clause_idx]:  # Only update if clause is not already satisfied
            clause = formula[clause_idx]
            # Check if the variable satisfies the clause
            if any((lit == var and value) or (lit == -var and not value) for lit in clause):
                clause_status[clause_idx] = True

def find_unit_clauses(formula: List[List[int]], assignment: Dict[int, bool], 
                      clause_status: List[bool]) -> List[int]:
    """Find unit clauses (clauses with only one unassigned literal)."""
    unit_literals = []
    
    for i, (clause, is_satisfied) in enumerate(zip(formula, clause_status)):
        if is_satisfied:
            continue
            
        unassigned_literals = []
        is_potentially_unit = True
        
        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                unassigned_literals.append(literal)
                if len(unassigned_literals) > 1:
                    is_potentially_unit = False
                    break
            elif (literal > 0 and assignment[var]) or (literal < 0 and not assignment[var]):
                # Clause is actually satisfied
                clause_status[i] = True
                is_potentially_unit = False
                break
        
        if is_potentially_unit and len(unassigned_literals) == 1:
            unit_literals.append(unassigned_literals[0])
    
    return unit_literals

def find_pure_literals(formula: List[List[int]], assignment: Dict[int, bool], 
                       all_variables: Set[int], clause_status: List[bool]) -> Dict[int, bool]:
    """Find pure literals (variables that appear with only one polarity)."""
    # Track positive and negative occurrences
    pos_occurrence = {var: False for var in all_variables if var not in assignment}
    neg_occurrence = {var: False for var in all_variables if var not in assignment}
    
    for i, (clause, is_satisfied) in enumerate(zip(formula, clause_status)):
        if is_satisfied:
            continue
            
        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                if literal > 0:
                    pos_occurrence[var] = True
                else:
                    neg_occurrence[var] = True
    
    pure_literals = {}
    for var in all_variables:
        if var not in assignment:
            if pos_occurrence[var] and not neg_occurrence[var]:
                pure_literals[var] = True
            elif neg_occurrence[var] and not pos_occurrence[var]:
                pure_literals[var] = False
    
    return pure_literals

def calculate_heuristic(clause_status: List[bool], unassigned_vars: int) -> int:
    """Calculate heuristic value based on unsatisfied clauses and unassigned variables."""
    unsatisfied_count = count_unsatisfied_clauses(clause_status)
    return unassigned_vars + 2 * unsatisfied_count

def calculate_jeroslow_wang(formula: List[List[int]], assignment: Dict[int, bool], 
                           clause_status: List[bool], all_variables: Set[int]) -> Dict[int, float]:
    """Calculate Jeroslow-Wang scores for all unassigned variables."""
    scores = {var: 0.0 for var in all_variables if var not in assignment}
    
    for i, (clause, is_satisfied) in enumerate(zip(formula, clause_status)):
        if is_satisfied:
            continue
            
        clause_size = sum(1 for lit in clause if abs(lit) not in assignment)
        weight = 2 ** -clause_size if clause_size > 0 else 0
        
        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                scores[var] += weight
    
    return scores

def next_literal_improved(formula: List[List[int]], assignment: Dict[int, bool], 
                         all_variables: Set[int], clause_status: List[bool]) -> Optional[int]:
    """Select the next variable to branch on using improved heuristics."""
    # Check for unit clauses first
    unit_literals = find_unit_clauses(formula, assignment, clause_status)
    if unit_literals:
        # Return the variable, not the literal value
        return abs(unit_literals[0])
    
    # Check for pure literals
    pure_literals = find_pure_literals(formula, assignment, all_variables, clause_status)
    if pure_literals:
        return next(iter(pure_literals.keys()))
    
    # Use Jeroslow-Wang heuristic
    scores = calculate_jeroslow_wang(formula, assignment, clause_status, all_variables)
    if scores:
        return max(scores, key=scores.get)
    
    # Fallback: choose any unassigned variable
    unassigned = all_variables - set(assignment.keys())
    return min(unassigned) if unassigned else None

def get_decision_value_for_variable(formula: List[List[int]], var: int, 
                                   assignment: Dict[int, bool], clause_status: List[bool],
                                   unit_literals: List[int], pure_literals: Dict[int, bool]) -> bool:
    """Determine the preferred value for a variable."""
    # For unit clauses, the decision is forced
    for literal in unit_literals:
        if abs(literal) == var:
            return literal > 0
    
    # For pure literals
    if var in pure_literals:
        return pure_literals[var]
    
    # Otherwise count positive vs negative occurrences in unsatisfied clauses
    pos_count = 0
    neg_count = 0
    
    for clause, is_satisfied in zip(formula, clause_status):
        if is_satisfied:
            continue
        
        for literal in clause:
            if abs(literal) == var:
                if literal > 0:
                    pos_count += 1
                else:
                    neg_count += 1
    
    return pos_count >= neg_count

def verify_solution(formula: List[List[int]], assignment: Dict[int, bool]) -> bool:
    """Verify that an assignment satisfies all clauses."""
    for clause in formula:
        if not any((lit > 0 and assignment[abs(lit)]) or 
                  (lit < 0 and not assignment[abs(lit)]) for lit in clause):
            return False
    return True

def astar_optimized(formula: List[List[int]], all_variables: Set[int]) -> Optional[Dict[int, bool]]:
    """A* search with optimizations for SAT solving."""
    priority_queue = []
    visited_states = set()
    tie_breaker = itertools.count()
    
    # Precompute variable to clauses map
    var_to_clauses = build_variable_to_clauses_map(formula, all_variables)
    
    # Initial state
    initial_assignment = {}
    initial_clause_status = initialize_clause_status(formula, initial_assignment)
    initial_h = calculate_heuristic(initial_clause_status, len(all_variables))
    
    # Priority queue entries: (f_score, g_score, tie_breaker, assignment, clause_status)
    heapq.heappush(priority_queue, (initial_h, 0, next(tie_breaker), initial_assignment, initial_clause_status))
    
    while priority_queue:
        f_score, g_score, _, current_assignment, current_clause_status = heapq.heappop(priority_queue)
        
        # Check if all clauses are satisfied
        if all(current_clause_status):
            # Fill in any unassigned variables (they don't affect satisfaction)
            for var in all_variables:
                if var not in current_assignment:
                    current_assignment[var] = True
            return current_assignment
        
        # Generate state key for visited check
        state_key = tuple(sorted(current_assignment.items()))
        if state_key in visited_states:
            continue
        visited_states.add(state_key)
        
        # Unit propagation and pure literal elimination loop
        propagation_done = True
        while propagation_done:
            propagation_done = False
            
            # Try unit propagation
            unit_literals = find_unit_clauses(formula, current_assignment, current_clause_status)
            pure_literals = find_pure_literals(formula, current_assignment, all_variables, current_clause_status)
            
            # Apply unit propagation
            for literal in unit_literals:
                var = abs(literal)
                if var not in current_assignment:
                    value = literal > 0
                    current_assignment[var] = value
                    update_clause_status(formula, current_clause_status, var, value, var_to_clauses)
                    propagation_done = True
            
            # Apply pure literal elimination
            for var, value in pure_literals.items():
                if var not in current_assignment:
                    current_assignment[var] = value
                    update_clause_status(formula, current_clause_status, var, value, var_to_clauses)
                    propagation_done = True
        
        # Check if solution found after propagation
        if all(current_clause_status):
            # Fill in any unassigned variables (they don't affect satisfaction)
            for var in all_variables:
                if var not in current_assignment:
                    current_assignment[var] = True
            return current_assignment
            
        # Check for contradictions (unsatisfiable clauses)
        if any(not status and all(abs(lit) in current_assignment for lit in clause) for status, clause in zip(current_clause_status, formula)):
            continue  # Skip this branch
        
        # Choose next variable to branch on
        next_variable = next_literal_improved(formula, current_assignment, all_variables, current_clause_status)
        if next_variable is None:
            if all(current_clause_status):
                # All clauses satisfied but some variables might be unassigned
                for var in all_variables:
                    if var not in current_assignment:
                        current_assignment[var] = True
                return current_assignment
            continue  # No more variables but not all clauses satisfied
        
        # Get unit literals and pure literals for decision value
        unit_literals = find_unit_clauses(formula, current_assignment, current_clause_status)
        pure_literals = find_pure_literals(formula, current_assignment, all_variables, current_clause_status)
        
        # Determine preferred value for this variable
        preferred_value = get_decision_value_for_variable(
            formula, next_variable, current_assignment, current_clause_status, unit_literals, pure_literals
        )
        
        # Try the preferred value first, then the opposite
        for decision in [preferred_value, not preferred_value]:
            new_assignment = current_assignment.copy()
            new_assignment[next_variable] = decision
            
            # Clone clause status
            new_clause_status = current_clause_status.copy()
            
            # Update clause status incrementally
            update_clause_status(formula, new_clause_status, next_variable, decision, var_to_clauses)
            
            # Skip unsatisfiable branches
            if any(not status and all(
                (lit > 0 and not new_assignment.get(abs(lit), True)) or 
                (lit < 0 and new_assignment.get(abs(lit), False))
                for lit in clause if abs(lit) in new_assignment
            ) for status, clause in zip(new_clause_status, formula)):
                continue
            
            new_g = g_score + 1
            unassigned_count = len(all_variables) - len(new_assignment)
            new_h = calculate_heuristic(new_clause_status, unassigned_count)
            new_f = new_g + new_h
            
            heapq.heappush(priority_queue, (new_f, new_g, next(tie_breaker), new_assignment, new_clause_status))
    
    return None

if __name__ == "__main__":
    filename = "..//data//cnf-06.txt"  
    clauses = parse_clauses(filename)
    all_vars = {abs(literal) for clause in clauses for literal in clause}

    result = astar_optimized(clauses, all_vars)
    
    if result is None:
        print("No satisfying assignment found.")
    else:
        print("Available assignment:")
        # Verify the solution before printing
        if verify_solution(clauses, result):
            for var, value in sorted(result.items()):
                print(f"{'-' if not value else ''}{var} ", end="")
        else:
            print("Error: Invalid solution found.")