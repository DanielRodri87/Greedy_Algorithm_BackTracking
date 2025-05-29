import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import time
import tracemalloc
import os
import random
import numpy as np
import seaborn as sns
from collections import defaultdict

# Configuração de estilo para gráficos modernos
sns.set_theme(style="whitegrid", palette="pastel")
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.figsize': (12, 8),
    'figure.dpi': 120
})

class Grafo:
    def __init__(self, vertices):
        self.V = vertices
        self.grafo = [[0] * vertices for _ in range(vertices)]
        self.nome_vertices = [f'V{i}' for i in range(vertices)]
        self.graus = [0] * vertices
    
    def adicionar_aresta(self, u, v):
        self.grafo[u][v] = 1
        self.grafo[v][u] = 1
        self.graus[u] += 1
        self.graus[v] += 1

    def eh_seguro(self, vertice, cor, cores):
        for i in range(self.V):
            if self.grafo[vertice][i] == 1 and cores[i] == cor:
                return False
        return True

    def dsatur_ordenacao(self):
        """Ordena vértices por saturação (cores adjacentes) e grau"""
        cores_adj = [set() for _ in range(self.V)]
        nao_coloridos = set(range(self.V))
        ordem = []
        
        while nao_coloridos:
            # Encontra o vértice com maior saturação
            max_sat = -1
            candidato = -1
            
            for v in nao_coloridos:
                sat = len(cores_adj[v])
                if sat > max_sat or (sat == max_sat and self.graus[v] > self.graus[candidato]):
                    max_sat = sat
                    candidato = v
            
            ordem.append(candidato)
            nao_coloridos.remove(candidato)
            
            # Atualiza saturação dos vizinhos
            for vizinho in range(self.V):
                if self.grafo[candidato][vizinho] and vizinho in nao_coloridos:
                    cores_adj[vizinho].add(candidato)
        
        return ordem

    def backtracking_dsatur(self, k, cores, pos, ordem):
        """Backtracking com ordenação DSATUR"""
        if pos == len(ordem):
            return True
            
        vertice = ordem[pos]
        
        # Tenta cores em ordem crescente
        for cor in range(1, k + 1):
            if self.eh_seguro(vertice, cor, cores):
                cores[vertice] = cor
                if self.backtracking_dsatur(k, cores, pos + 1, ordem):
                    return True
                cores[vertice] = 0  # Backtrack
                
        return False

    def colorir_grafo(self):
        """Encontra a coloração mínima usando DSATUR + Backtracking"""
        ordem = self.dsatur_ordenacao()
        
        # Encontra limite superior (DSATUR gulosso)
        cores = [0] * self.V
        for v in ordem:
            cores_adj = set()
            for viz in range(self.V):
                if self.grafo[v][viz] and cores[viz] != 0:
                    cores_adj.add(cores[viz])
            
            cor = 1
            while cor in cores_adj:
                cor += 1
            cores[v] = cor
        
        k_max = max(cores)
        
        # Refina com backtracking
        for k in range(1, k_max + 1):
            cores_tentativa = [0] * self.V
            if self.backtracking_dsatur(k, cores_tentativa, 0, ordem):
                return k, cores_tentativa
        
        return k_max, cores

def gerar_grafo_aleatorio(vertices, densidade=0.4):
    """Gera grafo aleatório com densidade controlada"""
    grafo = Grafo(vertices)
    for i in range(vertices):
        for j in range(i + 1, vertices):
            if random.random() < densidade:
                grafo.adicionar_aresta(i, j)
    return grafo

def medir_desempenho(funcao, *args):
    """Mede tempo e memória de execução"""
    inicio_tempo = time.perf_counter()
    tracemalloc.start()
    resultado = funcao(*args)
    mem_atual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tempo_exec = (time.perf_counter() - inicio_tempo) * 1000  # ms
    return tempo_exec, mem_pico, resultado

def plotar_grafo(grafo, cores, num_cores, caminho):
    """Cria visualização moderna do grafo colorido"""
    G = nx.Graph()
    
    # Paleta de cores moderna
    paleta = sns.color_palette("husl", num_cores)
    nomes_cores = [mcolors.rgb2hex(cor) for cor in paleta]
    
    # Adiciona vértices com cores
    for i in range(grafo.V):
        cor_idx = cores[i] - 1
        G.add_node(grafo.nome_vertices[i], color=nomes_cores[cor_idx])
    
    # Adiciona arestas
    for i in range(grafo.V):
        for j in range(i + 1, grafo.V):
            if grafo.grafo[i][j] == 1:
                G.add_edge(grafo.nome_vertices[i], grafo.nome_vertices[j])
    
    # Layout moderno
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, seed=42, k=0.8)
    cores_nos = [G.nodes[n]['color'] for n in G.nodes()]
    
    # Desenha com estilo moderno
    nx.draw_networkx_nodes(G, pos, node_size=900, node_color=cores_nos, 
                          alpha=0.95, edgecolors='black', linewidths=1.8)
    nx.draw_networkx_edges(G, pos, width=1.8, alpha=0.6, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', font_color='white')
    
    # Título e legenda
    plt.title(f'Coloração de Grafos (χ = {num_cores})', fontsize=20, pad=20)
    plt.axis('off')
    
    # Adicionar legenda de cores
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=nomes_cores[i], 
                         label=f'Cor {i+1}') for i in range(num_cores)]
    plt.legend(handles=legend_elements, loc='best', frameon=True, 
               shadow=True, fontsize=12, title="Legenda de Cores")
    
    plt.savefig(caminho, bbox_inches='tight', dpi=120)
    plt.close()

def plotar_grafico_tempos(vertices, tempos, caminho):
    """Gráfico moderno de tempo de execução"""
    plt.figure(figsize=(12, 8))
    
    # Gráfico de linha com área sombreada
    ax = sns.lineplot(x=vertices, y=tempos, marker='o', markersize=10, 
                     linewidth=3, color='#3498db')
    plt.fill_between(vertices, tempos, alpha=0.2, color='#3498db')
    
    # Adicionar valores nos pontos
    for i, txt in enumerate(tempos):
        ax.annotate(f'{txt:.2f} ms', (vertices[i], tempos[i]),
                   textcoords="offset points", xytext=(0,10), 
                   ha='center', fontsize=12, fontweight='bold')
    
    # Estilização
    plt.title('Tempo de Execução do Algoritmo DSATUR+Backtracking', fontsize=20, pad=20)
    plt.xlabel('Número de Vértices', fontsize=16, labelpad=15)
    plt.ylabel('Tempo (ms)', fontsize=16, labelpad=15)
    plt.grid(True, alpha=0.2)
    sns.despine(left=True, bottom=True)
    plt.savefig(caminho, bbox_inches='tight', dpi=120)
    plt.close()

def plotar_grafico_memoria(vertices, memorias, caminho):
    """Gráfico moderno de uso de memória"""
    plt.figure(figsize=(12, 8))
    
    # Gráfico de barras moderno
    ax = sns.barplot(x=vertices, y=memorias, palette='muted', alpha=0.95)
    
    # Adicionar valores nas barras
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2., height + 0.5,
                f'{height:.2f} KB', ha='center', fontsize=12, fontweight='bold')
    
    # Estilização
    plt.title('Uso de Memória do Algoritmo DSATUR+Backtracking', fontsize=20, pad=20)
    plt.xlabel('Número de Vértices', fontsize=16, labelpad=15)
    plt.ylabel('Memória (KB)', fontsize=16, labelpad=15)
    plt.grid(True, axis='y', alpha=0.2)
    sns.despine(left=True, bottom=True)
    plt.savefig(caminho, bbox_inches='tight', dpi=120)
    plt.close()

def executar_experimentos():
    """Executa experimentos e gera visualizações"""
    tamanhos_grafos = [5, 8, 10, 12, 15]
    resultados = []
    pasta_resultados = 'results'
    
    os.makedirs(pasta_resultados, exist_ok=True)
    
    print("🚀 Iniciando experimentos de coloração de grafos...")
    print("| Vértices | Tempo (ms) | Memória (KB) |")
    print("|----------|------------|--------------|")
    
    for n in tamanhos_grafos:
        grafo = gerar_grafo_aleatorio(n)
        tempo, memoria, (num_cores, cores) = medir_desempenho(grafo.colorir_grafo)
        
        resultados.append((n, tempo, memoria))
        
        # Salva visualização do grafo para tamanho médio
        if n == 10:
            caminho_grafico = os.path.join(pasta_resultados, 'grafo_colorido.png')
            plotar_grafo(grafo, cores, num_cores, caminho_grafico)
            print(f"✅ Visualização do grafo salva em {caminho_grafico}")
        
        print(f"| {n:8d} | {tempo:9.2f} | {memoria/1024:11.2f} |")
    
    # Processar resultados
    vertices = [r[0] for r in resultados]
    tempos = [r[1] for r in resultados]
    memorias = [r[2] / 1024 for r in resultados]  # KB
    
    # Gerar gráficos
    plotar_grafico_tempos(vertices, tempos, os.path.join(pasta_resultados, 'tempo_execucao.png'))
    plotar_grafico_memoria(vertices, memorias, os.path.join(pasta_resultados, 'uso_memoria.png'))
    
    print(f"📊 Gráficos de desempenho salvos em {pasta_resultados}")
    
    return resultados

if __name__ == "__main__":
    print("="*70)
    print("ALGORITMO AVANÇADO DE COLORAÇÃO DE GRAFOS".center(70))
    print("Combinação DSATUR + Backtracking".center(70))
    print("="*70)
    
    resultados = executar_experimentos()
    print("\n✅ Experimentos concluídos com sucesso!")
    
    # Demonstração final
    print("\n💡 Exemplo de coloração para grafo completo K5:")
    g = Grafo(5)
    for i in range(5):
        for j in range(i+1, 5):
            g.adicionar_aresta(i, j)
    
    num_cores, cores = g.colorir_grafo()
    print(f"Número cromático: {num_cores}")
    print(f"Coloração dos vértices: {cores}")
    
    print("\n✨ Todos os resultados foram salvos na pasta /results")