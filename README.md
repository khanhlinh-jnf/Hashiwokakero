# Hashiwokakero

This project explores AI techniques to solve the Hashiwokakero (Bridges) puzzle, a logic-based game where islands (nodes) must be connected with bridges while following specific constraints.

## Input
The input is a matrix where:
- `0` represents empty spaces.
- Positive numbers represent islands, with the number indicating the total number of bridges connected to that island.

### Example Input:
```
[
 [2 , 0 , 1],
 [0 , 0 , 0],
 [1 , 0 , 0]
]
```

## Output
The output is a matrix where:
- `|` means one vertical bridge.
- `$` means two vertical bridges.
- `-` means one horizontal bridge.
- `=` means two horizontal bridges.

### Example Output:
```
[
 [2, -, 1],
 [|, 0, 0],
 [1, 0 ,0]
]
```

## How PySAT Works
PySAT is a Python library designed to solve SAT problems (Boolean satisfiability). SAT-solvers only accept formulas in Conjunctive Normal Form (CNF), so this project logically encodes the Hashiwokakero puzzle into CNF to find a solution.

## Solution

### Encoding the Problem
For a Hashiwokakero map of size M x M, we instantiate a two-dimensional array `nodes` of type `Node`, where each node carries the following four variables:
`h1[i,j]`, `h2[i,j]`, `v1[i,j]`, `v2[i,j]`

### Logical Constraints
- One node can not have multiple type of bridges 
- For every non-island node that is a bridge the preceding and subsequent nodes in the direction of the bridge type also have the same
- On an island, based on its value, we determine the number of bridges connected to it, so for each n (number of bridges), there will be different constraints related to CNF
- Check connectivity

