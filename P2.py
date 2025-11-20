from collections import deque

# Grid: . empty, # wall, D dirty, C1/C2 bots
grid = [
    list("C1.D.."),
    list("..#D.."),
    list(".D..C2"),
]

ROWS, COLS = len(grid), len(grid[0])

bots = {}
dirt = set()
for r in range(ROWS):
    for c in range(COLS):
        if grid[r][c] in ("C1","C2"):
            bots[grid[r][c]] = (r,c)
        if grid[r][c] == "D":
            dirt.add((r,c))
initial_dirt = len(dirt)

cleaned = [[False]*COLS for _ in range(ROWS)]

def clean_area(start, allowed_cols):
    q = deque([start])
    cleaned[start[0]][start[1]] = True
    steps = 0
    cleaned_count = 0
    while q:
        r,c = q.popleft()
        steps += 1
        if (r,c) in dirt:
            dirt.remove((r,c)); cleaned_count += 1
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc = r+dr,c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and nc in allowed_cols and grid[nr][nc] != "#" and not cleaned[nr][nc]:
                cleaned[nr][nc] = True
                q.append((nr,nc))
    return steps, cleaned_count

left_cols = range(0, COLS//2)
right_cols = range(COLS//2, COLS)

steps_C1, cleaned_C1 = clean_area(bots["C1"], left_cols)
steps_C2, cleaned_C2 = clean_area(bots["C2"], right_cols)

# print final map with V for visited cleaned cells
print("\nFinal Clean Map:")
for r in range(ROWS):
    row = ""
    for c in range(COLS):
        if cleaned[r][c] and grid[r][c] == ".":
            row += "V"
        else:
            row += grid[r][c]
    print(row)

# Metrics
total_steps = steps_C1 + steps_C2
total_cleaned = cleaned_C1 + cleaned_C2
efficiency = total_cleaned / total_steps if total_steps>0 else 0

print("\nMetrics:")
print("Initial dirt:", initial_dirt)
print("Cleaned by C1:", cleaned_C1, "C2:", cleaned_C2)
print("Total cleaned:", total_cleaned)
print("Steps C1:", steps_C1, "C2:", steps_C2, "Total:", total_steps)
print("Efficiency (cells cleaned / step):", round(efficiency,4))
