import math
import random

# import map

# ======================
# PROBLEM DEFINITION
# ======================
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


# ======================
# CORE FUNCTIONS
# ======================
def distance(p1, p2):
    """Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def route_distance(route):
    """Total cost of a TSP route"""
    total = 0
    for i in range(len(route)):
        city1 = route[i]
        city2 = route[(i + 1) % len(route)]  # Loop back to start
        total += distance(cities[city1], cities[city2])
    return total

def get_neighbor(route):
    """Generate neighbor solution via 2-opt swap"""
    i, k = sorted(random.sample(range(1, len(route)), 2))
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

# ======================
# SIMULATED ANNEALING
# ======================
def simulated_annealing(initial_route, initial_temp, cooling_rate, min_temp, max_iter):
    current_route = initial_route.copy()
    current_cost = route_distance(current_route)
    best_route = current_route.copy()
    best_cost = current_cost

    temp = initial_temp
    iteration = 0

    while temp > min_temp and iteration < max_iter:
        # Generate neighbor
        neighbor_route = get_neighbor(current_route)
        neighbor_cost = route_distance(neighbor_route)

        # Cost difference (ΔE)
        delta = neighbor_cost - current_cost

        # Acceptance criteria
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor_route
            current_cost = neighbor_cost

            # Update best solution
            if current_cost < best_cost:
                best_route = current_route.copy()
                best_cost = current_cost

        # Cooling schedule (T = T * α)
        temp *= cooling_rate
        iteration += 1

    return best_route, best_cost

# ======================
# PARAMETERS & EXECUTION
# ======================
# SA Parameters
INITIAL_TEMP = 1000     # T_initial (high initial temperature)
COOLING_RATE = 0.995    # α (cooling rate, typically 0.8-0.999)
MIN_TEMP = 0.1          # Stopping temperature
MAX_ITER = 10000        # Safety stop

# Initial random solution
initial_route = list(cities.keys())
random.shuffle(initial_route)

# Run SA
best_route, best_cost = simulated_annealing(
    initial_route=initial_route,
    initial_temp=INITIAL_TEMP,
    cooling_rate=COOLING_RATE,
    min_temp=MIN_TEMP,
    max_iter=MAX_ITER
)

# ======================
# RESULTS
# ======================
print(f"Initial route: {initial_route} (Cost: {route_distance(initial_route):.2f})")
print(f"Optimized route: {best_route} (Cost: {best_cost:.2f})")
print(f"Improvement: {route_distance(initial_route) - best_cost:.2f}")
