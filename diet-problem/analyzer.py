# -*- coding: utf-8 -*-
"""
analyzer.py - Análise e visualização dos resultados do problema da dieta

Autor: José Brito
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import ALIMENTOS_DATA, RESTRICOES_RELAXADAS, NUTRIENTES

class DietAnalyzer:
    """
    Classe para análise e visualização dos resultados da dieta
    """
    
    def __init__(self):
        """Inicializa o analisador"""
        self.resultados = {}
        
        # Configurar matplotlib para usar fonte que suporta caracteres especiais
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['figure.figsize'] = (12, 8)
        # Check if 'seaborn-v0_8' is available, otherwise use 'default'
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
    
    def carregar_resultados(self, arquivo_json):
        """
        Carrega resultados de um arquivo JSON
        
        Args:
            arquivo_json (str): Caminho para o arquivo JSON
            
        Returns:
            dict: Resultados carregados
        """
        try:
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                resultados = json.load(f)
            print(f"Resultados carregados de {arquivo_json}")
            return resultados
        except FileNotFoundError:
            print(f"Arquivo {arquivo_json} não encontrado!")
            return None
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON em {arquivo_json}")
            return None
    
    def criar_grafico_barras_alimentos(self, resultados, titulo="Quantidade de Alimentos Selecionados"):
        """
        Cria gráfico de barras com os alimentos selecionados
        
        Args:
            resultados (dict): Resultados da otimização
            titulo (str): Título do gráfico
        """
        # Filtrar apenas alimentos com quantidade > 0
        alimentos_selecionados = {k: v for k, v in resultados['compras'].items() if v > 0}
        
        if not alimentos_selecionados:
            print("Nenhum alimento foi selecionado para o gráfico de barras!")
            return
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        
        alimentos = list(alimentos_selecionados.keys())
        quantidades = list(alimentos_selecionados.values())
        
        # Cores baseadas no preço (mais caro = mais vermelho)
        cores = []
        max_preco = max(ALIMENTOS_DATA.get(alimento, {}).get('preco', 0) for alimento in alimentos) if alimentos else 1
        for alimento in alimentos:
            preco = ALIMENTOS_DATA.get(alimento, {}).get('preco', 0)
            # Normalizar preço para escala de cor (0-1)
            preco_norm = preco / max_preco if max_preco > 0 else 0 # Avoid division by zero
            cores.append(plt.cm.RdYlBu_r(preco_norm))
        
        barras = ax.bar(alimentos, quantidades, color=cores, alpha=0.7, edgecolor='black')
        
        # Adicionar valores sobre as barras
        for barra, quantidade in zip(barras, quantidades):
            height = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2., height + 0.05,
                            f'{int(quantidade)}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Alimentos', fontsize=12, fontweight='bold')
        ax.set_ylabel('Quantidade (porções)', fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Rotacionar labels do eixo x para melhor legibilidade
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    def criar_grafico_pizza_custos(self, resultados, titulo="Distribuição de Custos por Alimento"):
        """
        Cria gráfico de pizza com a distribuição de custos
        
        Args:
            resultados (dict): Resultados da otimização
            titulo (str): Título do gráfico
        """
        # Calcular custos por alimento
        custos_alimentos = {}
        for alimento, quantidade in resultados['compras'].items():
            if quantidade > 0:
                preco_unitario = ALIMENTOS_DATA.get(alimento, {}).get('preco', 0)
                custos_alimentos[alimento] = preco_unitario * quantidade
        
        if not custos_alimentos:
            print("Nenhum custo para exibir no gráfico de pizza!")
            return
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(10, 8))
        
        alimentos = list(custos_alimentos.keys())
        custos = list(custos_alimentos.values())
        
        # Cores automáticas
        colors = plt.cm.Set3(np.linspace(0, 1, len(alimentos)))
        
        wedges, texts, autotexts = ax.pie(custos, labels=alimentos, autopct='%1.1f%%',
                                         colors=colors, startangle=90)
        
        # Melhorar aparência do texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def criar_grafico_nutrientes(self, resultados, titulo="Nutrientes Totais vs Restrições"):
        """
        Cria gráfico comparando nutrientes obtidos vs restrições
        
        Args:
            resultados (dict): Resultados da otimização
            titulo (str): Título do gráfico
        """
        nutrientes_obtidos = resultados['nutrientes_totais']
        
        # Preparar dados
        nutrientes_nomes = ['Energia\n(kcal)', 'Proteína\n(g)', 'Cálcio\n(mg)',
                            'Magnésio\n(mg)', 'Vitamina C\n(mg)']
        
        valores_obtidos = [
            nutrientes_obtidos.get('energia', 0),
            nutrientes_obtidos.get('proteina', 0),
            nutrientes_obtidos.get('calcio', 0),
            nutrientes_obtidos.get('magnesio', 0),
            nutrientes_obtidos.get('vitaminaC', 0)
        ]
        
        valores_min = [RESTRICOES_RELAXADAS['n_min'][i] for i in range(1, 6)]
        valores_max = [RESTRICOES_RELAXADAS['n_max'][i] for i in range(1, 6)]
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(14, 8))
        
        x = np.arange(len(nutrientes_nomes))
        width = 0.25
        
        bars1 = ax.bar(x - width, valores_min, width, label='Mínimo', color='lightcoral', alpha=0.7)
        bars2 = ax.bar(x, valores_obtidos, width, label='Obtido', color='lightblue', alpha=0.7)
        bars3 = ax.bar(x + width, valores_max, width, label='Máximo', color='lightgreen', alpha=0.7)
        
        # Adicionar valores sobre as barras
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + (max(valores_max)*0.01 if max(valores_max) > 0 else 1),
                                f'{height:.0f}', ha='center', va='bottom', fontsize=9)
        
        ax.set_xlabel('Nutrientes', fontsize=12, fontweight='bold')
        ax.set_ylabel('Quantidade', fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(nutrientes_nomes)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def criar_relatorio_completo(self, resultados, nome_arquivo="relatorio_dieta"):
        """
        Cria um relatório completo em texto
        
        Args:
            resultados (dict): Resultados da otimização
            nome_arquivo (str): Nome do arquivo de saída
        """
        relatorio = []
        relatorio.append("="*80)
        relatorio.append("RELATÓRIO COMPLETO DA DIETA OTIMIZADA")
        relatorio.append("="*80)
        relatorio.append(f"Data de geração: {resultados['timestamp']}")
        relatorio.append(f"Status da solução: {resultados['solve_result']}")
        relatorio.append("")
        
        # Resumo financeiro
        relatorio.append("RESUMO FINANCEIRO")
        relatorio.append("-"*40)
        relatorio.append(f"Custo total da dieta: R$ {resultados['objetivo']:.2f}")
        relatorio.append(f"Custo médio por porção: R$ {resultados['estatisticas']['custo_medio_porcao']:.2f}")
        relatorio.append("")
        
        # Alimentos selecionados
        relatorio.append("ALIMENTOS SELECIONADOS")
        relatorio.append("-"*40)
        total_porcoes = 0
        for alimento, quantidade in resultados['compras'].items():
            if quantidade > 0:
                preco_unitario = ALIMENTOS_DATA.get(alimento, {}).get('preco', 0)
                custo_total = preco_unitario * quantidade
                total_porcoes += quantidade
                relatorio.append(f"{alimento:<20}: {quantidade:2} porções × R$ {preco_unitario:5.2f} = R$ {custo_total:6.2f}")
        
        relatorio.append(f"\nTotal de porções: {total_porcoes}")
        relatorio.append(f"Diversidade: {resultados['estatisticas']['alimentos_selecionados']} alimentos únicos")
        relatorio.append("")
        
        # Análise nutricional
        relatorio.append("ANÁLISE NUTRICIONAL")
        relatorio.append("-"*40)
        nutrientes = resultados['nutrientes_totais']
        
        for i, nome_nutriente in NUTRIENTES.items():
            valor_obtido = nutrientes.get(nome_nutriente, 0)
            min_req = RESTRICOES_RELAXADAS['n_min'][i]
            max_req = RESTRICOES_RELAXADAS['n_max'][i]
            
            status = "✓ OK"
            if valor_obtido < min_req:
                status = "⚠ BAIXO"
            elif valor_obtido > max_req:
                status = "⚠ ALTO"
            
            unidade = "kcal" if nome_nutriente == "energia" else ("g" if nome_nutriente == "proteina" else "mg")
            relatorio.append(f"{nome_nutriente.capitalize():<12}: {valor_obtido:7.1f} {unidade} (min: {min_req}, max: {max_req}) {status}")
        
        relatorio.append("")
        
        # Recomendações
        relatorio.append("RECOMENDAÇÕES")
        relatorio.append("-"*40)
        
        if resultados['estatisticas']['alimentos_selecionados'] < len(ALIMENTOS_DATA) / 2 : # Arbitrary threshold for "low diversity"
            relatorio.append("• Considere aumentar a diversidade de alimentos para uma dieta mais equilibrada.")
        
        if resultados['objetivo'] > 100: # Arbitrary threshold for "high cost"
            relatorio.append("• Custo elevado - considere buscar alternativas mais econômicas.")
        
        if any(resultados['compras'].get(alimento, 0) >= 4 for alimento in ALIMENTOS_DATA if resultados['compras'].get(alimento, 0) > 0):
            relatorio.append("• Alguns alimentos estão em alta quantidade - verifique se há dependência excessiva.")
        
        relatorio.append("")
        relatorio.append("="*80)
        
        # Salvar relatório
        try:
            with open(f"{nome_arquivo}.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(relatorio))
            print(f"Relatório salvo em {nome_arquivo}.txt")
        except Exception as e:
            print(f"Erro ao salvar relatório em {nome_arquivo}.txt: {e}")
            
        # Também exibir no console
        print("\n".join(relatorio))
    
    def comparar_multiplas_solucoes(self, lista_resultados, nomes_solucoes):
        """
        Compara múltiplas soluções
        
        Args:
            lista_resultados (list): Lista de dicionários com resultados
            nomes_solucoes (list): Lista com nomes das soluções
        """
        if len(lista_resultados) != len(nomes_solucoes):
            print("Número de resultados deve ser igual ao número de nomes!")
            return
        
        # Criar DataFrame para comparação
        dados_comparacao = []
        
        for i, (resultados, nome) in enumerate(zip(lista_resultados, nomes_solucoes)):
            dados_comparacao.append({
                'Solução': nome,
                'Custo Total (R$)': resultados.get('objetivo', 0),
                'Alimentos Únicos': resultados['estatisticas'].get('alimentos_selecionados', 0),
                'Total Porções': resultados['estatisticas'].get('porcoes_totais', 0),
                'Custo/Porção (R$)': resultados['estatisticas'].get('custo_medio_porcao', 0),
                'Energia (kcal)': resultados['nutrientes_totais'].get('energia', 0),
                'Proteína (g)': resultados['nutrientes_totais'].get('proteina', 0)
            })
        
        df = pd.DataFrame(dados_comparacao)
        
        print("\n" + "="*100)
        print("COMPARAÇÃO MÚLTIPLA DE SOLUÇÕES")
        print("="*100)
        print(df.to_string(index=False))
        print("="*100)
        
        # Criar gráfico comparativo
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Gráfico 1: Custo Total
        ax1.bar(df['Solução'], df['Custo Total (R$)'], color='lightblue', alpha=0.7)
        ax1.set_title('Custo Total por Solução')
        ax1.set_ylabel('Custo (R$)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico 2: Diversidade
        ax2.bar(df['Solução'], df['Alimentos Únicos'], color='lightgreen', alpha=0.7)
        ax2.set_title('Diversidade de Alimentos')
        ax2.set_ylabel('Número de Alimentos')
        ax2.tick_params(axis='x', rotation=45)
        
        # Gráfico 3: Energia
        ax3.bar(df['Solução'], df['Energia (kcal)'], color='orange', alpha=0.7)
        ax3.set_title('Energia Total')
        ax3.set_ylabel('Energia (kcal)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Gráfico 4: Proteína
        ax4.bar(df['Solução'], df['Proteína (g)'], color='red', alpha=0.7)
        ax4.set_title('Proteína Total')
        ax4.set_ylabel('Proteína (g)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()

def exemplo_analise():
    """
    Exemplo de como usar a classe DietAnalyzer
    """
    analyzer = DietAnalyzer()
    
    resultados_basico = analyzer.carregar_resultados("resultados_basico.json")
    resultados_diversificado = analyzer.carregar_resultados("resultados_diversificado.json")
    
    if resultados_basico:
        print("Analisando solução básica...")
        analyzer.criar_grafico_barras_alimentos(resultados_basico, "Solução Ótima - Alimentos")
        analyzer.criar_grafico_pizza_custos(resultados_basico, "Solução Ótima - Distribuição de Custos")
        analyzer.criar_grafico_nutrientes(resultados_basico, "Solução Ótima - Nutrientes")
        analyzer.criar_relatorio_completo(resultados_basico, "relatorio_solucao_otima")
    
    if resultados_diversificado:
        print("\nAnalisando solução diversificada...")
        analyzer.criar_grafico_barras_alimentos(resultados_diversificado, "Solução Diversificada - Alimentos")
        analyzer.criar_grafico_pizza_custos(resultados_diversificado, "Solução Diversificada - Distribuição de Custos")
        analyzer.criar_grafico_nutrientes(resultados_diversificado, "Solução Diversificada - Nutrientes")
        analyzer.criar_relatorio_completo(resultados_diversificado, "relatorio_solucao_diversificada")
    
    if resultados_basico and resultados_diversificado:
        print("\nComparando soluções...")
        analyzer.comparar_multiplas_solucoes(
            [resultados_basico, resultados_diversificado],
            ["Ótima", "Diversificada"]
        )

if __name__ == "__main__":
    exemplo_analise()
