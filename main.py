import helper.make_conditions as make_conditions
import helper.convert_dnf_2_cnf as convert_dnf_2_cnf
import helper.astar as astar
import helper.backtracking as backtracking
import helper.brute_force as brute_force
import helper.pySAT as pySAT
import helper.visualize_result as visualize_result
import os

"""hello world"""

choice = input("Number of input: ")
name_folder = ["pySAT/", "astar/", "backtracking/", "brute_force/"]
algorithms = [
    pySAT.solve_cnf,
    astar.astar,
    backtracking.solve_cnf,
    brute_force.brute_force,
]
print("Choose the algorithm:\n1. pySAT\n2. A* Search\n3. Backtracking\n4. Brute Force")
algo = 0
while True:
    algo = int(input("Enter your choice: "))
    if algo in [1, 2, 3, 4]:
        break
    print("Invalid choice. Please try again.")
folder = name_folder[algo - 1]
algorithm = algorithms[algo - 1]

input_file = (
    "input/" + "input-" + choice + ".txt"
    if int(choice) > 9
    else "input/input-0" + choice + ".txt"
)
output_file = (
    "output/" + folder + "output-" + choice + ".txt"
    if int(choice) > 9
    else "output/" + folder + "output-0" + choice + ".txt"
)
clauses_file = (
    "data/" + folder + "clauses-" + choice + ".txt"
    if int(choice) > 9
    else "data/" + folder + "clauses-" + choice + ".txt"
)
cnf_file = (
    "data/" + folder + "cnf-" + choice + ".txt"
    if int(choice) > 9
    else "data/" + folder + "cnf-0" + choice + ".txt"
)
dict_file = (
    "data/" + folder + "dict_of_variables-" + choice + ".txt"
    if int(choice) > 9
    else "data/" + folder + "dict_of_variables-0" + choice + ".txt"
)
res_file = (
    "data/" + folder + "result-" + choice + ".txt"
    if int(choice) > 9
    else "data/" + folder + "result-0" + choice + ".txt"
)
analysis_file = (
    "data/" + folder + "analysis-" + choice + ".txt"
    if int(choice) > 9
    else "data/" + folder + "analysis-0" + choice + ".txt"
)

make_conditions.creat_conditions_file(input_file, clauses_file, dict_file)
convert_dnf_2_cnf.dnf_to_cnf(clauses_file, cnf_file)
os.remove(clauses_file)
algorithm(input_file, cnf_file, dict_file, res_file, analysis_file)
visualize_result.visualize(input_file, res_file, output_file)
