import random

import map

# cities = {
#     "A": (0,0),
#     "B": (1,5),
#     "C": (5,2),
#     "D": (3,6)
# }

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)** 0.5

def router_distance(route):
    dist = 0
    for i in range(len(route)):
        city1 = route[i]
        city2 = route[(i + 1 ) % len(route) ]
        dist += distance(map.cities[city1] , map.cities[city2])
        # city2 = round[:i] + route[i:k+1][::-1] + route[k+1:]
    return dist

def two_opt_swap(route, i , k):
    new_router = route[:i] + route[i:k+1][::-1] + route[k+1:]
    return new_router
def hill_climbing(route):
    best_distance = router_distance(route)
    improved = True

    while improved:
        improved = False
        for i in range(len(route) - 1):
            for k in range(i + 1 , len(route)):
                new_route = two_opt_swap(route , i , k)
                new_distance = router_distance(new_route)
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True
                    break
            if improved:
                break
        return route , best_distance

initial_route = list(map.cities.keys())
random.shuffle(initial_route)

print("Initial router ", initial_route)
print("Initial distance ", router_distance(initial_route))

best_route , best_distance = hill_climbing(initial_route)

print("Best route found : ", best_route)
print("Best distance" , best_distance)

# def f(x):
#     return - (x - 3)**2 + 5

# def hill_climb():
#     current_x = random.uniform(0,6)
#     step_size = 0.1
#     max_iteration = 100

#     for i in range(max_iteration):
#         neighbors = [current_x + step_size , current_x - step_size]
#         neighbors = [x for x in neighbors if 0 <= x <= 6 ]
#         neighbor_scores = [f(x) for x in neighbors]
#         best_neighbor_idx = neighbor_scores.index(max(neighbor_scores))
#         best_neighbor = neighbors[best_neighbor_idx]
#         if f(best_neighbor) > f(current_x):
#             current_x = best_neighbor
#         else:
#             break
#     return current_x , f(current_x)

# result_x, result_value = hill_climb()
# print(f"found maximum at x = {result_x:.2f}, value = {result_value:.2f}")
