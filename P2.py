from collections import deque

# ----------------------------------------------------
# BASE GRID (bots will be inserted manually after)
# ----------------------------------------------------
grid = [
    list("...D.."),
    list("..#D.."),
    list(".D...."),
]

ROWS, COLS = len(grid), len(grid[0])

# ----------------------------------------------------
# MANUALLY INSERT BOTS (this avoids ALL KeyErrors)
# ----------------------------------------------------
C1_pos = (0, 0)   # row 0, col 0
C2_pos = (2, 5)   # row 2, col 5

grid[C1_pos[0]][C1_pos[1]] = "1"
grid[C2_pos[0]][C2_pos[1]] = "2"

bots = {"C1": C1_pos, "C2": C2_pos}

# ----------------------------------------------------
# FIND DIRT
# ----------------------------------------------------
dirt = set()
for r in range(ROWS):
    for c in range(COLS):
        if grid[r][c] == "D":
            dirt.add((r, c))

print("Bots found:", bots)
print("Dirt found:", dirt)

initial_dirt = len(dirt)
visited = [[False]*COLS for _ in range(ROWS)]

# ----------------------------------------------------
# BFS CLEANING
# ----------------------------------------------------
def clean_area(start, allowed_cols):
    q = deque([start])
    visited[start[0]][start[1]] = True
    steps = 0
    cleaned_count = 0

    while q:
        r, c = q.popleft()
        steps += 1

        if (r, c) in dirt:
            dirt.remove((r, c))
            cleaned_count += 1

        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc

            if (0 <= nr < ROWS and 0 <= nc < COLS 
                and grid[nr][nc] != "#" 
                and nc in allowed_cols 
                and not visited[nr][nc]):

                visited[nr][nc] = True
                q.append((nr, nc))

    return steps, cleaned_count

# left and right halves
left_cols = range(0, COLS//2)
right_cols = range(COLS//2, COLS)

# ----------------------------------------------------
# RUN BOTH BOTS
# ----------------------------------------------------
steps_C1, cleaned_C1 = clean_area(bots["C1"], left_cols)
steps_C2, cleaned_C2 = clean_area(bots["C2"], right_cols)

# ----------------------------------------------------
# FINAL MAP
# ----------------------------------------------------
print("\nFinal Clean Map:")
for r in range(ROWS):
    row = ""
    for c in range(COLS):
        if visited[r][c] and grid[r][c] == ".":
            row += "V"
        else:
            row += grid[r][c]
    print(row)

# ----------------------------------------------------
# METRICS
# ----------------------------------------------------
total_steps = steps_C1 + steps_C2
total_cleaned = cleaned_C1 + cleaned_C2
efficiency = total_cleaned / total_steps if total_steps > 0 else 0

print("\nMetrics:")
print("Initial dirt:", initial_dirt)
print("Cleaned by C1:", cleaned_C1)
print("Cleaned by C2:", cleaned_C2)
print("Total cleaned:", total_cleaned)
print("Steps C1:", steps_C1, "Steps C2:", steps_C2)
print("Efficiency:", round(efficiency, 4))
