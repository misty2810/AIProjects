# grid: . empty, # wall
grid = [
    list("..#.."),
    list("....."),
    list("#...#"),
]
R,C = len(grid), len(grid[0])

robots = {"R1": {"pos":(0,0), "color":1}, "R2": {"pos":(0,4), "color":2}}
painted = [[0]*C for _ in range(R)]

def dfs_count(r,c,color):
    stack=[(r,c)]; count=0; visited=set()
    while stack:
        r,c = stack.pop()
        if not (0<=r<R and 0<=c<C): continue
        if grid[r][c] == "#" or painted[r][c] != 0 or (r,c) in visited: continue
        painted[r][c] = color; visited.add((r,c)); count += 1
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]: stack.append((r+dr,c+dc))
    return count

count1 = dfs_count(*robots["R1"]["pos"], robots["R1"]["color"])
count2 = dfs_count(*robots["R2"]["pos"], robots["R2"]["color"])
total_painted = count1 + count2

# print painted grid
print("\nPainted Grid (numbers indicate robot color):")
for r in painted: print(r)

# Metrics
free_cells = sum(1 for r in range(R) for c in range(C) if grid[r][c] != "#")
coverage = total_painted / free_cells if free_cells>0 else 0

print("\nMetrics:")
print("Painted by R1:", count1, "R2:", count2, "Total:", total_painted)
print("Free cells:", free_cells, "Coverage fraction:", round(coverage,4))
