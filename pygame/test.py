import random
import sys

import pygame

# ---------------- CONFIG ------------------------
CELL_SIZE = 32
COLS, ROWS = 25, 17
FPS = 60
BG_COLOR = (30, 30, 30)
WALL_COLOR = (255, 255, 255)
VISITED_COLOR = (50, 150, 255)
# -------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pygame.display.set_caption("Maze Generator – Milestone 2")
clock = pygame.time.Clock()


# ---- Cell Class ----
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self, surf):
        x = self.x * CELL_SIZE
        y = self.y * CELL_SIZE

        if self.visited:
            pygame.draw.rect(surf, VISITED_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

        # Draw walls
        if self.walls["top"]:
            pygame.draw.line(surf, WALL_COLOR, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(
                surf, WALL_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2
            )
        if self.walls["bottom"]:
            pygame.draw.line(
                surf, WALL_COLOR, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2
            )
        if self.walls["left"]:
            pygame.draw.line(surf, WALL_COLOR, (x, y + CELL_SIZE), (x, y), 2)


# ---- Create Grid ----
grid = [[Cell(x, y) for y in range(ROWS)] for x in range(COLS)]

# ---- DFS Maze Generator State ----
stack = []
current = grid[0][0]
current.visited = True
stack.append(current)


# ---- Get neighbors ----
def get_unvisited_neighbors(cell):
    neighbors = []
    x, y = cell.x, cell.y

    directions = [
        ("top", (x, y - 1)),
        ("right", (x + 1, y)),
        ("bottom", (x, y + 1)),
        ("left", (x - 1, y)),
    ]

    for direction, (nx, ny) in directions:
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            neighbor = grid[nx][ny]
            if not neighbor.visited:
                neighbors.append((direction, neighbor))
    return neighbors


# ---- Remove walls between two cells ----
def remove_walls(current, next_cell, direction):
    opposites = {"top": "bottom", "right": "left", "bottom": "top", "left": "right"}
    current.walls[direction] = False
    next_cell.walls[opposites[direction]] = False


# ---- MAIN LOOP ----
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)

    # Draw grid
    for col in grid:
        for cell in col:
            cell.draw(screen)

    # Maze generation step
    if stack:
        current = stack[-1]
        neighbors = get_unvisited_neighbors(current)
        if neighbors:
            direction, next_cell = random.choice(neighbors)
            remove_walls(current, next_cell, direction)
            next_cell.visited = True
            stack.append(next_cell)
        else:
            stack.pop()

    pygame.display.flip()
    clock.tick(FPS)
