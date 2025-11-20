from collections import deque

# --- FIXED MAZE ---
# Use single-char agent labels: 1 and 2
maze = [
    list("1...K."),
    list(".#..K."),
    list(".K...2"),
]

ROWS, COLS = len(maze), len(maze[0])

# locate agents and keys
agents = {}
keys = set()

for r in range(ROWS):
    for c in range(COLS):
        cell = maze[r][c]
        if cell == "1":
            agents["A1"] = (r, c)
        elif cell == "2":
            agents["A2"] = (r, c)
        elif cell == "K":
            keys.add((r, c))

initial_keys = len(keys)

visited = [[False] * COLS for _ in range(ROWS)]


def bfs_collect(start, cols_allowed):
    q = deque([start])
    visited[start[0]][start[1]] = True
    steps = 0
    collected = 0

    while q:
        r, c = q.popleft()
        steps += 1

        # collect key
        if (r, c) in keys:
            keys.remove((r, c))
            collected += 1

        # explore
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < ROWS
                and 0 <= nc < COLS
                and maze[nr][nc] != "#"
                and not visited[nr][nc]
                and nc in cols_allowed
            ):
                visited[nr][nc] = True
                q.append((nr, nc))

    return steps, collected


# divide maze into left and right halves
left_cols = range(0, COLS // 2)
right_cols = range(COLS // 2, COLS)

steps_A1, col_A1 = bfs_collect(agents["A1"], left_cols)
steps_A2, col_A2 = bfs_collect(agents["A2"], right_cols)


# ---- visualization ----
out = []
for r in range(ROWS):
    row = ""
    for c in range(COLS):
        if (r, c) in keys:
            row += "K"
        elif visited[r][c] and maze[r][c] == ".":
            row += "V"
        else:
            row += maze[r][c]
    out.append(row)

print("\nFinal Maze:")
for row in out:
    print(row)

# ---- Metrics (Option A) ----
total_steps = steps_A1 + steps_A2
collected_total = col_A1 + col_A2
efficiency = collected_total / total_steps if total_steps > 0 else 0

print("\nMetrics:")
print("Initial keys:", initial_keys)
print("Keys collected A1:", col_A1, "A2:", col_A2)
print("Total keys collected:", collected_total)
print("Steps A1:", steps_A1, "A2:", steps_A2, "Total:", total_steps)
print("Efficiency (keys/step):", round(efficiency, 4))
