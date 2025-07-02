import os
import time
from collections import deque

# here the maze map :)
maze = [
    list("S....#...................."),
    list("###..#.#######.#########.."),
    list("....#.......#.#..........#"),
    list(".####.#.###.#.##########.#"),
    list(".#....#...#.#.#..........#"),
    list(".#.###..###.#.######.#####"),
    list(".#........#.#......#.....#"),
    list(".######.#.#.#######.###.#."),
    list("..........#.#.......#.#..#"),
    list("######.#...#.#######.#.#.#"),
    list(".#....#.#.#.#.......#.#..#"),
    list(".#.####.#.#.#######.#.#..#"),
    list(".#......#.#.........#....#"),
    list(".########.##############.#"),
    list(".........................E"),
]
# maze = [
#     list("S...#..."),
#     list(".#.#.#.."),
#     list(".#.....#"),
#     list("###.#.#."),
#     list("...#...E"),
#     list(".#####.."),
# ]

direction = [(-1,0), (1,0), (0,-1), (0,1)]


def show(maze_map):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in maze:
        print(' '.join(row))

start = end = None
wall = '#'
free_path = '.'

for x in range(len(maze)):
    for y in range(len(maze[0])):
        if maze[x][y] == 'S':
            start = (x, y)
        if maze[x][y] == 'E':
            end = (x, y)


queue = deque([start])
visited = {start}
parent = {start : None}

while queue :
    row, col = queue.popleft()

    if maze[row][col] not in ('S','E'):
        maze[row][col] = '*'

    show(maze)
    time.sleep(0.9)

    if (row, col) == end:
        break

    for drow, dcol in direction:
        new_row, new_col = row + drow , col + dcol
        inside = 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0])

        if inside and maze[new_row][new_col] != '#' and (new_row, new_col) not in visited:
            queue.append((new_row,new_col))
            visited.add((new_row, new_col))
            # queue.popLeft(0)
            # print(visited)
            parent[(new_row, new_col)] = (row, col)

# Reconstruct path
cur = end
while cur and cur != start:
    r, c = cur
    if maze[r][c] not in ('S', 'E'):
        maze[r][c] = '@'
    cur = parent[cur]

# Final Maze
print("\nFinal Path:")
show(maze)

print(visited)


# show(maze)
