import math
import random
import time

import map
import matplotlib.pyplot as plt

# ======================
# PROBLEM DEFINITION
# ======================
# cities = {
#     "A": (0, 0),
#     "B": (1, 5),
#     "C": (5, 2),
#     "D": (3, 6),
#     "E": (7, 3),
#     "F": (2, 8)
# }

# ======================
# CORE FUNCTIONS
# ======================
def distance(p1, p2):
    """Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def route_cost(route):
    """Calculate total distance of a route"""
    return sum(distance(map.cities[route[i]], map.cities[route[(i+1)%len(route)]])
            for i in range(len(route)))

# ======================
# GENETIC OPERATORS
# ======================
def initialize_population(pop_size, city_list):
    """Creates random valid tours with some diversity"""
    population = []
    # Include some structured solutions
    population.append(city_list.copy())  # Original order
    population.append(city_list[::-1])   # Reversed order

    # Add random permutations for the rest
    for _ in range(pop_size - 2):
        population.append(random.sample(city_list, len(city_list)))
    return population

def tournament_selection(population, k=3):
    """Selects best from random k individuals"""
    tournament = random.sample(population, k)
    return min(tournament, key=lambda x: route_cost(x))

def ordered_crossover(parent1, parent2):
    """OX crossover preserving order"""
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[a:b] = parent1[a:b]

    ptr = b
    for city in parent2[b:] + parent2[:b]:
        if city not in child[a:b]:
            if ptr >= size:
                ptr = 0
            child[ptr] = city
            ptr += 1
    return child

def mutate(individual, mutation_rate):
    """Randomly swaps two cities with mutation_rate probability"""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# ======================
# GENETIC ALGORITHM
# ======================
def genetic_algorithm(cities, generations=100, pop_size=50,
                     mutation_rate=0.01, tournament_size=3):
    start_time = time.time()
    city_list = list(map.cities.keys())
    population = initialize_population(pop_size, city_list)

    # Tracking variables
    history = {
        'best_cost': [],
        'avg_cost': [],
        'diversity': [],
        'best_route': None
    }

    best_individual = min(population, key=lambda x: route_cost(x))
    best_cost = route_cost(best_individual)

    for gen in range(generations):
        new_population = []

        # Elitism: keep best individual
        population.sort(key=lambda x: route_cost(x))
        new_population.append(population[0])

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)
            child = ordered_crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

        # Calculate metrics
        costs = [route_cost(ind) for ind in population]
        current_best = min(costs)
        avg_cost = sum(costs)/len(costs)

        # Update best solution
        if current_best < best_cost:
            best_individual = population[costs.index(current_best)]
            best_cost = current_best

        # Track diversity (unique solutions)
        unique = len(set(tuple(ind) for ind in population))

        # Update history
        history['best_cost'].append(best_cost)
        history['avg_cost'].append(avg_cost)
        history['diversity'].append(unique/pop_size)
        history['best_route'] = best_individual

    history['runtime'] = time.time() - start_time
    return best_individual, best_cost, history

# ======================
# VISUALIZATION
# ======================
def visualize_ga_results(results):
    plt.figure(figsize=(15, 10))

    # Plot 1: Cost Progression
    plt.subplot(2, 2, 1)
    plt.plot(results['best_cost'], 'b-', label='Best Cost')
    plt.plot(results['avg_cost'], 'g--', label='Average Cost')
    plt.title('Cost Progression Through Generations')
    plt.xlabel('Generation')
    plt.ylabel('Tour Cost')
    plt.legend()
    plt.grid(True)

    # Plot 2: Population Diversity
    plt.subplot(2, 2, 2)
    plt.plot(results['diversity'], 'r-')
    plt.title('Population Diversity')
    plt.xlabel('Generation')
    plt.ylabel('Unique Solutions Ratio')
    plt.grid(True)

    # Plot 3: Runtime Information
    plt.subplot(2, 2, 3)
    plt.bar(['Runtime'], [results['runtime']], color='orange')
    plt.title(f'Total Execution Time: {results["runtime"]:.2f} seconds')
    plt.ylabel('Seconds')

    # Plot 4: Best Route Visualization
    plt.subplot(2, 2, 4)
    route = results['best_route']
    x = [map.cities[city][0] for city in route] + [map.cities[route[0]][0]]
    y = [map.cities[city][1] for city in route] + [map.cities[route[0]][1]]
    plt.plot(x, y, 'bo-')
    for city, (xi, yi) in map.cities.items():
        plt.text(xi, yi, city, fontsize=12, ha='center', va='bottom')
    plt.title(f'Best Route (Cost: {min(results["best_cost"]):.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# ======================
# MAIN EXECUTION
# ======================
if __name__ == "__main__":
    # Parameters
    params = {
        'generations': 200,
        'pop_size': 100,
        'mutation_rate': 0.02,
        'tournament_size': 5
    }

    print("=== GENETIC ALGORITHM FOR TSP ===")
    initial_route = list(map.cities.keys())
    print(f"Initial route: {initial_route}")
    print(f"Initial cost: {route_cost(initial_route):.2f}")

    # Run GA
    best_route, best_cost, history = genetic_algorithm(map.cities, **params)

    # Results
    print("\n=== RESULTS ===")
    print(f"Optimized route: {best_route}")
    print(f"Best cost: {best_cost:.2f}")
    print(f"Improvement: {route_cost(initial_route) - best_cost:.2f}")
    print(f"Runtime: {history['runtime']:.2f} seconds")

    # Visualize all results
    visualize_ga_results(history)
