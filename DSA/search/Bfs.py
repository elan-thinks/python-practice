import time
from collections import deque

import map

#first track the exact location of were to start and end
start = end = None
for x in range(len(map.park_map)):
    for y in range(len(map.park_map[0])):
        if map.park_map[x][y] == "S":
            start = (x, y)
        elif map.park_map[x][y] == "E":
            end = (x, y)


# setup
queue = deque([start])
visited = set()
parent = {}

while queue:
    # here take the first in node of the queue
    row, col = queue.popleft()
    current_node = (row, col)

    if current_node in visited:
        continue
    visited.add(current_node)

    if map.park_map[row][col] not in ("S", "E"):
        if map.park_map[row][col] in ("^", "¥", "="):
            map.park_map[row][col] = "X"
        else:
            map.park_map[row][col] = "."

    map.show(map.park_map)
    time.sleep(0.05)

    if current_node == end:
        print("\nReached the End!")
        break

    for drow, dcol in map.direction:
        new_row, new_col = row + drow, col + dcol
        new_pos = (new_row, new_col)

        if (
            0 <= new_row < len(map.park_map)
            and 0 <= new_col < len(map.park_map[0])
            and new_pos not in visited
            and map.park_map[new_row][new_col] not in ("#", "~", "$")
        ):

            queue.append(new_pos)
            parent[new_pos] = current_node

# here reconstruct the path
cost = 0
cur = end
while cur != start:
    r, c = cur
    if map.park_map[r][c] not in ("S", "E"):
        map.park_map[r][c] = "@"
        cost += 1  # treat all obstacles the same way with free path

    cur = parent.get(cur)
    if cur is None:
        print("\nNo path found!")
        break

# Final Maze Display
map.show(map.park_map)

print("")
print("    ----------------------------------------")
print("  |  Final Path Map with BFS                |")
print("  |  Total steps of the shortest Path: ", cost," |")
print("  |  Number of Nodes exploard : ", len(visited),"       |")
print("    ----------------------------------------")


