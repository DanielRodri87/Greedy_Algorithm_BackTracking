import random
import networkx as nx
import matplotlib.pyplot as plt
import time
import tracemalloc

colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "cyan"]

class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, u: int) -> int:
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u: int, v: int) -> bool:
        u_root = self.find(u)
        v_root = self.find(v)
        if u_root == v_root:
            return False
        if self.rank[u_root] < self.rank[v_root]:
            self.parent[u_root] = v_root
        else:
            self.parent[v_root] = u_root
            if self.rank[u_root] == self.rank[v_root]:
                self.rank[u_root] += 1
        return True

class Graph:
    def __init__(self):
        self._vertices = []
        self._edges = []
        self._adjacency_list = {}

    def get_vertices(self) -> list:
        return self._vertices

    def get_edges(self) -> list:
        return self._edges

    def get_adjacency_list(self) -> dict:
        return self._adjacency_list

    def generate_graph(self, num_vertices: int, density: float):
        self._vertices = list(range(num_vertices))
        self._edges = []
        self._adjacency_list = {i: [] for i in range(num_vertices)}

        vertices = list(range(num_vertices))
        random.shuffle(vertices)
        for i in range(1, num_vertices):
            u = vertices[i]
            v = vertices[random.randint(0, i - 1)]
            w = random.randint(1, 15)
            self._edges.append((u, v, w))
            self._adjacency_list[u].append((v, w))
            self._adjacency_list[v].append((u, w))

        possible_edges = [(i, j) for i in range(num_vertices) for j in range(i + 1, num_vertices)]
        used_edges = {(min(u, v), max(u, v)) for u, v, _ in self._edges}

        for u, v in possible_edges:
            if (u, v) not in used_edges and random.random() < density:
                w = random.randint(1, 15)
                self._edges.append((u, v, w))
                self._adjacency_list[u].append((v, w))
                self._adjacency_list[v].append((u, w))

def kruskal(graph: Graph) -> list:
    num_vertices = len(graph.get_vertices())
    edges = sorted(graph.get_edges(), key=lambda x: x[2])
    uf = UnionFind(num_vertices)
    mst = []
    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
    return mst

def build_mst_adjacency_list(mst: list, num_vertices: int) -> dict:
    adj_list = {i: [] for i in range(num_vertices)}
    for u, v, _ in mst:
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list

def is_safe(vertex, color, assignment, adjacency_list):
    for neighbor in adjacency_list[vertex]:
        if assignment[neighbor] == color:
            return False
    return True

def backtracking_coloring(adjacency_list: dict, max_colors: int) -> list:
    num_vertices = len(adjacency_list)
    assignment = [-1] * num_vertices

    def backtrack(v):
        if v == num_vertices:
            return True
        for color in range(max_colors):
            if is_safe(v, color, assignment, adjacency_list):
                assignment[v] = color
                if backtrack(v + 1):
                    return True
                assignment[v] = -1
        return False

    for m in range(1, len(colors) + 1):
        if backtrack(0):
            return [colors[c] for c in assignment]
    return None  # Falha ao encontrar coloração

def plot_mst(mst: list, vertex_colors: list, num_vertices: int):
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))
    for u, v, w in mst:
        G.add_edge(u, v, weight=w)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=[vertex_colors[v] for v in G.nodes()], node_size=200)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

def executar_experimentos_bt():
    tamanhos_grafos = [5, 8, 10, 12, 15]
    resultados = []

    print("\n🚀 Iniciando experimentos de coloração de grafos (Backtracking)...")
    print("| Vértices | Tempo (ms) | Memória (KB) |")
    print("|----------|------------|--------------|")

    for num_vertices in tamanhos_grafos:
        inicio_tempo = time.perf_counter()
        tracemalloc.start()

        graph = Graph()
        graph.generate_graph(num_vertices, 0.4)
        
        # Usar o grafo original (não a MST)
        adj_list = graph.get_adjacency_list()
        # Remover pesos das arestas
        adj_list_unweighted = {
            v: [neighbor for neighbor, _ in neighbors] 
            for v, neighbors in adj_list.items()
        }
        vertex_colors = backtracking_coloring(adj_list_unweighted, len(colors))

        memoria = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        tempo = (time.perf_counter() - inicio_tempo) * 1000

        resultados.append((num_vertices, tempo, memoria))
        print(f"| {num_vertices:8d} | {tempo:9.2f} | {memoria/1024:11.2f} |")

    return resultados

if __name__ == "__main__":
    from .results import salvar_resultados
    resultados_backtracking = executar_experimentos_bt()
    print("\n✅ Experimentos do algoritmo backtracking concluídos!")
