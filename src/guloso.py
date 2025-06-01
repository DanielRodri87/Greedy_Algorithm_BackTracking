import random
import networkx as nx
import matplotlib.pyplot as plt
import time
import tracemalloc

# Lista de cores disponíveis para os vértices
colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "cyan"]

# --- Estrutura Union-Find ---
class UnionFind:
    """
    Estrutura de dados Union-Find para detecção de ciclos em grafos.
    Implementa compressão de caminho e união por rank para otimização.
    """
    
    def __init__(self, size: int):
        """
        Inicializa a estrutura Union-Find com `size` elementos.
        Args:
            size: Número de elementos (vértices) no grafo.
        """
        self.parent = list(range(size))
        self.rank = [0] * size
    
    def find(self, u: int) -> int:
        """
        Encontra a raiz do conjunto ao qual `u` pertence, com compressão de caminho.
        Args:
            u: Elemento a ser encontrado.
        Returns:
            Raiz do conjunto de `u`.
        """
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Compressão de caminho
        return self.parent[u]
    
    def union(self, u: int, v: int) -> bool:
        """
        Une os conjuntos de `u` e `v`, se eles não estiverem no mesmo conjunto.
        Args:
            u: Primeiro elemento.
            v: Segundo elemento.
        Returns:
            True se a união foi realizada, False se já estavam no mesmo conjunto.
        """
        u_root = self.find(u)
        v_root = self.find(v)
        if u_root == v_root:
            return False
        if self.rank[u_root] < self.rank[v_root]:
            self.parent[u_root] = v_root
        else:
            self.parent[v_root] = u_root
            if self.rank[u_root] == self.rank[v_root]:
                self.rank[u_root] += 1  # União por rank
        return True

# --- Classe Graph ---
class Graph:
    """
    Representa um grafo não dirigido com vértices e arestas ponderadas.
    """
    
    def __init__(self):
        """
        Inicializa um grafo vazio.
        """
        self._vertices = []
        self._edges = []
        self._adjacency_list = {}
    
    def get_vertices(self) -> list:
        """
        Retorna a lista de vértices do grafo.
        
        Returns:
            Lista de vértices.
        """
        return self._vertices
    
    def get_edges(self) -> list:
        """
        Retorna a lista de arestas do grafo.
        
        Returns:
            Lista de arestas, cada uma como uma tupla (u, v, w).
        """
        return self._edges
    
    def get_adjacency_list(self) -> dict:
        """
        Retorna a lista de adjacência do grafo.
        
        Returns:
            Dicionário onde as chaves são vértices e os valores são listas de tuplas (vizinho, peso).
        """
        return self._adjacency_list
    
    def generate_graph(self, num_vertices: int, density: float):
        """
        Gera um grafo aleatório conexo com base na densidade de arestas.

        Args:
            num_vertices: Número de vértices.
            density: Probabilidade de adicionar arestas extras além da árvore mínima.
        """
        self._vertices = list(range(num_vertices))
        self._edges = []
        self._adjacency_list = {i: [] for i in range(num_vertices)}
        
        # Cria uma árvore geradora aleatória para garantir conexidade (n - 1 arestas)
        vertices = list(range(num_vertices))
        random.shuffle(vertices)
        for i in range(1, num_vertices):
            u = vertices[i]
            v = vertices[random.randint(0, i - 1)]
            w = random.randint(1, 15)
            self._edges.append((u, v, w))
            self._adjacency_list[u].append((v, w))
            self._adjacency_list[v].append((u, w))

        # Tenta adicionar arestas extras com base na densidade
        possible_edges = [(i, j) for i in range(num_vertices) for j in range(i + 1, num_vertices)]
        used_edges = {(min(u, v), max(u, v)) for u, v, _ in self._edges}
        
        for u, v in possible_edges:
            if (u, v) not in used_edges and random.random() < density:
                w = random.randint(1, 15)
                self._edges.append((u, v, w))
                self._adjacency_list[u].append((v, w))
                self._adjacency_list[v].append((u, w))


# --- Funções Auxiliares ---
def kruskal(graph: Graph) -> list:
    """
    Aplica o algoritmo de Kruskal para encontrar a Árvore Geradora Mínima (MST) do grafo.
    
    Args:
        graph: Instância da classe Graph representando o grafo.
    Returns:
        Lista de arestas da MST, cada uma como uma tupla (u, v, w).
    """
    num_vertices = len(graph.get_vertices())
    edges = sorted(graph.get_edges(), key=lambda x: x[2])  # Ordena as arestas pelo peso
    
    uf = UnionFind(num_vertices)
    mst = []
    for u, v, w in edges:
        print(f"Verificando aresta {u} - {v} : {w}")
        if uf.union(u, v):
            mst.append((u, v, w))
    return mst

def build_mst_adjacency_list(mst: list, num_vertices: int) -> dict:
    """
    Constrói a lista de adjacência para a MST a partir da lista de arestas da MST.
    
    Args:
        mst: Lista de arestas da MST.
        num_vertices: Número de vértices no grafo.
    Returns:
        Dicionário representando a lista de adjacência da MST.
    """
    adj_list = {i: [] for i in range(num_vertices)}
    for u, v, _ in mst:
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list


def greedy_coloring(adjacency_list: dict, colors: list) -> list:
    """
    Realiza a coloração gulosa dos vértices com base na lista de adjacência.
    
    Args:
        adjacency_list: Lista de adjacência do grafo.
        colors: Lista de cores disponíveis.
    Returns:
        Lista onde cada elemento é a cor atribuída ao vértice correspondente.
    """
    num_vertices = len(adjacency_list)
    vertex_colors = [None] * num_vertices
    for vertex in range(num_vertices):
        used_colors = {vertex_colors[neighbor] for neighbor in adjacency_list[vertex] 
                       if vertex_colors[neighbor] is not None}
        for color in colors:
            if color not in used_colors:
                vertex_colors[vertex] = color
                break
    return vertex_colors


def greedy_coloring_by_degree(adjacency_list: dict, colors: list) -> list:
    num_vertices = len(adjacency_list)
    vertex_degrees = [(v, len(adjacency_list[v])) for v in range(num_vertices)]
    sorted_vertices = [v for v, _ in sorted(vertex_degrees, key=lambda x: x[1], reverse=True)]
    vertex_colors = [None] * num_vertices
    for vertex in sorted_vertices:
        used_colors = {vertex_colors[neighbor] for neighbor in adjacency_list[vertex] 
                       if vertex_colors[neighbor] is not None}
        for color in colors:
            if color not in used_colors:
                vertex_colors[vertex] = color
                break
    return vertex_colors

def executar_guloso():
    """Executa experimentos do algoritmo guloso"""
    tamanhos_grafos = [10, 15, 20, 25, 50]
    resultados = []
    
    print("\n🚀 Iniciando experimentos de coloração de grafos (Guloso)...")
    print("| Vértices | Tempo (ms) | Memória (KB) |")
    print("|----------|------------|--------------|")
    
    for num_vertices in tamanhos_grafos:
        inicio_tempo = time.perf_counter()
        tracemalloc.start()
        
        graph = Graph()
        graph.generate_graph(num_vertices, 0.4)
        
        # CORREÇÃO: Usar o grafo original (não a MST)
        adj_list = graph.get_adjacency_list()
        # Remover pesos das arestas
        adj_list_unweighted = {
            v: [neighbor for neighbor, _ in neighbors] 
            for v, neighbors in adj_list.items()
        }
        vertex_colors = greedy_coloring(adj_list_unweighted, colors)
        
        memoria = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        tempo = (time.perf_counter() - inicio_tempo) * 1000
        
        resultados.append((num_vertices, tempo, memoria))
        print(f"| {num_vertices:8d} | {tempo:9.2f} | {memoria/1024:11.2f} |")
    
    return resultados

def executar_guloso_por_grau():
    """Executa experimentos do algoritmo guloso"""
    tamanhos_grafos = [10, 15, 20, 25, 50]
    resultados = []
    
    print("\n🚀 Iniciando experimentos de coloração de grafos (Guloso)...")
    print("| Vértices | Tempo (ms) | Memória (KB) |")
    print("|----------|------------|--------------|")
    
    for num_vertices in tamanhos_grafos:
        inicio_tempo = time.perf_counter()
        tracemalloc.start()
        
        graph = Graph()
        graph.generate_graph(num_vertices, 0.4)
        
        # CORREÇÃO: Usar o grafo original (não a MST)
        adj_list = graph.get_adjacency_list()
        # Remover pesos das arestas
        adj_list_unweighted = {
            v: [neighbor for neighbor, _ in neighbors] 
            for v, neighbors in adj_list.items()
        }
        vertex_colors = greedy_coloring_by_degree(adj_list_unweighted, colors)
        
        memoria = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        tempo = (time.perf_counter() - inicio_tempo) * 1000
        
        resultados.append((num_vertices, tempo, memoria))
        print(f"| {num_vertices:8d} | {tempo:9.2f} | {memoria/1024:11.2f} |")
    
    return resultados


if __name__ == "__main__":
    # from .results import salvar_resultados
    import tracemalloc
    
    resultados_guloso = executar_experimentos()
    print("\n✅ Experimentos do algoritmo guloso concluídos!")