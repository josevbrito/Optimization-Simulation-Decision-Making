# -*- coding: utf-8 -*-
"""
Problema da Mochila - RPG Treasure Hunt
Arquivo principal para executar diferentes solucionadores
Autor: José Brito
"""

import sys
from knapsack_data import print_dataset_info
from ampl_solver import KnapsackAMPLSolver, AMPL_AVAILABLE
from alternative_solver import KnapsackDynamicSolver, compare_with_greedy

def show_menu():
    """
    Mostra o menu de opções
    """
    print("\n" + "="*60)
    print("PROBLEMA DA MOCHILA - CENÁRIO RPG")
    print("="*60)
    print("Escolha uma opção:")
    print("1. Ver informações do dataset")
    print("2. Resolver com AMPL (se disponível)")
    print("3. Resolver com Programação Dinâmica")
    print("4. Comparar soluções (DP vs Guloso)")
    print("5. Gerar arquivos AMPL")
    print("6. Executar análise completa")
    print("0. Sair")
    print("-"*60)

def option_1():
    """Mostra informações do dataset"""
    print_dataset_info()

def option_2():
    """Resolve com AMPL"""
    if not AMPL_AVAILABLE:
        print("\n❌ AMPL não está disponível.")
        print("Para usar o solucionador AMPL, instale com: pip install amplpy")
        return
    
    try:
        from ampl_files_generator import generate_all_ampl_files
        
        print("\nResolvendo com AMPL...")
        generate_all_ampl_files()
        
        solver = KnapsackAMPLSolver()
        if solver.solve_knapsack():
            solver.print_solution()
        else:
            print("Falha ao resolver com AMPL.")
    except Exception as e:
        print(f"Erro ao executar solucionador AMPL: {e}")

def option_3():
    """Resolve com Programação Dinâmica"""
    print("\nResolvendo com Programação Dinâmica...")
    solver = KnapsackDynamicSolver()
    solver.solve()
    solver.print_solution()

def option_4():
    """Compara soluções"""
    print("\nComparando soluções...")
    compare_with_greedy()

def option_5():
    """Gera arquivos AMPL"""
    try:
        from ampl_files_generator import generate_all_ampl_files
        print("\nGerando arquivos AMPL...")
        generate_all_ampl_files()
    except Exception as e:
        print(f"Erro ao gerar arquivos AMPL: {e}")

def option_6():
    """Executa análise completa"""
    print("\n" + "="*80)
    print("ANÁLISE COMPLETA DO PROBLEMA DA MOCHILA")
    print("="*80)
    
    # 1. Mostrar dataset
    print_dataset_info()
    
    # 2. Resolver com programação dinâmica
    print("\n🔍 RESOLVENDO COM PROGRAMAÇÃO DINÂMICA...")
    dp_solver = KnapsackDynamicSolver()
    dp_solver.solve()
    dp_solver.print_solution()
    
    # 3. Comparar com guloso
    print("\n🔍 COMPARANDO COM ALGORITMO GULOSO...")
    compare_with_greedy()
    
    # 4. Tentar AMPL se disponível
    if AMPL_AVAILABLE:
        try:
            from ampl_files_generator import generate_all_ampl_files
            print("\n🔍 RESOLVENDO COM AMPL...")
            generate_all_ampl_files()
            
            ampl_solver = KnapsackAMPLSolver()
            if ampl_solver.solve_knapsack():
                print("\n✅ Solução AMPL:")
                ampl_solver.print_solution()
            else:
                print("❌ Falha ao resolver com AMPL.")
        except Exception as e:
            print(f"❌ Erro com AMPL: {e}")
    else:
        print("\n⚠️  AMPL não disponível. Instale com: pip install amplpy")
    
    print("\n" + "="*80)
    print("ANÁLISE COMPLETA FINALIZADA")
    print("="*80)

def main():
    """
    Função principal com menu interativo
    """
    print("Bem-vindo ao Solucionador do Problema da Mochila!")
    
    while True:
        try:
            show_menu()
            choice = input("Digite sua escolha: ").strip()
            
            if choice == '0':
                print("Saindo... Obrigado por usar o programa!")
                sys.exit(0)
            elif choice == '1':
                option_1()
            elif choice == '2':
                option_2()
            elif choice == '3':
                option_3()
            elif choice == '4':
                option_4()
            elif choice == '5':
                option_5()
            elif choice == '6':
                option_6()
            else:
                print("❌ Opção inválida. Tente novamente.")
            
            input("\nPressione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\nPrograma interrompido pelo usuário. Saindo...")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()