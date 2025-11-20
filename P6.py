!pip install scipy matplotlib numpy

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
import heapq
import random

# =============== GRID SETUP =======================
GRID_SIZE = 20
grid = np.zeros((GRID_SIZE, GRID_SIZE))

# Add random obstacles
for _ in range(40):
    grid[random.randint(0, 19)][random.randint(0, 19)] = 1  # 1 = obstacle

# Drone bases
drone_positions = [(0, 0), (19, 19)]

# Package delivery locations
packages = [(random.randint(0, 19), random.randint(0, 19)) for _ in range(6)]

# Remove packages that accidentally land on obstacles
packages = [p for p in packages if grid[p] == 0]

print("Drone Starting Points:", drone_positions)
print("Package Locations:", packages)


# =============== A* SEARCH =========================

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    if grid[goal] == 1:  # Can't reach if obstacle on target
        return None

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    moves = [(1,0),( -1,0),(0,1),(0,-1)]

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for m in moves:
            neighbor = (current[0] + m[0], current[1] + m[1])

            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if grid[neighbor] == 1: continue  # obstacle

                temp_g = g_score[current] + 1

                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g
                    f_score[neighbor] = temp_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


# =============== COST MATRIX FOR HUNGARIAN =========

cost_matrix = np.zeros((2, len(packages)))

for d in range(2):
    for p in range(len(packages)):
        cost_matrix[d][p] = heuristic(drone_positions[d], packages[p])

row_ind, col_ind = linear_sum_assignment(cost_matrix)

assignments = {0: [], 1: []}
for drone, pkg_idx in zip(row_ind, col_ind):
    assignments[drone].append(packages[pkg_idx])

print("\nPackage Assignment:")
print(assignments)


# =============== PATH SIMULATION ====================

heatmap = np.zeros((GRID_SIZE, GRID_SIZE))
total_time = 0

for d in range(2):
    cur_pos = drone_positions[d]

    for target in assignments[d]:
        path = astar(grid, cur_pos, target)

        if path is not None:
            for cell in path:
                heatmap[cell] += 1
            total_time += len(path)
            cur_pos = target

print("\nTotal Delivery Time:", total_time)

# =============== HEATMAP OUTPUT =====================

plt.figure(figsize=(6,6))
plt.title("Drone Coverage Heatmap")
plt.imshow(heatmap, cmap="hot", interpolation="nearest")
plt.colorbar()
plt.show()
