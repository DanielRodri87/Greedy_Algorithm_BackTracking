import matplotlib.pyplot as plt
import seaborn as sns
import os

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

def salvar_resultados(resultados_backtracking, resultados_guloso):
    """Salva e plota os resultados comparativos"""
    pasta_resultados = 'results'
    os.makedirs(pasta_resultados, exist_ok=True)
    
    print("\n📊 Gerando gráficos comparativos...")
    
    vertices = [r[0] for r in resultados_backtracking]
    tempo_back = [r[1] for r in resultados_backtracking]
    mem_back = [r[2]/1024 for r in resultados_backtracking]
    
    tempo_guloso = [r[1] for r in resultados_guloso]
    mem_guloso = [r[2]/1024 for r in resultados_guloso]
    
    print("Salvando gráfico de tempo...")
    plotar_comparativo_tempo(
        vertices, 
        tempo_back, 
        tempo_guloso,
        os.path.join(pasta_resultados, 'comparativo_tempo.png')
    )
    
    print("Salvando gráfico de memória...")
    plotar_comparativo_memoria(
        vertices,
        mem_back,
        mem_guloso,
        os.path.join(pasta_resultados, 'comparativo_memoria.png')
    )
