import os
import time
from algorithms import *


number = int(input("Number of input: "))
matrix = getCNF(number)
correctionVariables = findVariableAutoCorrection(matrix)

startTime = time.time()
result = bruteForce(matrix, number)
endTime = time.time()
duration = endTime - startTime


print(f"Execution time: {duration:.2f} seconds")
if result:
    print("Solution:", result)
else:
    print("No solution found.")
