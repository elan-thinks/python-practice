import heapq
import sys
from collections import deque

import pygame

# Constants
TILE_SIZE = 64
GRID_WIDTH = 5
GRID_HEIGHT = 5
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH + 200  # Extra space for UI
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT
FPS = 60

# Terrain types
TRAIL = 0  # Cost 1
FOREST = 1  # Cost 3
WATER = 2  # Impassable

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BLUE = (30, 144, 255)
BROWN = (139, 69, 19)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lost Hiker Pathfinding")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# Sample grid from the assignment
grid = [
    [0, 0, 1, 2, 0],
    [1, 2, 0, 1, 0],
    [0, 1, 0, 2, 0],
    [0, 0, 0, 1, 0],
    [2, 1, 2, 0, 0],
]

# Game state
start_pos = (0, 0)
end_pos = (4, 4)
current_algorithm = "BFS"  # Default algorithm
path = []
explored_nodes = []
total_cost = 0
running = True


def draw_grid():
    """Draw the grid with terrain colors"""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            # Draw terrain
            if grid[y][x] == TRAIL:
                pygame.draw.rect(screen, GREEN, rect)
            elif grid[y][x] == FOREST:
                pygame.draw.rect(screen, DARK_GREEN, rect)
            elif grid[y][x] == WATER:
                pygame.draw.rect(screen, BLUE, rect)

            # Draw grid lines
            pygame.draw.rect(screen, BLACK, rect, 1)

            # Draw start and end positions
            if (x, y) == start_pos:
                pygame.draw.rect(screen, RED, rect.inflate(-10, -10))
            elif (x, y) == end_pos:
                pygame.draw.rect(screen, YELLOW, rect.inflate(-10, -10))

            # Draw explored nodes (faded)
            if (
                (x, y) in explored_nodes
                and (x, y) not in path
                and (x, y) != start_pos
                and (x, y) != end_pos
            ):
                s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                s.fill((255, 255, 0, 128))  # Yellow with transparency
                screen.blit(s, (x * TILE_SIZE, y * TILE_SIZE))

            # Draw path
            if (x, y) in path and (x, y) != start_pos and (x, y) != end_pos:
                pygame.draw.rect(
                    screen, (255, 165, 0), rect.inflate(-15, -15)
                )  # Orange


def draw_ui():
    """Draw the UI panel on the right"""
    panel_rect = pygame.Rect(GRID_WIDTH * TILE_SIZE, 0, 200, SCREEN_HEIGHT)
    pygame.draw.rect(screen, GRAY, panel_rect)

    # Title
    title = font.render("Lost Hiker Pathfinding", True, BLACK)
    screen.blit(title, (GRID_WIDTH * TILE_SIZE + 10, 10))

    # Algorithm selection
    algo_text = font.render("Select Algorithm:", True, BLACK)
    screen.blit(algo_text, (GRID_WIDTH * TILE_SIZE + 10, 50))

    # Algorithm buttons
    algorithms = ["BFS", "DFS", "UCS"]
    for i, algo in enumerate(algorithms):
        color = (100, 200, 100) if algo == current_algorithm else (200, 200, 200)
        btn_rect = pygame.Rect(GRID_WIDTH * TILE_SIZE + 10, 80 + i * 30, 180, 25)
        pygame.draw.rect(screen, color, btn_rect)
        pygame.draw.rect(screen, BLACK, btn_rect, 1)
        algo_label = font.render(algo, True, BLACK)
        screen.blit(algo_label, (btn_rect.x + 5, btn_rect.y + 5))

    # Results
    if path:
        results_text = font.render(f"Algorithm: {current_algorithm}", True, BLACK)
        screen.blit(results_text, (GRID_WIDTH * TILE_SIZE + 10, 180))

        cost_text = font.render(f"Total Cost: {total_cost}", True, BLACK)
        screen.blit(cost_text, (GRID_WIDTH * TILE_SIZE + 10, 200))

        nodes_text = font.render(f"Nodes Explored: {len(explored_nodes)}", True, BLACK)
        screen.blit(nodes_text, (GRID_WIDTH * TILE_SIZE + 10, 220))

        path_text = font.render(f"Path Length: {len(path)}", True, BLACK)
        screen.blit(path_text, (GRID_WIDTH * TILE_SIZE + 10, 240))

        # Path coordinates
        path_coords = font.render("Path:", True, BLACK)
        screen.blit(path_coords, (GRID_WIDTH * TILE_SIZE + 10, 260))

        for i, (x, y) in enumerate(path[:5]):  # Show first 5 path steps
            coord_text = font.render(f"({x}, {y})", True, BLACK)
            screen.blit(coord_text, (GRID_WIDTH * TILE_SIZE + 10, 280 + i * 20))

        if len(path) > 5:
            dots_text = font.render("...", True, BLACK)
            screen.blit(dots_text, (GRID_WIDTH * TILE_SIZE + 10, 280 + 5 * 20))


def get_terrain_cost(x, y):
    """Return the cost of moving to this cell"""
    if grid[y][x] == TRAIL:
        return 1
    elif grid[y][x] == FOREST:
        return 3
    return float("inf")  # Water is impassable


def get_neighbors(x, y):
    """Return valid neighboring cells (up, down, left, right)"""
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] != WATER:
            neighbors.append((nx, ny))
    return neighbors


def bfs(start, end):
    """Breadth-First Search implementation"""
    queue = deque([(start, [start])])
    visited = set([start])
    explored = set([start])

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            return path, explored

        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                explored.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return None, explored  # No path found


def dfs(start, end):
    """Depth-First Search implementation"""
    stack = [(start, [start])]
    visited = set([start])
    explored = set([start])

    while stack:
        (x, y), path = stack.pop()

        if (x, y) == end:
            return path, explored

        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                explored.add((nx, ny))
                stack.append(((nx, ny), path + [(nx, ny)]))

    return None, explored  # No path found


def ucs(start, end):
    """Uniform Cost Search implementation"""
    heap = []
    heapq.heappush(heap, (0, start, [start]))
    visited = set([start])
    explored = set([start])

    while heap:
        cost, (x, y), path = heapq.heappop(heap)

        if (x, y) == end:
            return path, explored, cost

        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                explored.add((nx, ny))
                new_cost = cost + get_terrain_cost(nx, ny)
                heapq.heappush(heap, (new_cost, (nx, ny), path + [(nx, ny)]))

    return None, explored, 0  # No path found


def run_algorithm():
    """Run the selected algorithm and update results"""
    global path, explored_nodes, total_cost

    if current_algorithm == "BFS":
        path, explored_nodes = bfs(start_pos, end_pos)
        if path:
            total_cost = sum(
                get_terrain_cost(x, y) for (x, y) in path[1:]
            )  # Exclude start position
        else:
            total_cost = 0
    elif current_algorithm == "DFS":
        path, explored_nodes = dfs(start_pos, end_pos)
        if path:
            total_cost = sum(get_terrain_cost(x, y) for (x, y) in path[1:])
        else:
            total_cost = 0
    elif current_algorithm == "UCS":
        path, explored_nodes, total_cost = ucs(start_pos, end_pos)


# Initial run
run_algorithm()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Check if clicked on grid
            if mx < GRID_WIDTH * TILE_SIZE:
                tx = mx // TILE_SIZE
                ty = my // TILE_SIZE

                # Left click sets start position
                if event.button == 1 and grid[ty][tx] != WATER:
                    start_pos = (tx, ty)
                    run_algorithm()

                # Right click sets end position
                elif event.button == 3 and grid[ty][tx] != WATER:
                    end_pos = (tx, ty)
                    run_algorithm()

            # Check if clicked on algorithm buttons
            elif GRID_WIDTH * TILE_SIZE <= mx < SCREEN_WIDTH:
                if 80 <= my <= 155:  # Algorithm buttons area
                    algo_index = (my - 80) // 30
                    if 0 <= algo_index <= 2:
                        current_algorithm = ["BFS", "DFS", "UCS"][algo_index]
                        run_algorithm()

    # Drawing
    screen.fill(WHITE)
    draw_grid()
    draw_ui()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
