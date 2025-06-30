# -*- coding: utf-8 -*-
"""
Alternative Knapsack Problem Solver (without AMPL)
Implementation using dynamic programming
Author: José Brito
"""

from knapsack_data import ITENS_DATA, MAX_KNAPSACK_WEIGHT, print_dataset_info

class KnapsackDynamicSolver:
    """
    Knapsack problem solver using dynamic programming
    """
    
    def __init__(self):
        self.items = list(ITENS_DATA.keys())
        self.weights = [ITENS_DATA[item]['weight'] for item in self.items]
        self.values = [ITENS_DATA[item]['value'] for item in self.items]
        self.capacity = int(MAX_KNAPSACK_WEIGHT * 10)  # Multiply by 10 to work with integers
        self.solution = None
        self.max_value = 0
    
    def solve(self):
        """
        Solves the knapsack problem using dynamic programming
        """
        n = len(self.items)
        weights_int = [int(w * 10) for w in self.weights]  # Convert to integers
        
        # DP table
        dp = [[0 for _ in range(self.capacity + 1)] for _ in range(n + 1)]
        
        # Fill the DP table
        for i in range(1, n + 1):
            for w in range(1, self.capacity + 1):
                if weights_int[i-1] <= w:
                    dp[i][w] = max(
                        self.values[i-1] + dp[i-1][w - weights_int[i-1]],
                        dp[i-1][w]
                    )
                else:
                    dp[i][w] = dp[i-1][w]
        
        # The maximum value is in dp[n][capacity]
        self.max_value = dp[n][self.capacity]
        
        # Reconstruct the solution
        self.solution = [0] * n
        w = self.capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                self.solution[i-1] = 1
                w -= weights_int[i-1]
        
        return self.max_value
    
    def get_selected_items(self):
        """
        Returns a list of selected items
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
        Returns the total weight of the selected items
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
        Prints the detailed solution
        """
        if self.solution is None:
            print("No solution available. Run solve() first.")
            return
        
        print("\n" + "="*80)
        print("RESULT ANALYSIS (Dynamic Programming)")
        print("="*80)
        
        selected_items = self.get_selected_items()
        not_selected_items = [item for item in self.items if item not in selected_items]
        total_weight = self.get_total_weight()
        
        print(f"Total knapsack value: ${self.max_value}")
        print(f"Total weight used: {total_weight:.1f} kg out of {MAX_KNAPSACK_WEIGHT} kg")
        print(f"Remaining capacity: {MAX_KNAPSACK_WEIGHT - total_weight:.1f} kg")
        
        print("\nSelected Items:")
        print("-" * 60)
        for item in selected_items:
            data = ITENS_DATA[item]
            print(f"• {item.replace('_', ' '):<20} - Weight: {data['weight']:>4} kg, Value: ${data['value']:>4}")
        
        print("\nNon-Selected Items:")
        print("-" * 60)
        for item in not_selected_items:
            data = ITENS_DATA[item]
            print(f"• {item.replace('_', ' '):<20} - Weight: {data['weight']:>4} kg, Value: ${data['value']:>4}")
        
        # Additional analysis
        print("\nItem Analysis:")
        print("-" * 60)
        
        # Calculate value per weight for analysis
        value_per_weight = []
        for item in self.items:
            data = ITENS_DATA[item]
            ratio = data['value'] / data['weight']
            value_per_weight.append((item, ratio, item in selected_items))
        
        # Sort by value/weight ratio
        value_per_weight.sort(key=lambda x: x[1], reverse=True)
        
        print("Ranking by Value/Weight:")
        for i, (item, ratio, selected) in enumerate(value_per_weight, 1):
            status = "✓ Selected" if selected else "✗ Not Selected"
            print(f"{i:2d}. {item.replace('_', ' '):<20} - Ratio: ${ratio:6.2f}/kg - {status}")
        
        print("\nConclusion:")
        print("-" * 60)
        print("The dynamic programming solution guarantees global optimality.")
        print("The algorithm considered all possible combinations to find")
        print("the best solution within the knapsack's weight limit.")

def compare_with_greedy():
    """
    Compares the optimal solution with a greedy approach
    """
    print("\n" + "="*80)
    print("COMPARISON: DYNAMIC PROGRAMMING vs GREEDY ALGORITHM")
    print("="*80)
    
    # Optimal solution (dynamic programming)
    dp_solver = KnapsackDynamicSolver()
    dp_value = dp_solver.solve()
    
    # Greedy solution (by value/weight ratio)
    items_ratio = []
    for item in ITENS_DATA:
        data = ITENS_DATA[item]
        ratio = data['value'] / data['weight']
        items_ratio.append((item, data['weight'], data['value'], ratio))
    
    # Sort by descending ratio
    items_ratio.sort(key=lambda x: x[3], reverse=True)
    
    greedy_weight = 0
    greedy_value = 0
    greedy_items = []
    
    for item, weight, value, ratio in items_ratio:
        if greedy_weight + weight <= MAX_KNAPSACK_WEIGHT:
            greedy_items.append(item)
            greedy_weight += weight
            greedy_value += value
    
    print(f"Optimal Solution (Dynamic Prog.): ${dp_value}")
    print(f"Greedy Solution (Value/Weight):    ${greedy_value}")
    print(f"Difference:                      ${dp_value - greedy_value}")
    
    if dp_value == greedy_value:
        print("\n✓ The greedy algorithm found the optimal solution in this case!")
    else:
        print(f"\n✗ The greedy algorithm missed ${dp_value - greedy_value} in value.")
    
    return dp_solver

def main():
    """
    Main function to run the alternative solver
    """
    print("Starting the alternative Knapsack Problem solver...")
    
    # Show dataset information
    print_dataset_info()
    
    # Solve using dynamic programming
    print("\nSolving with Dynamic Programming...")
    solver = KnapsackDynamicSolver()
    max_value = solver.solve()
    solver.print_solution()
    
    # Compare with greedy algorithm
    compare_with_greedy()

if __name__ == "__main__":
    main()