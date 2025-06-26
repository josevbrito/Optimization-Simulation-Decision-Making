# -*- coding: utf-8 -*-
"""
Solucionador AMPL para o Problema da Mochila
Autor: José Brito
"""

try:
    from amplpy import AMPL, ampl_notebook
    AMPL_AVAILABLE = True
except ImportError:
    AMPL_AVAILABLE = False
    print("AVISO: amplpy não está instalado. Use 'pip install amplpy' para instalar.")

from knapsack_data import ITENS_DATA, PESO_MAX_MOCHILA, print_dataset_info
from ampl_files_generator import generate_all_ampl_files

class KnapsackAMPLSolver:
    """
    Classe para resolver o problema da mochila usando AMPL
    """
    
    def __init__(self):
        self.ampl = None
        self.solution = None
        self.objective_value = None
        
    def setup_ampl_environment(self):
        """
        Configura o ambiente AMPL
        """
        if not AMPL_AVAILABLE:
            raise ImportError("amplpy não está disponível. Instale com: pip install amplpy")
        
        try:
            # Configuração do ambiente AMPL
            self.ampl = ampl_notebook(
                modules=["coin"],
                license_uuid="default",
            )
            print("Ambiente AMPL configurado com sucesso!")
        except Exception as e:
            print(f"Erro ao configurar AMPL: {e}")
            raise
    
    def solve_knapsack(self, model_file="mochila.mod", data_file="mochila.dat"):
        """
        Resolve o problema da mochila usando AMPL
        """
        if not self.ampl:
            self.setup_ampl_environment()
        
        try:
            # Carrega modelo e dados
            self.ampl.read(model_file)
            self.ampl.read_data(data_file)
            
            # Define o solver
            self.ampl.option['solver'] = 'cbc'
            
            # Resolve o problema
            self.ampl.solve()
            
            # Obtém a solução
            self.solution = self.ampl.get_variable('Incluir').get_values().to_dict()
            self.objective_value = self.ampl.get_objective('Valor_Total').value()
            
            print("Problema resolvido com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao resolver o problema: {e}")
            return False
    
    def print_solution(self):
        """
        Imprime a solução detalhada
        """
        if not self.solution:
            print("Nenhuma solução disponível. Execute solve_knapsack() primeiro.")
            return
        
        print("\n" + "="*80)
        print("ANÁLISE DO RESULTADO")
        print("="*80)
        
        # Valor total
        print(f"Valor total da mochila: ${self.objective_value:.0f}")
        
        # Itens selecionados
        selected_items = []
        not_selected_items = []
        total_weight = 0
        
        for item_name, include in self.solution.items():
            if include == 1:
                selected_items.append(item_name)
                total_weight += ITENS_DATA[item_name]['peso']
            else:
                not_selected_items.append(item_name)
        
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
        
        print("\nConclusão:")
        print("-" * 60)
        print("A solução otimizada conseguiu maximizar o valor da mochila selecionando")
        print("itens de alto valor e com pesos que se ajustam ao limite de 10 kg.")
        print("O modelo demonstrou eficiência na escolha dos itens mais vantajosos.")

def main():
    """
    Função principal para executar o solucionador
    """
    print("Iniciando o solucionador do Problema da Mochila...")
    
    # Mostra informações do dataset
    print_dataset_info()
    
    # Gera arquivos AMPL
    generate_all_ampl_files()
    
    # Resolve o problema
    solver = KnapsackAMPLSolver()
    
    try:
        if solver.solve_knapsack():
            solver.print_solution()
        else:
            print("Falha ao resolver o problema.")
    except ImportError as e:
        print(f"Erro: {e}")
        print("Para usar este solucionador, instale o amplpy com: pip install amplpy")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()