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

def get_neighbor(route):
    """Generate neighbor solution via 2-opt swap"""
    i, k = sorted(random.sample(range(1, len(route)), 2))
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

# ======================
# SIMULATED ANNEALING
# ======================
def simulated_annealing(initial_route, initial_temp, cooling_rate, min_temp, max_iter):
    """Enhanced SA with comprehensive tracking"""
    start_time = time.time()
    current_route = initial_route.copy()
    current_cost = route_cost(current_route)
    best_route = current_route.copy()
    best_cost = current_cost

    # Tracking variables
    history = {
        'temperature': [],
        'current_cost': [],
        'best_cost': [],
        'acceptance_rate': [],
        'runtime': 0
    }

    temp = initial_temp
    accepted = 0

    for iteration in range(max_iter):
        neighbor_route = get_neighbor(current_route)
        neighbor_cost = route_cost(neighbor_route)
        delta = neighbor_cost - current_cost

        # Acceptance criteria
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor_route
            current_cost = neighbor_cost
            accepted += 1

            # Update best solution
            if current_cost < best_cost:
                best_route = current_route.copy()
                best_cost = current_cost

        # Record progress
        history['temperature'].append(temp)
        history['current_cost'].append(current_cost)
        history['best_cost'].append(best_cost)
        history['acceptance_rate'].append(accepted/(iteration+1))

        # Cooling schedule
        temp *= cooling_rate
        if temp < min_temp:
            break

    history['runtime'] = time.time() - start_time
    return {
        'best_route': best_route,
        'best_cost': best_cost,
        'history': history,
        'iterations': iteration + 1
    }

# ======================
# VISUALIZATION
# ======================
def visualize_results(result):
    plt.figure(figsize=(15, 10))

    # Plot 1: Cost Progression
    plt.subplot(2, 2, 1)
    plt.plot(result['history']['best_cost'], label='Best Cost')
    plt.plot(result['history']['current_cost'], label='Current Cost')
    plt.title('Cost Progression')
    plt.xlabel('Iteration')
    plt.ylabel('Tour Cost')
    plt.legend()
    plt.grid(True)

    # Plot 2: Temperature Schedule
    plt.subplot(2, 2, 2)
    plt.plot(result['history']['temperature'])
    plt.title('Temperature Schedule')
    plt.xlabel('Iteration')
    plt.ylabel('Temperature')
    plt.grid(True)

    # Plot 3: Acceptance Rate
    plt.subplot(2, 2, 3)
    plt.plot(result['history']['acceptance_rate'])
    plt.title('Acceptance Rate')
    plt.xlabel('Iteration')
    plt.ylabel('Acceptance Probability')
    plt.grid(True)

    # Plot 4: Best Route Visualization
    plt.subplot(2, 2, 4)
    route = result['best_route']
    x = [map.cities[city][0] for city in route] + [map.cities[route[0]][0]]
    y = [map.cities[city][1] for city in route] + [map.cities[route[0]][1]]
    plt.plot(x, y, 'o-')
    for city, (xi, yi) in map.cities.items():
        plt.text(xi, yi, city, fontsize=12, ha='center', va='bottom')
    plt.title(f'Best Route (Cost: {result["best_cost"]:.2f})')
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
        'initial_temp': 1000,
        'cooling_rate': 0.995,
        'min_temp': 0.1,
        'max_iter': 10000
    }

    # Initial random solution
    initial_route = list(map.cities.keys())
    random.shuffle(initial_route)

    print("=== SIMULATED ANNEALING TSP OPTIMIZATION ===")
    print(f"Initial route: {initial_route}")
    print(f"Initial cost: {route_cost(initial_route):.2f}")

    # Run SA
    result = simulated_annealing(
        initial_route=initial_route,
        **params
    )

    # Results
    print("\n=== RESULTS ===")
    print(f"Optimized route: {result['best_route']}")
    print(f"Best cost: {result['best_cost']:.2f}")
    print(f"Improvement: {route_cost(initial_route) - result['best_cost']:.2f}")
    print(f"Time: {result['history']['runtime']:.4f}s")
    print(f"Iterations: {result['iterations']}")

    # Visualize all results
    visualize_results(result)
