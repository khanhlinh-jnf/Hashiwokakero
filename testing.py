from itertools import combinations

# mapping: [ n[i-1][j].v1, n[i-1][j].v2, n[i+1][j].v1, n[i+1][j].v2, n[i][j-1].h1, n[i][j-1].h2, n[i][j+1].h1, n[i][j+1].h2 ]

arr = [1, 2, 3, 4, 5, 6, 7, 8]
bridge_sum_DNF = {}

for r in range(0, 5):
    for comb in combinations(arr, r):
        s = set()
        subsequent_pair = False
        count_hor = 0
        count_ver = 0
        total = 0
        toAdd = set([-1, -2, -3, -4, -5, -6, -7, -8])
        for num in comb:
            if num <= 4:
                count_ver += 1
            else:
                count_hor += 1
            if (((num - 1) in toAdd) and (num % 2 == 0)):
                subsequent_pair = True
            else:
                s.add(num)
            toAdd.add(num)
            toAdd.remove(-num)

        # prevent invalid combinations of 2, 3 or 4 truthy variables
        # this is where the optimisation happens
        if (count_hor > 2) or (count_ver > 2) or (subsequent_pair): continue

        total = sum(2 if x % 2 == 0 else 1 for x in comb)
        if total not in bridge_sum_DNF:
            bridge_sum_DNF[total] = []
        bridge_sum_DNF[total].append(list(toAdd))

for i in range(0, 9):
    print(f"bridge_sum_DNF[{i}]=[", end=' ')
    for clause in bridge_sum_DNF[i]:
        print('[', end=' ')
        print(*clause, sep=", ", end=' ')
        print('], ', end=' ')
    print(']')


bridge_sum_CNF = {}


def invert(sublist):
    return [-el for el in sublist]


for key, clauses in bridge_sum_DNF.items():
    filtered_sublists = []
    for clause in clauses:
        filtered_sublists.append(invert(clause))
    bridge_sum_DNF[key] = filtered_sublists

for key1 in bridge_sum_DNF.keys():
    for key2, clauses in bridge_sum_DNF.items():
        if (key1 != key2):
            if key1 not in bridge_sum_CNF:
                bridge_sum_CNF[key1] = []
            bridge_sum_CNF[key1].extend(clauses)

for i in range(0, 9):
    print(f"bridge_sum_CNF[{i}]=[", end=' ')
    print(len(bridge_sum_CNF[i]))
    for clause in bridge_sum_CNF[i]:
        print('[', end=' ')
        print(*clause, sep=", ", end=' ')
        print('], ', end=' ')
    print(']')