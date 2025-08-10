import math
import random

# ======================
# PROBLEM DEFINITION
# ======================
cities = {
    "A": (0, 0),
    "B": (1, 5),
    "C": (5, 2),
    "D": (3, 6),
    "E": (7, 3),
    "F": (2, 8)
}

# ======================
# CORE FUNCTIONS
# ======================
def distance(p1, p2):
    """Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def route_cost(route):
    """Fitness function (lower cost = better)"""
    return sum(distance(cities[route[i]], cities[route[(i+1)%len(route)]])
            for i in range(len(route)))

# ======================
# GENETIC OPERATORS
# ======================
def initialize_population(pop_size, cities):
    """Creates random valid tours"""
    city_list = list(cities.keys())
    return [random.sample(city_list, len(city_list)) for _ in range(pop_size)]

def tournament_selection(population, k=3):
    """Selects best from random k individuals"""
    tournament = random.sample(population, k)
    return min(tournament, key=lambda x: route_cost(x))

def ordered_crossover(parent1, parent2):
    """OX crossover preserving order"""
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))

    # Initialize child with None values
    child = [None]*size

    # Copy segment from parent1
    child[a:b] = parent1[a:b]

    # Fill remaining from parent2 (order preserved)
    ptr = b
    for city in parent2[b:] + parent2[:b]:
        if city not in child[a:b]:
            if ptr >= size :
                ptr = 0
            child[ptr] = city
            ptr += 1

    return child

def swap_mutation(individual, mutation_rate=0.01):
    """Randomly swaps two cities"""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# ======================
# GENETIC ALGORITHM
# ======================
def genetic_algorithm(cities, generations=100, pop_size=50,
                     mutation_rate=0.01, tournament_size=3):
    # Initialize population
    population = initialize_population(pop_size, cities)
    best_individual = min(population, key=lambda x: route_cost(x))
    best_cost = route_cost(best_individual)

    for gen in range(generations):
        new_population = []

        # Elitism: keep best individual
        new_population.append(best_individual)

        while len(new_population) < pop_size:
            # Selection
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)

            # Crossover
            child = ordered_crossover(parent1, parent2)

            # Mutation
            child = swap_mutation(child, mutation_rate)

            new_population.append(child)

        # Update population
        population = new_population

        # Track best solution
        current_best = min(population, key=lambda x: route_cost(x))
        current_cost = route_cost(current_best)
        if current_cost < best_cost:
            best_individual = current_best
            best_cost = current_cost

    return best_individual, best_cost

# ======================
# EXECUTION
# ======================
# GA Parameters
GENERATIONS = 200
POP_SIZE = 100
MUTATION_RATE = 0.02
TOURNAMENT_SIZE = 5

# Run GA
best_route, best_cost = genetic_algorithm(
    cities=cities,
    generations=GENERATIONS,
    pop_size=POP_SIZE,
    mutation_rate=MUTATION_RATE,
    tournament_size=TOURNAMENT_SIZE
)

# ======================
# RESULTS
# ======================
print(f"Optimized Route: {best_route}")
print(f"Total Distance: {best_cost:.2f}")
print(f"Improvement over random: {route_cost(random.sample(list(cities.keys()), len(cities))) - best_cost:.2f}")


# import map
# import math
# import random
# # from collections import defualtdict

# # cities = {
# #     "A": (0,0),
# #     "B": (1,5),
# #     "C": (5,2),
# #     "D": (3,6),
# #     "E": (7,3),
# #     "G": (2,8)
# # }

# def distance(p1, p2):
#     return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# def router_distance(route):
#     dist = 0
#     for i in range(len(route)):
#         city1 = route[i]
#         city2 = route[(i + 1 ) % len(route) ]
#         dist += distance(map.cities[city1] , map.cities[city2])
#     return dist
# def create_population(pop_size , city_list):
#     population = []
#     for i in range(pop_size):
#         individual = city_list.copy()
#         random.shuffle(individual)
#         population.append(individual)
#     return population

# def select_parent(population , tournament_size):
#     tournament = random.sample(population , tournament_size)
#     tournament.sort(key=lambda x : router_distance(x))
#     return tournament[0]
# def crossover(parent1 , parent2):
#     size = len(parent1)
#     child = [None]*size

#     start, end = sorted(random.sample(range(size), 2))
#     child[start:end] = parent1[start:end]

#     ptr = end
#     for city in parent2[end:] + parent2[:end]:
#         if city not in child[start:end]:
#             if ptr >= size :
#                 ptr = 0
#             child[ptr] = city
#             ptr += 1
#     return child
# def mutate(individual , mutation_rate):
#     if random.random() < mutation_rate:
#          i, j = random.sample(range(len(individual)), 2 )
#          individual[i], individual[j] = individual[j], individual[i]
#     return individual

# def evolution(city_list, pop_size, generations, tournament_size,mutation_rate):
#     population = create_population(pop_size, city_list)

#     for gen in range(generations):
#         new_population = []

#         population.sort(key = lambda x: router_distance(x))
#         new_population.append(population[0])

#         while len(new_population) < pop_size:
#             parent1 = select_parent(population, tournament_size)
#             parent2 = select_parent(population, tournament_size)
#             child = crossover(parent1 , parent2)
#             child = mutate(child, mutation_rate)
#             new_population.append(child)
#         population = new_population

#     population.sort(key=lambda x :router_distance(x))
#     return population[0], router_distance(population[0])


# pop_size = 50
# generation = 100
# tournament_size = 5
# mutation_rate = 0.1

# initial_route = list(map.cities.keys())
# # random.shuffle(initial_route)

# print("Initial router ", initial_route)
# print("Initial distance ", router_distance(initial_route))

# best_route , best_distance = evolution(initial_route, pop_size,generation, tournament_size, mutation_rate)

# print("Best route found : ", best_route)
# print("Best distance" , best_distance)

