from functools import lru_cache

# Example graph with 4 cities and distances
graph = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]

n = len(graph)


# Bitmask DP TSP
@lru_cache(maxsize=None)
def tsp(mask, pos):
    """
    mask : int -> bitmask representing visited cities
    pos : int -> current city
    returns minimum cost to visit all cities starting from pos
    """
    if mask == (1 << n) - 1:
        return graph[pos][0]  # Return to starting city

    ans = float("inf")
    for city in range(n):
        if mask & (1 << city) == 0:  # If city not visited
            ans = min(ans, graph[pos][city] + tsp(mask | (1 << city), city))
    return ans


# Start TSP from city 0
min_cost = tsp(1, 0)
print(f"Minimum cost to visit all cities: {min_cost}")


# Optional: reconstruct path
def reconstruct_path():
    mask = 1
    pos = 0
    path = [0]
    while mask != (1 << n) - 1:
        next_city = None
        best_cost = float("inf")
        for city in range(n):
            if mask & (1 << city) == 0:
                cost = graph[pos][city] + tsp(mask | (1 << city), city)
                if cost < best_cost:
                    best_cost = cost
                    next_city = city
        path.append(next_city)
        mask |= 1 << next_city
        pos = next_city
    path.append(0)  # return to start
    return path


print("Optimal path:", reconstruct_path())
