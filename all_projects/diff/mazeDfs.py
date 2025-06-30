import time
import os
from typing import Tuple

# The big maze from earlier (15x25)
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


def show(maze):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in maze:
        print(' '.join(row))
    print()

def find_pos(ch) -> Tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == ch:
                return (i, j)
    return None

# Locate start and end
start = find_pos('S')
end = find_pos('E')

# Directions: up, down, left, right
DIRS = [(-1,0), (1,0), (0,-1), (0,1)]

# DFS variables
stack = [start]
visited = {start}
parent = {start: None}

# DFS loop
while stack:
    r, c = stack.pop()

    if maze[r][c] not in ('S', 'E'):
        maze[r][c] = '*'

    show(maze)
    time.sleep(0.6)

    if (r, c) == end:
        break

    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
            if maze[nr][nc] != '#' and (nr, nc) not in visited:
                stack.append((nr, nc))
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)

# Reconstruct path
cur = end
while cur and cur != start:
    r, c = cur
    if maze[r][c] not in ('S', 'E'):
        maze[r][c] = '*'
    cur = parent[cur]

# Final output
show(maze)
print("DFS completed!")
