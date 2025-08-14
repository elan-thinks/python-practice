import os
import random
import sys

import pygame

# ------------ CONFIG --------------------------
CELL_SIZE = 32
COLS, ROWS = 25, 17
FPS = 60
ASSETS_DIR = "assets"
# ----------------------------------------------

pygame.init()
screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pygame.display.set_caption("Image Tile map Game")
clock = pygame.time.Clock()


# ------------- LOAD IMAGES --------------------
def load_tile(name):
    path = os.path.join(ASSETS_DIR, name + ".png")
    return pygame.transform.scale(pygame.image.load(path), (CELL_SIZE, CELL_SIZE))


TERRAIN_TYPES = {
    "grass": load_tile("grass"),
    "water": load_tile("water"),
    "rocks": load_tile("rocks"),
    "road": load_tile("road"),
    "mountain": load_tile("mountain"),
}

terrain_map = [
    [random.choice(list(TERRAIN_TYPES.keys())) for _ in range(ROWS)]
    for _ in range(COLS)
]

# ------------- PLAYER -------------------------
player_pos = [0, 0]
player_img = pygame.Surface((CELL_SIZE - 3, CELL_SIZE - 3))
player_img.fill((255, 255, 0))


# ------------ DRAW FUNCTIONS ------------------
def draw_map():
    for x in range(COLS):
        for y in range(ROWS):
            terrain = terrain_map[x][y]
            img = TERRAIN_TYPES[terrain]
            screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE))


def draw_player():
    px, py = player_pos
    screen.blit(player_img, (px * CELL_SIZE + 4, py * CELL_SIZE + 4))


# ------------ INPUT HANDLING ------------------
def move_player(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < COLS and 0 <= new_y < ROWS:
        player_pos[0] = new_x
        player_pos[1] = new_y


# ---------------- MAIN LOOP -------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_player(-1, 0)
    if keys[pygame.K_RIGHT]:
        move_player(1, 0)
    if keys[pygame.K_UP]:
        move_player(0, -1)
    if keys[pygame.K_DOWN]:
        move_player(0, 1)

    screen.fill((0, 0, 0))
    draw_map()
    draw_player()
    pygame.display.flip()
    clock.tick(FPS)
