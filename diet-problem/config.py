# -*- coding: utf-8 -*-
"""
config.py - Configurações e dados para o problema da dieta

Autor: José Brito
"""

# Dados dos alimentos
ALIMENTOS_DATA = {
    'Aveia': {
        'max_porcoes': 4,
        'tamanho': 28,
        'energia': 110,
        'proteina': 4,
        'calcio': 2,
        'magnesio': 26,
        'vitaminaC': 0,
        'ferro': 6,
        'preco': 10.57
    },
    'Frango': {
        'max_porcoes': 5,
        'tamanho': 100,
        'energia': 205,
        'proteina': 32,
        'calcio': 12,
        'magnesio': 1.2,
        'vitaminaC': 2,
        'ferro': 1.3,
        'preco': 16.25
    },
    'Ovos': {
        'max_porcoes': 3,
        'tamanho': 2,
        'energia': 160,
        'proteina': 13,
        'calcio': 54,
        'magnesio': 10,
        'vitaminaC': 0,
        'ferro': 1.2,
        'preco': 1.6
    },
    'Leite_Integral': {
        'max_porcoes': 8,
        'tamanho': 237,
        'energia': 160,
        'proteina': 8,
        'calcio': 285,
        'magnesio': 0,
        'vitaminaC': 0,
        'ferro': 11,
        'preco': 8
    },
    'Torta_de_Cereja': {
        'max_porcoes': 2,
        'tamanho': 170,
        'energia': 420,
        'proteina': 4,
        'calcio': 22,
        'magnesio': 9,
        'vitaminaC': 1,
        'ferro': 1.9,
        'preco': 25
    },
    'Feijao_com_Carne': {
        'max_porcoes': 3,
        'tamanho': 206,
        'energia': 260,
        'proteina': 14,
        'calcio': 80,
        'magnesio': 31,
        'vitaminaC': 0.6,
        'ferro': 0.8,
        'preco': 4
    },
    'Iogurte': {
        'max_porcoes': 4,
        'tamanho': 3,
        'energia': 58,
        'proteina': 10,
        'calcio': 110,
        'magnesio': 11,
        'vitaminaC': 0.1,
        'ferro': 0.1,
        'preco': 10
    },
    'Arroz': {
        'max_porcoes': 6,
        'tamanho': 30,
        'energia': 500,
        'proteina': 9.4,
        'calcio': 28,
        'magnesio': 25,
        'vitaminaC': 0.01,
        'ferro': 0.8,
        'preco': 8.9
    },
    'Carne': {
        'max_porcoes': 6,
        'tamanho': 143,
        'energia': 143,
        'proteina': 26,
        'calcio': 6,
        'magnesio': 29,
        'vitaminaC': 0,
        'ferro': 1.2,
        'preco': 40
    },
    'Batata': {
        'max_porcoes': 6,
        'tamanho': 54,
        'energia': 323,
        'proteina': 2,
        'calcio': 12,
        'magnesio': 28,
        'vitaminaC': 19,
        'ferro': 0.78,
        'preco': 3.29
    }
}

# Restrições nutricionais
RESTRICOES_ORIGINAIS = {
    'n_min': {
        1: 2500,  # Energia mínima (kcal)
        2: 56,    # Proteína mínima (g)
        3: 1000,  # Cálcio mínimo (mg)
        4: 400,   # Magnésio mínimo (mg)
        5: 90     # Vitamina C mínima (mg)
    },
    'n_max': {
        1: 3000,  # Energia máxima (kcal)
        2: 100,   # Proteína máxima (g)
        3: 1300,  # Cálcio máximo (mg)
        4: 420,   # Magnésio máximo (mg)
        5: 200    # Vitamina C máxima (mg)
    }
}

# Restrições relaxadas (para permitir solução viável)
RESTRICOES_RELAXADAS = {
    'n_min': {
        1: 2200,  # Energia mínima (kcal)
        2: 50,    # Proteína mínima (g)
        3: 800,   # Cálcio mínimo (mg)
        4: 300,   # Magnésio mínimo (mg)
        5: 70     # Vitamina C mínima (mg)
    },
    'n_max': {
        1: 3500,  # Energia máxima (kcal)
        2: 200,   # Proteína máxima (g)
        3: 1400,  # Cálcio máximo (mg)
        4: 500,   # Magnésio máximo (mg)
        5: 220    # Vitamina C máxima (mg)
    }
}

# Mapeamento de nutrientes
NUTRIENTES = {
    1: 'energia',
    2: 'proteina',
    3: 'calcio',
    4: 'magnesio',
    5: 'vitaminaC'
}

# Configurações do solver
SOLVER_CONFIG = {
    'solver': 'cbc',
    'time_limit': 300,  # 5 minutos
    'mip_gap': 0.01     # 1% de gap
}
