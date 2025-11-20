from collections import deque

maze = [
    list("###########"),
    list("#A..#..V..#"),
    list("#...#.....#"),
    list("#..V...#..#"),
    list("#.....#..B#"),
    list("###########")
]

R,C = len(maze), len(maze[0])

def find(ch):
    return [(r,c) for r in range(R) for c in range(C) if maze[r][c]==ch]

A = find('A')[0]; B = find('B')[0]
victims = find('V')

def bfs_dist(start):
    q=deque([start]); dist={start:0}
    while q:
        r,c = q.popleft()
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and maze[nr][nc] != '#' and (nr,nc) not in dist:
                dist[(nr,nc)] = dist[(r,c)] + 1
                q.append((nr,nc))
    return dist

distA=bfs_dist(A); distB=bfs_dist(B)

taskA=[]; taskB=[]
for v in victims:
    dA=distA.get(v,1e9); dB=distB.get(v,1e9)
    if dA<=dB: taskA.append(v)
    else: taskB.append(v)

def greedy_route_len(start, targets):
    # sum of Manhattan approximated steps visiting targets in given order
    pos=start; steps=0
    for t in targets:
        steps += abs(pos[0]-t[0]) + abs(pos[1]-t[1])
        pos = t
    return steps

steps_A = greedy_route_len(A, taskA)
steps_B = greedy_route_len(B, taskB)
rescued_A = len(taskA); rescued_B = len(taskB)
total_steps = steps_A + steps_B

print("\nRescue Mission Metrics:")
print("Tasks assigned A:", taskA, "B:", taskB)
print("Rescued A:", rescued_A, "B:", rescued_B, "Total:", rescued_A+rescued_B)
print("Steps A:", steps_A, "B:", steps_B := steps_B, "Total Steps:", total_steps)
print("Efficiency (rescued / step):", round((rescued_A+rescued_B)/total_steps if total_steps>0 else 0,4))
