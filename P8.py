from collections import deque

grid = [
    list("1..R.."),
    list("..#..R"),
    list(".R..2."),
]

Rn, C = len(grid), len(grid[0])

agents = {}
resources = []

# Read grid
for r in range(Rn):
    for c in range(C):
        ch = grid[r][c]
        if ch in ("1","2"):
            agents[ch] = (r,c)
        elif ch == "R":
            resources.append((r,c))

# BFS distance
def bfs_len(start, goal):
    q = deque([(start,0)])
    seen = {start}
    while q:
        (r,c),d = q.popleft()
        if (r,c) == goal:
            return d
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc = r+dr, c+dc
            if 0 <= nr < Rn and 0 <= nc < C and grid[nr][nc] != "#" and (nr,nc) not in seen:
                seen.add((nr,nc))
                q.append(((nr,nc), d+1))
    return 9999

# INITIAL POSITIONS
tasks = list(resources)
posA = agents["1"]
posB = agents["2"]

collected = {"1":0, "2":0}
times = {"1":0, "2":0}

# ---- COOPERATIVE LOOP ----
while tasks:

    # Agent 1 picks nearest
    if tasks:
        nearestA = min(tasks, key=lambda r: abs(r[0]-posA[0]) + abs(r[1]-posA[1]))
        tasks.remove(nearestA)
        distA = bfs_len(posA, nearestA)
        posA = nearestA
        collected["1"] += 1
        times["1"] += distA

    # Agent 2 picks nearest (if tasks left)
    if tasks:
        nearestB = min(tasks, key=lambda r: abs(r[0]-posB[0]) + abs(r[1]-posB[1]))
        tasks.remove(nearestB)
        distB = bfs_len(posB, nearestB)
        posB = nearestB
        collected["2"] += 1
        times["2"] += distB

# Compute metrics
total_collected = sum(collected.values())
total_time = times["1"] + times["2"]
efficiency = total_collected / total_time if total_time > 0 else 0

print("\nResource Collection Metrics:")
print("Collected:", collected)
print("Times:", times)
print("Efficiency:", round(efficiency,4))


# -------------------------------
# VISUALIZATION (ASCII GRID)
# -------------------------------
def show_grid(grid, posA, posB, collected):
    print("\n=== FINAL GRID (A = Agent1, B = Agent2) ===\n")
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[0])):
            if (r,c) == posA:
                row += "A  "
            elif (r,c) == posB:
                row += "B  "
            elif grid[r][c] == "#":
                row += "## "
            elif grid[r][c] == "R":
                row += "R  "
            elif grid[r][c] in ("1","2"):
                row += grid[r][c] + "  "
            else:
                row += ".  "
        print(row)
    print("\n============================\n")
    print("Final Positions:")
    print("Agent 1 (A):", posA)
    print("Agent 2 (B):", posB)
    print("Resources Collected:", collected)

# CALL VISUALIZER
show_grid(grid, posA, posB, collected)
