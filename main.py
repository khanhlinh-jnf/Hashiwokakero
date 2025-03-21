import os
import sys 
from src.initial import init 
from src.parseInput import readFile 
from src.buitlConstaints import buildConstraints
from src.output import print_to_txt
from src.solve import solve

field_info = readFile("input/input-03.txt")
field, neighbours = init(field_info)
nodes, formula = buildConstraints(field)
model = solve(formula, neighbours, len(field[0]))
print_to_txt(nodes, model)
