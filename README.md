# 🌟 Projeto 02: Avaliação da Complexidade do Algoritmo Smoothsort

Este projeto tem como objetivo analisar a complexidade computacional do algoritmo de ordenação **Smoothsort** por meio de sua implementação em Python e avaliação experimental de desempenho.

## 1. O Algoritmo: Smoothsort

O Smoothsort é uma variação adaptativa e estável do Heapsort, notável por sua eficiência em listas que já estão **parcialmente ordenadas**. Ele mantém uma complexidade de pior caso de $O(n \log n)$, mas pode se aproximar de $O(n)$ em casos otimistas (Melhor Caso).

Para construir seu *heap* suave, o Smoothsort utiliza os **Números de Leonardo**.

## 2. Requisitos de Execução

* **Linguagem:** Python 3.14.0
* **Bibliotecas Necessárias:**
    * `matplotlib`: Para a geração dos gráficos de desempenho.
    * `timeit` ou `time`: Para medição de tempo precisa.
    * `random`: Para geração das listas de teste.

Para instalar as dependências:
```bash
pip install matplotlib