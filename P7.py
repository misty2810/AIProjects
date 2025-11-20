import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# 1. Create a simple empty grid
# -------------------------------
GRID_SIZE = 15
grid = np.zeros((GRID_SIZE, GRID_SIZE))   # 0 = empty cell

# -------------------------------
# 2. Assign each robot a region
#    Robot 1 paints the left half
#    Robot 2 paints the right half
# -------------------------------
region = np.zeros((GRID_SIZE, GRID_SIZE))
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        if j < GRID_SIZE // 2:
            region[i][j] = 1   # Robot 1 region
        else:
            region[i][j] = 2   # Robot 2 region

# -------------------------------
# 3. DFS Painting Function
# -------------------------------
def dfs_paint(start_x, start_y, robot_id, paint_grid):
    stack = [(start_x, start_y)]
    visited = set()

    while stack:
        x, y = stack.pop()

        # Avoid revisiting
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Paint only if belongs to this robot
        if region[x][y] == robot_id:
            paint_grid[x][y] = robot_id

        # Possible moves: up, down, left, right
        moves = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            # Check boundaries
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if (nx, ny) not in visited:
                    stack.append((nx, ny))

# -------------------------------
# 4. Prepare paint grid
# -------------------------------
paint = np.zeros((GRID_SIZE, GRID_SIZE))

# Robot starting positions
robot1_start = (0, 0)
robot2_start = (0, GRID_SIZE - 1)

# -------------------------------
# 5. Run DFS Painting
# -------------------------------
dfs_paint(robot1_start[0], robot1_start[1], 1, paint)
dfs_paint(robot2_start[0], robot2_start[1], 2, paint)

# -------------------------------
# 6. Create color image
# -------------------------------
colors = {
    0: (1, 1, 1),      # white (unpainted)
    1: (0.3, 0.5, 1),  # blue for Robot 1
    2: (0.3, 1, 0.5)   # green for Robot 2
}

image = np.zeros((GRID_SIZE, GRID_SIZE, 3))
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        image[i][j] = colors[paint[i][j]]

# -------------------------------
# 7. Show final painted grid
# -------------------------------
plt.figure(figsize=(6, 6))
plt.title("Grid Painting Agents (Simple Version)")
plt.imshow(image)
plt.axis("off")
plt.show()
