import itertools

n = int(input()) 
e = int(input()) 

INF = float('inf')
graph = [[INF]*(n+1) for _ in range(n+1)]
edge_used = {}

for _ in range(e):
    eid, u, v, w = map(int, input().split())
    if w < graph[u][v]:
        graph[u][v] = w
        graph[v][u] = w
        edge_used[(u, v)] = eid
        edge_used[(v, u)] = eid

start = int(input()) 

nodes = list(range(1, n+1))
min_cost = INF
best_edges = []

for perm in itertools.permutations([x for x in nodes if x != start]):
    path = [start] + list(perm) + [start]
    cost = 0
    edges_taken = []
    valid = True
    for i in range(len(path)-1):
        u, v = path[i], path[i+1]
        if graph[u][v] == INF:
            valid = False
            break
        cost += graph[u][v]
        edges_taken.append(edge_used[(u, v)])
    if valid and cost < min_cost:
        min_cost = cost
        best_edges = edges_taken

print("Cost:", min_cost)
print("Route:", ", ".join(map(str, best_edges)))

