import time
import os
from collections import deque



# Define the maze
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


def show(m):
    os.system('cls' if os.name == 'nt' else 'clear')  # ← Clear screen
    for row in m:
        print(' '.join(row))
    print()

# Find start and end
start = end = None
for r in range(len(maze)):
    for c in range(len(maze[0])):
        if maze[r][c] == 'S':
            start = (r, c)
        elif maze[r][c] == 'E':
            end = (r, c)

# BFS
queue   = deque([start])
visited = {start}
parent  = {start: None}
DIRS = [(-1,0), (1,0), (0,-1), (0,1)]

while queue:
    r, c = queue.popleft()

    # Visual: mark visited path
    if maze[r][c] not in ('S', 'E'):
        maze[r][c] = '*'  # use '@' or '.' to show path

    show(maze)
    time.sleep(0.9)  # <- add delay to animate!

    if (r, c) == end:
        break

    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        inside = 0 <= nr < len(maze) and 0 <= nc < len(maze[0])
        if inside and maze[nr][nc] != '#' and (nr, nc) not in visited:
            queue.append((nr, nc))
            visited.add((nr, nc))
            parent[(nr, nc)] = (r, c)

# Reconstruct path
cur = end
while cur and cur != start:
    r, c = cur
    if maze[r][c] not in ('S', 'E'):
        maze[r][c] = '*'
    cur = parent[cur]

# Final Maze
print("\nFinal Path:")
show(maze)
