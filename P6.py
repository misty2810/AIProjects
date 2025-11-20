import heapq

grid = [
    list("D...P."),
    list(".#..#."),
    list("..P..D"),
]
R,C = len(grid), len(grid[0])

drones=[]; packages=[]
for r in range(R):
    for c in range(C):
        if grid[r][c]=='D': drones.append((r,c))
        if grid[r][c]=='P': packages.append((r,c))

def astar(start, goal):
    pq=[(0,start,0)]; seen=set()
    while pq:
        _, (r,c), cost = heapq.heappop(pq)
        if (r,c)==goal: return cost
        if (r,c) in seen: continue
        seen.add((r,c))
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and grid[nr][nc] != "#":
                h = abs(nr-goal[0])+abs(nc-goal[1])
                heapq.heappush(pq,(cost+1+h,(nr,nc),cost+1))
    return 0

# greedy assignment to nearest drone
assign = {}
for p in packages:
    best = min(drones, key=lambda d: abs(d[0]-p[0])+abs(d[1]-p[1]))
    assign.setdefault(best, []).append(p)

heat = [[0]*C for _ in range(R)]
total_time = 0
delivered = {d:0 for d in drones}

for d in drones:
    if d not in assign: continue
    pos = d
    for pkg in assign[d]:
        dist = astar(pos, pkg)
        # approximate path mark: increment heat along straight Manhattan line
        steps = dist if dist>0 else abs(pos[0]-pkg[0])+abs(pos[1]-pkg[1])
        total_time += steps
        delivered[d] += 1
        pos = pkg

# Metrics
total_delivered = sum(delivered.values())
efficiency = total_delivered / total_time if total_time>0 else 0

print("\nDrone Delivery Metrics:")
print("Packages delivered per drone:")
for d in drones:
    print(f" Drone {d}: {delivered.get(d,0)}")
print("Total delivery time (approx steps):", total_time)
print("Total delivered:", total_delivered)
print("Efficiency (packages / time):", round(efficiency,4))
