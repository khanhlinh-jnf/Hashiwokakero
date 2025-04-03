from itertools import product

def parse_condition(line):
    clauses = line.strip().split("|")
    dnf = []
    for clause in clauses:
        terms = clause.strip().replace("(", "").replace(")", "")
        elements = frozenset(
            map(int, terms.split("&"))
        )  
        dnf.append(elements)
    return dnf


def distribute_or_over_and(dnf):
    if not dnf:
        return []

    cnf = dnf[0]  
    for clause in dnf[1:]:
        new_cnf = set()
        for a, b in product(cnf, clause):
            if isinstance(a, int):
                a = frozenset([a])
            if isinstance(b, int):
                b = frozenset([b])
            new_cnf.add(a | b) 
        cnf = new_cnf
    return cnf


def is_or_clause(line):
    return "&" not in line


def is_and_only_clause(line):
    return "|" not in line and "&" in line


def dnf_to_cnf(file_input, file_output):
    with open(file_input, "r") as f:
        lines = f.readlines()

    cnf_conditions = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue 

        if is_or_clause(line):
            condition = line.replace("(", "").replace(")", "").replace("|", "").strip()
            cnf_conditions.add(condition) 
        elif is_and_only_clause(line):
            elements = line.replace("(", "").replace(")", "").split("&")
            cnf_conditions.update(
                e.strip() for e in elements
            )  
        else:
            dnf = parse_condition(line)
            cnf = distribute_or_over_and(dnf)
            for clause in cnf:
                if isinstance(
                    clause, int
                ):  
                    cnf_conditions.add(str(clause).strip())
                else:
                    cnf_conditions.add(
                        " ".join(map(str, clause)).strip()
                    ) 

    with open(file_output, "w") as f:
        if not cnf_conditions:
            f.write("1\n")
            f.write("-1\n")
        for cnf in cnf_conditions:  
            f.write(cnf.strip() + "\n")
