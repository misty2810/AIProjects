import heapq
import matplotlib.pyplot as plt
import numpy as np
import time
from IPython.display import clear_output

# -----------------------------
# 1. Create a simple grid
# -----------------------------
GRID_SIZE = 10
grid = np.zeros((GRID_SIZE, GRID_SIZE))   # 0 = free cell

# Add a few obstacles
grid[4][3:8] = 1
grid[6][1:5] = 1

# -----------------------------
# 2. A* Pathfinding
# -----------------------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal, grid):
    moves = [(1,0),(-1,0),(0,1),(0,-1)]
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {start: None}
    g_score = {start: 0}

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            # reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in moves:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny] == 1:  
                    continue  # obstacle
                
                new_cost = g_score[current] + 1
                if (nx, ny) not in g_score or new_cost < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = new_cost
                    priority = new_cost + heuristic((nx, ny), goal)
                    heapq.heappush(pq, (priority, (nx, ny)))
                    came_from[(nx, ny)] = current

    return None

# -----------------------------
# 3. Agent start & goal
# -----------------------------
agent1_start = (0, 0)
agent2_start = (9, 9)

agent1_goal  = (9, 0)
agent2_goal  = (0, 9)

# Compute A* paths
path1 = astar(agent1_start, agent1_goal, grid)
path2 = astar(agent2_start, agent2_goal, grid)

# -----------------------------
# 4. Cooperative Collision Avoidance
# -----------------------------
t = 0
final_positions_1 = []
final_positions_2 = []

while t < max(len(path1), len(path2)):

    # Agent 1 position
    if t < len(path1):
        pos1 = path1[t]
    else:
        pos1 = path1[-1]

    # Agent 2 position
    if t < len(path2):
        pos2 = path2[t]
    else:
        pos2 = path2[-1]

    # Collision check (same cell)
    if pos1 == pos2:
        # Let agent 2 wait one step
        if t < len(path2):
            pos2 = final_positions_2[-1]

    final_positions_1.append(pos1)
    final_positions_2.append(pos2)

    t += 1

# -----------------------------
# 5. Animate the movement
# -----------------------------
for step in range(len(final_positions_1)):
    clear_output(wait=True)

    img = np.ones((GRID_SIZE, GRID_SIZE, 3))

    # Color obstacles
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 1:
                img[i][j] = (0,0,0)  # black obstacles

    # Agent trails
    for s in range(step + 1):
        x1, y1 = final_positions_1[s]
        x2, y2 = final_positions_2[s]
        img[x1][y1] = (0.2, 0.5, 1)   # blue (agent 1)
        img[x2][y2] = (1, 0.4, 0.4)   # red (agent 2)

    # Current positions
    x1, y1 = final_positions_1[step]
    x2, y2 = final_positions_2[step]
    img[x1][y1] = (0, 0, 1)   # dark blue
    img[x2][y2] = (1, 0, 0)   # dark red

    plt.figure(figsize=(5,5))
    plt.imshow(img)
    plt.title(f"Step {step}")
    plt.axis("off")
    plt.show()

    time.sleep(0.3)
