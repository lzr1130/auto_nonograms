def generate_line_patterns(length, clues, prefix=None):
    if prefix is None:
        prefix = []
    if not clues:
        rem = length - len(prefix)
        return [prefix + [0]*rem]

    results = []
    k = clues[0]
    max_start = length - sum(clues) - (len(clues) - 1)

    for start in range(max_start + 1):
        part = prefix + [0]*start + [1]*k
        if len(part) < length:
            part.append(0)
        for pat in generate_line_patterns(length, clues[1:], part):
            if len(pat) == length:
                results.append(pat)
    return results

def filter_patterns(patterns, current):
    res = []
    for p in patterns:
        ok = True
        for a, b in zip(p, current):
            if b != -1 and a != b:
                ok = False
                break
        if ok:
            res.append(p)
    return res

def solve_nonogram(row_clues, col_clues):
    H, W = len(row_clues), len(col_clues)
    grid = [[-1]*W for _ in range(H)]

    row_patterns = [generate_line_patterns(W, clues) for clues in row_clues]
    col_patterns = [generate_line_patterns(H, clues) for clues in col_clues]

    def update():
        changed = True
        while changed:
            changed = False
            for r in range(H):
                valid = filter_patterns(row_patterns[r], grid[r])
                row_patterns[r] = valid
                for c in range(W):
                    vals = set(p[c] for p in valid)
                    if len(vals) == 1 and grid[r][c] != list(vals)[0]:
                        grid[r][c] = list(vals)[0]
                        changed = True
            for c in range(W):
                col = [grid[r][c] for r in range(H)]
                valid = filter_patterns(col_patterns[c], col)
                col_patterns[c] = valid
                for r in range(H):
                    vals = set(p[r] for p in valid)
                    if len(vals) == 1 and grid[r][c] != list(vals)[0]:
                        grid[r][c] = list(vals)[0]
                        changed = True

    def dfs():
        update()
        if all(all(v != -1 for v in row) for row in grid):
            return True

        for r in range(H):
            for c in range(W):
                if grid[r][c] == -1:
                    for val in (1, 0):
                        backup = [row[:] for row in grid]
                        grid[r][c] = val
                        if dfs():
                            return True
                        grid[:] = backup
                    return False
        return True

    if dfs():
        return grid
    return None

def print_grid(grid):
    for row in grid:
        print("".join("█" if x == 1 else "·" for x in row))

if __name__ == "__main__":

    col_clues = [
        [3], [5], [1,1], [3], [5],
        [3,3], [1,1,1], [15], [1,1,1], [3,3],
        [5], [3], [1,1], [5], [3]
    ]

    row_clues = [
        [3], [5], [1,1], [3], [5],
        [3,3], [1,1,1], [15], [1,1,1], [3,3],
        [5], [3], [1,1], [5], [3]
    ]

    ans = solve_nonogram(row_clues, col_clues)
    print("Solved:\n")
    print_grid(ans)