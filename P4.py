# minimal warehouse pickup
def manhattan(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])

grid = [
    "##########",
    "#A...P..D#",
    "#...##...#",
    "#..P..B..#",
    "#...P....#",
    "##########"
]
grid = [list(r) for r in grid]
R,C = len(grid), len(grid[0])

def find(ch):
    pts=[]
    for r in range(R):
        for c in range(C):
            if grid[r][c]==ch: pts.append((r,c))
    return pts

A = find("A")[0]
B = find("B")[0]
pickup_points = find("P")
drop = find("D")[0]

# assign by closest to starting agent (greedy)
tasks_A=[]; tasks_B=[]
for p in pickup_points:
    if manhattan(A,p) <= manhattan(B,p): tasks_A.append(p)
    else: tasks_B.append(p)

def greedy_path_len(start, target):
    # Manhattan greedy steps count (ignores obstacles)
    return abs(start[0]-target[0])+abs(start[1]-target[1])

def execute_tasks(agent_start, tasks):
    time = 0
    pos = agent_start
    items = 0
    for t in tasks:
        time += greedy_path_len(pos,t); pos = t
        time += greedy_path_len(pos,drop); pos = drop
        items += 1
    return time, items

time_A, items_A = execute_tasks(A, tasks_A)
time_B, items_B = execute_tasks(B, tasks_B)

# Metrics
total_time = time_A + time_B
total_items = items_A + items_B
efficiency = total_items / total_time if total_time>0 else 0

print("\nWarehouse Pickup Metrics:")
print("Tasks A:", tasks_A)
print("Tasks B:", tasks_B)
print("Time A:", time_A, "Time B:", time_B, "Total time:", total_time)
print("Items A:", items_A, "Items B:", items_B, "Total items:", total_items)
print("Efficiency (items / time):", round(efficiency,4))
