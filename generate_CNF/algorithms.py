import os
from itertools import combinations

def getCNF(number):
    # Read the CNF file
    filePath = "data/cnf-"
    if number > 9:
        filePath += str(number) + ".txt"
    else:
        filePath += "0" + str(number) + ".txt" 
    matrix = []
    with open(filePath, 'r') as file:
        clauses = file.readlines()
        for clause in clauses:
            clause = clause.replace("\n", "")
            row = []
            for literal in clause.split(" "):
                row.append(int(literal))
            matrix.append(row)
    return matrix

def getNumberOfVariables(filePath):
    with open(filePath, 'r') as file:
        return len(file.readlines())

def checkValidAnswer(matrix, hashTable):
    for clause in matrix:
        flag = False
        for literal in clause:
            if literal < 0:
                if not hashTable[abs(literal)]:
                    flag = True
                    break
            else:
                if hashTable[literal]:
                    flag = True
                    break
        if not flag:
            return False
    return True

def generate_combinations(n, k):
    elements = list(range(1, n + 1))
    return list(combinations(elements, k))

def findVariableAutoCorrection(cnf):
    correctionVariables = {}
    for clause in cnf:
        if len(clause) == 1:
            if clause[0] < 0:
                correctionVariables[abs(clause[0])] = False
            else:
                correctionVariables[clause[0]] = True
    return correctionVariables

def bruteForce(matrix, number):
    filePath = "data/dict_of_variables-"
    if number > 9:
        filePath += str(number) + ".txt"
    else:
        filePath += "0" + str(number) + ".txt"
    hashTable = {}
    numberOfVariables = getNumberOfVariables(filePath)
    for i in range(1, numberOfVariables + 1):
        hashTable[i] = True
    if checkValidAnswer(matrix, hashTable):
        return hashTable
    for i in range(1, numberOfVariables + 1):
        list = generate_combinations(numberOfVariables, i)
        for combination in list:
            for element in combination:
                hashTable[element] = False
            if checkValidAnswer(matrix, hashTable):
                print("SATISFIABLE")
                return hashTable
            for element in combination:
                hashTable[element] = True
    print("UNSATISFIABLE")
    return None
    
def backTracking(hashTable, matrix, curVar, numberOfVar):
    if curVar == numberOfVar + 1:
        if checkValidAnswer(matrix, hashTable):
            return True
        return False
    hashTable[curVar] = True
    if backTracking(hashTable, matrix, curVar + 1, numberOfVar):
        return True
    hashTable[curVar] = False
    if backTracking(hashTable, matrix, curVar + 1, numberOfVar):
        return True
    return False