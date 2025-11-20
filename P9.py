from collections import deque

grid = [
    list("A1..F."),
    list("..#..F"),
    list(".F..A2"),
]
R,C = len(grid), len(grid[0])

fires = [(r,c) for r in range(R) for c in range(C) if grid[r][c]=="F"]
agents = { "A1": (0,0), "A2": (2,5) }  # positions correspond to A1/A2 marks

def bfs(start, goal):
    q=deque([(start,0)]); seen={start}
    while q:
        (r,c),d = q.popleft()
        if (r,c)==goal: return d
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and grid[nr][nc] != "#" and (nr,nc) not in seen:
                seen.add((nr,nc)); q.append(((nr,nc),d+1))
    return 9999

def spread_once(flist):
    new=[]
    for r,c in list(flist):
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and grid[nr][nc]=='.':
                grid[nr][nc]='F'; new.append((nr,nc))
    return flist+new

# simple simulate: each round fire spreads then agents extinguish nearest fires greedily
time = 0
extinguished = {"A1":0,"A2":0}
fires = [(r,c) for r in range(R) for c in range(C) if grid[r][c]=="F"]

while fires:
    fires = spread_once(fires)
    time += 1
    for agent, pos in agents.items():
        if not fires: break
        # pick nearest fire
        nearest = min(fires, key=lambda f: abs(f[0]-pos[0])+abs(f[1]-pos[1]))
        d = bfs(pos, nearest)
        if d >= 9999:
            continue
        # agent moves (we approximate by teleporting to fire for metrics)
        agents[agent] = nearest
        if nearest in fires:
            fires.remove(nearest)
            grid[nearest[0]][nearest[1]]='.'  # extinguished
            extinguished[agent] += 1

total_extinguished = sum(extinguished.values())
efficiency = total_extinguished / time if time>0 else 0

print("\nFirefighting Metrics:")
print("Time units elapsed:", time)
print("Extinguished A1:", extinguished["A1"], "A2:", extinguished["A2"], "Total:", total_extinguished)
print("Efficiency (extinguished / time):", round(efficiency,4))
