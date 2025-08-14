# from collections import defaultdict
from collections import deque

# --------------- graph ---------------
graph = {
    "Alice": {"Bob", "Carol", "David"},
    "Bob": {"Alice", "Emily", "Frank", "Grace"},
    "Carol": {"Alice", "Hannah", "Ian"},
    "David": {"Alice", "Jack", "Kevin"},
    "Emily": {"Bob", "Liam", "Mia"},
    "Frank": {"Bob", "Noah", "Olivia"},
    "Grace": {"Bob", "Paul"},
    "Hannah": {"Carol", "Quinn"},
    "Ian": {"Carol", "Rachel", "Steve"},
    "Jack": {"David", "Tina"},
    "Kevin": {"David", "Uma"},
    "Liam": {"Emily", "Victor"},
    "Mia": {"Emily", "Wendy"},
    "Noah": {"Frank", "Xander"},
    "Olivia": {"Frank", "Yasmine"},
    "Paul": {"Grace", "Zoe"},
    "Quinn": {"Hannah", "Rachel"},
    "Rachel": {"Ian", "Quinn"},
    "Steve": {"Ian", "Tina"},
    "Tina": {"Jack", "Steve", "Uma"},
    "Uma": {"Kevin", "Tina", "Victor"},
    "Victor": {"Liam", "Uma", "Wendy"},
    "Wendy": {"Mia", "Victor", "Xander"},
    "Xander": {"Noah", "Wendy", "Yasmine"},
    "Yasmine": {"Olivia", "Xander", "Zoe"},
    "Zoe": {"Paul", "Yasmine"},
}


# --------------- BFS ---------------
def bfs_shortest_path(g, start, goal):
    if start == goal:
        return [start]
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.popleft()
        for neighbor in g[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                if neighbor == goal:  # target found → reconstruct
                    return build_path(parent, goal)
                queue.append(neighbor)
    return None  # no path


def build_path(parent, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


# --------------- run ---------------
start, end = "Alice", "Zoe"
path = bfs_shortest_path(graph, start, end)

if path:
    print("Shortest path:", " → ".join(path))
    print("Cost (hops):", len(path) - 1)
else:
    print(f"No connection between {start} and {end}")
