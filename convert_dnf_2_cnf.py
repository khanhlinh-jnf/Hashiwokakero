from itertools import product


def parse_condition(line):
    """Chuyển chuỗi điều kiện thành danh sách các mệnh đề DNF."""
    clauses = line.strip().split("|")
    dnf = []
    for clause in clauses:
        terms = clause.strip().replace("(", "").replace(")", "")
        elements = set(map(int, terms.split("&")))  # Chuyển thành tập hợp số nguyên
        dnf.append(elements)
    return dnf


def distribute_or_over_and(dnf):
    """Chuyển DNF sang CNF bằng cách phân phối OR qua AND."""
    if not dnf:
        return []

    cnf = dnf[0]  # Bắt đầu với điều kiện đầu tiên
    for clause in dnf[1:]:
        new_cnf = []
        for a, b in product(cnf, clause):
            if isinstance(a, int):
                a = {a}
            if isinstance(b, int):
                b = {b}
            new_cnf.append(a | b)  # Hợp hai tập hợp lại
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

    cnf_conditions = []
    for line in lines:
        line = line.strip()
        if not line:
            continue  # Bỏ qua dòng trống

        if is_or_clause(line):
            cnf_conditions.append(
                line.replace("(", "").replace(")", "").replace("|", "")
            )  # Giữ nguyên nếu toàn OR, bỏ dấu |
        elif is_and_only_clause(line):
            elements = line.replace("(", "").replace(")", "").split("&")
            cnf_conditions.extend(elements)  # Mỗi phần tử một dòng
        else:
            dnf = parse_condition(line)
            cnf = distribute_or_over_and(dnf)
            for clause in cnf:
                if isinstance(
                    clause, int
                ):  # Nếu chỉ là số nguyên, convert thành chuỗi luôn
                    cnf_conditions.append(str(clause))
                else:
                    cnf_conditions.append(
                        " ".join(map(str, clause))
                    )  # Mỗi mệnh đề CNF một dòng

    with open(file_output, "w") as f:
        for cnf in cnf_conditions:
            f.write(cnf + "\n")

