from src.initial import init 
from src.parseInput import readFile 
from src.buitlConstaints import buildConstraints
from src.output import print_to_txt
from src.solve import solve

field_info, number = readFile("input/input-01.txt")
field, neighbours = init(field_info)
nodes, formula = buildConstraints(field, number)
model = solve(formula, neighbours, len(field[0]))
print_to_txt(nodes, model, number)
