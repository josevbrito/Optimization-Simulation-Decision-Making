# -*- coding: utf-8 -*-
"""
Knapsack Problem Data - RPG Scenario

Dataset created as part of an RPG game scenario, where the goal is to decide 
which items a character should carry in their backpack (which supports 10kg) to 
maximize the total value of the objects, without exceeding the weight limit.
"""

# RPG item data
ITENS_DATA = {
    'Ancient_Coin': {'weight': 1.0, 'value': 300, 'description': 'Rare gold coin, valuable for collectors.'},
    'Diamond': {'weight': 2.0, 'value': 1500, 'description': 'Precious stone found in a mysterious chest.'},
    'Gold_Bar': {'weight': 5.0, 'value': 2500, 'description': 'Pure gold bar, but very heavy.'},
    'Silver_Necklace': {'weight': 1.5, 'value': 800, 'description': 'Silver necklace decorated with precious stones.'},
    'Magic_Potion': {'weight': 3.0, 'value': 1200, 'description': 'Priceless magic potion for alchemists.'},
    'Ancient_Book': {'weight': 2.5, 'value': 500, 'description': 'Ancient book containing lost secrets of civilization.'},
    'Crown': {'weight': 4.0, 'value': 2200, 'description': 'Royal crown encrusted with rubies and sapphires.'},
    'Jade_Statue': {'weight': 6.0, 'value': 2800, 'description': 'Sacred jade figurine, revered by ancient peoples.'},
    'Sapphire_Ring': {'weight': 0.5, 'value': 900, 'description': 'Sapphire ring that belonged to a legendary king.'},
    'Treasure_Map': {'weight': 1.0, 'value': 1100, 'description': 'Map leading to hidden treasure, valuable to hunters.'}
}

# Problem settings
MAX_KNAPSACK_WEIGHT = 10  # kg

def get_items_list():
    """Returns the list of item names"""
    return list(ITENS_DATA.keys())

def get_item_weights():
    """Returns a dictionary with item weights"""
    return {item: data['weight'] for item, data in ITENS_DATA.items()}

def get_item_values():
    """Returns a dictionary with item values"""
    return {item: data['value'] for item, data in ITENS_DATA.items()}

def get_item_descriptions():
    """Returns a dictionary with item descriptions"""
    return {item: data['description'] for item, data in ITENS_DATA.items()}

def print_dataset_info():
    """Prints information about the dataset"""
    print("=" * 80)
    print("KNAPSACK PROBLEM STUDY - RPG SCENARIO")
    print("Author: José Brito")
    print("=" * 80)
    print(f"Maximum backpack capacity: {MAX_KNAPSACK_WEIGHT} kg")
    print(f"Number of available items: {len(ITENS_DATA)}")
    print("\nAvailable Items:")
    print("-" * 80)
    
    for item, data in ITENS_DATA.items():
        print(f"{item:<20} | Weight: {data['weight']:>4} kg | Value: ${data['value']:>4} | {data['description']}")
    
    print("-" * 80)