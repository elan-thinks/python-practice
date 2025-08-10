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
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def route_cost(route):
    return sum(distance(map.cities[route[i]], map.cities[route[(i+1)%len(route)]])
            for i in range(len(route)))

def two_opt_swap(route, i, k):
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

# ======================
# HILL CLIMBING ALGORITHM
# ======================
def hill_climbing(initial_route, max_iterations=1000):
    start_time = time.time()
    current_route = initial_route.copy()
    current_cost = route_cost(current_route)
    best_route = current_route.copy()
    best_cost = current_cost

    cost_progression = [best_cost]
    iteration_data = []

    for iteration in range(max_iterations):
        improved = False

        for i in range(1, len(current_route) - 1):
            for k in range(i + 1, len(current_route)):
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

        cost_progression.append(best_cost)
        iteration_data.append({
            'iteration': iteration,
            'current_cost': current_cost,
            'best_cost': best_cost,
            'time_elapsed': time.time() - start_time
        })

        if not improved:
            break

    return {
        'final_route': best_route,
        'final_cost': best_cost,
        'time_taken': time.time() - start_time,
        'cost_progression': cost_progression,
        'iteration_data': iteration_data
    }

# ======================
# VISUALIZATION
# ======================
def visualize_results(results):
    plt.figure(figsize=(15, 10))

    # Plot 1: Convergence
    plt.subplot(2, 2, 1)
    for i, result in enumerate(results[:3]):  # Show first 3 runs
        plt.plot(result['cost_progression'],
                label=f'Run {i+1} (Final: {result["final_cost"]:.2f})')
    plt.title('Cost Progression')
    plt.xlabel('Iteration')
    plt.ylabel('Tour Cost')
    plt.legend()
    plt.grid(True)

    # Plot 2: Runtime
    plt.subplot(2, 2, 2)
    runtimes = [r['time_taken'] for r in results]
    plt.bar(range(len(runtimes)), runtimes, color='skyblue')
    plt.title('Time Taken per Run')
    plt.xlabel('Run Number')
    plt.ylabel('Seconds')
    plt.grid(axis='y')

    # Plot 3: Cost Distribution
    plt.subplot(2, 2, 3)
    final_costs = [r['final_cost'] for r in results]
    plt.hist(final_costs, bins=5, edgecolor='black')
    plt.title('Final Costs Distribution')
    plt.xlabel('Tour Cost')
    plt.ylabel('Frequency')

    # Plot 4: Best Route Visualization
    plt.subplot(2, 2, 4)
    best_run = min(results, key=lambda x: x['final_cost'])
    route = best_run['final_route']
    x = [map.cities[city][0] for city in route] + [map.cities[route[0]][0]]
    y = [map.cities[city][1] for city in route] + [map.cities[route[0]][1]]
    plt.plot(x, y, 'o-')
    for city, (xi, yi) in map.cities.items():
        plt.text(xi, yi, city, fontsize=12, ha='center', va='bottom')
    plt.title(f'Best Route (Cost: {best_run["final_cost"]:.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# ======================
# MAIN EXECUTION
# ======================
if __name__ == "__main__":
    num_runs = 5
    results = []

    print("=== HILL CLIMBING TSP OPTIMIZATION ===")
    for run in range(num_runs):
        initial_route = list(map.cities.keys())
        random.shuffle(initial_route)
        print(f"\nRun {run+1}: Initial cost = {route_cost(initial_route):.2f}")

        result = hill_climbing(initial_route)
        results.append(result)

        print(f"Final cost: {result['final_cost']:.2f}")
        print(f"Time taken: {result['time_taken']:.4f}s")
        print(f"Improvement: {route_cost(initial_route) - result['final_cost']:.2f}")

    # Summary Statistics
    print("\n=== SUMMARY ===")
    print(f"Best solution: {min(r['final_cost'] for r in results):.2f}")
    print(f"Worst solution: {max(r['final_cost'] for r in results):.2f}")
    print(f"Average solution: {sum(r['final_cost'] for r in results)/len(results):.2f}")
    print(f"Average time: {sum(r['time_taken'] for r in results)/len(results):.4f}s")

    # Visualize all results
    visualize_results(results)
