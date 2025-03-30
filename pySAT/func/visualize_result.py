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
    """Chuyển đổi chuỗi từ dạng (((a, b, c), (d, e, f)), n) thành ((a, b), (d, e), n)."""
    line = line.strip()  # Xóa khoảng trắng đầu cuối
    if not line.startswith("(") or not line.endswith(")"):
        return None  # Không hợp lệ nếu không có dấu ngoặc

    # Loại bỏ dấu ngoặc ngoài cùng
    line = line[1:-1]

    # Tách phần số cuối (n) khỏi phần tuple chính
    parts = line.rsplit(",", 1)  # Chia từ cuối, giữ tối đa 1 dấu phẩy
    tuple_part = parts[0].strip()  # Phần tuple chính
    last_number = int(parts[1].strip())  # Số cuối (n)

    # Xóa dấu ngoặc ngoài cùng của phần tuple chính
    tuple_part = tuple_part[1:-1]

    # Chia tiếp hai phần (a, b, c) và (d, e, f)
    sub_parts = tuple_part.split("), (")  # Tách hai tuple con
    first_tuple = tuple(
        map(int, sub_parts[0].replace("(", "").replace(")", "").split(","))
    )  # Chuyển thành số
    second_tuple = tuple(
        map(int, sub_parts[1].replace("(", "").replace(")", "").split(","))
    )

    # Chỉ lấy 2 số đầu của mỗi tuple
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


def visualize(input_file, result_file, output_file):
    matrix = read_matrix(input_file)
    solution = read_solution(result_file)
    visualize_result(matrix, solution)
    fout = open(output_file, "w")
    for row in matrix:
        for col in row:
            fout.write(col + " ")
        fout.write("\n")
