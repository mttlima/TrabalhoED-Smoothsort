import time
import random
import matplotlib
matplotlib.use("Agg")  # backend sem interface gráfica
import matplotlib.pyplot as plt
import os
from typing import List, Any
from operator import attrgetter

from smoothsort import smoothsort  # Importa seu algoritmo


# -----------------------------------------------------------
# 1. CLASSE DE OBJETO PERSONALIZADO
# -----------------------------------------------------------

class Pessoa:
    """Objeto usado nos testes (ordenado por idade)."""
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self.idade = idade

    __lt__ = lambda self, other: self.idade < other.idade
    __gt__ = lambda self, other: self.idade > other.idade

    def __repr__(self):
        return f"Pessoa({self.nome}, {self.idade})"


# -----------------------------------------------------------
# 2. GERAÇÃO DE LISTAS
# -----------------------------------------------------------

def gerar_lista_aleatoria(tamanho: int, tipo: str) -> List[Any]:
    if tipo == "int":
        return [random.randint(0, tamanho * 10) for _ in range(tamanho)]

    elif tipo == "str":
        chars = 'abcdefghijklmnopqrstuvwxyz'
        return [''.join(random.choices(chars, k=5)) for _ in range(tamanho)]

    elif tipo == "obj":
        nomes = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
        return [Pessoa(random.choice(nomes), random.randint(18, 60))
                for _ in range(tamanho)]

    return []


# -----------------------------------------------------------
# 3. MEDIÇÃO DE DESEMPENHO - OTIMIZADO
# -----------------------------------------------------------

def medir_desempenho(algoritmo_ord, tamanhos: List[int], tipo_dado: str, cenario: str) -> List[float]:
    tempos = []

    print(f"\n--- Smoothsort - {tipo_dado.upper()} (Cenário: {cenario}) ---")
    print(f"{'Tamanho':<12} | {'Tempo (ms)':>12}")
    print("-" * 28)

    for n in tamanhos:

        data = gerar_lista_aleatoria(n, tipo_dado)

        # ---------- Melhor Caso ----------
        if cenario == "ordenado":
            if tipo_dado == "obj":
                data.sort(key=attrgetter("idade"))  # rápido
            else:
                data.sort()

        # ---------- Pior Caso ----------
        elif cenario == "inverso":
            if tipo_dado == "obj":
                data.sort(reverse=True, key=attrgetter("idade"))
            else:
                data.sort(reverse=True)

        # ---------- Decrescente ----------
        elif cenario == "decrescente":
            # Apenas pede ordenação DESC no smoothsort
            pass

        # ---------- Aleatório ----------
        # nada a fazer

        # Medição do tempo
        data_copy = data.copy()
        start = time.time()

        algoritmo_ord(data_copy, reverse=(cenario == "decrescente"))

        end = time.time()

        tempo = (end - start) * 1000
        tempos.append(tempo)

        print(f"{n:<12} | {tempo:>10.4f}")

    return tempos


# -----------------------------------------------------------
# 4. GERAÇÃO DOS GRÁFICOS - PRONTO PARA ENTREGA
# -----------------------------------------------------------

def gerar_grafico(tamanhos: List[int], tempos: List[float], titulo: str, filename: str):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='b')

    plt.title(titulo)
    plt.xlabel("Tamanho da Entrada (N)")
    plt.ylabel("Tempo de Execução (ms)")

    plt.xscale('log')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    plt.tight_layout()

    caminho = f"graficos/{filename}"
    plt.savefig(caminho)
    plt.close()

    print(f"→ Gráfico salvo em: {caminho}")


# -----------------------------------------------------------
# 5. EXECUÇÃO PRINCIPAL
# -----------------------------------------------------------

if __name__ == "__main__":

    # Criar pasta de gráficos
    if not os.path.exists("graficos"):
        os.makedirs("graficos")

    TAMANHOS_TESTE = [100, 1_000, 10_000, 50_000, 100_000]

    # 1 - Melhor Caso
    tempos_melhor = medir_desempenho(smoothsort, TAMANHOS_TESTE, "int", "ordenado")
    gerar_grafico(TAMANHOS_TESTE, tempos_melhor,
                  "Smoothsort - Inteiros Já Ordenados (Melhor Caso O(n))",
                  "smoothsort_inteiros_melhor_caso.png")

    # 2 - Caso Médio
    tempos_medio = medir_desempenho(smoothsort, TAMANHOS_TESTE, "int", "aleatório")
    gerar_grafico(TAMANHOS_TESTE, tempos_medio,
                  "Smoothsort - Inteiros Aleatórios (Caso Médio O(n log n))",
                  "smoothsort_inteiros_aleatorios.png")

    # 3 - Pior Caso
    tempos_pior = medir_desempenho(smoothsort, TAMANHOS_TESTE, "int", "inverso")
    gerar_grafico(TAMANHOS_TESTE, tempos_pior,
                  "Smoothsort - Inteiros Inversamente Ordenados (Pior Caso O(n log n))",
                  "smoothsort_inteiros_pior_caso.png")

    # 4 - Strings
    tempos_str = medir_desempenho(smoothsort, TAMANHOS_TESTE, "str", "aleatório")
    gerar_grafico(TAMANHOS_TESTE, tempos_str,
                  "Smoothsort - Desempenho em Strings Aleatórias",
                  "smoothsort_strings_aleatorias.png")
    
    # --- CENÁRIO 5: TIPOS DE DADOS - OBJETOS ---
    tempos_objetos = medir_desempenho(smoothsort, TAMANHOS_TESTE, "obj", "aleatório")
    gerar_grafico(
        TAMANHOS_TESTE, 
        tempos_objetos, 
        "Smoothsort - Desempenho em Objetos (Chave: Idade)",
        "smoothsort_objetos_aleatorios.png"
    )

    # 6 - Decrescente
    tempos_desc = medir_desempenho(smoothsort, TAMANHOS_TESTE, "int", "decrescente")
    gerar_grafico(TAMANHOS_TESTE, tempos_desc,
                  "Smoothsort - Inteiros (Ordenação Decrescente)",
                  "smoothsort_inteiros_decrescente.png")

    print("\n✅ Testes concluídos! Gráficos gerados na pasta /graficos.")
