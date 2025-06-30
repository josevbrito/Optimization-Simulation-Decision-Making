# Knapsack Problem - RPG Scenario 🎮

This project implements different solvers for the **Knapsack Problem** using an RPG scenario where an adventurer must choose which treasures to carry in their backpack to maximize the total value, while respecting a 10kg weight limit.

## 📁 File Structure

```

├── knapsack\_data.py          \# Problem data (items, weights, values)
├── ampl\_files\_generator.py   \# AMPL file generator (.mod, .dat, .run)
├── ampl\_solver.py           \# Solver using AMPL
├── alternative\_solver.py    \# Solver using Dynamic Programming
├── main.py                  \# Main file with interactive menu
├── requirements.txt         \# Project dependencies
└── README.md               \# This file

````

## 🎯 Problem Description

**Scenario**: An adventurer found 10 valuable treasures during a treasure hunt, but their backpack can only hold **10kg**. Which combination of items maximizes the total value?

### 🏺 Available Items

| Item               | Weight (kg) | Value ($) | Description                                                         |
|--------------------|-------------|-----------|---------------------------------------------------------------------|
| Ancient Coin       | 1.0         | 300       | Rare gold coin, valuable to collectors                              |
| Diamond            | 2.0         | 1500      | Precious stone found in a mysterious chest                          |
| Gold Bar           | 5.0         | 2500      | Pure gold bar, but very heavy                                       |
| Silver Necklace    | 1.5         | 800       | Silver necklace decorated with precious stones                      |
| Magic Potion       | 3.0         | 1200      | Priceless magic potion for alchemists                               |
| Ancient Book       | 2.5         | 500       | Ancient book containing lost secrets of civilization                |
| Crown              | 4.0         | 2200      | Royal crown encrusted with rubies and sapphires                     |
| Jade Statue        | 6.0         | 2800      | Sacred jade figurine, revered by ancient peoples                    |
| Sapphire Ring      | 0.5         | 900       | Sapphire ring that belonged to a legendary king                     |
| Treasure Map       | 1.0         | 1100      | Map leading to hidden treasure, valuable to hunters                 |

## 🚀 How to Run

### Simple Execution
```bash
python main.py
````

### Run Modules Individually

1.  **View problem data:**
```bash
python knapsack_data.py
```

2.  **Generate AMPL files:**
```bash
python ampl_files_generator.py
```

3.  **Run alternative solver:**
```bash
python alternative_solver.py
```

4.  **Run AMPL solver (if available):**
```bash
python ampl_solver.py
```

## 🔧 Installation

### Basic Dependencies

The project works with only the standard Python library (no external dependencies).

### Optional Dependencies

To use the AMPL solver:

```bash
pip install amplpy
```

## 📊 Solution Methods

### 1\. **AMPL Solver** (`ampl_solver.py`)

  - Uses professional mathematical modeling
  - Requires `amplpy` installation
  - Automatically generates .mod, .dat, and .run files
  - Guarantees optimal solution

### 2\. **Dynamic Programming** (`alternative_solver.py`)

  - Pure Python implementation
  - Classic algorithm for the knapsack problem
  - Complexity: O(n × W)
  - Guarantees optimal solution
  - Requires no external dependencies

### 3\. **Greedy Algorithm** (for comparison)

  - Selects items by highest value/weight ratio
  - Fast but does not guarantee optimality
  - Used for comparison with the optimal solution

## 🎮 Interactive Menu

The `main.py` file offers a menu with the following options:

```
1. View dataset information
2. Solve with AMPL (if available)
3. Solve with Dynamic Programming
4. Compare solutions (DP vs Greedy)
5. Generate AMPL files
6. Run full analysis
0. Exit
```

## 📈 Expected Results

**Optimal Solution:**

  - **Total Value:** $6800
  - **Total Weight:** 9.0 kg
  - **Selected Items:**
      - Sapphire Ring (0.5 kg, $900)
      - Silver Necklace (1.5 kg, $800)
      - Crown (4.0 kg, $2200)
      - Diamond (2.0 kg, $1500)
      - Treasure Map (1.0 kg, $1100)
      - Ancient Coin (1.0 kg, $300)

## 🔬 Mathematical Model

**Objective Function:**

```
Maximize: Σ (value[i] × include[i])
```

**Constraints:**

```
Σ (weight[i] × include[i]) ≤ 10 kg
include[i] ∈ {0, 1}
```

Where `include[i]` is a binary variable indicating whether item `i` has been selected.

## 📝 Generated AMPL Files

  - **knapsack.mod**: Mathematical model
  - **knapsack.dat**: Problem data
  - **knapsack.run**: Execution script with reports

## 🤝 Contributions

This project was created as educational material to demonstrate different approaches to solving the Knapsack Problem.

## 📄 Author

**José Brito** - Implementation and documentation of the RPG scenario

-----

*Have fun exploring different optimization algorithms\! 🎯*
