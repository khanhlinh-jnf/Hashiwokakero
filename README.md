# Hashiwokakero Solver

This project explores AI techniques to solve the **Hashiwokakero (Bridges)** puzzle, a logic-based game where islands (nodes) must be connected with bridges while adhering to specific constraints.

---

## Project Structure
```
HASHIWOKAKERO/
|── data/                           # Store data that related to logic and solving problem of each algorithms.
│   ├── astar/                      
│   ├── backtracking/
│   ├── brute_force/
│   ├── pySAT/
├── helper/
│   ├── pycache/                    # Compiled Python cache files.
│   ├── astar.py                    # Helper functions specific to the A* algorithm implementation.
│   ├── backtracking.py             # Helper functions specific to the backtracking algorithm implementation.
│   ├── brute_force.py              # Helper functions specific to the brute-force algorithm implementation.
│   ├── convert_dnf_2_cnf.py        # Converts Disjunctive Normal Form (DNF) to Conjunctive Normal Form (CNF) for SAT solving.
│   ├── make_conditions.py          # Generates conditions or constraints for the Hashiwokakero puzzle.
│   ├── pySAT.py                    # Helper functions for integrating PySAT with the project.
│   ├── visualize_result.py         # Visualizes the results of the solving algorithms.
├── input/
├── output/
├── main.py                         # Entry point of the program.
├── README.md
├── requirement.txt                 # Dependencies for the project.                               
```
---

## 🚀 How to Run the Code
Before running the code, ensure you have installed the required dependencies. You can do this by running:

```bash
pip install -r requirement.txt
```
To execute the program, use the following command in your terminal:

```bash
py main.py
```

### Steps:
1. Enter the number of test cases you want to run.
2. Enter the algorithm you want to use for solving
3. The output will be generated and saved in the `output` folder.

---

## Description of the input
- input 1 is sample in the assignment
- input 2 is sample in the assignment
- input 3 is sample in the assignment
- input 4 and 5, I created them by myself to test the code
- input 5 is 6x6
- input 6 is 7x7
- input 7 is 11x11
- input 8 is 13x13
- input 9 is 17x17
- input 10 is 20x20

## 📥 Input Description
The following test cases are available:
- **Input 1 & 2**: Provided as samples in the assignment.
- **Input 3**: Another sample from the assignment.
- **Input 4 & 5**: Custom test cases created for additional verification.
- **Input 5**: 7x7 grid.
- **Input 6**: 9x9 grid.
- **Input 7**: 11×11 grid.
- **Input 8**: 13×13 grid.
- **Input 9**: 17×17 grid.
- **Input 10**: 20×20 grid.

Each test case follows the standard Hashiwokakero format and adheres to the puzzle's logical constraints.

---

🎯 **Happy Solving!**
