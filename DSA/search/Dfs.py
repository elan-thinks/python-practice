import time

import map

# Movement directions: up, down, left, right
direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Find start (S) and end (E) positions
start = end = None
for x in range(len(map.park_map)):
    for y in range(len(map.park_map[0])):
        if map.park_map[x][y] == "S":
            start = (x, y)
        elif map.park_map[x][y] == "E":
            end = (x, y)



# DFS setup
stack = [start]
visited = {start}
parent = {start: None}

while stack:
    row, col = stack.pop()

    if map.park_map[row][col] not in ("S", "E"):
        if map.park_map[row][col] in ("^", "¥", "="):
            map.park_map[row][col] = "X"
        else:
            map.park_map[row][col] = "."

    map.show(map.park_map)
    time.sleep(0.1)

    if (row, col) == end:
        print("Reached the End!")
        break

    for drow, dcol in direction:
        new_row, new_col = row + drow, col + dcol
        inside = 0 <= new_row < len(map.park_map) and 0 <= new_col < len(map.park_map[0])
        new_pos = (new_row, new_col)

        if inside and new_pos not in visited:
            cell = map.park_map[new_row][new_col]
            if cell in map.cell_cost and map.cell_cost[cell] != float("inf"):
                stack.append(new_pos)
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
    cur = parent.get(cur, None)

# Final display
map.show(map.park_map)
print("\nFinal Path Map ")
print("\nTotal cost of the Path  : ", cost)
print("Number of Nodes exploard", len(parent))
