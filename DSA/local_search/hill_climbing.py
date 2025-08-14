# hill_climbing.py
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

def two_opt_swap(route, i, k):
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

def hill_climbing(initial_route, max_iterations=10000, max_neighbors_sampled=100):
    start_time = time.time()
    current_route = initial_route.copy()
    current_cost = route_cost(current_route)

    cost_progression_time = [(0, current_cost)]
    cost_progression_iterations = [(0, current_cost)]

    for iteration in range(max_iterations):
        improved = False

        for _ in range(max_neighbors_sampled):
            i, k = sorted(random.sample(range(len(current_route)), 2))
            new_route = two_opt_swap(current_route, i, k)
            new_cost = route_cost(new_route)

            if new_cost < current_cost:
                current_route = new_route
                current_cost = new_cost
                cost_progression_time.append((time.time() - start_time, current_cost))
                cost_progression_iterations.append((iteration, current_cost))
                improved = True
                break

        if not improved:
            break

    elapsed = time.time() - start_time
    return current_route, current_cost, elapsed, cost_progression_time, cost_progression_iterations

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
    ax2.plot(x_values, costs, marker='o')
    ax2.set_title(f"{title}: Best Cost Progression (vs. Time)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Best Tour Cost")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    random.seed(42)
    initial_route = list(city_map.cities.keys())
    random.shuffle(initial_route)

    best_route, best_cost, elapsed, progression_time, progression_iterations = hill_climbing(initial_route)

    print("--- Hill Climbing Results ---")
    print(f"Final tour cost: {best_cost:.2f}")
    print(f"Time taken: {elapsed:.3f}s")

    route_str = " -> ".join(best_route) + " -> " + best_route[0]
    print(f"Best route: {route_str}")

    print("\nCost Progression (Iteration, Cost):")
    for iteration, cost in progression_iterations:
        print(f"  Iteration {iteration}: {cost:.2f}")

    plot_results(best_route, city_map.cities, progression_time, "Hill Climbing")
