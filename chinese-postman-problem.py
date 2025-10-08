from collections import defaultdict, deque
from itertools import combinations
import sys

class ChinesePostman:
    def __init__(self):
        self.graph = defaultdict(list)  
        self.edges = []  
        self.nodes = set()  
    def add_edge(self, edge_id, u, v, weight):
        self.edges.append((edge_id, u, v, weight))
        self.graph[u].append((v, weight, edge_id))
        self.graph[v].append((u, weight, edge_id))
        self.nodes.add(u)
        self.nodes.add(v)
    
    def get_degrees(self):
        degrees = {}
        for node in self.graph:
            degrees[node] = len(self.graph[node])
        return degrees
    
    def find_odd_vertices(self):
        degrees = self.get_degrees()
        odd_vertices = [node for node in self.nodes if degrees[node] % 2 == 1]
        return odd_vertices
    
    def find_shortest_paths(self):
        INF = float('inf')
        nodes_list = list(self.nodes)
        dist = defaultdict(lambda: defaultdict(lambda: INF))
        next_node = defaultdict(lambda: defaultdict(lambda: None))
        for node in nodes_list:
            dist[node][node] = 0
        for node in nodes_list:
            for neighbor, weight, _ in self.graph[node]:
                if weight < dist[node][neighbor]:
                    dist[node][neighbor] = weight
                    next_node[node][neighbor] = neighbor
        for k in nodes_list:
            for i in nodes_list:
                for j in nodes_list:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]
        return dist, next_node

    def find_min_weight_matching(self, odd_vertices, dist):
        if len(odd_vertices) == 0:
            return []
        min_cost = float('inf')
        best_matching = None
        def generate_pairings(vertices):
            if len(vertices) == 0:
                return [[]]
            if len(vertices) == 2:
                return [[(vertices[0], vertices[1])]]
            first = vertices[0]
            rest = vertices[1:]
            pairings = []
            for i, partner in enumerate(rest):
                pair = (first, partner)
                remaining = rest[:i] + rest[i+1:]
                for sub_pairing in generate_pairings(remaining):
                    pairings.append([pair] + sub_pairing)
            return pairings
        all_pairings = generate_pairings(odd_vertices)
        for pairing in all_pairings:
            cost = sum(dist[u][v] for u, v in pairing)
            if cost < min_cost:
                min_cost = cost
                best_matching = pairing
        return best_matching

    def get_path_edges(self, u, v, next_node):
        if next_node[u][v] is None:
            return []
        path = []
        current = u
        while current != v:
            next_vertex = next_node[current][v]
            best_eid = None
            best_weight = float('inf')
            for neighbor, weight, eid in self.graph[current]:
                if neighbor == next_vertex and weight < best_weight:
                    best_weight = weight
                    best_eid = eid
            path.append(best_eid)
            current = next_vertex
        return path

    def build_adjacency_matrix(self):
        adj_matrix = defaultdict(lambda: defaultdict(list))
        for node in self.graph:
            for neighbor, weight, eid in self.graph[node]:
                adj_matrix[node][neighbor].append(eid)
        for node in adj_matrix:
            for neighbor in adj_matrix[node]:
                adj_matrix[node][neighbor].sort()
        return adj_matrix

    def find_eulerian_circuit(self, adj_matrix, start):
        circuit = []
        stack = [start]
        current_path = []
        while stack:
            v = stack[-1]
            found = False
            for u in sorted(adj_matrix[v].keys()):
                if adj_matrix[v][u]:
                    eid = adj_matrix[v][u].pop(0)
                    if eid in adj_matrix[u][v]:
                        adj_matrix[u][v].remove(eid)
                    current_path.append(eid)
                    stack.append(u)
                    found = True
                    break
            if not found:
                if current_path:
                    circuit.append(current_path.pop())
                stack.pop()
        return circuit[::-1]

    def solve(self, start):
        total_cost = sum(w for _, _, _, w in self.edges)
        odd_vertices = self.find_odd_vertices()
        adj_matrix = self.build_adjacency_matrix()
        duplicate_cost = 0
        if len(odd_vertices) > 0:
            dist, next_node = self.find_shortest_paths()
            matching = self.find_min_weight_matching(odd_vertices, dist)
            for u, v in matching:
                duplicate_cost += dist[u][v]
                path_edges = self.get_path_edges(u, v, next_node)
                for eid in path_edges:
                    for edge_id, node_u, node_v, weight in self.edges:
                        if edge_id == eid:
                            adj_matrix[node_u][node_v].append(eid)
                            adj_matrix[node_v][node_u].append(eid)
                            break
            for node in adj_matrix:
                for neighbor in adj_matrix[node]:
                    adj_matrix[node][neighbor].sort()
        circuit = self.find_eulerian_circuit(adj_matrix, start)
        return total_cost + duplicate_cost, circuit

def main():
    n = int(input())
    e = int(input())
    cpp = ChinesePostman()
    for _ in range(e):
        eid, u, v, w = map(int, input().split())
        cpp.add_edge(eid, u, v, w)
    start = int(input())
    cost, route = cpp.solve(start)
    print(f"Cost: {cost}")
    print(f"Route: {', '.join(map(str, route))}")

if __name__ == "__main__":
    main()