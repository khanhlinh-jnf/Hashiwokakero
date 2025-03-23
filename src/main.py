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
    for intersection in intersections:
        print(f"{intersection[0][0].getIndex()} to {intersection[0][1].getIndex()} and {intersection[1][0].getIndex()} to {intersection[1][1].getIndex()} are intersections")

if __name__ == '__main__':
    main()