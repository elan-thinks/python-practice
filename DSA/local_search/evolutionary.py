import math
import random

import map

# from collections import defualtdict

# cities = {
#     "A": (0,0),
#     "B": (1,5),
#     "C": (5,2),
#     "D": (3,6),
#     "E": (7,3),
#     "G": (2,8)
# }

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def router_distance(route):
    dist = 0
    for i in range(len(route)):
        city1 = route[i]
        city2 = route[(i + 1 ) % len(route) ]
        dist += distance(map.cities[city1] , map.cities[city2])
    return dist
def create_population(pop_size , city_list):
    population = []
    for i in range(pop_size):
        individual = city_list.copy()
        random.shuffle(individual)
        population.append(individual)
    return population

def select_parent(population , tournament_size):
    tournament = random.sample(population , tournament_size)
    tournament.sort(key=lambda x : router_distance(x))
    return tournament[0]
def crossover(parent1 , parent2):
    size = len(parent1)
    child = [None]*size

    start, end = sorted(random.sample(range(size), 2))
    child[start:end] = parent1[start:end]

    ptr = end
    for city in parent2[end:] + parent2[:end]:
        if city not in child[start:end]:
            if ptr >= size :
                ptr = 0
            child[ptr] = city
            ptr += 1
    return child
def mutate(individual , mutation_rate):
    if random.random() < mutation_rate:
         i, j = random.sample(range(len(individual)), 2 )
         individual[i], individual[j] = individual[j], individual[i]
    return individual

def evolution(city_list, pop_size, generations, tournament_size,mutation_rate):
    population = create_population(pop_size, city_list)

    for gen in range(generations):
        new_population = []

        population.sort(key = lambda x: router_distance(x))
        new_population.append(population[0])

        while len(new_population) < pop_size:
            parent1 = select_parent(population, tournament_size)
            parent2 = select_parent(population, tournament_size)
            child = crossover(parent1 , parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population

    population.sort(key=lambda x :router_distance(x))
    return population[0], router_distance(population[0])


pop_size = 50
generation = 100
tournament_size = 5
mutation_rate = 0.1

initial_route = list(map.cities.keys())
# random.shuffle(initial_route)

print("Initial router ", initial_route)
print("Initial distance ", router_distance(initial_route))

best_route , best_distance = evolution(initial_route, pop_size,generation, tournament_size, mutation_rate)

print("Best route found : ", best_route)
print("Best distance" , best_distance)


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
