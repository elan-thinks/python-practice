import csv
import json
import sys

import pygame

# ────────────────────────────────────────────────────────────
# CONSTANTS
# ────────────────────────────────────────────────────────────
TILE_SIZE = 16
PADDING = 1  # 1px padding in tileset
map_WIDTH = 40
map_HEIGHT = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Tools
TOOL_TERRAIN = 0
TOOL_DECOR = 1
TOOL_BRUSH = 2  # New brush tool
current_tool = TOOL_TERRAIN
selected_tile_index = 0
brush_size = 1  # Default brush size

# View settings
camera_x, camera_y = 0, 0
zoom_level = 1.0
MAX_ZOOM = 4.0
MIN_ZOOM = 0.5

# Undo system
undo_stack = []
undo_limit = 20  # Max undo steps to keep

GRASS = 0
GRASS_DOT = 1
GRASS_PATCHY = 2
GRASS_FULL = 3
GRASS_FULL = 4

CLIFF_TL = 5
CLIFF_TR = 6
CLIFF_BL = 7
CLIFF_BR = 8
CLIFF_IN_TL = 9
CLIFF_IN_TR = 10
CLIFF_IN_BL = 11
CLIFF_IN_BR = 12

WATER_TL = 13
WATER_TR = 14
WATER_BL = 15
WATER_BR = 16
WATER_LILY = 17
WATER_CENTER = 18
WATER_BOTTOM = 19

DEC_TREE_SMALL = 0
DEC_TREE_STUMP_LEFT = 1
DEC_TREE_STUMP_RIGHT = 2
DEC_MUSHROOM_RED1 = 3
DEC_MUSHROOM_RED2 = 4
DEC_LOG_HORIZONTAL = 5
DEC_REED_SMALL = 6
DEC_REED_MEDIUM = 7
DEC_REED_TALL = 8
DEC_ROCK_SMALL = 9
DEC_ROCK_MEDIUM = 10
DEC_ROCK_BIG = 11
DEC_TREE_BIG_TL = 12  # part of large tree (top‑left)
DEC_TREE_BIG_TR = 13
DEC_TREE_BIG_BL = 14
DEC_TREE_BIG_BR = 15
DEC_TREE_PINE_TOP = 16
DEC_TREE_PINE_MID = 17
DEC_TREE_PINE_BASE = 18

DECOR_NAMES = {
    0: "TREE_SMALL",
    1: "TREE_STUMP_L",
    2: "TREE_STUMP_R",
    3: "MUSHROOM_RED1",
    4: "MUSHROOM_RED2",
    5: "LOG_HORZ",
    6: "REED_S",
    7: "REED_M",
    8: "REED_L",
    9: "ROCK_S",
    10: "ROCK_M",
    11: "ROCK_L",
    12: "TREE_BIG_TL",
    13: "TREE_BIG_TR",
    14: "TREE_BIG_BL",
    15: "TREE_BIG_BR",
    16: "TREE_PINE_TOP",
    17: "TREE_PINE_MID",
    18: "TREE_PINE_BASE",
}

# ────────────────────────────────────────────────────────────
# INITIALISE PYGAME
# ────────────────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Forest Tileset Demo – Terrain + Decorations")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)

# ────────────────────────────────────────────────────────────
# LOAD GRAPHICS
# ────────────────────────────────────────────────────────────
tileset_img = pygame.image.load(
    "assets/TopDownFantasy-Forest/Tiles/Tileset1xPadding.png"
).convert_alpha()
decor_img = pygame.image.load(
    "assets/TopDownFantasy-Forest/Decorations/Decorations.png"
).convert_alpha()


def draw_palette():
    palette_width = 100
    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (SCREEN_WIDTH - palette_width, 0, palette_width, SCREEN_HEIGHT),
    )

    # Draw tool selection buttons
    tools = ["Terrain", "Decor", "Brush"]
    for i, tool in enumerate(tools):
        color = (100, 100, 255) if current_tool == i else (70, 70, 70)
        pygame.draw.rect(
            screen,
            color,
            (SCREEN_WIDTH - palette_width + 5, 5 + i * 25, palette_width - 10, 20),
        )
        text = font.render(tool, True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH - palette_width + 15, 10 + i * 25))

    # Draw brush size selector if brush tool is active
    if current_tool == TOOL_BRUSH:
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (SCREEN_WIDTH - palette_width + 5, 80, palette_width - 10, 20),
        )
        text = font.render(f"Size: {brush_size}", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH - palette_width + 15, 85))

    # Draw tile palette
    tile_list = tiles if current_tool == TOOL_TERRAIN else decorations
    for i, tile in enumerate(tile_list):
        x = SCREEN_WIDTH - 96 + (i % 2) * (TILE_SIZE + 4)
        y = 110 + (i // 2) * (TILE_SIZE + 4)
        scaled_tile = pygame.transform.scale(
            tile, (int(TILE_SIZE * zoom_level), int(TILE_SIZE * zoom_level))
        )
        screen.blit(scaled_tile, (x, y))
        if i == selected_tile_index:
            pygame.draw.rect(
                screen, (255, 255, 0), (x - 1, y - 1, TILE_SIZE + 2, TILE_SIZE + 2), 2
            )


def slice_padded_tileset(
    sheet: pygame.Surface, w: int, h: int, padding: int
) -> list[pygame.Surface]:
    tiles = []
    sw, sh = sheet.get_size()
    cols = (sw + padding) // (w + padding)
    rows = (sh + padding) // (h + padding)
    for row in range(rows):
        for col in range(cols):
            x = col * (w + padding)
            y = row * (h + padding)
            tiles.append(sheet.subsurface(pygame.Rect(x, y, w, h)))
    return tiles


def slice_sheet(sheet: pygame.Surface, w: int, h: int) -> list[pygame.Surface]:
    tiles = []
    sw, sh = sheet.get_size()
    for y in range(0, sh, h):
        for x in range(0, sw, w):
            tiles.append(sheet.subsurface(pygame.Rect(x, y, w, h)))
    return tiles


tiles = slice_padded_tileset(tileset_img, TILE_SIZE, TILE_SIZE, PADDING)
decorations = slice_sheet(decor_img, TILE_SIZE, TILE_SIZE)

# ────────────────────────────────────────────────────────────
# DATA ‑‑ TERRAIN & DECORATION mapS
# ────────────────────────────────────────────────────────────
map_layout = [[GRASS_FULL for _ in range(map_WIDTH)] for _ in range(map_HEIGHT)]
decor_map = [[None for _ in range(map_WIDTH)] for _ in range(map_HEIGHT)]


# ────────────────────────────────────────────────────────────
# UNDO SYSTEM
# ────────────────────────────────────────────────────────────
def save_state():
    """Save the current state of both maps for undo functionality"""
    if len(undo_stack) >= undo_limit:
        undo_stack.pop(0)

    # Save copies of both maps
    terrain_copy = [row[:] for row in map_layout]
    decor_copy = [row[:] for row in decor_map]
    undo_stack.append((terrain_copy, decor_copy))


def undo():
    """Revert to the previous state"""
    if undo_stack:
        terrain_copy, decor_copy = undo_stack.pop()
        for y in range(map_HEIGHT):
            for x in range(map_WIDTH):
                map_layout[y][x] = terrain_copy[y][x]
                decor_map[y][x] = decor_copy[y][x]


# ────────────────────────────────────────────────────────────
# SAVE/LOAD FUNCTIONS
# ────────────────────────────────────────────────────────────
def save_to_csv(filename):
    """Save the map data to a CSV file"""
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Save terrain map
        writer.writerow(["TERRAIN map"])
        for row in map_layout:
            writer.writerow(row)
        # Save decoration map
        writer.writerow(["DECORATION map"])
        for row in decor_map:
            writer.writerow([str(x) if x is not None else "None" for x in row])


def load_from_csv(filename):
    """Load map data from a CSV file"""
    global map_layout, decor_map
    try:
        with open(filename, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            current_map = None
            map_layout = []
            decor_map = []

            for row in reader:
                if not row:
                    continue
                if row[0] == "TERRAIN map":
                    current_map = "terrain"
                    continue
                elif row[0] == "DECORATION map":
                    current_map = "decor"
                    continue

                if current_map == "terrain":
                    map_layout.append([int(x) for x in row])
                elif current_map == "decor":
                    decor_map.append([int(x) if x != "None" else None for x in row])

        # Ensure maps are the correct size
        map_layout = map_layout[:map_HEIGHT]
        decor_map = decor_map[:map_HEIGHT]
        for y in range(len(map_layout)):
            map_layout[y] = map_layout[y][:map_WIDTH]
        for y in range(len(decor_map)):
            decor_map[y] = decor_map[y][:map_WIDTH]

        # Fill any missing space
        for y in range(len(map_layout), map_HEIGHT):
            map_layout.append([GRASS_FULL] * map_WIDTH)
        for y in range(len(decor_map), map_HEIGHT):
            decor_map.append([None] * map_WIDTH)
        for y in range(map_HEIGHT):
            if len(map_layout[y]) < map_WIDTH:
                map_layout[y].extend([GRASS_FULL] * (map_WIDTH - len(map_layout[y])))
            if len(decor_map[y]) < map_WIDTH:
                decor_map[y].extend([None] * (map_WIDTH - len(decor_map[y])))

        save_state()  # Save the loaded state for undo
        return True
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return False


def save_to_json(filename):
    """Save the map data to a JSON file"""
    data = {
        "terrain": map_layout,
        "decor": [[x if x is not None else "None" for x in row] for row in decor_map],
        "metadata": {
            "tile_size": TILE_SIZE,
            "map_width": map_WIDTH,
            "map_height": map_HEIGHT,
        },
    }
    with open(filename, "w") as jsonfile:
        json.dump(data, jsonfile, indent=2)


def load_from_json(filename):
    """Load map data from a JSON file"""
    global map_layout, decor_map
    try:
        with open(filename, "r") as jsonfile:
            data = json.load(jsonfile)
            map_layout = data.get(
                "terrain", [[GRASS_FULL] * map_WIDTH for _ in range(map_HEIGHT)]
            )
            decor_data = data.get(
                "decor", [[None] * map_WIDTH for _ in range(map_HEIGHT)]
            )

            # Convert 'None' strings back to None
            decor_map = []
            for row in decor_data:
                new_row = []
                for item in row:
                    if item == "None":
                        new_row.append(None)
                    else:
                        new_row.append(int(item))
                decor_map.append(new_row)

            # Ensure maps are the correct size
            map_layout = map_layout[:map_HEIGHT]
            decor_map = decor_map[:map_HEIGHT]
            for y in range(len(map_layout)):
                map_layout[y] = map_layout[y][:map_WIDTH]
            for y in range(len(decor_map)):
                decor_map[y] = decor_map[y][:map_WIDTH]

            # Fill any missing space
            for y in range(len(map_layout), map_HEIGHT):
                map_layout.append([GRASS_FULL] * map_WIDTH)
            for y in range(len(decor_map), map_HEIGHT):
                decor_map.append([None] * map_WIDTH)
            for y in range(map_HEIGHT):
                if len(map_layout[y]) < map_WIDTH:
                    map_layout[y].extend(
                        [GRASS_FULL] * (map_WIDTH - len(map_layout[y]))
                    )
                if len(decor_map[y]) < map_WIDTH:
                    decor_map[y].extend([None] * (map_WIDTH - len(decor_map[y])))

            save_state()  # Save the loaded state for undo
            return True
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return False


def save_to_txt(filename):
    """Save the map data to a simple text file"""
    with open(filename, "w") as txtfile:
        # Save terrain map
        txtfile.write("TERRAIN map\n")
        for row in map_layout:
            txtfile.write(",".join(map(str, row)) + "\n")
        # Save decoration map
        txtfile.write("DECORATION map\n")
        for row in decor_map:
            txtfile.write(
                ",".join(str(x) if x is not None else "None" for x in row) + "\n"
            )


def load_from_txt(filename):
    """Load map data from a text file"""
    global map_layout, decor_map
    try:
        with open(filename, "r") as txtfile:
            current_map = None
            map_layout = []
            decor_map = []

            for line in txtfile:
                line = line.strip()
                if not line:
                    continue
                if line == "TERRAIN map":
                    current_map = "terrain"
                    continue
                elif line == "DECORATION map":
                    current_map = "decor"
                    continue

                if current_map == "terrain":
                    map_layout.append([int(x) for x in line.split(",")])
                elif current_map == "decor":
                    decor_map.append(
                        [int(x) if x != "None" else None for x in line.split(",")]
                    )

        # Ensure maps are the correct size
        map_layout = map_layout[:map_HEIGHT]
        decor_map = decor_map[:map_HEIGHT]
        for y in range(len(map_layout)):
            map_layout[y] = map_layout[y][:map_WIDTH]
        for y in range(len(decor_map)):
            decor_map[y] = decor_map[y][:map_WIDTH]

        # Fill any missing space
        for y in range(len(map_layout), map_HEIGHT):
            map_layout.append([GRASS_FULL] * map_WIDTH)
        for y in range(len(decor_map), map_HEIGHT):
            decor_map.append([None] * map_WIDTH)
        for y in range(map_HEIGHT):
            if len(map_layout[y]) < map_WIDTH:
                map_layout[y].extend([GRASS_FULL] * (map_WIDTH - len(map_layout[y])))
            if len(decor_map[y]) < map_WIDTH:
                decor_map[y].extend([None] * (map_WIDTH - len(decor_map[y])))

        save_state()  # Save the loaded state for undo
        return True
    except Exception as e:
        print(f"Error loading TXT: {e}")
        return False


# ────────────────────────────────────────────────────────────
# DRAW HELPERS
# ────────────────────────────────────────────────────────────
def draw_map() -> None:
    """Draw the terrain map with camera and zoom adjustments"""
    scaled_tile_size = int(TILE_SIZE * zoom_level)

    # Calculate visible area
    start_x = max(0, camera_x // scaled_tile_size)
    start_y = max(0, camera_y // scaled_tile_size)
    end_x = min(map_WIDTH, (camera_x + SCREEN_WIDTH) // scaled_tile_size + 1)
    end_y = min(map_HEIGHT, (camera_y + SCREEN_HEIGHT) // scaled_tile_size + 1)

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            tile_index = map_layout[y][x]
            if 0 <= tile_index < len(tiles):
                # Calculate screen position with camera offset
                screen_x = x * scaled_tile_size - camera_x
                screen_y = y * scaled_tile_size - camera_y

                # Only draw if visible on screen
                if (
                    -scaled_tile_size <= screen_x < SCREEN_WIDTH
                    and -scaled_tile_size <= screen_y < SCREEN_HEIGHT
                ):
                    scaled_tile = pygame.transform.scale(
                        tiles[tile_index], (scaled_tile_size, scaled_tile_size)
                    )
                    screen.blit(scaled_tile, (screen_x, screen_y))


def draw_decorations() -> None:
    """Draw decorations with camera and zoom adjustments"""
    scaled_tile_size = int(TILE_SIZE * zoom_level)

    # Calculate visible area
    start_x = max(0, camera_x // scaled_tile_size)
    start_y = max(0, camera_y // scaled_tile_size)
    end_x = min(map_WIDTH, (camera_x + SCREEN_WIDTH) // scaled_tile_size + 1)
    end_y = min(map_HEIGHT, (camera_y + SCREEN_HEIGHT) // scaled_tile_size + 1)

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            deco_index = decor_map[y][x]
            if deco_index is not None and 0 <= deco_index < len(decorations):
                # Calculate screen position with camera offset
                screen_x = x * scaled_tile_size - camera_x
                screen_y = y * scaled_tile_size - camera_y

                # Only draw if visible on screen
                if (
                    -scaled_tile_size <= screen_x < SCREEN_WIDTH
                    and -scaled_tile_size <= screen_y < SCREEN_HEIGHT
                ):
                    scaled_deco = pygame.transform.scale(
                        decorations[deco_index], (scaled_tile_size, scaled_tile_size)
                    )
                    screen.blit(scaled_deco, (screen_x, screen_y))


def draw_ui():
    """Draw UI elements like status text"""
    # Display current tool and coordinates
    tools = ["Terrain", "Decor", "Brush"]
    status_text = (
        f"Tool: {tools[current_tool]} | Zoom: {zoom_level:.1f}x | Brush: {brush_size}"
    )
    text_surface = font.render(status_text, True, (255, 255, 255))
    screen.blit(text_surface, (5, 5))

    # Display save/load instructions
    help_text = "S: Save | L: Load | Z: Undo | Mouse Wheel: Zoom | +/-: Brush Size"
    help_surface = font.render(help_text, True, (200, 200, 200))
    screen.blit(help_surface, (5, SCREEN_HEIGHT - 20))


# ────────────────────────────────────────────────────────────
# BRUSH TOOL FUNCTIONS
# ────────────────────────────────────────────────────────────
def apply_brush(x, y, place=True):
    """Apply the brush at the given tile coordinates"""
    save_state()  # Save state before brush application for undo

    half_brush = brush_size // 2
    start_x = max(0, x - half_brush)
    start_y = max(0, y - half_brush)
    end_x = min(map_WIDTH - 1, x + half_brush)
    end_y = min(map_HEIGHT - 1, y + half_brush)

    for brush_y in range(start_y, end_y + 1):
        for brush_x in range(start_x, end_x + 1):
            if current_tool == TOOL_TERRAIN:
                if place:
                    map_layout[brush_y][brush_x] = selected_tile_index
                else:
                    map_layout[brush_y][brush_x] = GRASS_FULL
            elif current_tool == TOOL_DECOR:
                if place:
                    decor_map[brush_y][brush_x] = selected_tile_index
                else:
                    decor_map[brush_y][brush_x] = None


# ────────────────────────────────────────────────────────────
# MAIN LOOP
# ────────────────────────────────────────────────────────────
running = True
dragging = False
last_mouse_pos = (0, 0)

# Save initial state
save_state()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                current_tool = (current_tool + 1) % 3  # Cycle through tools
                selected_tile_index = 0  # reset selection on switch

            # Save/Load shortcuts
            elif event.key == pygame.K_s:
                # Open a simple dialog to choose save format
                print("Save options: 1) CSV 2) JSON 3) TXT")
                choice = input("Choose format (1-3): ")
                if choice == "1":
                    save_to_csv("map_data.csv")
                    print("Saved to map_data.csv")
                elif choice == "2":
                    save_to_json("map_data.json")
                    print("Saved to map_data.json")
                elif choice == "3":
                    save_to_txt("map_data.txt")
                    print("Saved to map_data.txt")

            elif event.key == pygame.K_l:
                # Open a simple dialog to choose load format
                print("Load options: 1) CSV 2) JSON 3) TXT")
                choice = input("Choose format (1-3): ")
                if choice == "1":
                    if load_from_csv("map_data.csv"):
                        print("Loaded from map_data.csv")
                    else:
                        print("Error loading CSV")
                elif choice == "2":
                    if load_from_json("map_data.json"):
                        print("Loaded from map_data.json")
                    else:
                        print("Error loading JSON")
                elif choice == "3":
                    if load_from_txt("map_data.txt"):
                        print("Loaded from map_data.txt")
                    else:
                        print("Error loading TXT")

            # Undo shortcut
            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                undo()

            # Brush size adjustment
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                brush_size = min(brush_size + 2, 9)  # Max brush size 9
            elif event.key == pygame.K_MINUS:
                brush_size = max(brush_size - 2, 1)  # Min brush size 1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            last_mouse_pos = (mx, my)

            # Check if clicked inside palette
            if mx >= SCREEN_WIDTH - 100:
                tile_list = tiles if current_tool == TOOL_TERRAIN else decorations
                for i in range(len(tile_list)):
                    x = SCREEN_WIDTH - 96 + (i % 2) * (TILE_SIZE + 4)
                    y = 110 + (i // 2) * (TILE_SIZE + 4)
                    tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    if tile_rect.collidepoint(mx, my):
                        selected_tile_index = i
                        break
            else:
                # map click
                scaled_tile_size = int(TILE_SIZE * zoom_level)
                tx = (mx + camera_x) // scaled_tile_size
                ty = (my + camera_y) // scaled_tile_size

                if 0 <= tx < map_WIDTH and 0 <= ty < map_HEIGHT:
                    save_state()  # Save before making changes

                    if event.button == 1:  # left click = place
                        if current_tool == TOOL_BRUSH:
                            apply_brush(tx, ty, place=True)
                        elif current_tool == TOOL_TERRAIN:
                            map_layout[ty][tx] = selected_tile_index
                        else:
                            decor_map[ty][tx] = selected_tile_index
                    elif event.button == 3:  # right click = erase
                        if current_tool == TOOL_BRUSH:
                            apply_brush(tx, ty, place=False)
                        elif current_tool == TOOL_TERRAIN:
                            map_layout[ty][tx] = GRASS_FULL
                        else:
                            decor_map[ty][tx] = None

                # Middle mouse button for dragging
                elif event.button == 2:
                    dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:  # Middle mouse button
                dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mx, my = pygame.mouse.get_pos()
                dx, dy = mx - last_mouse_pos[0], my - last_mouse_pos[1]
                camera_x = max(
                    0,
                    min(
                        camera_x - dx,
                        map_WIDTH * int(TILE_SIZE * zoom_level) - SCREEN_WIDTH,
                    ),
                )
                camera_y = max(
                    0,
                    min(
                        camera_y - dy,
                        map_HEIGHT * int(TILE_SIZE * zoom_level) - SCREEN_HEIGHT,
                    ),
                )
                last_mouse_pos = (mx, my)

        elif event.type == pygame.MOUSEWHEEL:
            # Zoom in/out with mouse wheel
            zoom_delta = 0.1 if event.y > 0 else -0.1
            new_zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom_level + zoom_delta))

            # Adjust camera to zoom toward mouse position
            mx, my = pygame.mouse.get_pos()

            # Calculate world coordinates before zoom
            world_x = mx + camera_x
            world_y = my + camera_y

            # Apply zoom
            zoom_level = new_zoom

            # Calculate new camera position to keep mouse over same world point
            camera_x = world_x - mx
            camera_y = world_y - my

            # Clamp camera to map bounds
            max_camera_x = max(
                0, map_WIDTH * int(TILE_SIZE * zoom_level) - SCREEN_WIDTH
            )
            max_camera_y = max(
                0, map_HEIGHT * int(TILE_SIZE * zoom_level) - SCREEN_HEIGHT
            )
            camera_x = max(0, min(camera_x, max_camera_x))
            camera_y = max(0, min(camera_y, max_camera_y))

    # Drawing
    screen.fill((0, 0, 0))  # clear
    draw_map()
    draw_decorations()
    draw_palette()
    draw_ui()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
