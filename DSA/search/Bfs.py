import time
from collections import deque

import map

# Movement: up, down, left, right
direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Locate start (S) and end (E)
start = end = None
for x in range(len(map.park_map)):
    for y in range(len(map.park_map[0])):
        if map.park_map[x][y] == "S":
            start = (x, y)
        elif map.park_map[x][y] == "E":
            end = (x, y)


# Breadth-First Search setup
queue = deque([start])
visited = {start}
parent = {start: None}

while queue:
    row, col = queue.popleft()

    if map.park_map[row][col] not in ("S", "E"):
        if map.park_map[row][col] in ("^", "¥", "="):
            map.park_map[row][col] = "X"
        else:
            map.park_map[row][col] = "."

    map.show(map.park_map)
    time.sleep(0.05)

    if (row, col) == end:
        break


    for drow, dcol in direction:
        new_row, new_col = row + drow, col + dcol
        inside_bounds = 0 <= new_row < len(map.park_map) and 0 <= new_col < len(map.park_map[0])
        new_pos = (new_row, new_col)

        if (inside_bounds and map.park_map[new_row][new_col] not in ("#","$","~") and new_pos not in visited):
            queue.append(new_pos)
            visited.add(new_pos)
            parent[new_pos] = (row, col)

# Reconstruct path
cost = 0
cur = end
while cur and cur != start:
    r, c = cur
    if map.park_map[r][c] not in ("S", "E"):
        map.park_map[r][c] = "@"
        cost += 1
    cur = parent[cur]

# Final Maze Display
map.show(map.park_map)
print("\nFinal Path Map ")
print("\nTotal cost of the Path  : ", cost)
print("Number of Nodes exploard", len(parent))
