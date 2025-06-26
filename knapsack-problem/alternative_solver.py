# -*- coding: utf-8 -*-
"""
Solucionador Alternativo para o Problema da Mochila (sem AMPL)
Implementação usando programação dinâmica
Autor: José Brito
"""

from knapsack_data import ITENS_DATA, PESO_MAX_MOCHILA, print_dataset_info

class KnapsackDynamicSolver:
    """
    Solucionador do problema da mochila usando programação dinâmica
    """
    
    def __init__(self):
        self.items = list(ITENS_DATA.keys())
        self.weights = [ITENS_DATA[item]['peso'] for item in self.items]
        self.values = [ITENS_DATA[item]['valor'] for item in self.items]
        self.capacity = int(PESO_MAX_MOCHILA * 10)  # Multiplicar por 10 para trabalhar com inteiros
        self.solution = None
        self.max_value = 0
    
    def solve(self):
        """
        Resolve o problema da mochila usando programação dinâmica
        """
        n = len(self.items)
        weights_int = [int(w * 10) for w in self.weights]  # Converter para inteiros
        
        # Tabela DP
        dp = [[0 for _ in range(self.capacity + 1)] for _ in range(n + 1)]
        
        # Preencher a tabela DP
        for i in range(1, n + 1):
            for w in range(1, self.capacity + 1):
                if weights_int[i-1] <= w:
                    dp[i][w] = max(
                        self.values[i-1] + dp[i-1][w - weights_int[i-1]],
                        dp[i-1][w]
                    )
                else:
                    dp[i][w] = dp[i-1][w]
        
        # O valor máximo está em dp[n][capacity]
        self.max_value = dp[n][self.capacity]
        
        # Reconstruir a solução
        self.solution = [0] * n
        w = self.capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                self.solution[i-1] = 1
                w -= weights_int[i-1]
        
        return self.max_value
    
    def get_selected_items(self):
        """
        Retorna lista de itens selecionados
        """
        if self.solution is None:
            return []
        
        selected = []
        for i, selected_flag in enumerate(self.solution):
            if selected_flag == 1:
                selected.append(self.items[i])
        return selected
    
    def get_total_weight(self):
        """
        Retorna o peso total dos itens selecionados
        """
        if self.solution is None:
            return 0
        
        total = 0
        for i, selected_flag in enumerate(self.solution):
            if selected_flag == 1:
                total += self.weights[i]
        return total
    
    def print_solution(self):
        """
        Imprime a solução detalhada
        """
        if self.solution is None:
            print("Nenhuma solução disponível. Execute solve() primeiro.")
            return
        
        print("\n" + "="*80)
        print("ANÁLISE DO RESULTADO (Programação Dinâmica)")
        print("="*80)
        
        selected_items = self.get_selected_items()
        not_selected_items = [item for item in self.items if item not in selected_items]
        total_weight = self.get_total_weight()
        
        print(f"Valor total da mochila: ${self.max_value}")
        print(f"Peso total utilizado: {total_weight:.1f} kg de {PESO_MAX_MOCHILA} kg")
        print(f"Capacidade restante: {PESO_MAX_MOCHILA - total_weight:.1f} kg")
        
        print("\nItens Selecionados:")
        print("-" * 60)
        for item in selected_items:
            data = ITENS_DATA[item]
            print(f"• {item.replace('_', ' '):<20} - Peso: {data['peso']:>4} kg, Valor: ${data['valor']:>4}")
        
        print("\nItens Não Selecionados:")
        print("-" * 60)
        for item in not_selected_items:
            data = ITENS_DATA[item]
            print(f"• {item.replace('_', ' '):<20} - Peso: {data['peso']:>4} kg, Valor: ${data['valor']:>4}")
        
        # Análise adicional
        print("\nAnálise dos Itens:")
        print("-" * 60)
        
        # Calcular valor por peso para análise
        value_per_weight = []
        for item in self.items:
            data = ITENS_DATA[item]
            ratio = data['valor'] / data['peso']
            value_per_weight.append((item, ratio, item in selected_items))
        
        # Ordenar por valor/peso
        value_per_weight.sort(key=lambda x: x[1], reverse=True)
        
        print("Ranking por Valor/Peso:")
        for i, (item, ratio, selected) in enumerate(value_per_weight, 1):
            status = "✓ Selecionado" if selected else "✗ Não selecionado"
            print(f"{i:2d}. {item.replace('_', ' '):<20} - Ratio: ${ratio:6.2f}/kg - {status}")
        
        print("\nConclusão:")
        print("-" * 60)
        print("A solução da programação dinâmica garante a otimalidade global.")
        print("O algoritmo considerou todas as combinações possíveis para encontrar")
        print("a melhor solução dentro do limite de peso da mochila.")

def compare_with_greedy():
    """
    Compara a solução ótima com uma abordagem gulosa (greedy)
    """
    print("\n" + "="*80)
    print("COMPARAÇÃO: PROGRAMAÇÃO DINÂMICA vs ALGORITMO GULOSO")
    print("="*80)
    
    # Solução ótima (programação dinâmica)
    dp_solver = KnapsackDynamicSolver()
    dp_value = dp_solver.solve()
    
    # Solução gulosa (por valor/peso)
    items_ratio = []
    for item in ITENS_DATA:
        data = ITENS_DATA[item]
        ratio = data['valor'] / data['peso']
        items_ratio.append((item, data['peso'], data['valor'], ratio))
    
    # Ordenar por ratio decrescente
    items_ratio.sort(key=lambda x: x[3], reverse=True)
    
    greedy_weight = 0
    greedy_value = 0
    greedy_items = []
    
    for item, weight, value, ratio in items_ratio:
        if greedy_weight + weight <= PESO_MAX_MOCHILA:
            greedy_items.append(item)
            greedy_weight += weight
            greedy_value += value
    
    print(f"Solução Ótima (Prog. Dinâmica): ${dp_value}")
    print(f"Solução Gulosa (Valor/Peso):    ${greedy_value}")
    print(f"Diferença:                      ${dp_value - greedy_value}")
    
    if dp_value == greedy_value:
        print("\n✓ O algoritmo guloso encontrou a solução ótima neste caso!")
    else:
        print(f"\n✗ O algoritmo guloso perdeu ${dp_value - greedy_value} em valor.")
    
    return dp_solver

def main():
    """
    Função principal para executar o solucionador alternativo
    """
    print("Iniciando o solucionador alternativo do Problema da Mochila...")
    
    # Mostra informações do dataset
    print_dataset_info()
    
    # Resolve usando programação dinâmica
    print("\nResolvendo com Programação Dinâmica...")
    solver = KnapsackDynamicSolver()
    max_value = solver.solve()
    solver.print_solution()
    
    # Comparação com algoritmo guloso
    compare_with_greedy()

if __name__ == "__main__":
    main()