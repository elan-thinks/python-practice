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
    "~": "Water : Dangerous and impassable",
    "^": "Mountain : passable but slow" ,
    "¥": "Tree  : passable, but slow",
   "¥¥": "Dense forest : passable, but very slow",
    "$": "Snake : Dangerous and impassable",
    "=": "Bridge : Walkable ,but very slow",
    "X": "All Visited-Passable Terrains/Obstacles",
    "@": "The final best selected path"
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
# cell_cost = {"S": 0, ".": 1, "🌳": 2,"🌴": 2, "⛰️": 10,"~":3, "🌊":float("inf"),"#": float("inf"), "E": 0}
park_map = [
    list("##########################"),
    list("S  # = ==~=   #       #  #"),
    list("     ^ #  ## # #####  ^ # "),
    list("  =# #       #     #==~ # "),
    list(" #=# ### #^¥ ##### # ¥¥ # "),
    list(" # # ~ # #  ¥^   # #    # "),
    list(" #=### ¥ ¥¥ #  ### #######"),
    list(" #     ¥$¥$  #     #     #"),
    list(" # ####¥¥¥^¥ #¥^¥# # ### #"),
    list(" #    #  ¥ ~     #     ^ #"),
    list("  =^=#### ¥ ¥ ### #^#¥# ##"),
    list("¥# ¥    #      # ¥   # # #"),
    list("   # ¥¥¥ ##### ^ #~~   # #"),
    list(" # #   #     # #     #   #"),
    list(" # ###=### # # # ¥¥¥ ~ ^¥#"),
    list(" # ^     ~   ^       ¥ ^ E"),
    list("##########################"),
]
# park_map = [
#     list("S......#....🌊....#..🐉🐉...⛰️...#"),
#     list("..##..#.#.🌴🌴###.#.##⛰️🦁#..#.#.#"),
#     list("...🌴#......🌴.🌴.....#..#.🌋....#"),
#     list(".#.#.###.#.#.🦁🌳🦁🌳#.#.##.#....#"),
#     list(".#..⛰️🌊...#...🌊⛰️..#.#....#....#"),
#     list(".####⛰️.#..#🌳🌳🌴.###.#######...#"),
#     list(".#..🌳..#.....🐉..#.#....🌴🌴....#"),
#     list("....🌊.#.#🌳🌳##.###🌋..#.###....#"),
#     list(".#....🌳🌳🦁🌳..#.....#.#...#....#"),
#     list(".#.###🌳🌳##.🐉##🌋#.#.#.##.#.#..#"),
#     list(".⛰️...#...#..🌋.#.#...#.#.🐉.🌋..#"),
#     list(".🌴.#.#.#.##🌴🌴#.#.#🌊#...#.#...#"),
#     list(".#.#...#..🌊.#..#...🌳🌳...🌳#...#"),
#     list(".🌳.🌴🌴#..#🌊.#...#.#####.....#.."),
#     list("...🌳.🌳.........🌳.....🌊..#....E"),
# ]


def show(maze_map):
    os.system("cls" if os.name == "nt" else "clear")
    for row in maze_map:
        print(" ".join(row))


show(park_map)
