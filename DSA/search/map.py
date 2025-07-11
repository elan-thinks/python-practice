import os

""""
    Map Layout:
    ────────────
    The 'park_map' is a 17x26 grid defined as a list of strings
    (each row turned into a list of characters). This represents
    a forest environment with a mix of terrain and hazards. :)
"""
legend = {
    "S": "Start Point",
    "E": "End : Goal",
    " ": "Walkable path, Normal ground",
    "#": "Wall/rock : impassable",
    "~": "Water body : Dangerous and impassable",
    "^": "Mountain : passable but slow",
    "¥": "Tree  : passable, but slow ,get slower in densed area",
    "$": "Snake : Dangerous and impassable",
    "=": "Bridge : Walkable ,but very slow",
    ".": "All Visited-free path",
    "X": "All Visited-Passable Terrains/Obstacles",
    "@": "The final best selected path",
}
# Define costs for different terrain types
cell_cost = {
    "S": 0,
    " ": 1,
    "^": 2,
    "#": float("inf"),
    "$": float("inf"),
    "~": float("inf"),
    "¥": 3,
   "¥¥": 4,
    "=": 5,
    "E": 0,
}
park_map = [
    list("##########################"),
    list("S    = ==~=   #       #  #"),
    list("   #^^ #  ## # #####  ^ # "),
    list("  =# # ^^    #     #==~ # "),
    list(" #=# ### #^¥ ##### # ¥¥ # "),
    list(" # # ~ # #  ¥^   # #    # "),
    list(" #=### ¥ ¥¥ #  ### #######"),
    list(" #     ¥$¥$  #     #     #"),
    list(" # ####¥¥¥^¥ #¥^¥# # ### #"),
    list(" #    #  ¥ ~     #     ^ #"),
    list("  =^=#### ¥ ¥ ### #^#¥#  #"),
    list("¥##¥    #      # ¥   # # E"),
    list(" # # ¥¥¥ ##### ^ #~~   # #"),
    list(" # #   #     # #     #   #"),
    list(" # ###=### # # # ¥¥¥ ~ ^¥#"),
    list("   ^¥    ¥   ^       ¥ ^ #"),
    list("##########################"),
]
#another map :)
# park_map = [
#     list("##########################"),
#     list("S  ^   ==~=    #      #  #"),
#     list("   #^^ ###¥¥ # #####  ^ # "),
#     list("  =# #       ¥     #==~ # "),
#     list(" #=# ### #^¥ ##### # ¥¥ # "),
#     list(" # # ~ #    ¥^   # #    # "),
#     list(" #=### ¥ ¥¥ # ^### #######"),
#     list(" #     ¥$¥$  #     #     #"),
#     list(" # ####¥¥¥^¥ #¥^¥# # ### #"),
#     list("      #  ¥ ~     =     ^ #"),
#     list(" ==^ #### ¥ ¥ ### # # #$^#"),
#     list(" #¥¥==          ¥¥  =# #  "),
#     list(" # # ¥¥¥^##### ^ #~~   #  "),
#     list(" # #   #     #         # #"),
#     list(" # ###=### # ### ¥¥¥ ~   #"),
#     list("   ^¥    ¥   ^       ^ ¥  "),
#     list("#########################E"),
# ]

direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]

"""
Sooo ,this custom-designed map help us to understand how different pathfinding algorithms behave.
We explored how the structure of a map can influence the paths chosen by each algorithm.

The explorer moves in four directions: left, right, up, and down.

DFS (Depth-First Search):
- Uses a stack, so it dives deep in one direction (usually down) before backtracking.
- It's unpredictable, can easily get lost, and doesn't consider cost at all — it may choose expensive paths just because they're next.
- Fun to watch, but not very trustworthy :)

BFS (Breadth-First Search):
- Uses a queue, so it spreads evenly and guarantees the shortest path in terms of steps.
- But it also ignores cost, often choosing to go through obstacles just because they’re closer.
- A bit of a risk taker :)!

UCS (Uniform Cost Search):
- Very cost-aware — avoids expensive terrain and carefully calculates each step.
- Sometimes ends up taking a longer path just to avoid costly tiles.
- Smart, but maybe too cautious and doesn't always consider the bigger picture.

Overall, designing and testing multiple maps helped us see the clear differences between algorithms.
Each one has its own logic and flaws — and that’s what made this so interesting!
"""


# small version of map...just for Test :)
# cell_cost = {"S": 0, " ": 1, "^": 2, "#": float("inf"), "~": float("inf"), "E": 0}

# park_map = [
#     list("###########"),
#     list("#S  #     #"),
#     list("#  ^^^  ^ #"),
#     list("#  E    ^ #"),
#     list("###########"),
# ]


def show(maze_map):
    os.system("cls" if os.name == "nt" else "clear")
    print(" ")
    for row in maze_map:
        print(" ".join(row))


show(park_map)
