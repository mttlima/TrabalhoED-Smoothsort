import time
import random
import matplotlib.pyplot as plt
import os
from typing import List, Any
from smoothsort import smoothsort # Importa o algoritmo principal

# --- 1. CLASSE PARA TESTE DE OBJETOS (REQUISITO 2.2) ---

class Pessoa:
    """
    Classe de objeto customizado para testar a ordenação de objetos,
    onde a chave de ordenação é a 'idade'.
    """
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self.idade = idade
    
    # Métodos de comparação são necessários para que o Smoothsort
    # possa comparar instâncias de Pessoa. A ordenação é baseada na 'idade'.
    def __lt__(self, other):
        """Less Than: usado para a comparação arr[i] < arr[j]."""
        return self.idade < other.idade
    
    def __gt__(self, other):
        """Greater Than: usado para a comparação arr[i] > arr[j]."""
        return self.idade > other.idade
        
    def __repr__(self):
        """Representação para debug, se necessário."""
        return f"Pessoa({self.nome}, {self.idade})"

# --- 2. GERAÇÃO DE LISTAS DE TESTE ---

def gerar_lista_aleatoria(tamanho: int, tipo: str) -> List[Any]:
    """
    Gera uma lista de dados aleatórios para diferentes cenários.
    
    :param tamanho: O número de elementos na lista.
    :param tipo: "int", "str" ou "obj" (para Pessoa).
    :return: A lista gerada.
    """
    if tipo == "int":
        # Inteiros aleatórios dentro de uma faixa razoável
        return [random.randint(0, tamanho * 10) for _ in range(tamanho)]
    elif tipo == "str":
        # Strings aleatórias de 5 caracteres
        chars = 'abcdefghijklmnopqrstuvwxyz'
        return [''.join(random.choices(chars, k=5)) for _ in range(tamanho)]
    elif tipo == "obj":
        # Objetos 'Pessoa' com nome aleatório e idade entre 18 e 60
        nomes = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
        return [Pessoa(random.choice(nomes), random.randint(18, 60)) for _ in range(tamanho)]
    return []

# --- 3. MEDIÇÃO DE DESEMPENHO (REQUISITO 2.2) ---

def medir_desempenho(algoritmo_ord, tamanhos: List[int], tipo_dado: str, cenario: str) -> List[float]:
    """
    Mede o tempo de execução do algoritmo para diversos tamanhos e cenários.

    :param algoritmo_ord: A função de ordenação (smoothsort).
    :param tamanhos: Lista de tamanhos de N a serem testados (ex: 100, 10000).
    :param tipo_dado: Tipo de dados ("int", "str", "obj").
    :param cenario: "aleatório", "ordenado" (Melhor Caso) ou "inverso" (Pior Caso).
    :return: Lista contendo os tempos de execução em milissegundos.
    """
    tempos = []
    
    print(f"\n--- Testando Smoothsort com {tipo_dado} (Cenário: {cenario}) ---")
    print(f"{'Tamanho (N)':<15} | {'Tempo (ms)':>12}")
    print("-" * 28)
    
    for n in tamanhos:
        # 1. Preparação dos dados para o cenário específico
        data = gerar_lista_aleatoria(n, tipo=tipo_dado)
        
        if cenario == "ordenado":
            # Geração do Melhor Caso: lista já ordenada (espera-se O(n))
            data.sort(key=lambda x: x.idade if tipo_dado == 'obj' else x)
        elif cenario == "inverso":
            # Geração do Pior Caso: lista inversamente ordenada (espera-se O(n log n))
            data.sort(reverse=True, key=lambda x: x.idade if tipo_dado == 'obj' else x)
            
        # 2. Temporização (Utiliza time.time() para precisão)
        data_copy = data.copy() # Copia para garantir que a ordenação anterior não afete
        start_time = time.time()
        
        # Chamada do algoritmo: Testando a ordenação crescente (padrão)
        algoritmo_ord(data_copy, reverse=(cenario == "decrescente")) #se o cenário for descrescente usar reverse TRUE, caso contrário reverse=FALSE
        
        end_time = time.time()
        
        tempo_ms = (end_time - start_time) * 1000 # Conversão para milissegundos
        tempos.append(tempo_ms)
        print(f"{n:<15,} | {tempo_ms:>10.4f}")

    return tempos

# --- 4. GERAÇÃO DE GRÁFICOS (REQUISITO 2.3) ---

def gerar_grafico(tamanhos: List[int], tempos: List[float], titulo: str, filename: str):
    """
    Gera e salva o gráfico de tempo vs. tamanho de entrada (Matplotlib).
    (REQUISITO 4 - Qualidade dos gráficos)

    :param tamanhos: Eixo X (Tamanho da Entrada).
    :param tempos: Eixo Y (Tempo de Execução em ms).
    :param titulo: Título do gráfico.
    :param filename: Nome do arquivo para salvar.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='b', label='Smoothsort')
    
    # Configuração dos Rótulos (REQUISITO 2.3)
    plt.title(titulo) 
    plt.xlabel("Tamanho da Entrada (N)") # Eixo rotulado
    plt.ylabel("Tempo de Execução (ms)") # Eixo rotulado
    
    # Ajuste da escala para visualização de Big O em N log N
    plt.xscale('log') 
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    
    # Salvar o gráfico na pasta 'graficos/'
    save_path = f"graficos/{filename}"
    plt.savefig(save_path)
    print(f"\nGráfico salvo em: {save_path}")
    plt.close() # Fecha a figura para liberar memória

# --- 5. EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    
    # Certifica-se de que a pasta 'graficos' existe
    if not os.path.exists("graficos"):
        os.makedirs("graficos")

    # Tamanhos de entrada a serem testados (REQUISITO 2.2)
    TAMANHOS_TESTE = [100, 1_000, 10_000, 50_000, 100_000, 200_000] 
    
    # --- CENÁRIO 1: MELHOR CASO (JÁ ORDENADO) ---
    tempos_ordenados_int = medir_desempenho(smoothsort, TAMANHOS_TESTE, "int", "ordenado")
    gerar_grafico(
        TAMANHOS_TESTE, 
        tempos_ordenados_int, 
        "Smoothsort - Inteiros Já Ordenados (Melhor Caso O(n))",
        "smoothsort_inteiros_melhor_caso.png"
    )

    # --- CENÁRIO 2: INTEIROS ALEATÓRIOS (CASO MÉDIO) ---
    tempos_aleatorios_int = medir_desempenho(smoothsort, TAMANHOS_TESTE, "int", "aleatório")
    gerar_grafico(
        TAMANHOS_TESTE, 
        tempos_aleatorios_int, 
        "Smoothsort - Inteiros Aleatórios (Caso Médio O(n log n))",
        "smoothsort_inteiros_aleatorios.png"
    )

    # 3. PIOR CASO (Inteiros Inversamente Ordenados) - Espera-se O(n log n)
    # Chama a função 'medir_desempenho' com o parâmetro cenario="inverso"
    tempos_inversos_int = medir_desempenho(smoothsort, TAMANHOS_TESTE, "int", "inverso") 
    
    # Gera o gráfico específico para o pior caso
    gerar_grafico(
        TAMANHOS_TESTE, 
        tempos_inversos_int, 
        "Smoothsort - Inteiros Inversamente Ordenados (Pior Caso O(n log n))",
        "smoothsort_inteiros_pior_caso.png" # NOVO NOME DE ARQUIVO
    )
    
    # --- CENÁRIO 4: TIPOS DE DADOS - STRINGS ---
    tempos_strings = medir_desempenho(smoothsort, TAMANHOS_TESTE, "str", "aleatório")
    gerar_grafico(
        TAMANHOS_TESTE, 
        tempos_strings, 
        "Smoothsort - Desempenho em Strings Aleatórias",
        "smoothsort_strings_aleatorias.png"
    )

    # --- CENÁRIO 5: TIPOS DE DADOS - OBJETOS ---
    tempos_objetos = medir_desempenho(smoothsort, TAMANHOS_TESTE, "obj", "aleatório")
    gerar_grafico(
        TAMANHOS_TESTE, 
        tempos_objetos, 
        "Smoothsort - Desempenho em Objetos (Chave: Idade)",
        "smoothsort_objetos_aleatorios.png"
    )

    # --- CENÁRIO 6: ORDENAR DECRESCENTE ---
    tempos_decrescente = medir_desempenho(smoothsort, TAMANHOS_TESTE, "int", "decrescente")
    gerar_grafico(
        TAMANHOS_TESTE,
        tempos_decrescente,
        "Smoothsort - Inteiros (Ordenação Decrescente)",
        "smoothsort_inteiros_decrescente.png"
)

    print("\n✅ Todos os testes de desempenho foram concluídos e os gráficos foram salvos na pasta 'graficos/'.")