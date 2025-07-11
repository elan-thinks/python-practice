import time

import map

#first track the exact location of were to start and end
start = end = None
for i in range(len(map.park_map)):
    for j in range(len(map.park_map[0])):
        if map.park_map[i][j] == "S":
            start = (i, j)
        elif map.park_map[i][j] == "E":
            end = (i, j)

# DFS setup
stack = [start]
visited = set()
parent = {}

while stack:
    #here pops the last node of the stack
    row, col = stack.pop()
    current = (row, col)

    if current in visited:
        continue
    visited.add(current)

    if map.park_map[row][col] not in ("S", "E"):
        if map.park_map[row][col] in ("^", "¥", "="):
            map.park_map[row][col] = "X"
        else:
            map.park_map[row][col] = "."

    map.show(map.park_map)
    time.sleep(0.05)

    if current == end:
        print("\nReached the End!")
        break

    for dx, dy in map.direction:
        new_r, new_c = row + dx, col + dy
        new_pos = (new_r, new_c)

        if (
            0 <= new_r < len(map.park_map)
            and 0 <= new_c < len(map.park_map[0])
            and new_pos not in visited
            and map.park_map[new_r][new_c] not in ("#", "~", "$")
        ):

            stack.append(new_pos)
            parent[new_pos] = current  # Track path

# here econstruct path
cur = end
cost = 0
while cur != start:
    r, c = cur
    if map.park_map[r][c] not in ("S", "E"):
        map.park_map[r][c] = "@"
        cost += 1  # treat all obstacles the same way with free path

    cur = parent.get(cur)
    if cur is None:
        print("\nNo path found!")
        break

# Final display
map.show(map.park_map)

print("")
print("    --------------------------------------")
print("  |  Final Path Map with DFS              |")
print("  |  Total steps of the Path :", cost,"        |")
print("  |  Number of Nodes Explored:", len(visited),"       |")
print("    --------------------------------------")

