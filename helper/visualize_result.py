def read_matrix(file_path):
    filein = open(file_path, "r")
    matrix = []
    for line in filein:
        row = []
        for col in line.split(","):
            row.append(col.strip())
        matrix.append(row)
    filein.close()
    return matrix

def parse_custom_tuple(line):
    line = line.strip() 
    if not line.startswith("(") or not line.endswith(")"):  
        return None 
    line = line[1:-1]  
    parts = line.rsplit(",", 1)  
    tuple_part = parts[0].strip()  
    last_number = int(parts[1].strip()) 
    tuple_part = tuple_part[1:-1]
    sub_parts = tuple_part.split("), (")  
    first_tuple = tuple(map(int, sub_parts[0].replace("(", "").replace(")", "").split(",")))  
    second_tuple = tuple(map(int, sub_parts[1].replace("(", "").replace(")", "").split(",")))
    first_tuple = first_tuple[:2]
    second_tuple = second_tuple[:2]

    return (first_tuple, second_tuple, last_number)

def read_solution(file_path):
    filein = open(file_path, "r")
    solution = []
    for line in filein:
        parsed = parse_custom_tuple(line)
        solution.append(parsed)
    filein.close()
    return solution

def visualize_result(matrix, solution):
    for pair in solution:
        x1, y1 = pair[0]
        x2, y2 = pair[1]
        n = pair[2]

        if x1 == x2:
            symbol = "-" if n == 1 else "="
            for i in range(y1 + 1, y2):
                matrix[x1][i] = symbol
        elif y1 == y2:
            symbol = "|" if n == 1 else "$"
            for i in range(x1 + 1, x2):
                matrix[i][y1] = symbol
def visualize(input_file,result_file, output_file):
    matrix = read_matrix(input_file)
    solution = read_solution(result_file)
    visualize_result(matrix, solution)
    fout = open(output_file, "w")
    for row in matrix:
        for col in row:
            fout.write(col + " ")
        fout.write("\n")

def visualize_fail(output_file):
    fout = open(output_file, "w")
    fout.write("No solution found\n")
    fout.close()