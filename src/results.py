import matplotlib.pyplot as plt
import seaborn as sns
import os
import networkx as nx
import random
from .backtracking import backtracking_coloring
from .guloso import greedy_coloring, greedy_coloring_by_degree, colors

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

def plotar_comparativo_tempo(vertices, tempo_backtracking, tempo_guloso, caminho):
    """Gráfico comparativo de tempo de execução"""
    plt.figure(figsize=(12, 8))
    
    plt.plot(vertices, tempo_backtracking, 'o-', label='Backtracking Puro', linewidth=3, markersize=10)
    plt.plot(vertices, tempo_guloso, 's-', label='Algoritmo Guloso', linewidth=3, markersize=10)
    
    plt.title('Comparação de Tempo de Execução', fontsize=20, pad=20)
    plt.xlabel('Número de Vértices', fontsize=16, labelpad=15)
    plt.ylabel('Tempo (ms)', fontsize=16, labelpad=15)
    plt.legend(fontsize=14)
    plt.grid(True, alpha=0.3)
    
    plt.savefig(caminho, bbox_inches='tight', dpi=120)
    plt.close()

def plotar_comparativo_memoria(vertices, mem_backtracking, mem_guloso, caminho):
    """Gráfico comparativo de uso de memória"""
    plt.figure(figsize=(12, 8))
    
    width = 0.35
    x = range(len(vertices))
    
    plt.bar([i - width/2 for i in x], mem_backtracking, width, label='Backtracking Puro', alpha=0.8)
    plt.bar([i + width/2 for i in x], mem_guloso, width, label='Algoritmo Guloso', alpha=0.8)
    
    plt.title('Comparação de Uso de Memória', fontsize=20, pad=20)
    plt.xlabel('Número de Vértices', fontsize=16, labelpad=15)
    plt.ylabel('Memória (KB)', fontsize=16, labelpad=15)
    plt.xticks(x, vertices)
    plt.legend(fontsize=14)
    
    plt.savefig(caminho, bbox_inches='tight', dpi=120)
    plt.close()

def plotar_exemplo_grafo(G, colors, titulo, caminho):
    """Plota um exemplo de grafo colorido"""
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=500)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos)
    
    plt.title(titulo, fontsize=16, pad=20)
    plt.axis('off')
    plt.savefig(caminho, bbox_inches='tight', dpi=120)
    plt.close()

def gerar_grafo_exemplo(num_vertices=8, densidade=0.4):
    """Gera um grafo de exemplo para visualização"""
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))
    
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < densidade:
                G.add_edge(i, j)
    
    return G

def salvar_resultados(resultados_backtracking, resultados_guloso1, resultados_guloso2):
    """Salva e plota os resultados comparativos"""
    pasta_resultados = 'results'
    os.makedirs(pasta_resultados, exist_ok=True)
    
    print("\n📊 Gerando gráficos comparativos...")
    
    # Gerar exemplos visuais
    print("Gerando exemplos visuais dos algoritmos...")
    G = gerar_grafo_exemplo()
    
    # Converter grafo para formato adequado
    adj_list = {n: list(G.neighbors(n)) for n in G.nodes()}
    
    # Colorir com backtracking
    cores_bt = backtracking_coloring(adj_list, len(colors))
    if cores_bt:
        plotar_exemplo_grafo(G, cores_bt, 
                           'Exemplo de Coloração - Backtracking',
                           os.path.join(pasta_resultados, 'exemplo_backtracking.png'))
    
    # Colorir com algoritmo guloso
    cores_guloso = greedy_coloring(adj_list, colors)
    plotar_exemplo_grafo(G, cores_guloso, 
                        'Exemplo de Coloração - Gulosoem em Ordem',
                        os.path.join(pasta_resultados, 'exemplo_guloso.png'))
    
    # Colorir com algoritmo guloso por grau
    cores_guloso_grau = greedy_coloring_by_degree(adj_list, colors)
    plotar_exemplo_grafo(G, cores_guloso_grau, 
                        'Exemplo de Coloração - Guloso por Grau',
                        os.path.join(pasta_resultados, 'exemplo_guloso_grau.png'))    

    # Gerar gráficos de desempenho
    vertices = [r[0] for r in resultados_backtracking]
    tempo_back = [r[1] for r in resultados_backtracking]
    mem_back = [r[2]/1024 for r in resultados_backtracking]
    
    tempo_guloso = [r[1] for r in resultados_guloso1]
    mem_guloso = [r[2]/1024 for r in resultados_guloso1]
    
    tempo_guloso_grau = [r[1] for r in resultados_guloso2]
    mem_guloso_grau = [r[2]/1024 for r in resultados_guloso2]
    
    print("Salvando gráficos de desempenho...")
    # Gráfico de tempo
    plt.figure(figsize=(12, 8))
    plt.plot(vertices, tempo_back, 'o-', label='Backtracking Puro', linewidth=3, markersize=10)
    plt.plot(vertices, tempo_guloso, 's-', label='Algoritmo Guloso', linewidth=3, markersize=10)
    plt.plot(vertices, tempo_guloso_grau, 'd-', label='Guloso por Grau', linewidth=3, markersize=10)
    plt.title('Comparação de Tempo de Execução', fontsize=20, pad=20)
    plt.xlabel('Número de Vértices', fontsize=16, labelpad=15)
    plt.ylabel('Tempo (ms)', fontsize=16, labelpad=15)
    plt.legend(fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(pasta_resultados, 'comparativo_tempo.png'), bbox_inches='tight', dpi=120)
    plt.close()
    
    # Gráfico de memória
    plt.figure(figsize=(12, 8))
    width = 0.25
    x = range(len(vertices))
    plt.bar([i - width for i in x], mem_back, width, label='Backtracking Puro', alpha=0.8)
    plt.bar(x, mem_guloso, width, label='Guloso em Ordem', alpha=0.8)
    plt.bar([i + width for i in x], mem_guloso_grau, width, label='Guloso por Grau', alpha=0.8)
    plt.title('Comparação de Uso de Memória', fontsize=20, pad=20)
    plt.xlabel('Número de Vértices', fontsize=16, labelpad=15)
    plt.ylabel('Memória (KB)', fontsize=16, labelpad=15)
    plt.xticks(x, vertices)
    plt.legend(fontsize=14)
    plt.savefig(os.path.join(pasta_resultados, 'comparativo_memoria.png'), bbox_inches='tight', dpi=120)
    plt.close()
