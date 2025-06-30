# -*- coding: utf-8 -*-
"""
AMPL Solver for the Knapsack Problem
"""

try:
    from amplpy import AMPL, ampl_notebook
    AMPL_AVAILABLE = True
except ImportError:
    AMPL_AVAILABLE = False
    print("WARNING: amplpy is not installed. Use 'pip install amplpy' to install it.")

from knapsack_data import ITENS_DATA, MAX_KNAPSACK_WEIGHT, print_dataset_info
from ampl_files_generator import generate_all_ampl_files

class KnapsackAMPLSolver:
    """
    Class to solve the knapsack problem using AMPL
    """
    
    def __init__(self):
        self.ampl = None
        self.solution = None
        self.objective_value = None
        
    def setup_ampl_environment(self):
        """
        Sets up the AMPL environment
        """
        if not AMPL_AVAILABLE:
            raise ImportError("amplpy is not available. Install with: pip install amplpy")
        
        try:
            # AMPL environment configuration
            self.ampl = ampl_notebook(
                modules=["coin"],
                license_uuid="default",
            )
            print("AMPL environment configured successfully!")
        except Exception as e:
            print(f"Error configuring AMPL: {e}")
            raise
    
    def solve_knapsack(self, model_file="mochila.mod", data_file="mochila.dat"):
        """
        Solves the knapsack problem using AMPL
        """
        if not self.ampl:
            self.setup_ampl_environment()
        
        try:
            # Load model and data
            self.ampl.read(model_file)
            self.ampl.read_data(data_file)
            
            # Set the solver
            self.ampl.option['solver'] = 'cbc'
            
            # Solve the problem
            self.ampl.solve()
            
            # Get the solution
            self.solution = self.ampl.get_variable('Include').get_values().to_dict()
            self.objective_value = self.ampl.get_objective('Total_value').value()
            
            print("Problem solved successfully!")
            return True
            
        except Exception as e:
            print(f"Error solving the problem: {e}")
            return False
    
    def print_solution(self):
        """
        Prints the detailed solution
        """
        if not self.solution:
            print("No solution available. Run solve_knapsack() first.")
            return
        
        print("\n" + "="*80)
        print("RESULT ANALYSIS")
        print("="*80)
        
        # Total value
        print(f"Total knapsack value: ${self.objective_value:.0f}")
        
        # Selected items
        selected_items = []
        not_selected_items = []
        total_weight = 0
        
        for item_name, include in self.solution.items():
            if include == 1:
                selected_items.append(item_name)
                total_weight += ITENS_DATA[item_name]['weight']
            else:
                not_selected_items.append(item_name)
        
        print(f"Total weight used: {total_weight:.1f} kg out of {MAX_KNAPSACK_WEIGHT} kg")
        print(f"Remaining capacity: {MAX_KNAPSACK_WEIGHT - total_weight:.1f} kg")
        
        print("\nSelected Items:")
        print("-" * 60)
        for item in selected_items:
            data = ITENS_DATA[item]
            print(f"• {item.replace('_', ' '):<20} - Weight: {data['weight']:>4} kg, Value: ${data['value']:>4}")
        
        print("\nNot Selected Items:")
        print("-" * 60)
        for item in not_selected_items:
            data = ITENS_DATA[item]
            print(f"• {item.replace('_', ' '):<20} - Weight: {data['weight']:>4} kg, Value: ${data['value']:>4}")
        
        print("\nConclusion:")
        print("-" * 60)
        print("The optimized solution successfully maximized the knapsack's value by selecting")
        print("high-value items with weights that fit within the 10 kg limit.")
        print("The model demonstrated efficiency in choosing the most advantageous items.")

def main():
    """
    Main function to run the solver
    """
    print("Starting the Knapsack Problem solver...")
    
    # Show dataset information
    print_dataset_info()
    
    # Generate AMPL files
    generate_all_ampl_files()
    
    # Solve the problem
    solver = KnapsackAMPLSolver()
    
    try:
        if solver.solve_knapsack():
            solver.print_solution()
        else:
            print("Failed to solve the problem.")
    except ImportError as e:
        print(f"Error: {e}")
        print("To use this solver, install amplpy with: pip install amplpy")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()