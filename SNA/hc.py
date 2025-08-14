import random

# Cities and coordinates (simple example)
cities = {
    "A": (12, 34),
    "B": (45, 67),
    "C": (23, 78),
    "D": (56, 12),
    "E": (34, 90),
    "F": (78, 56),
    "G": (90, 34),
    "H": (67, 89),
    "I": (11, 22),
    "J": (88, 77),
    "K": (54, 32),
    "L": (29, 65),
    "M": (73, 21),
    "N": (44, 55),
    "O": (19, 88),
    "P": (92, 14),
    "Q": (38, 48),
    "R": (60, 73),
    "S": (85, 49),
    "T": (15, 66),
    "U": (47, 28),
    "V": (64, 36),
    "W": (26, 57),
    "X": (32, 81),
    "Y": (59, 18),
    "Z": (40, 92),
    "AA": (75, 29),
    "AB": (28, 44),
    "AC": (53, 80),
    "AD": (17, 53),
    "AE": (71, 46),
    "AF": (30, 27),
    "AG": (49, 94),
    "AH": (83, 40),
    "AI": (66, 59),
    "AJ": (12, 97),
    "AK": (93, 61),
    "AL": (58, 33),
    "AM": (25, 73),
    "AN": (41, 19),
    "AO": (36, 86),
    "AP": (97, 54),
    "AQ": (21, 37),
    "AR": (82, 25),
    "AS": (46, 72),
    "AT": (61, 85),
    "AU": (18, 47),
    "AV": (27, 91),
    "AW": (50, 64),
    "AX": (76, 15),
    "AY": (69, 95),
    "AZ": (14, 60),
    "BA": (33, 50),
    "BB": (80, 32),
    "BC": (57, 99)
}


# Calculate Euclidean distance between two points
def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# Calculate total route distance
def route_distance(route):
    dist = 0
    for i in range(len(route)):
        city1 = route[i]
        city2 = route[(i + 1) % len(route)]  # wrap around to start
        dist += distance(cities[city1], cities[city2])
    return dist

# 2-opt swap
def two_opt_swap(route, i, k):
    new_route = route[:i] + route[i:k+1][::-1] + route[k+1:]
    return new_route

# Hill Climbing using 2-opt
def hill_climbing_2opt(route):
    best_distance = route_distance(route)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for k in range(i + 1, len(route)):
                new_route = two_opt_swap(route, i, k)
                new_distance = route_distance(new_route)
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True
                    break
            if improved:
                break
    return route, best_distance

# Initial random route
initial_route = list(cities.keys())
random.shuffle(initial_route)

print("Initial route:", initial_route)
print("Initial distance:", route_distance(initial_route))

best_route, best_distance = hill_climbing_2opt(initial_route)

print("\nBest route found:", best_route)
print("Best distance:", best_distance)
