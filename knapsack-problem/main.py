# -*- coding: utf-8 -*-
"""
Knapsack Problem - RPG Treasure Hunt
Main file to run different solvers
"""

import sys
from knapsack_data import print_dataset_info
from ampl_solver import KnapsackAMPLSolver, AMPL_AVAILABLE
from alternative_solver import KnapsackDynamicSolver, compare_with_greedy

def show_menu():
    """
    Displays the options menu
    """
    print("\n" + "="*60)
    print("KNAPSACK PROBLEM - RPG SCENARIO")
    print("="*60)
    print("Choose an option:")
    print("1. View dataset information")
    print("2. Solve with AMPL (if available)")
    print("3. Solve with Dynamic Programming")
    print("4. Compare solutions (DP vs Greedy)")
    print("5. Generate AMPL files")
    print("6. Run full analysis")
    print("0. Exit")
    print("-"*60)

def option_1():
    """Shows dataset information"""
    print_dataset_info()

def option_2():
    """Solves with AMPL"""
    if not AMPL_AVAILABLE:
        print("\n❌ AMPL is not available.")
        print("To use the AMPL solver, install with: pip install amplpy")
        return
    
    try:
        from ampl_files_generator import generate_all_ampl_files
        
        print("\nSolving with AMPL...")
        generate_all_ampl_files()
        
        solver = KnapsackAMPLSolver()
        if solver.solve_knapsack():
            solver.print_solution()
        else:
            print("Failed to solve with AMPL.")
    except Exception as e:
        print(f"Error running AMPL solver: {e}")

def option_3():
    """Solves with Dynamic Programming"""
    print("\nSolving with Dynamic Programming...")
    solver = KnapsackDynamicSolver()
    solver.solve()
    solver.print_solution()

def option_4():
    """Compares solutions"""
    print("\nComparing solutions...")
    compare_with_greedy()

def option_5():
    """Generates AMPL files"""
    try:
        from ampl_files_generator import generate_all_ampl_files
        print("\nGenerating AMPL files...")
        generate_all_ampl_files()
    except Exception as e:
        print(f"Error generating AMPL files: {e}")

def option_6():
    """Runs a full analysis"""
    print("\n" + "="*80)
    print("FULL KNAPSACK PROBLEM ANALYSIS")
    print("="*80)
    
    # 1. Show dataset
    print_dataset_info()
    
    # 2. Solve with dynamic programming
    print("\n🔍 SOLVING WITH DYNAMIC PROGRAMMING...")
    dp_solver = KnapsackDynamicSolver()
    dp_solver.solve()
    dp_solver.print_solution()
    
    # 3. Compare with greedy
    print("\n🔍 COMPARING WITH GREEDY ALGORITHM...")
    compare_with_greedy()
    
    # 4. Try AMPL if available
    if AMPL_AVAILABLE:
        try:
            from ampl_files_generator import generate_all_ampl_files
            print("\n🔍 SOLVING WITH AMPL...")
            generate_all_ampl_files()
            
            ampl_solver = KnapsackAMPLSolver()
            if ampl_solver.solve_knapsack():
                print("\n✅ AMPL Solution:")
                ampl_solver.print_solution()
            else:
                print("❌ Failed to solve with AMPL.")
        except Exception as e:
            print(f"❌ Error with AMPL: {e}")
    else:
        print("\n⚠️  AMPL not available. Install with: pip install amplpy")
    
    print("\n" + "="*80)
    print("FULL ANALYSIS COMPLETE")
    print("="*80)

def main():
    """
    Main function with interactive menu
    """
    print("Welcome to the Knapsack Problem Solver!")
    
    while True:
        try:
            show_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '0':
                print("Exiting... Thanks for using the program!")
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
                print("❌ Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()