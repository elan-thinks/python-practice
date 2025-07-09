import heapq
import time

import map

max_length = max(len(row) for row in map.park_map)
for row in map.park_map:
    row.extend([" "] * (max_length - len(row)))
    print(max_length)
    print(row)

direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]


start = end = None

for x in range(len(map.park_map)):
    for y in range(len(map.park_map[0])):
        if map.park_map[x][y] == "S":
            start = (x, y)
        if map.park_map[x][y] == "E":
            end = (x, y)

heap = [(0, start, [])]
parent = {start: None}
cost_so_far = {start: 0}

while heap:
    cost, (row, col), path = heapq.heappop(heap)

    if map.park_map[row][col] not in ("S", "E"):
        if map.park_map[row][col] in ("^", "¥", "="):
            map.park_map[row][col] = "X"
        else:
            map.park_map[row][col] = "."

    map.show(map.park_map)
    time.sleep(0.1)

    if (row, col) == end:
        print("\nPath:", path + [(row, col)], "\nTotal cost:", cost)
        break

    count_trees = 0
    for drow, dcol in direction:
        new_row, new_col = row + drow, col + dcol
        if 0 <= new_row < len(map.park_map) and 0 <= new_col < len(map.park_map[0]):
            cell = map.park_map[new_row][new_col]
            step_cost = map.cell_cost.get(cell, float("inf"))
            new_cost = cost + step_cost
            if map.park_map[new_row][new_col] == "¥":
               count_trees += 1

            if step_cost != float("inf"):
                if (new_row, new_col) not in cost_so_far or new_cost < cost_so_far[(new_row, new_col)]:
                    cost_so_far[(new_row, new_col)] = new_cost
                    heapq.heappush(
                        heap, (new_cost, (new_row, new_col), path + [(row, col)])
                    )
                    parent[(new_row, new_col)] = (row, col)

# Reconstruct path
cost = 0
cur = end
while cur and cur != start:
    r, c = cur
    if map.park_map[r][c] not in ("S", "E"):
        map.park_map[r][c] = "@"
        cost += map.cell_cost.get(map.park_map[r][c], 1)  # Default
    cur = parent[cur]

map.show(map.park_map)
print("\nFinal Path Map ")
print("\nTotal cost of the Path  : ", cost)
print("Number of Nodes exploard", len(parent))
