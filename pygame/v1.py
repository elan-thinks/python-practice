import sys

import pygame_gui

import pygame

# --- Constants ---
WIDTH, HEIGHT = 800, 640
ROWS, COLS = 8, 8
TILE_SIZE = 60
FPS = 60

# Grid types
EMPTY, TREE, ROCK, HIKER, GOAL, PATH = range(6)

# Colors
GREEN = (170, 215, 81)
DARK_GREEN = (110, 170, 70)
BROWN = (139, 69, 19)
GRAY = (120, 120, 120)
BLUE = (173, 216, 230)
ORANGE = (255, 150, 50)
WHITE = (255, 255, 255)
BEIGE = (250, 230, 190)

# Sample map Data
map_data = [
    [0, 1, 0, 0, 2, 0, 0, 4],
    [0, 1, 0, 0, 2, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 2, 0],
    [2, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 2, 0, 0, 1, 0],
    [0, 2, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 2, 0, 0, 0],
    [3, 0, 0, 0, 1, 0, 2, 0],
]
mock_path = [
    (7, 0),
    (6, 1),
    (5, 2),
    (4, 3),
    (3, 4),
    (2, 4),
    (1, 4),
    (0, 4),
    (0, 5),
    (0, 6),
    (0, 7),
]

# --- Init Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost Hiker – Real GUI")
clock = pygame.time.Clock()

# Font for emojis
font = pygame.font.SysFont("Arial", 24)

# --- Init UI Manager ---
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=["BFS", "DFS", "UCS"],
    starting_option="BFS",
    relative_rect=pygame.Rect((10, 10), (100, 30)),
    manager=ui_manager,
)

start_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((120, 10), (80, 30)), text="Start", manager=ui_manager
)
pause_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((210, 10), (80, 30)), text="Pause", manager=ui_manager
)
reset_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 10), (80, 30)), text="Reset", manager=ui_manager
)

status_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((400, 10), (300, 30)),
    text="Steps: 0 | Time: 0.0s | Mode: BFS",
    manager=ui_manager,
)


# --- Draw Functions ---
def draw_tile(x, y, type):
    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    if type == EMPTY:
        pygame.draw.rect(screen, GREEN, rect)
    elif type == TREE:
        pygame.draw.rect(screen, DARK_GREEN, rect)
    elif type == ROCK:
        pygame.draw.rect(screen, GRAY, rect)
    elif type == HIKER:
        pygame.draw.rect(screen, ORANGE, rect)
        screen.blit(font.render("🧍", True, WHITE), (x + 15, y + 10))
    elif type == GOAL:
        pygame.draw.rect(screen, BROWN, rect)
        screen.blit(font.render("⛺", True, WHITE), (x + 15, y + 10))
    elif type == PATH:
        pygame.draw.rect(screen, BLUE, rect)


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            tile_type = map_data[row][col]
            if (row, col) in mock_path:
                draw_tile(col * TILE_SIZE, row * TILE_SIZE + 50, PATH)
            draw_tile(col * TILE_SIZE, row * TILE_SIZE + 50, tile_type)
            pygame.draw.rect(
                screen,
                WHITE,
                (col * TILE_SIZE, row * TILE_SIZE + 50, TILE_SIZE, TILE_SIZE),
                1,
            )


# --- Main Loop ---
def main():
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui_manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_btn:
                    print("Start clicked!")
                elif event.ui_element == pause_btn:
                    print("Pause clicked!")
                elif event.ui_element == reset_btn:
                    print("Reset clicked!")

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                selected = dropdown.selected_option
                print("Algorithm changed to:", selected)
                status_label.set_text(f"Steps: 0 | Time: 0.0s | Mode: {selected}")

        ui_manager.update(dt)
        screen.fill(BEIGE)
        draw_grid()
        ui_manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
