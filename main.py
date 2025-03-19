import make_conditions
import convert_dnf_2_cnf
import solver

# make_conditions.main()
# convert_dnf_2_cnf.dnf_to_cnf("conditions.txt", "cnf.txt")
solver.solve_cnf("cnf.txt", "dict_of_variables.txt", "result.txt")