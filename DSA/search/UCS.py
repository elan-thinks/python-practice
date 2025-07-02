import heapq
import os
import time

maze = [
    list("S...#....~....#.......#..."),
    list(".###.#.#####.#.#####..#.#."),
    list("...#.#.....#.#.....#..#.#."),
    list(".#.#.###.#.#.#####.#.##.#."),
    list(".#...~.#.#...^...#.#....#."),
    list(".#####.#.#####.###.#######"),
    list(".#.....#.....#.....#.....#"),
    list(".#.#########.#####.#.###.#"),
    list(".#.........#.....#.#...#.#"),
    list(".#.#######.#####.#.###.#.#"),
    list(".#.#.....#.....#.#...#.#.#"),
    list(".#.#.###.#####.#.###.#.#.#"),
    list(".#.#...#.....#.#.....#...#"),
    list(".#.###.#####.#.#######.#.#"),
    list("...#.....~...#.........#.E"),
]


cell_cost = {"S": 0, ".": 1, "~": 5, "^": 10, "#": float("inf"), "E": 0}

direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def show(maze_map):
    os.system("cls" if os.name == "nt" else "clear")
    for row in maze_map:
        print(" ".join(row))


start = end = None

for x in range(len(maze)):
    for y in range(len(maze[0])):
        if maze[x][y] == "S":
            start = (x, y)
        if maze[x][y] == "E":
            end = (x, y)

heap = [(0, start, [])]
parent = {start: None}
cost_so_far = {start: 0}

while heap:
    cost, (row, col), path = heapq.heappop(heap)

    if maze[row][col] not in ("S", "E"):
        maze[row][col] = "*"

    show(maze)
    time.sleep(0.1)

    if (row, col) == end:
        print("\nPath:", path + [(row, col)], "\nTotal cost:", cost)
        break

    for drow, dcol in direction:
        new_row, new_col = row + drow, col + dcol
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
            cell = maze[new_row][new_col]
            step_cost = cell_cost.get(cell, float("inf"))
            new_cost = cost + step_cost

            if step_cost != float("inf"):
                if (new_row, new_col) not in cost_so_far or new_cost < cost_so_far[
                    (new_row, new_col)
                ]:
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
    if maze[r][c] not in ("S", "E"):
        maze[r][c] = "@"
    cur = parent[cur]
    cost += 1

show(maze)
print("\nFinal Path:")
print("total cost is  : ", cost)
