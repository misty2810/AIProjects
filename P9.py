from collections import deque
import copy

grid = [
    list("A1..F."),
    list("..#..F"),
    list(".F..A2"),
]
R,C = len(grid), len(grid[0])

def print_grid(g):
    for row in g:
        print("".join(row))
    print("-" * C)

fires = [(r,c) for r in range(R) for c in range(C) if grid[r][c]=="F"]
agents = { "A1": (0,0), "A2": (2,5) }

def bfs(start, goal):
    q = deque([(start,0)])
    seen = {start}
    while q:
        (r,c),d = q.popleft()
        if (r,c) == goal: return d
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc = r+dr, c+dc
            if 0<=nr<R and 0<=nc<C and grid[nr][nc] != "#" and (nr,nc) not in seen:
                seen.add((nr,nc))
                q.append(((nr,nc), d+1))
    return 9999

def spread_once(flist):
    new=[]
    for r,c in list(flist):
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and grid[nr][nc]=='.':
                grid[nr][nc]='F'
                new.append((nr,nc))
    return flist + new

time = 0
extinguished = {"A1":0,"A2":0}

print("Initial Grid")
print_grid(grid)

while fires:
    # fire spreads
    fires = spread_once(fires)
    time += 1

    # agents act
    for agent, pos in agents.items():
        if not fires: break

        nearest = min(fires, key=lambda f: abs(f[0]-pos[0])+abs(f[1]-pos[1]))
        d = bfs(pos, nearest)
        if d >= 9999:
            continue

        # teleport move
        agents[agent] = nearest

        if nearest in fires:
            fires.remove(nearest)
            grid[nearest[0]][nearest[1]] = agent  # show agent extinguished here
            extinguished[agent] += 1

    print(f"After time = {time}")
    print_grid(grid)

total_extinguished = sum(extinguished.values())
efficiency = total_extinguished / time if time>0 else 0

print("\nFinal Metrics:")
print("Time units:", time)
print("A1 extinguished:", extinguished["A1"])
print("A2 extinguished:", extinguished["A2"])
print("Total:", total_extinguished)
print("Efficiency:", round(efficiency,4))
