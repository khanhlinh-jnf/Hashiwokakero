from itertools import combinations
import time


def parse_string_to_tuple_list(string_list):
    tuple_list = []
    for item in string_list:
        tuple_list.append(eval(item))
    return tuple_list


def read_matrix(file_path):
    with open(file_path, "r") as filein:
        return [[int(col) for col in line.split(",")] for line in filein]


def find_islands(matrix):
    return [
        (r, c, matrix[r][c])
        for r in range(len(matrix))
        for c in range(len(matrix[0]))
        if matrix[r][c] != 0
    ]


def load_variable_mapping(dict_file):
    variable_map = {}
    with open(dict_file, "r") as f:
        for line in f:
            key, value = line.strip().split(":", 1)
            variable_map[int(key)] = value.strip()
    return variable_map


def is_connected(edges, nodes):
    parent = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    for node in nodes:
        parent[node[:2]] = node[:2]

    for edge in edges:
        union(edge[0][:2], edge[1][:2])

    return len({find(node[:2]) for node in nodes}) == 1

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
                hashMap[clause[1]] = True
                hashMap[-clause[1]] = False
            elif clause[1] in hashMap and hashMap[clause[1]] == False:
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

def brute_force(input_file, file_condition, file_dict, file_output, analysis_file):
    cnf = loadCNF(file_condition)
    hashMap = findCorrectionVariables(cnf)
    excluded = findExcluded(hashMap)
    numberOfVariables = getNumberOfVariables(file_dict)
    variable_map = load_variable_mapping(file_dict)
    islands = find_islands(read_matrix(input_file))
    start_time = time.time()
    if checkValidAnswer(cnf, hashMap):
        positive_vars = [var for var in range(1, numberOfVariables + 1) if hashMap[var]]
        edges = [variable_map[var] for var in positive_vars if variable_map[var][-2] == ")"]
        edges = parse_string_to_tuple_list(edges)
        if is_connected(edges, islands):
            with open(file_output, "w") as f:
                for result in positive_vars:
                    if variable_map[result][-2] != ")":
                        f.write(f"{variable_map[result]}\n")
            with open(analysis_file, "w") as f:
                f.write(f"Time: {round(time.time() - start_time,2)} seconds\n")
                for result in positive_vars:
                    f.write(f"{result} ")
            return True
    for i in range(1, numberOfVariables + 1):
        combinations = generateCombinations(numberOfVariables, i, excluded)
        if len(combinations) == 0:
            continue
        for combination in combinations:
            for literal in combination:
                hashMap[literal] = False
            if checkValidAnswer(cnf, hashMap):
                positive_vars = [var for var in range(1, numberOfVariables + 1) if hashMap[var]]
                edges = [variable_map[var] for var in positive_vars if variable_map[var][-2] == ")"]
                edges = parse_string_to_tuple_list(edges)
                if is_connected(edges, islands):
                    with open(file_output, "w") as f:
                        for result in positive_vars:
                            if variable_map[result][-2] != ")":
                                f.write(f"{variable_map[result]}\n")
                    with open(analysis_file, "w") as f:
                        f.write(
                            f"Time: {round((time.time() - start_time)*1000)} miliseconds\n"
                        )
                        for result in positive_vars:
                            f.write(f"{result} ")
                    return True
            for literal in combination:
                hashMap[literal] = True
    with open(file_output, "w") as f:
        f.write("UNSAT\n")
    with open(analysis_file, "w") as f:
        f.write(f"Time: {round((time.time() - start_time)*1000)} miliseconds\n")
    return False
