import math
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
    return dist

def get_neighbor(route):
    i , k = sorted(random.sample(range(1, len(route)),2))
    new_router = route[:i] + route[i:k+1][::-1] + route[k+1:]
    return new_router

def simulated_annealing(initial_route, initial_temp, cooling_rate,min_temp,max_iter):
    current_route = initial_route.copy()
    current_distance = router_distance(current_route)
    best_route = current_route.copy()
    best_distance = current_distance

    temp = initial_temp
    iteration = 0

    while temp > min_temp and  iteration < max_iter:
        neighbor_route = get_neighbor(current_route)
        neighbor_distance = router_distance(neighbor_route)

        delta = neighbor_distance - current_distance

        if delta < 0 and random.random() < math.exp(-delta / temp):
            current_route = neighbor_route
            current_distance = neighbor_distance

            if current_distance < best_distance:
                best_route = current_route.copy()
                best_distance = current_distance
        # else :
            # accept =  random.random() < math.exp(-delta / temp)  #P(accept) = e^(- change E/T)
            # current_route = neighbor_route
            # current_distance = neighbor_distance
        temp *= cooling_rate      #cooling rate Tnew = Told * a  ... a = 0.995
        return best_route , best_distance

initial_temp = 1000  # high starting temp
cooling_rate = 0.995
min_temp = 0.1
max_iter = 10000

initial_route = list(map.cities.keys())
random.shuffle(initial_route)

print("Initial router ", initial_route)
print("Initial distance ", router_distance(initial_route))

best_route , best_distance = simulated_annealing(initial_route, initial_temp, cooling_rate, min_temp, max_iter)

print("Best route found : ", best_route)
print("Best distance" , best_distance)
