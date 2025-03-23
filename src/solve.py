from pysat.solvers import Solver


def solve(f, neighbours, y):

    # connectively check
    def traversal(island, model, neighbours, counter, seen):
        def pos(i, j): return 4 * ( y * i + j )
        i, j = island 

        right = model[pos(i, j + 1):(pos(i, j + 1) + 4)]
        down = model[pos(i + 1, j):(pos(i + 1, j) + 4)]
        left = model[(pos(i, j - 1)):(pos(i, j - 1) + 4)]
        up = model[(pos(i - 1, j)):(pos(i - 1, j) + 4)]
        # print(right, down, left, up) 

        if (right[0] > 0 or right[1] > 0) and (neighbours[(i, j)][0] not in seen):
            seen.add(neighbours[(i, j)][0])
            counter += traversal(neighbours[(i, j)][0], model, neighbours, 1, seen)

        if (down[2] > 0 or down[3] > 0) and (neighbours[(i, j)][1] not in seen):
            seen.add(neighbours[(i, j)][1])
            counter += traversal(neighbours[(i, j)][1], model, neighbours, 1, seen)

        if (left[0] > 0 or left[1] > 0) and (neighbours[(i, j)][2] not in seen):
            seen.add(neighbours[(i, j)][2])
            counter += traversal(neighbours[(i, j)][2], model, neighbours, 1, seen)

        if (up[2] > 0 or up[3] > 0) and (neighbours[(i, j)][3] not in seen):
            seen.add(neighbours[(i, j)][3])
            counter += traversal(neighbours[(i, j)][3], model, neighbours, 1, seen)

        return counter

    with Solver(bootstrap_with=f) as s:
        s.solve()
        for m in s.enum_models():
            start = list(neighbours.keys())[0]
            seen = set([start])

            if traversal(start, m, neighbours, 1, seen) == len(neighbours.keys()): return m
    return None