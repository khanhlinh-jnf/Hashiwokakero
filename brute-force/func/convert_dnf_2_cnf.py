from itertools import product


def parse_condition(line):
    """Chuyển chuỗi điều kiện thành danh sách các mệnh đề DNF."""
    clauses = line.strip().split("|")
    dnf = []
    for clause in clauses:
        terms = clause.strip().replace("(", "").replace(")", "")
        elements = frozenset(
            map(int, terms.split("&"))
        )  # Dùng frozenset để dễ dàng so sánh
        dnf.append(elements)
    return dnf


def distribute_or_over_and(dnf):
    """Chuyển DNF sang CNF bằng cách phân phối OR qua AND."""
    if not dnf:
        return []

    cnf = dnf[0]  # Bắt đầu với điều kiện đầu tiên
    for clause in dnf[1:]:
        new_cnf = set()
        for a, b in product(cnf, clause):
            if isinstance(a, int):
                a = frozenset([a])
            if isinstance(b, int):
                b = frozenset([b])
            new_cnf.add(a | b)  # Hợp hai tập hợp lại (loại bỏ trùng lặp)
        cnf = new_cnf
    return cnf


def is_or_clause(line):
    """Kiểm tra xem dòng có phải toàn OR hay không."""
    return "&" not in line


def is_and_only_clause(line):
    """Kiểm tra xem dòng chỉ chứa toán tử & không."""
    return "|" not in line and "&" in line


def dnf_to_cnf(file_input, file_output):
    """Chuyển đổi DNF sang CNF nếu cần và lưu vào file khác."""
    with open(file_input, "r") as f:
        lines = f.readlines()

    cnf_conditions = set()  # Sử dụng tập hợp để loại bỏ điều kiện trùng lặp

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Bỏ qua dòng trống

        if is_or_clause(line):
            condition = line.replace("(", "").replace(")", "").replace("|", "").strip()
            cnf_conditions.add(condition)  # Giữ nguyên nếu toàn OR
        elif is_and_only_clause(line):
            elements = line.replace("(", "").replace(")", "").split("&")
            cnf_conditions.update(
                e.strip() for e in elements
            )  # Mỗi phần tử một dòng, xóa khoảng trắng
        else:
            dnf = parse_condition(line)
            cnf = distribute_or_over_and(dnf)
            for clause in cnf:
                if isinstance(
                    clause, int
                ):  # Nếu chỉ là số nguyên, convert thành chuỗi luôn
                    cnf_conditions.add(str(clause).strip())
                else:
                    cnf_conditions.add(
                        " ".join(map(str, clause)).strip()
                    )  # Mỗi mệnh đề CNF một dòng, xóa khoảng trắng

    # Ghi ra file (đảm bảo không có dòng trùng lặp)
    with open(file_output, "w") as f:
        for cnf in cnf_conditions:  # Sắp xếp để dễ kiểm tra
            f.write(cnf.strip() + "\n")
