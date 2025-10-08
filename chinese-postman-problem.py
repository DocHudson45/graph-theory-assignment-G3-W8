from collections import defaultdict, deque
from itertools import combinations
import sys

class ChinesePostman:
    def __init__(self):
        self.graph = defaultdict(list)
        self.edges = []
        self.vertices = set()
        
    def add_edge(self, edge_id, u, v, cost):
        self.graph[u].append((v, cost, edge_id))
        self.graph[v].append((u, cost, edge_id))
        self.edges.append((edge_id, u, v, cost))
        self.vertices.add(u)
        self.vertices.add(v)
    
    def get_degree(self):
        degree = defaultdict(int)
        for u in self.vertices:
            degree[u] = len(self.graph[u])
        return degree
    
    def find_odd_vertices(self):
        degree = self.get_degree()
        odd_vertices = []
        for v in self.vertices:
            if degree[v] % 2 == 1:
                odd_vertices.append(v)
        return odd_vertices
    
    def shortest_path(self, start, end):
        # find shortest path between 2 vertices using dijkstra
        if start == end:
            return 0, []
        dist = defaultdict(lambda: float('inf'))
        parent = {}
        dist[start] = 0
        visited = set()
        while len(visited) < len(self.vertices):
            min_dist = float('inf')
            u = None
            for v in self.vertices:
                if v not in visited and dist[v] < min_dist:
                    min_dist = dist[v]
                    u = v
            if u is None or dist[u] == float('inf'):
                break 
            visited.add(u)
            seen_neighbors = {}
            for v, cost, edge_id in self.graph[u]:
                if v not in seen_neighbors or cost < seen_neighbors[v]:
                    seen_neighbors[v] = cost
            for v, min_cost in seen_neighbors.items():
                if dist[u] + min_cost < dist[v]:
                    dist[v] = dist[u] + min_cost
                    parent[v] = u
        if end not in parent and start != end:
            return float('inf'), []
        path = []
        current = end
        while current != start:
            path.append(current)
            if current not in parent:
                return float('inf'), []
            current = parent[current]
        path.append(start)
        path.reverse()
        return dist[end], path
    
    def find_minimum_matching(self, odd_vertices):
        if len(odd_vertices) == 0:
            return []
        n_odd = len(odd_vertices)
        pairwise_dist = {}
        pairwise_path = {}
        for i in range(n_odd):
            for j in range(i + 1, n_odd):
                u, v = odd_vertices[i], odd_vertices[j]
                dist, path = self.shortest_path(u, v)
                pairwise_dist[(i, j)] = dist
                pairwise_path[(i, j)] = path

        def find_all_matchings(vertices):
            if len(vertices) == 0:
                return [[]]
            if len(vertices) == 2:
                return [[(vertices[0], vertices[1])]]
            matchings = []
            first = vertices[0]
            rest = vertices[1:]
            for i, second in enumerate(rest):
                remaining = rest[:i] + rest[i+1:]
                for matching in find_all_matchings(remaining):
                    matchings.append([(first, second)] + matching)
            return matchings
        indices = list(range(n_odd))
        all_matchings = find_all_matchings(indices)
        min_cost = float('inf')
        best_matching = None
        for matching in all_matchings:
            cost = sum(pairwise_dist[(min(i, j), max(i, j))] for i, j in matching)
            if cost < min_cost:
                min_cost = cost
                best_matching = matching
        result = []
        if best_matching:
            for i, j in best_matching:
                u, v = odd_vertices[i], odd_vertices[j]
                path = pairwise_path[(min(i, j), max(i, j))]
                result.append((u, v, path))
        return result
    
    def find_eulerian_path(self, start):
        adj = defaultdict(list)
        for u in self.graph:
            for v, cost, edge_id in self.graph[u]:
                adj[u].append((v, edge_id))
        for u in adj:
            adj[u].sort(key=lambda x: x[0])
        used_edges = set()
        stack = [start]
        path = []
        while stack:
            curr = stack[-1]
            found = False
            while adj[curr]:
                next_v, edge_id = adj[curr].pop(0)
                if edge_id not in used_edges:
                    used_edges.add(edge_id)
                    stack.append(next_v)
                    found = True
                    break
            if not found:
                path.append(stack.pop())
        path.reverse()
        return path

    def solve(self, start):
        total_cost = sum(cost for _, _, _, cost in self.edges)
        odd_vertices = self.find_odd_vertices()
        matching = self.find_minimum_matching(odd_vertices)
        matching_cost = 0
        for u, v, path in matching:
            for i in range(len(path) - 1):
                from_v = path[i]
                to_v = path[i + 1]
                min_cost = float('inf')
                min_edge = None
                for neighbor, cost, edge_id in self.graph[from_v]:
                    if neighbor == to_v and cost < min_cost:
                        min_cost = cost
                        min_edge = (neighbor, cost, edge_id)
                if min_edge:
                    neighbor, cost, edge_id = min_edge
                    self.graph[from_v].append((neighbor, cost, edge_id))
                    self.graph[to_v].append((from_v, cost, edge_id))
                    matching_cost += cost
        route = self.find_eulerian_path(start)
        final_cost = total_cost + matching_cost
        return final_cost, route

def main():
    n = int(input())
    e = int(input())
    cpp = ChinesePostman()
    for _ in range(e):
        parts = list(map(int, input().split()))
        edge_id = parts[0]
        u = parts[1]
        v = parts[2]
        cost = parts[3]
        cpp.add_edge(edge_id, u, v, cost)
    start = int(input())
    cost, route = cpp.solve(start)
    print(f"\nCost: {cost}")
    route_str = ", ".join(map(str, route))
    print(f"Route: {route_str}")

if __name__ == "__main__":
    main()