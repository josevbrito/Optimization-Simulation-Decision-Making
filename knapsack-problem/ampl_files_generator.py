# -*- coding: utf-8 -*-
"""
Gerador de Arquivos AMPL para o Problema da Mochila
Autor: José Brito
"""

from knapsack_data import ITENS_DATA, PESO_MAX_MOCHILA, get_items_list

def generate_ampl_model_file(filename="mochila.mod"):
    """
    Gera o arquivo .mod do AMPL com o modelo matemático do problema da mochila
    """
    model_content = """# Definição do conjunto de itens
set ITEM;

# Parâmetros dos itens
param peso{ITEM};     # Peso de cada item (em kg)
param valor{ITEM};    # Valor de cada item (em dólares)
param peso_max;       # Peso máximo permitido na mochila

# Variáveis de decisão
var Incluir{j in ITEM} binary;  # 1 se o item for incluído, 0 caso contrário

# Função objetivo: maximizar o valor total dos itens na mochila
maximize Valor_Total: sum{j in ITEM} valor[j] * Incluir[j];

# Restrição de peso: o peso total dos itens selecionados não pode exceder o limite máximo da mochila
subject to Peso_Total: sum{j in ITEM} peso[j] * Incluir[j] <= peso_max;
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(model_content)
    
    print(f"Arquivo {filename} gerado com sucesso!")

def generate_ampl_data_file(filename="mochila.dat"):
    """
    Gera o arquivo .dat do AMPL com os dados do problema
    """
    items_list = get_items_list()
    
    # Início do arquivo
    data_content = "# Definição do conjunto de itens\n"
    data_content += f"set ITEM := {' '.join(items_list)};\n\n"
    
    # Parâmetros de peso
    data_content += "# Parâmetros dos itens\n"
    data_content += "param peso :=\n"
    for item, data in ITENS_DATA.items():
        data_content += f"{item:<20} {data['peso']}\n"
    data_content += ";\n\n"
    
    # Parâmetros de valor
    data_content += "param valor :=\n"
    for item, data in ITENS_DATA.items():
        data_content += f"{item:<20} {data['valor']}\n"
    data_content += ";\n\n"
    
    # Peso máximo da mochila
    data_content += f"# Peso máximo da mochila\n"
    data_content += f"param peso_max := {PESO_MAX_MOCHILA};\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data_content)
    
    print(f"Arquivo {filename} gerado com sucesso!")

def generate_ampl_run_file(filename="mochila.run"):
    """
    Gera um arquivo .run do AMPL para executar o modelo
    """
    run_content = """# Script de execução do problema da mochila
reset;
model mochila.mod;
data mochila.dat;
option solver cbc;
solve;

# Exibir resultados
display Incluir;
display Valor_Total;
display Peso_Total;

# Relatório detalhado
printf "\\n=== RELATÓRIO DA SOLUÇÃO ===\\n";
printf "Valor total otimizado: $%.2f\\n", Valor_Total;
printf "Peso total utilizado: %.2f kg\\n", sum{j in ITEM} peso[j] * Incluir[j];
printf "Capacidade restante: %.2f kg\\n", peso_max - sum{j in ITEM} peso[j] * Incluir[j];

printf "\\nItens selecionados:\\n";
for {j in ITEM: Incluir[j] = 1} {
    printf "- %s (Peso: %.1f kg, Valor: $%.0f)\\n", j, peso[j], valor[j];
}

printf "\\nItens não selecionados:\\n";
for {j in ITEM: Incluir[j] = 0} {
    printf "- %s (Peso: %.1f kg, Valor: $%.0f)\\n", j, peso[j], valor[j];
}
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(run_content)
    
    print(f"Arquivo {filename} gerado com sucesso!")

def generate_all_ampl_files():
    """
    Gera todos os arquivos AMPL necessários
    """
    print("Gerando arquivos AMPL...")
    generate_ampl_model_file()
    generate_ampl_data_file()
    generate_ampl_run_file()
    print("Todos os arquivos AMPL foram gerados com sucesso!")

if __name__ == "__main__":
    generate_all_ampl_files()