from pysat.solvers import Solver


def load_variable_mapping(dict_file):
    """Đọc file ánh xạ biến số nguyên với giá trị tương ứng."""
    variable_map = {}
    with open(dict_file, "r") as f:
        for line in f:
            key, value = line.strip().split(":", 1)  # Tách số nguyên và giá trị
            variable_map[int(key)] = value.strip()  # Lưu vào dictionary
    return variable_map


def solve_cnf(file_input, file_dict, file_output):
    """Giải bài toán SAT từ file CNF, ánh xạ kết quả và lưu vào file kết quả."""
    clauses = []

    # Đọc file CNF
    with open(file_input, "r") as f:
        for line in f:
            clause = list(map(int, line.strip().split()))
            clauses.append(clause)

    # Tải ánh xạ biến
    variable_map = load_variable_mapping(file_dict)

    # Khởi tạo bộ giải SAT
    solver = Solver(name="g3")  # Sử dụng Glucose3

    for clause in clauses:
        solver.add_clause(clause)

    # Tìm nghiệm
    if solver.solve():
        model = solver.get_model()  # Lấy một nghiệm hợp lệ
        positive_vars = [var for var in model if var > 0]  # Lấy các biến dương (đúng)

        # Ánh xạ các biến hợp lệ sang giá trị từ dictionary

        with open(file_output, "w") as f:
            for result in positive_vars:
                f.write(f"{result}: {variable_map[result]}\n")
    else:
        with open(file_output, "w") as f:
            f.write("UNSAT\n")  # Không có nghiệm hợp lệ

    solver.delete()  # Giải phóng bộ nhớ
    

