# -*- coding: utf-8 -*-
"""
AMPL File Generator for the Knapsack Problem
"""

from knapsack_data import ITENS_DATA, MAX_KNAPSACK_WEIGHT, get_items_list

def generate_ampl_model_file(filename="knapsack.mod"):
    """
    Generates the AMPL .mod file with the mathematical model of the knapsack problem
    """
    model_content = """# Definition of the set of items
set ITEM;

# Item parameters
param weight{ITEM};     # Weight of each item (in kg)
param value{ITEM};    # Value of each item (in dollars)
param max_weight;       # Maximum allowed weight in the knapsack

# Decision variables
var Include{j in ITEM} binary;  # 1 if the item is included, 0 otherwise

# Objective function: maximize the total value of items in the knapsack
maximize Total_Value: sum{j in ITEM} value[j] * Include[j];

# Weight constraint: the total weight of selected items cannot exceed the maximum knapsack limit
subject to Total_Weight: sum{j in ITEM} weight[j] * Include[j] <= max_weight;
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(model_content)
    
    print(f"File {filename} generated successfully!")

def generate_ampl_data_file(filename="knapsack.dat"):
    """
    Generates the AMPL .dat file with the problem data
    """
    items_list = get_items_list()
    
    # Start of the file
    data_content = "# Definition of the set of items\n"
    data_content += f"set ITEM := {' '.join(items_list)};\n\n"
    
    # Weight parameters
    data_content += "# Item parameters\n"
    data_content += "param weight :=\n"
    for item, data in ITENS_DATA.items():
        data_content += f"{item:<20} {data['weight']}\n"
    data_content += ";\n\n"
    
    # Value parameters
    data_content += "param value :=\n"
    for item, data in ITENS_DATA.items():
        data_content += f"{item:<20} {data['value']}\n"
    data_content += ";\n\n"
    
    # Maximum knapsack weight
    data_content += f"# Maximum knapsack weight\n"
    data_content += f"param max_weight := {MAX_KNAPSACK_WEIGHT};\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data_content)
    
    print(f"File {filename} generated successfully!")

def generate_ampl_run_file(filename="knapsack.run"):
    """
    Generates an AMPL .run file to execute the model
    """
    run_content = """# Knapsack problem execution script
reset;
model knapsack.mod;
data knapsack.dat;
option solver cbc;
solve;

# Display results
display Include;
display Total_Value;
display Total_Weight;

# Detailed report
printf "\\n=== SOLUTION REPORT ===\\n";
printf "Optimized total value: $%.2f\\n", Total_Value;
printf "Total weight used: %.2f kg\\n", sum{j in ITEM} weight[j] * Include[j];
printf "Remaining capacity: %.2f kg\\n", max_weight - sum{j in ITEM} weight[j] * Include[j];

printf "\\nSelected items:\\n";
for {j in ITEM: Include[j] = 1} {
    printf "- %s (Weight: %.1f kg, Value: $%.0f)\\n", j, weight[j], value[j];
}

printf "\\nNon-selected items:\\n";
for {j in ITEM: Include[j] = 0} {
    printf "- %s (Weight: %.1f kg, Value: $%.0f)\\n", j, weight[j], value[j];
}
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(run_content)
    
    print(f"File {filename} generated successfully!")

def generate_all_ampl_files():
    """
    Generates all necessary AMPL files
    """
    print("Generating AMPL files...")
    generate_ampl_model_file()
    generate_ampl_data_file()
    generate_ampl_run_file()
    print("All AMPL files have been generated successfully!")

if __name__ == "__main__":
    generate_all_ampl_files()