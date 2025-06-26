# -*- coding: utf-8 -*-
"""
models.py - Definições dos modelos AMPL para o problema da dieta

Autor: José Brito
"""

# Modelo básico da dieta
MODELO_BASICO = """
# Definição do conjunto de alimentos
set ALIMENTO;

# Parâmetros dos alimentos
param max_porcoes{ALIMENTO};  # Quantidade máxima permitida de cada alimento
param tamanho{ALIMENTO};      # Tamanho da porção (em gramas ou mL)
param energia{ALIMENTO};      # Energia (kcal)
param proteina{ALIMENTO};     # Proteína (g)
param calcio{ALIMENTO};       # Cálcio (mg)
param magnesio{ALIMENTO};     # Magnésio (mg)
param vitaminaC{ALIMENTO};    # Vitamina C (mg)
param ferro{ALIMENTO};        # Ferro (mg)
param preco{ALIMENTO};        # Preço (unidade monetária)

# Limites mínimos e máximos para nutrientes
param n_min{1..5};  # Valores mínimos recomendados
param n_max{1..5};  # Valores máximos permitidos

# Variáveis de decisão
var Compra{j in ALIMENTO} integer >= 0, <= max_porcoes[j];

# Função objetivo: minimizar o custo total da dieta
minimize Custo_Total: sum{j in ALIMENTO} preco[j] * Compra[j];

# Restrições de nutrientes
subject to Energia:    n_min[1] <= sum{j in ALIMENTO} energia[j] * Compra[j]    <= n_max[1];
subject to Proteina:  n_min[2] <= sum{j in ALIMENTO} proteina[j] * Compra[j]  <= n_max[2];
subject to Calcio:    n_min[3] <= sum{j in ALIMENTO} calcio[j] * Compra[j]     <= n_max[3];
subject to Magnesio:  n_min[4] <= sum{j in ALIMENTO} magnesio[j] * Compra[j]  <= n_max[4];
subject to VitaminaC: n_min[5] <= sum{j in ALIMENTO} vitaminaC[j] * Compra[j] <= n_max[5];
"""

# Modelo com diversidade (incentiva maior variedade de alimentos)
MODELO_DIVERSIFICADO = """
# Definição do conjunto de alimentos
set ALIMENTO;

# Parâmetros dos alimentos
param max_porcoes{ALIMENTO};  # Quantidade máxima permitida de cada alimento
param tamanho{ALIMENTO};      # Tamanho da porção (em gramas ou mL)
param energia{ALIMENTO};      # Energia (kcal)
param proteina{ALIMENTO};     # Proteína (g)
param calcio{ALIMENTO};       # Cálcio (mg)
param magnesio{ALIMENTO};     # Magnésio (mg)
param vitaminaC{ALIMENTO};    # Vitamina C (mg)
param ferro{ALIMENTO};        # Ferro (mg)
param preco{ALIMENTO};        # Preço (unidade monetária)

# Limites mínimos e máximos para nutrientes
param n_min{1..5};  # Valores mínimos recomendados
param n_max{1..5};  # Valores máximos permitidos

# Variáveis de decisão
var Compra{j in ALIMENTO} integer >= 0, <= max_porcoes[j];

# Variável auxiliar para indicar se um alimento foi escolhido (1 se foi escolhido, 0 caso contrário)
var Escolhido{j in ALIMENTO} binary;

# Restrição para ativar Escolhido apenas se Compra[j] for maior que zero
subject to Ativa_Escolhido {j in ALIMENTO}:
    Compra[j] <= max_porcoes[j] * Escolhido[j];

# Função objetivo: minimizar o custo total da dieta, incentivando a diversidade
minimize Custo_Total:
    sum{j in ALIMENTO} preco[j] * Compra[j]
    + 0.5 * (card(ALIMENTO) - sum{j in ALIMENTO} Escolhido[j]);  # Penaliza poucas escolhas

# Restrições de nutrientes
subject to Energia:    n_min[1] <= sum{j in ALIMENTO} energia[j] * Compra[j]    <= n_max[1];
subject to Proteina:  n_min[2] <= sum{j in ALIMENTO} proteina[j] * Compra[j]  <= n_max[2];
subject to Calcio:    n_min[3] <= sum{j in ALIMENTO} calcio[j] * Compra[j]     <= n_max[3];
subject to Magnesio:  n_min[4] <= sum{j in ALIMENTO} magnesio[j] * Compra[j]  <= n_max[4];
subject to VitaminaC: n_min[5] <= sum{j in ALIMENTO} vitaminaC[j] * Compra[j] <= n_max[5];

# Restrição para evitar que um único alimento seja dominante (máximo de 4 porções por alimento)
subject to Limite_Individual {j in ALIMENTO}:
    Compra[j] <= 4;
"""

def salvar_modelo(modelo_str, nome_arquivo):
    """
    Salva o modelo AMPL em um arquivo .mod
    
    Args:
        modelo_str (str): String contendo o modelo AMPL
        nome_arquivo (str): Nome do arquivo (sem extensão)
    """
    with open(f"{nome_arquivo}.mod", "w", encoding="utf-8") as f:
        f.write(modelo_str)
    print(f"Modelo salvo em {nome_arquivo}.mod")

def criar_modelos():
    """
    Cria os arquivos .mod com os modelos definidos
    """
    salvar_modelo(MODELO_BASICO, "dieta_basico")
    salvar_modelo(MODELO_DIVERSIFICADO, "dieta_diversificado")
    print("Todos os modelos foram criados com sucesso!")

if __name__ == "__main__":
    criar_modelos()
