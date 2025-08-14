import heapq
import time

import map

# Find start and end
start = end = None
for x in range(len(map.park_map)):
    for y in range(len(map.park_map[0])):
        if map.park_map[x][y] == "S":
            start = (x, y)
        elif map.park_map[x][y] == "E":
            end = (x, y)

# Initialize UCS
heap = [(0, start)]  # (cost, (x, y))
cost_so_far = {start: 0}
visited = set()
parent = {}

while heap:
    current_cost, (row, col) = heapq.heappop(heap)
    current_node = (row, col)

    if current_node in visited:
        continue
    visited.add(current_node)

    if current_node == end:
        print("\nGoal reached! Total cost:", current_cost)
        break

    # Visualization
    if map.park_map[row][col] not in ("S", "E"):
        terrain = map.park_map[row][col]
        map.park_map[row][col] = "X" if terrain in ("^", "¥", "=") else "."
        map.show(map.park_map)
        time.sleep(0.05)

    # Explore neighbors
    for drow, dcol in map.direction:
        new_row, new_col = row + drow, col + dcol
        new_node = (new_row, new_col)

        # Check boundaries
        if 0 <= new_row < len(map.park_map) and 0 <= new_col < len(map.park_map[0]):
            terrain = map.park_map[new_row][new_col]

            step_cost = map.cell_cost.get(terrain, 1)
            new_cost = current_cost + step_cost

            if new_node not in cost_so_far or new_cost < cost_so_far[new_node]:
                cost_so_far[new_node] = new_cost
                parent[new_node] = current_node
                heapq.heappush(heap, (new_cost, new_node))

# Reconstruct and mark path
cur = end
path_cost = 0
while cur and cur != start:
    r, c = cur
    if map.park_map[r][c] not in ("S", "E"):
        path_cost += map.cell_cost.get(map.park_map[r][c], 1)
        map.park_map[r][c] = "@"
    cur = parent.get(cur)

# Final display
map.show(map.park_map)
print("")
print("    --------------------------------------")
print("  |  Final Path Map with UCS              |")
print("  |  Total cost of the shortest path:", cost_so_far.get(end, float("inf"))," |")
print("  |  Number of nodes explored:", len(visited),"       |")
print("    --------------------------------------")

