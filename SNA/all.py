import math
import random
import time

import matplotlib.pyplot as plt

# ------------------------
# Dataset: 50 fixed cities
# ------------------------
random.seed(42)
NUM_CITIES = 50
CITIES = {i: (random.uniform(0, 1000), random.uniform(0, 1000)) for i in range(NUM_CITIES)}

# ------------------------
# Distance and Cost
# ------------------------
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def route_cost(route):
    return sum(distance(CITIES[route[i]], CITIES[route[(i+1) % len(route)]]) for i in range(len(route)))

def two_opt_swap(route, i, k):
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

# ------------------------
# 1) Hill Climbing
# ------------------------
def hill_climbing(initial_route, max_iterations=200):
    start = time.time()
    current_route = initial_route.copy()
    current_cost = route_cost(current_route)
    best_route = current_route.copy()
    best_cost = current_cost

    for _ in range(max_iterations):
        improved = False
        for i in range(1, len(current_route)-1):
            for k in range(i+1, len(current_route)):
                new_route = two_opt_swap(current_route, i, k)
                new_cost = route_cost(new_route)
                if new_cost < best_cost:
                    best_route = new_route.copy()
                    best_cost = new_cost
                    current_route = new_route.copy()
                    current_cost = new_cost
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break

    return best_route, best_cost, time.time() - start

# ------------------------
# 2) Simulated Annealing
# ------------------------
def get_neighbor(route):
    i, k = sorted(random.sample(range(1, len(route)), 2))
    return two_opt_swap(route, i, k)

def simulated_annealing(initial_route, initial_temp=1000, cooling_rate=0.999, min_temp=0.1, max_iter=5000):
    start = time.time()
    current_route = initial_route.copy()
    current_cost = route_cost(current_route)
    best_route = current_route.copy()
    best_cost = current_cost

    temp = initial_temp
    cost_progression = []

    for iteration in range(max_iter):
        neighbor_route = get_neighbor(current_route)
        neighbor_cost = route_cost(neighbor_route)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor_route
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_route = current_route.copy()
                best_cost = current_cost

        cost_progression.append(best_cost)
        temp *= cooling_rate
        if temp < min_temp:
            break

    return best_route, best_cost, time.time() - start, cost_progression

# ------------------------
# 3) Genetic Algorithm
# ------------------------
def create_population(size, cities):
    population = []
    base_route = list(cities.keys())
    for _ in range(size):
        route = base_route.copy()
        random.shuffle(route)
        population.append(route)
    return population

def fitness(route):
    return 1 / route_cost(route)  # Higher fitness = shorter route

def tournament_selection(pop, k=3):
    selected = random.sample(pop, k)
    selected.sort(key=lambda r: route_cost(r))
    return selected[0]

def order_crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[a:b+1] = parent1[a:b+1]

    fill_pos = (b+1) % size
    parent2_pos = (b+1) % size

    while None in child:
        if parent2[parent2_pos] not in child:
            child[fill_pos] = parent2[parent2_pos]
            fill_pos = (fill_pos + 1) % size
        parent2_pos = (parent2_pos + 1) % size
    return child

def mutate(route, mutation_rate=0.02):
    route = route.copy()
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route)-1)
            route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm(cities, population_size=100, generations=200, mutation_rate=0.02):
    start = time.time()
    population = create_population(population_size, cities)
    best_route = min(population, key=lambda r: route_cost(r))
    best_cost = route_cost(best_route)
    cost_progression = [best_cost]

    for _ in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = order_crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population

        current_best = min(population, key=lambda r: route_cost(r))
        current_best_cost = route_cost(current_best)
        if current_best_cost < best_cost:
            best_route = current_best
            best_cost = current_best_cost
        cost_progression.append(best_cost)

    return best_route, best_cost, time.time() - start, cost_progression

# ------------------------
# Run and compare all algorithms
# ------------------------
def main():
    base_route = list(CITIES.keys())
    random.shuffle(base_route)

    print("Running Hill Climbing...")
    hc_route, hc_cost, hc_time = hill_climbing(base_route)
    print(f"HC Cost: {hc_cost:.2f}, Time: {hc_time:.2f}s")

    print("Running Simulated Annealing...")
    sa_route, sa_cost, sa_time, sa_progression = simulated_annealing(base_route)
    print(f"SA Cost: {sa_cost:.2f}, Time: {sa_time:.2f}s")

    print("Running Genetic Algorithm...")
    ga_route, ga_cost, ga_time, ga_progression = genetic_algorithm(CITIES)
    print(f"GA Cost: {ga_cost:.2f}, Time: {ga_time:.2f}s")

    # Visualization
    plt.figure(figsize=(18, 12))

    # Plot 1: Cost progression
    plt.subplot(2, 2, 1)
    plt.plot(sa_progression, label='Simulated Annealing')
    plt.plot(ga_progression, label='Genetic Algorithm')
    plt.axhline(hc_cost, color='orange', linestyle='--', label='Hill Climbing (final cost)')
    plt.title("Cost Progression")
    plt.xlabel("Iterations")
    plt.ylabel("Tour Cost")
    plt.legend()
    plt.grid()

    # Plot 2: Route visualization HC
    plt.subplot(2, 2, 2)
    x = [CITIES[city][0] for city in hc_route] + [CITIES[hc_route[0]][0]]
    y = [CITIES[city][1] for city in hc_route] + [CITIES[hc_route[0]][1]]
    plt.plot(x, y, 'o-', label='HC route')
    plt.title(f"Hill Climbing Route (Cost: {hc_cost:.2f})")
    plt.grid()

    # Plot 3: Route visualization SA
    plt.subplot(2, 2, 3)
    x = [CITIES[city][0] for city in sa_route] + [CITIES[sa_route[0]][0]]
    y = [CITIES[city][1] for city in sa_route] + [CITIES[sa_route[0]][1]]
    plt.plot(x, y, 'o-', color='green', label='SA route')
    plt.title(f"Simulated Annealing Route (Cost: {sa_cost:.2f})")
    plt.grid()

    # Plot 4: Route visualization GA
    plt.subplot(2, 2, 4)
    x = [CITIES[city][0] for city in ga_route] + [CITIES[ga_route[0]][0]]
    y = [CITIES[city][1] for city in ga_route] + [CITIES[ga_route[0]][1]]
    plt.plot(x, y, 'o-', color='red', label='GA route')
    plt.title(f"Genetic Algorithm Route (Cost: {ga_cost:.2f})")
    plt.grid()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
