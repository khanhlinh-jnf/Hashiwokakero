import func.make_conditions as make_conditions
import func.convert_dnf_2_cnf as convert_dnf_2_cnf
import func.solver as solver
import func.visualize_result as visualize_result

'''hello world'''

choice = input("Number of input: ")
input_file = "input/"+"input" + choice + ".txt"
output_file = "output/"+"output" + choice + ".txt"

make_conditions.creat_conditions_file(
    input_file,
    "./data/information.txt",
    "./data/conditions.txt",
    "./data/dict_of_variables.txt",
)
convert_dnf_2_cnf.dnf_to_cnf("./data/conditions.txt", "./data/cnf.txt")
solver.solve_cnf(input_file,"./data/cnf.txt", "./data/dict_of_variables.txt", "./data/result.txt")
visualize_result.visualize(input_file, "./data/result.txt", output_file)
