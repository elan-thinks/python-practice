# evolutionary.py
import math
import random
import time

import city_map
import matplotlib.pyplot as plt


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def route_cost(route):
    cities = city_map.cities
    return sum(distance(cities[route[i]], cities[route[(i+1) % len(route)]]) for i in range(len(route)))

def create_route(city_list):
    route = city_list[:]
    random.shuffle(route)
    return route

def initial_population(pop_size, city_list):
    return [create_route(city_list) for _ in range(pop_size)]

def rank_routes(population):
    fitness_results = [(route, route_cost(route)) for route in population]
    fitness_results.sort(key=lambda x: x[1])
    return fitness_results

def selection(ranked, elite_size):
    selection_results = [r[0] for r in ranked[:elite_size]]
    fitness_sum = sum(1.0 / r[1] for r in ranked)
    probs = [(1.0 / r[1]) / fitness_sum for r in ranked]

    while len(selection_results) < len(ranked):
        pick = random.choices(ranked, weights=probs, k=1)[0][0]
        selection_results.append(pick)
    return selection_results

def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child_p1 = parent1[start:end+1]
    child_p2 = [city for city in parent2 if city not in child_p1]
    return child_p2[:start] + child_p1 + child_p2[start:]

def mutate(route, mutation_rate):
    for _ in range(len(route)):
        if random.random() < mutation_rate:
            swap_with_1, swap_with_2 = random.sample(range(len(route)), 2)
            route[swap_with_1], route[swap_with_2] = route[swap_with_2], route[swap_with_1]
    return route

def next_generation(current_gen, elite_size, mutation_rate):
    ranked = rank_routes(current_gen)
    selection_results = selection(ranked, elite_size)

    children = []
    children.extend(selection_results[:elite_size])

    for i in range(len(current_gen) - elite_size):
        parent1 = random.choice(selection_results)
        parent2 = random.choice(selection_results)
        child = crossover(parent1, parent2)
        children.append(child)

    next_gen = [mutate(child, mutation_rate) for child in children]

    return next_gen

def genetic_algorithm(pop_size=500, elite_size=50, mutation_rate=0.01, generations=1000):
    city_list = list(city_map.cities.keys())
    population = initial_population(pop_size, city_list)
    start_time = time.time()

    best_route = None
    best_cost = float('inf')
    cost_progression_time = []
    cost_progression_generations = []

    for gen in range(1, generations + 1):
        population = next_generation(population, elite_size, mutation_rate)
        ranked = rank_routes(population)
        current_best = ranked[0]

        if current_best[1] < best_cost:
            best_route, best_cost = current_best
            cost_progression_time.append((time.time() - start_time, best_cost))
            cost_progression_generations.append((gen, best_cost))

    elapsed = time.time() - start_time
    return best_route, best_cost, elapsed, cost_progression_time, cost_progression_generations

def plot_results(best_route, cities, progression_data, title):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot 1: Best Route
    route_coords = [cities[city] for city in best_route]
    route_coords.append(cities[best_route[0]])
    x_coords, y_coords = zip(*route_coords)

    ax1.plot(x_coords, y_coords, 'o-')
    ax1.set_title(f"{title}: Best Tour")
    ax1.set_xlabel("X-coordinate")
    ax1.set_ylabel("Y-coordinate")
    ax1.grid(True)

    for city, (x, y) in cities.items():
        ax1.text(x, y, city, ha='right', va='bottom')

    # Plot 2: Cost Progression
    x_values, costs = zip(*progression_data)
    ax2.plot(x_values, costs)
    ax2.set_title(f"{title}: Best Cost Progression (vs. Time)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Best Tour Cost")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    random.seed(42)
    best_route, best_cost, elapsed, progression_time, progression_generations = genetic_algorithm()

    print("--- Genetic Algorithm Results ---")
    print(f"Final tour cost: {best_cost:.2f}")
    print(f"Time taken: {elapsed:.3f}s")

    route_str = " -> ".join(best_route) + " -> " + best_route[0]
    print(f"Best route: {route_str}")

    print("\nCost Progression (Generation, Cost):")
    for generation, cost in progression_generations:
        print(f"  Generation {generation}: {cost:.2f}")

    plot_results(best_route, city_map.cities, progression_time, "Genetic Algorithm")
