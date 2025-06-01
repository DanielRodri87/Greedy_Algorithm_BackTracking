from src.backtracking import executar_experimentos_bt
from src.guloso import executar_guloso, executar_guloso_por_grau    
from src.results import salvar_resultados

def main():
    print("="*70)
    print("COMPARAÇÃO DE ALGORITMOS DE COLORAÇÃO".center(70))
    print("="*70)
    
    # Executa experimentos com backtracking puro
    resultados_backtracking = executar_experimentos_bt()
    
    # Executa experimentos com algoritmo guloso
    resultados_guloso = executar_guloso()

    resultados_guloso2 = executar_guloso_por_grau()
    
    # Salva resultados comparativos
    salvar_resultados(resultados_backtracking, resultados_guloso, resultados_guloso2)
    
    print("\n✨ Resultados comparativos gerados com sucesso!")
    print("📊 Verifique os gráficos na pasta 'results'")

if __name__ == "__main__":
    main()
