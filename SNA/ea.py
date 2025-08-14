import math
import random
import time

# -----------------------------
# Replace this 'cities' dict with your 55-city dictionary
# -----------------------------
cities = {
    "A": (12, 34), "B": (45, 67), "C": (23, 78), "D": (56, 12), "E": (34, 90),
    "F": (78, 56), "G": (90, 34), "H": (67, 89), "I": (11, 22), "J": (88, 77),
    "K": (54, 32), "L": (29, 65), "M": (73, 21), "N": (44, 55), "O": (19, 88),
    "P": (92, 14), "Q": (38, 48), "R": (60, 73), "S": (85, 49), "T": (15, 66),
    "U": (47, 28), "V": (64, 36), "W": (26, 57), "X": (32, 81), "Y": (59, 18),
    "Z": (40, 92), "AA": (75, 29), "AB": (28, 44), "AC": (53, 80), "AD": (17, 53),
    "AE": (71, 46), "AF": (30, 27), "AG": (49, 94), "AH": (83, 40), "AI": (66, 59),
    "AJ": (12, 97), "AK": (93, 61), "AL": (58, 33), "AM": (25, 73), "AN": (41, 19),
    "AO": (36, 86), "AP": (97, 54), "AQ": (21, 37), "AR": (82, 25), "AS": (46, 72),
    "AT": (61, 85), "AU": (18, 47), "AV": (27, 91), "AW": (50, 64), "AX": (76, 15),
    "AY": (69, 95), "AZ": (14, 60), "BA": (33, 50), "BB": (80, 32), "BC": (57, 99)
}

# -----------------------------
# Precompute distance matrix for speed
# -----------------------------
city_list = list(cities.keys())
N = len(city_list)
index = {city: i for i, city in enumerate(city_list)}

coords = [cities[c] for c in city_list]
dist_matrix = [[0.0]*N for _ in range(N)]
for i in range(N):
    x1,y1 = coords[i]
    for j in range(N):
        x2,y2 = coords[j]
        dx = x1-x2; dy = y1-y2
        dist_matrix[i][j] = math.hypot(dx, dy)

def route_distance(route):
    """route as list of city names"""
    d = 0.0
    for i in range(len(route)):
        a = index[route[i]]
        b = index[route[(i+1) % len(route)]]
        d += dist_matrix[a][b]
    return d

# -----------------------------
# Genetic components
# -----------------------------
def create_population(pop_size):
    pop = []
    base = city_list[:]
    for _ in range(pop_size):
        indiv = base[:]
        random.shuffle(indiv)
        pop.append(indiv)
    return pop

def tournament_select(population, k):
    """Return one individual via k-size tournament (lower distance = better)."""
    sample = random.sample(population, k)
    sample.sort(key=route_distance)
    return sample[0][:]  # return copy

def ordered_crossover(p1, p2):
    """Ordered Crossover (OX) producing a valid child tour."""
    size = len(p1)
    child = [None]*size
    a, b = sorted(random.sample(range(size), 2))
    # copy slice from p1
    child[a:b+1] = p1[a:b+1]
    fill_pos = (b+1) % size
    for gene in p2[b+1:] + p2[:b+1]:
        if gene not in child:
            child[fill_pos] = gene
            fill_pos = (fill_pos + 1) % size
    return child

# -----------------------------
# 2-opt local improvement
# -----------------------------
def two_opt_improve(route, max_no_improve=100):
    """Perform iterative 2-opt until no improvement for max_no_improve consecutive attempts.
       Returns improved route (new list) and its distance."""
    best = route[:]
    best_cost = route_distance(best)
    no_improve = 0
    size = len(best)
    # To keep it fast: randomize i,k order rather than exhaustive
    while no_improve < max_no_improve:
        improved = False
        # try all pairs but in random order to avoid same pattern
        pairs = [(i, k) for i in range(1, size-1) for k in range(i+1, size)]
        random.shuffle(pairs)
        for (i, k) in pairs:
            new_route = best[:i] + best[i:k+1][::-1] + best[k+1:]
            new_cost = route_distance(new_route)
            if new_cost < best_cost - 1e-12:
                best = new_route
                best_cost = new_cost
                improved = True
                break
        if improved:
            no_improve = 0
        else:
            no_improve += 1
    return best, best_cost

# -----------------------------
# Hybrid Genetic Algorithm
# -----------------------------
def hybrid_genetic(pop_size=400, generations=800, tournament_size=12,
                   mutation_rate=0.25, elitism=10, local_improve_children=2):
    """Run GA with 2-opt local improvement on children."""
    pop = create_population(pop_size)
    # evaluate
    pop.sort(key=route_distance)
    best_overall = pop[0][:]
    best_overall_cost = route_distance(best_overall)
    start_time = time.time()

    for gen in range(1, generations+1):
        new_pop = []
        # Elitism: copy top 'elitism' individuals
        pop.sort(key=route_distance)
        elites = [ind[:] for ind in pop[:elitism]]
        new_pop.extend(elites)

        # create rest of population
        while len(new_pop) < pop_size:
            p1 = tournament_select(pop, tournament_size)
            p2 = tournament_select(pop, tournament_size)
            child = ordered_crossover(p1, p2)

            # mutation: with some chance apply 2-opt (strong) or swap (light)
            if random.random() < mutation_rate:
                if random.random() < 0.6:
                    # apply short 2-opt improvement as mutation (limited work)
                    child, _ = two_opt_improve(child, max_no_improve=local_improve_children)
                else:
                    # small swap mutation
                    i,j = random.sample(range(len(child)), 2)
                    child[i], child[j] = child[j], child[i]

            # optionally run a short 2-opt on every child for stronger hillclimb
            child, child_cost = two_opt_improve(child, max_no_improve=3)
            new_pop.append(child)

        pop = new_pop

        # track best
        pop.sort(key=route_distance)
        gen_best = pop[0][:]
        gen_best_cost = route_distance(gen_best)
        if gen_best_cost < best_overall_cost:
            best_overall = gen_best[:]
            best_overall_cost = gen_best_cost

        # Print progress occasionally
        if gen % 50 == 0 or gen == 1:
            elapsed = time.time() - start_time
            print(f"Gen {gen:4d} | Best this gen: {gen_best_cost:.4f} | Best overall: {best_overall_cost:.4f} | time: {elapsed:.1f}s")

    return best_overall, best_overall_cost

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    random.seed(123)  # set seed for reproducibility; remove or change to test randomness
    start = time.time()
    best_route, best_dist = hybrid_genetic(
        pop_size=350,        # ~300-500 recommended for 55 cities
        generations=800,     # 500-2000 depending on time
        tournament_size=14,
        mutation_rate=0.28,
        elitism=12,
        local_improve_children=2
    )
    elapsed = time.time() - start
    print("\n=== FINAL ===")
    print("Best route found:", best_route)
    print("Best distance: {:.6f}".format(best_dist))
    print("Elapsed time: {:.1f}s".format(elapsed))
