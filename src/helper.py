from itertools import combinations
from island import Island

def findIsland(matrix):
    islands = []
    for rowIndex, row in enumerate(matrix):
        for colIndex, element in enumerate(row):
            if element != 0:
                island = Island(rowIndex, colIndex, element)
                islands.append(island)
    return islands

def checkConnectionValid(island1, island2, matrix):
    row1 = island1.getRow()
    col1 = island1.getCol()
    row2 = island2.getRow()
    col2 = island2.getCol()
    if row1 == row2:
        for i in range(min(col1, col2)+1, max(col1, col2)):
            if matrix[row1][i] != 0:
                return False
    if col1 == col2:
        for i in range(min(row1, row2)+1, max(row1, row2)):
            if matrix[i][col1] != 0:
                return False
    return True


def findConnections(matrix, islands):
    connections = []
    visited = set()
    for island in islands:  
        row = island.getIndex()[0]
        col = island.getIndex()[1]
        for subIsland in islands:
            subRow = subIsland.getIndex()[0]
            subCol = subIsland.getIndex()[1]
            if row == subRow and col == subCol:
                continue
            if row == subRow and frozenset([island, subIsland]) not in visited:
                if checkConnectionValid(island, subIsland, matrix):
                    visited.add(frozenset([island, subIsland]))
                    connections.append((island, subIsland))
            if col == subCol and frozenset([island, subIsland]) not in visited:
                if checkConnectionValid(island, subIsland, matrix):
                    visited.add(frozenset([island, subIsland]))
                    connections.append((island, subIsland))
    
    return connections

def isIntersection(pairIsland1, pairIsland2):
    # check pair1 and pair2 is parallel
    obj1 = pairIsland1[0]
    obj2 = pairIsland1[1]
    obj3 = pairIsland2[0]
    obj4 = pairIsland2[1]

    if obj1.getRow() == obj2.getRow() and obj3.getRow() == obj4.getRow():
        return False
    if obj1.getCol() == obj2.getCol() and obj3.getCol() == obj4.getCol():
        return False
    
    if obj1.getRow() == obj2.getRow():
        minCol = min(obj1.getCol(), obj2.getCol())
        maxCol = max(obj1.getCol(), obj2.getCol())  
        if obj3.getCol() <= minCol or obj3.getCol() >= maxCol:
            return False
        else:
            minRow = min(obj3.getRow(), obj4.getRow())
            maxRow = max(obj3.getRow(), obj4.getRow())
            if obj1.getRow() <= minRow or obj1.getRow() >= maxRow:
                return False
            return True
    else:
        minRow = min(obj1.getRow(), obj2.getRow())
        maxRow = max(obj1.getRow(), obj2.getRow())
        if obj3.getRow() <= minRow or obj3.getRow() >= maxRow:
            return False
        else:
            minCol = min(obj3.getCol(), obj4.getCol())
            maxCol = max(obj3.getCol(), obj4.getCol())
            if obj1.getCol() <= minCol or obj1.getCol() >= maxCol:
                return False
    return True



def findIntersection(connections):
    intersections = []
    for i in range(len(connections) - 1):
        for j in range(i + 1, len(connections)):
            if isIntersection(connections[i], connections[j]):
                intersections.append((connections[i], connections[j]))
    
    return intersections

def getBridgeConnection(islands, connections):
    map = {}
    for island in islands:
        for connection in connections:
            if island in connection:
                if island not in map:
                    map[island] = []
                map[island].append(connection)
    
    return map

def generateConditionsOfIslandAndSameBridge(islands, possibleBridges):
    resIsland = {}
    resBridge = {}
    for island in islands:
        resIsland[island] = {}
        for possibleBridge in possibleBridges[island]:
            condition1 = (possibleBridge, 1)
            resIsland[island][condition1] = False
            
            if possibleBridge[0].getNumberOfConnections() != 1 and possibleBridge[1].getNumberOfConnections() != 1:
                condition2 = (possibleBridge, 2)
                resIsland[island][condition2] = False
    return resIsland

def checkPossible2Bridge(connection):
    if connection[0].getNumberOfConnections() == 1 or connection[1].getNumberOfConnections() == 1:
        return False
    return True

def getListOfClauses(connections):
    result = []
    for connection in connections:
        condition1 = (connection, 1)
        if (checkPossible2Bridge(connection)):
            condition2 = (connection, 2)
            result.append([condition1, condition2])
        else:
            result.append([condition1])
    return result

def getDictOfLiterals(clauses):
    dict = {}
    num = 1
    for clause in clauses:
        for literal in clause:
            dict[literal] = num
            num += 1
    return dict