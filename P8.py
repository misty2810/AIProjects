from collections import deque
import heapq

# grid: . empty, # wall, R resource, A1/A2 agents
grid = [
    list("A1..R."),
    list("..#..R"),
    list(".R..A2"),
]
Rn,C = len(grid), len(grid[0])

agents = {}
resources=[]
for r in range(Rn):
    for c in range(C):
        ch = grid[r][c]
        if ch in ("A1","A2"): agents[ch]=(r,c)
        if ch == "R": resources.append((r,c))

def bfs_len(start, goal):
    q=deque([(start,0)]); seen={start}
    while q:
        (r,c),d = q.popleft()
        if (r,c)==goal: return d
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<Rn and 0<=nc<C and grid[nr][nc] != "#" and (nr,nc) not in seen:
                seen.add((nr,nc)); q.append(((nr,nc),d+1))
    return 9999

# Shared task queue (greedy nearest for each agent in turn)
tasks = list(resources)
collected = {"A1":0,"A2":0}
times = {"A1":0,"A2":0}

for agent in ["A1","A2"]:
    pos = agents[agent]
    while tasks:
        # pick closest resource to this agent's current position
        res = min(tasks, key=lambda r: abs(r[0]-pos[0])+abs(r[1]-pos[1]))
        tasks.remove(res)
        dist = bfs_len(pos, res)
        if dist >= 9999:
            continue
        times[agent] += dist
        collected[agent] += 1
        pos = res

total_collected = sum(collected.values())
total_time = times["A1"] + times["A2"]
efficiency = total_collected / total_time if total_time>0 else 0

print("\nResource Collection Metrics:")
print("Collected A1:", collected["A1"], "A2:", collected["A2"])
print("Time A1:", times["A1"], "A2:", times["A2"], "Total time:", total_time)
print("Efficiency (resources / time):", round(efficiency,4))
