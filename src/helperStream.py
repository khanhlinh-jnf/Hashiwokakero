import os
from island import Island

def readMatrix(filePath):
    with open(filePath) as readStream:
        matrix = []
        for line in readStream:
            line = line.replace(" ", "")
            row = []
            for col in line.split(","):
                row.append(int(col))
            matrix.append(row)
    return matrix

def writeLiterals(clauses):
    num = 1
    with open("data/literals.txt", "w") as writeStream:
        for clause in clauses:
            for connection in clause:
                writeStream.write(f"{num}: {connection[0][0].getIndex()} to {connection[0][1].getIndex()} Amount: {connection[1]}\n")
                num += 1

def findLiteral(bridge, literalDict):
    for key in literalDict:
        # print(f"{connection[0]} to {key[0]}")
        if bridge == key:
            return literalDict[key]
    return -1

def writeCNF(clauses, literalDict, intersections):
    with open("data/cnf.txt", "w") as writeStream:
        for clause in clauses:
            if len(clause) == 1:
                writeStream.write(f"{literalDict[clause[0]]} \n")
            else:
                for connection in clause:
                    writeStream.write(f"{literalDict[connection]} ")
                writeStream.write("\n")
                for connection in clause:
                    writeStream.write(f"-{literalDict[connection]} ")
                writeStream.write("\n")
        for intersection in intersections:
            connection1 = intersection[0]
            connection2 = intersection[1]
            var1 = int(findLiteral((connection1, 1), literalDict))
            var2 = int(findLiteral((connection1, 2), literalDict))
            var3 = int(findLiteral((connection2, 1), literalDict))
            var4 = int(findLiteral((connection2, 2), literalDict))
            if var2 == -1 and var4 == -1:
                writeStream.write(f"-{var1} -{var3} \n")
            elif var4 == -1:
                writeStream.write(f"-{var1} -{var3} \n")
                writeStream.write(f"-{var2} -{var3} \n")
                writeStream.write(f"-{var1} -{var2} -{var3} \n")
            elif var2 == -1:
                writeStream.write(f"-{var1} -{var3} \n")
                writeStream.write(f"-{var1} -{var4} \n")
                writeStream.write(f"-{var1} -{var3} -{var4} \n")
            else:
                writeStream.write(f"-{var1} -{var3} -{var4} \n")
                writeStream.write(f"-{var2} -{var3} -{var4} \n")
                writeStream.write(f"-{var1} -{var2} -{var3} \n")
                writeStream.write(f"-{var1} -{var2} -{var4} \n")

        