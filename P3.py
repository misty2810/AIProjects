import heapq, time, os

# small grid; G denotes both goals but we pick two Gs
grid = [
    "##########",
    "#A....#..#",
    "#....##..#",
    "#........#",
    "#..#..#G.#",
    "#..#..#..#",
    "#..#..##.#",
    "#..B....G#",
    "##########"
]
grid = [list(r) for r in grid]
R, C = len(grid), len(grid[0])
DIRS = [(1,0),(-1,0),(0,1),(0,-1),(0,0)]

def find(ch):
    res=[]
    for r in range(R):
        for c in range(C):
            if grid[r][c]==ch: res.append((r,c))
    return res

A_start = find("A")[0]
B_start = find("B")[0]
Gs = find("G")
A_goal = Gs[0]; B_goal = Gs[1]

def inside(r,c): return 0<=r<R and 0<=c<C
def free(r,c): return grid[r][c] != '#'
def h(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])

def astar(start, goal):
    pq=[(0,start)]; came={start:None}; cost={start:0}
    while pq:
        _, (r,c) = heapq.heappop(pq)
        if (r,c)==goal: break
        for dr,dc in DIRS:
            nr,nc=r+dr,c+dc
            if inside(nr,nc) and free(nr,nc):
                ncst = cost[(r,c)]+1
                if (nr,nc) not in cost or ncst < cost[(nr,nc)]:
                    cost[(nr,nc)] = ncst
                    heapq.heappush(pq,(ncst+h((nr,nc),goal),(nr,nc)))
                    came[(nr,nc)] = (r,c)
    if goal not in came: return []
    path=[]; cur=goal
    while cur:
        path.append(cur); cur=came[cur]
    return path[::-1]

# plan A then B with simple time-avoidance
pathA = astar(A_start, A_goal)
# simple avoid map: positions of A by time
avoid = {t:pos for t,pos in enumerate(pathA)}

def astar_avoid(start, goal, avoid_map):
    pq=[(0,start,0)]; came={(start,0):None}; cost={(start,0):0}
    while pq:
        _, (r,c), t = heapq.heappop(pq)
        if (r,c)==goal:
            # reconstruct
            cur=(r,c,t); path=[]
            while cur:
                path.append(cur[0:2]); cur=came[cur]
            return path[::-1]
        for dr,dc in DIRS:
            nr,nc=r+dr,c+dc; nt=t+1
            if not(inside(nr,nc) and free(nr,nc)): continue
            if nt in avoid_map and (nr,nc)==avoid_map[nt]: continue
            if (r,c) in avoid_map.values() and nt-1 in avoid_map and avoid_map.get(nt-1)==(nr,nc) and avoid_map.get(nt)==(r,c): continue
            state=(nr,nc,nt)
            new = cost[(r,c,t)] + 1
            if state not in cost or new < cost[state]:
                cost[state]=new
                heapq.heappush(pq,(new+h((nr,nc),goal),(nr,nc),nt))
                came[state]=(r,c,t)
    return []

pathB = astar_avoid(B_start, B_goal, avoid)

# visualization quick print
print("\nPlanned A path length:", len(pathA))
print("Planned B path length:", len(pathB))

# --- Metrics (Option A) ---
steps_A = len(pathA)
steps_B = len(pathB)
reached_A = 1 if pathA and pathA[-1]==A_goal else 0
reached_B = 1 if pathB and pathB[-1]==B_goal else 0
total_steps = steps_A + steps_B
success_rate = (reached_A+reached_B)/2

print("\nMetrics:")
print("Steps A:", steps_A, "B:", steps_B, "Total:", total_steps)
print("Reached goals A,B:", reached_A, reached_B)
print("Success rate (fraction goals reached):", success_rate)
print("Efficiency (goals/step):", round((reached_A+reached_B)/total_steps if total_steps>0 else 0,4))
