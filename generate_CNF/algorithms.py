import time 
from itertools import combinations

def loadCNF(filePath):
    cnf = []
    with open(filePath, "r") as file:
        lines = file.readlines()
    for line in lines:
        line = line.replace("\n", "")
        clause = []
        for variable in line.split(" "):
            clause.append(int(variable))
        if clause:
            cnf.append(clause)
    return cnf

def getNumberOfVariables(filePath):
    with open(filePath, "r") as file:
        return len(file.readlines())

def findCorrectionVariables(cnf):
    hashMap = {}
    for clause in cnf:
        if len(clause) == 1:
            hashMap[clause[0]] = True
            hashMap[-clause[0]] = False
    for clause in cnf:
        if len(clause) == 2:
            if clause[0] in hashMap and hashMap[clause[0]] == False:
                # print(f"{clause} add variable {clause[1]}")
                hashMap[clause[1]] = True
                hashMap[-clause[1]] = False
            elif clause[1] in hashMap and hashMap[clause[1]] == False:
                # print(f"{clause} add variable {clause[0]}")
                hashMap[clause[0]] = True
                hashMap[-clause[0]] = False
    return hashMap

def findExcluded(hashMap):
    excluded = set()
    for key in hashMap:
        if key > 0:
            excluded.add(key)
    return excluded

def checkValidAnswer(cnf, hashTable):
    for clause in cnf:
        satisfied = False
        for literal in clause:
            if literal > 0:
                if literal in hashTable and hashTable[literal] == True:
                    satisfied = True
                    break
            else:  # literal < 0
                neg_literal = -literal
                if neg_literal in hashTable and hashTable[neg_literal] == False:
                    satisfied = True
                    break
        if not satisfied:
            return False
    return True

def generateCombinations(n, k, exclude=None):
    if exclude is None:
        exclude = set()
    elements = set(range(1, n + 1)) - set(exclude)
    return list(combinations(elements, k))

def bruteForce(cnf, numberOfVariables, excluded, hashMap):
    if checkValidAnswer(cnf, hashMap):
        print("Valid answer found")
        return hashMap, True
    for i in range(1, numberOfVariables + 1):
        combinations = generateCombinations(numberOfVariables, i, excluded)
        if len(combinations) == 0:
            continue
        for combination in combinations:
            for literal in combination:
                hashMap[literal] = False
            if checkValidAnswer(cnf, hashMap):
                print("SATISFIABLE")
                return hashMap, True
            for literal in combination:
                hashMap[literal] = True
    print("UNSATISFIABLE")
    return hashMap, False

def backTracking(cnf, hashMap, excluded, curVar, numberOfVar):
    if curVar == numberOfVar + 1:
        if checkValidAnswer(cnf, hashMap):
            return True
        return False
    if curVar in excluded:
        return backTracking(cnf, hashMap, excluded, curVar + 1, numberOfVar)
    hashMap[curVar] = True
    if backTracking(cnf, hashMap, excluded, curVar + 1, numberOfVar):
        return True
    hashMap[curVar] = False
    if backTracking(cnf, hashMap, excluded, curVar + 1, numberOfVar):
        return True
    return False

if __name__ == "__main__":
    number = input("Enter: ")
    cnfPath = f"data/cnf-0{number}.txt"
    dictOfVariablesPath = f"data/dict_of_variables-0{number}.txt"

    cnf = loadCNF(cnfPath)
    hashMap = findCorrectionVariables(cnf)
    excluded = findExcluded(hashMap)
    numberOfVariables = getNumberOfVariables(dictOfVariablesPath)

    for i in range(1, numberOfVariables + 1):
        if i in excluded:
            continue
        hashMap[i] = True

    # if(backTracking(cnf, hashMap, excluded, 1, numberOfVariables)):
    #     for i in range(1, numberOfVariables + 1):
    #         print(i, ":", hashMap[i])

    res, flag = bruteForce(cnf, numberOfVariables, excluded, hashMap)
    if flag:
        for i in range(1, numberOfVariables + 1):
            print(i, ":", res[i])
    else:
        print("UNSATISFIABLE")
    