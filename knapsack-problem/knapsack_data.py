# -*- coding: utf-8 -*-
"""
Dados do Problema da Mochila - Cenário RPG
Autor: José Brito

Dataset criado como parte de um cenário de jogo de RPG, onde o objetivo é decidir 
quais itens um personagem deve carregar em sua mochila (que suporta 10kg) para 
maximizar o valor total dos objetos, sem ultrapassar o limite de peso.
"""

# Dados dos itens do RPG
ITENS_DATA = {
    'Moeda_Antiga': {'peso': 1.0, 'valor': 300, 'descricao': 'Moeda de ouro rara, valiosa para colecionadores.'},
    'Diamante': {'peso': 2.0, 'valor': 1500, 'descricao': 'Pedra preciosa encontrada em um baú misterioso.'},
    'Barra_de_Ouro': {'peso': 5.0, 'valor': 2500, 'descricao': 'Barra de ouro puro, mas muito pesada.'},
    'Colar_de_Prata': {'peso': 1.5, 'valor': 800, 'descricao': 'Colar de prata decorado com pedras preciosas.'},
    'Pocao_Magica': {'peso': 3.0, 'valor': 1200, 'descricao': 'Poção mágica de valor inestimável para alquimistas.'},
    'Livro_Antigo': {'peso': 2.5, 'valor': 500, 'descricao': 'Livro antigo contendo segredos perdidos da civilização.'},
    'Coroa': {'peso': 4.0, 'valor': 2200, 'descricao': 'Coroa real incrustada com rubis e safiras.'},
    'Estatua_de_Jade': {'peso': 6.0, 'valor': 2800, 'descricao': 'Estatueta de jade sagrado, venerada por povos antigos.'},
    'Anel_de_Safira': {'peso': 0.5, 'valor': 900, 'descricao': 'Anel de safira que pertencia a um rei lendário.'},
    'Mapa_do_Tesouro': {'peso': 1.0, 'valor': 1100, 'descricao': 'Mapa que leva a um tesouro escondido, valioso para caçadores.'}
}

# Configurações do problema
PESO_MAX_MOCHILA = 10  # kg

def get_items_list():
    """Retorna a lista de nomes dos itens"""
    return list(ITENS_DATA.keys())

def get_item_weights():
    """Retorna dicionário com pesos dos itens"""
    return {item: data['peso'] for item, data in ITENS_DATA.items()}

def get_item_values():
    """Retorna dicionário com valores dos itens"""
    return {item: data['valor'] for item, data in ITENS_DATA.items()}

def get_item_descriptions():
    """Retorna dicionário com descrições dos itens"""
    return {item: data['descricao'] for item, data in ITENS_DATA.items()}

def print_dataset_info():
    """Imprime informações sobre o dataset"""
    print("=" * 80)
    print("ESTUDO DO PROBLEMA DA MOCHILA - CENÁRIO RPG")
    print("Autor: José Brito")
    print("=" * 80)
    print(f"Capacidade máxima da mochila: {PESO_MAX_MOCHILA} kg")
    print(f"Número de itens disponíveis: {len(ITENS_DATA)}")
    print("\nItens disponíveis:")
    print("-" * 80)
    
    for item, data in ITENS_DATA.items():
        print(f"{item:<20} | Peso: {data['peso']:>4} kg | Valor: ${data['valor']:>4} | {data['descricao']}")
    
    print("-" * 80)