from collections import defaultdict
import heapq

class ChinesePostman:
    def __init__(self):
        self.graph = defaultdict(list)
        self.edges = {}  
        self.nodes = set()

    def add_edge(self, edge_id, u, v, weight):
        existing_edges = [(neighbor, w, eid) for neighbor, w, eid in self.graph[u] if neighbor == v and w > weight]
        if existing_edges:
            old_eid = existing_edges[0][2]
            old_weight = existing_edges[0][1]
            self.graph[u] = [(n, w, e) for n, w, e in self.graph[u] if e != old_eid]
            self.graph[v] = [(n, w, e) for n, w, e in self.graph[v] if e != old_eid]
            del self.edges[old_eid]
            self.edges[edge_id] = (u, v, weight)
            self.graph[u].append((v, weight, edge_id))
            self.graph[v].append((u, weight, edge_id))
            self.edges[old_eid] = (u, v, old_weight)
            self.graph[u].append((v, old_weight, old_eid))
            self.graph[v].append((u, old_weight, old_eid))
        else:
            self.edges[edge_id] = (u, v, weight)
            self.graph[u].append((v, weight, edge_id))
            self.graph[v].append((u, weight, edge_id))
        self.nodes.add(u)
        self.nodes.add(v)

    def get_degrees(self):
        degrees = {}
        for node in self.nodes:
            degrees[node] = len(self.graph[node])
        return degrees
    
    def find_odd_vertices(self):
        degrees = self.get_degrees()
        odd_vertices = [node for node in self.nodes if degrees[node] % 2 == 1]
        return odd_vertices
    
    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        predecessors = {node: None for node in self.nodes}
        edge_used = {}
        pq = [(0, start)]
        while pq:
            current_dist, current = heapq.heappop(pq)
            if current_dist > distances[current]:
                continue
            for neighbor, weight, edge_id in self.graph[current]:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = current
                    edge_used[neighbor] = edge_id
                    heapq.heappush(pq, (new_dist, neighbor))
        path = []
        current = end
        while predecessors[current] is not None:
            path.append(edge_used[current])
            current = predecessors[current]
        return distances[end], path[::-1]

    def find_min_weight_matching(self, odd_vertices):
        if len(odd_vertices) == 0:
            return []
        pairings = {}
        for i in range(len(odd_vertices)):
            for j in range(i + 1, len(odd_vertices)):
                u, v = odd_vertices[i], odd_vertices[j]
                dist, path = self.dijkstra(u, v)
                pairings[(u, v)] = (dist, path)
        remaining = odd_vertices[:]
        matching = []
        total_cost = 0
        matched_paths = []
        while remaining:
            current = remaining.pop(0)
            best_match = min(remaining, key=lambda v: pairings.get((min(current, v), max(current, v)), (float('inf'), []))[0])
            remaining.remove(best_match)
            key = (min(current, best_match), max(current, best_match))
            cost, path = pairings[key]
            matching.append((current, best_match))
            total_cost += cost
            matched_paths.extend(path)
        return matching, matched_paths, total_cost

    def find_eulerian_circuit(self, adj_matrix, start):
        circuit = []
        stack = [start]
        visited_edges = set()
        while stack:
            v = stack[-1]
            found = False
            for u in sorted(adj_matrix[v].keys()):
                available = [eid for eid in adj_matrix[v][u] if eid not in visited_edges]
                if available:
                    best_eid = min(available, key=lambda e: self.edges[e][2])
                    visited_edges.add(best_eid)
                    stack.append(u)
                    circuit.append(best_eid)
                    found = True
                    break
            if not found:
                stack.pop()
        return circuit[::-1]

    def solve(self, start):
        total_cost = sum(weight for _, _, weight in self.edges.values())
        odd_vertices = self.find_odd_vertices()
        duplicate_cost = 0
        matched_paths = []
        if len(odd_vertices) > 0:
            matching, matched_paths, duplicate_cost = self.find_min_weight_matching(odd_vertices)
        route = list(self.edges.keys()) + matched_paths
        return total_cost + duplicate_cost, route

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