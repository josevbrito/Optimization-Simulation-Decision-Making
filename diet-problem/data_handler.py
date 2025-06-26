# -*- coding: utf-8 -*-
"""
data_handler.py - Manipulação e criação de arquivos de dados para AMPL

Autor: José Brito
"""

from config import ALIMENTOS_DATA, RESTRICOES_ORIGINAIS, RESTRICOES_RELAXADAS

def criar_arquivo_dat(alimentos_data, restricoes, nome_arquivo):
    """
    Cria um arquivo .dat com os dados dos alimentos e restrições
    
    Args:
        alimentos_data (dict): Dicionário com dados dos alimentos
        restricoes (dict): Dicionário com as restrições nutricionais
        nome_arquivo (str): Nome do arquivo (sem extensão)
    """
    
    # Lista de alimentos
    alimentos_lista = list(alimentos_data.keys())
    
    # Início do arquivo .dat
    conteudo = "# Definição do conjunto de alimentos\n"
    conteudo += f"set ALIMENTO := {' '.join(alimentos_lista)};\n\n"
    
    # Parâmetros dos alimentos
    conteudo += "# Parâmetros dos alimentos\n"
    conteudo += "param: max_porcoes tamanho energia proteina calcio magnesio vitaminaC ferro preco :=\n"
    
    for alimento, dados in alimentos_data.items():
        linha = f"{alimento:15} {dados['max_porcoes']:2} {dados['tamanho']:3} {dados['energia']:3} "
        linha += f"{dados['proteina']:4} {dados['calcio']:3} {dados['magnesio']:4} "
        linha += f"{dados['vitaminaC']:4} {dados['ferro']:4} {dados['preco']:5}\n"
        conteudo += linha
    
    conteudo += ";\n\n"
    
    # Limites mínimos
    conteudo += "# Limites mínimos e máximos para nutrientes\n"
    conteudo += "param n_min :=\n"
    for i, valor in restricoes['n_min'].items():
        comentario = {
            1: "# Energia mínima (kcal)",
            2: "# Proteína mínima (g)",
            3: "# Cálcio mínimo (mg)",
            4: "# Magnésio mínimo (mg)",
            5: "# Vitamina C mínima (mg)"
        }
        conteudo += f"{i} {valor:4}  {comentario[i]}\n"
    conteudo += ";\n\n"
    
    # Limites máximos
    conteudo += "param n_max :=\n"
    for i, valor in restricoes['n_max'].items():
        comentario = {
            1: "# Energia máxima (kcal)",
            2: "# Proteína máxima (g)",
            3: "# Cálcio máximo (mg)",
            4: "# Magnésio máximo (mg)",
            5: "# Vitamina C máxima (mg)"
        }
        conteudo += f"{i} {valor:4}  {comentario[i]}\n"
    conteudo += ";\n"
    
    # Salvar arquivo
    with open(f"{nome_arquivo}.dat", "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    print(f"Arquivo de dados salvo em {nome_arquivo}.dat")

def exibir_tabela_alimentos(alimentos_data):
    """
    Exibe uma tabela formatada com os dados dos alimentos
    
    Args:
        alimentos_data (dict): Dicionário com dados dos alimentos
    """
    print("\n" + "="*120)
    print("TABELA DE ALIMENTOS")
    print("="*120)
    
    # Cabeçalho
    header = f"{'Nome':<18} {'Max.Porç':<8} {'Tam.(g)':<7} {'Energ.(cal)':<11} {'Prot.(g)':<8} "
    header += f"{'Cálc.(mg)':<9} {'Magn.(mg)':<9} {'Vit.C(mg)':<9} {'Ferro(mg)':<9} {'Preço(R$)':<10}"
    print(header)
    print("-"*120)
    
    # Dados
    for i, (nome, dados) in enumerate(alimentos_data.items()):
        linha = f"{nome:<18} {dados['max_porcoes']:<8} {dados['tamanho']:<7} {dados['energia']:<11} "
        linha += f"{dados['proteina']:<8} {dados['calcio']:<9} {dados['magnesio']:<9} "
        linha += f"{dados['vitaminaC']:<9} {dados['ferro']:<9} {dados['preco']:<10}"
        print(linha)
    
    print("="*120)

def comparar_restricoes():
    """
    Compara as restrições originais com as relaxadas
    """
    print("\n" + "="*80)
    print("COMPARAÇÃO DE RESTRIÇÕES NUTRICIONAIS")
    print("="*80)
    
    nutrientes_nomes = {
        1: 'Energia (kcal)',
        2: 'Proteína (g)',
        3: 'Cálcio (mg)',
        4: 'Magnésio (mg)',
        5: 'Vitamina C (mg)'
    }
    
    print(f"{'Nutriente':<15} {'Original Min':<12} {'Relaxado Min':<12} {'Original Max':<12} {'Relaxado Max':<12}")
    print("-"*80)
    
    for i in range(1, 6):
        nome = nutrientes_nomes[i].split(' ')[0]
        orig_min = RESTRICOES_ORIGINAIS['n_min'][i]
        relax_min = RESTRICOES_RELAXADAS['n_min'][i]
        orig_max = RESTRICOES_ORIGINAIS['n_max'][i]
        relax_max = RESTRICOES_RELAXADAS['n_max'][i]
        
        print(f"{nome:<15} {orig_min:<12} {relax_min:<12} {orig_max:<12} {relax_max:<12}")
    
    print("="*80)

def criar_todos_arquivos_dat():
    """
    Cria todos os arquivos .dat necessários para o estudo
    """
    # Arquivo com restrições originais
    criar_arquivo_dat(ALIMENTOS_DATA, RESTRICOES_ORIGINAIS, "dieta_original")
    
    # Arquivo com restrições relaxadas
    criar_arquivo_dat(ALIMENTOS_DATA, RESTRICOES_RELAXADAS, "dieta_relaxado")
    
    print("\nTodos os arquivos .dat foram criados com sucesso!")

if __name__ == "__main__":
    # Exibir tabela de alimentos
    exibir_tabela_alimentos(ALIMENTOS_DATA)
    
    # Comparar restrições
    comparar_restricoes()
    
    # Criar arquivos .dat
    criar_todos_arquivos_dat()
