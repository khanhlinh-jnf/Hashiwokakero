import func.make_conditions as make_conditions
import func.convert_dnf_2_cnf as convert_dnf_2_cnf
import func.solver as solver
import func.visualize_result as visualize_result
import os

"""hello world"""

choice = input("Number of input: ")
input_file = (
    "input/" + "input-" + choice + ".txt"
    if int(choice) > 9
    else "input/input-0" + choice + ".txt"
)
output_file = (
    "output/" + "output-" + choice + ".txt"
    if int(choice) > 9
    else "output/output-0" + choice + ".txt"
)
clauses_file = (
    "./data/clauses-" + choice + ".txt"
    if int(choice) > 9
    else "./data/clauses-0" + choice + ".txt"
)
cnf_file = (
    "./data/cnf-" + choice + ".txt"
    if int(choice) > 9
    else "./data/cnf-0" + choice + ".txt"
)
dict_file = (
    "./data/dict_of_variables-" + choice + ".txt"
    if int(choice) > 9
    else "./data/dict_of_variables-0" + choice + ".txt"
)
res_file = (
    "./data/result-" + choice + ".txt"
    if int(choice) > 9
    else "./data/result-0" + choice + ".txt"
)
analysis_file = (
    "./data/analysis-" + choice + ".txt"
    if int(choice) > 9
    else "./data/analysis-0" + choice + ".txt"
)

make_conditions.creat_conditions_file(input_file, clauses_file, dict_file)
convert_dnf_2_cnf.dnf_to_cnf(clauses_file, cnf_file)
os.remove(clauses_file)
solver.solve_cnf(input_file, cnf_file, dict_file, res_file, analysis_file)
visualize_result.visualize(input_file, res_file, output_file)
