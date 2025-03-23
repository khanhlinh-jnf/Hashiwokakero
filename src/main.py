from helper import *
from island import *
from helperStream import *

def main():
    filePath = "inputs/input-01.txt"
    matrix = readMatrix(filePath) 
    islands = findIsland(matrix) # list of island
    connections = findConnections(matrix, islands) # list of tuple (island, island) that can be connected
    intersections = findIntersection(connections) 
    clauses = getListOfClauses(connections)
    literalDict = getDictOfLiterals(clauses)
    writeCNF(clauses, literalDict, intersections)
    writeLiterals(clauses)

if __name__ == '__main__':
    main()