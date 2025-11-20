from collections import deque
import numpy as np

grid = [
    list("??#???"),
    list("??????"),
    list("??#???"),
]
R,C = len(grid), len(grid[0])

agents = {"A1": {"pos":(1,0), "cols": range(0,C//2)}, "A2": {"pos":(1,C-1), "cols": range(C//2,C)}}
explored = np.zeros((R,C), dtype=int)

def explore(start, allowed_cols, agent_id):
    q=deque([start]); seen={start}; count=0
    while q:
        r,c = q.popleft()
        if grid[r][c] != "#":
            explored[r][c] += agent_id; count += 1
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and nc in allowed_cols and (nr,nc) not in seen and grid[nr][nc] != "#":
                seen.add((nr,nc)); q.append((nr,nc))
    return count

count1 = explore(agents["A1"]["pos"], agents["A1"]["cols"], 1)
count2 = explore(agents["A2"]["pos"], agents["A2"]["cols"], 2)
total_explored = count1 + count2
free_cells = sum(1 for r in range(R) for c in range(C) if grid[r][c] != "#")
efficiency = total_explored / free_cells if free_cells>0 else 0

print("\nExploration Metrics:")
print("Cells explored by A1:", count1, "A2:", count2, "Total:", total_explored)
print("Free cells:", free_cells, "Exploration coverage fraction:", round(efficiency,4))
print("\nExploration heatmap (numeric array):")
print(explored)
