# -*- coding: utf-8 -*-
"""
solver.py - Solucionador para o problema da dieta usando AMPL

Autor: José Brito
"""

import os
import json
from datetime import datetime
from amplpy import AMPL, ampl_notebook
from config import ALIMENTOS_DATA, NUTRIENTES, SOLVER_CONFIG

class DietSolver:
    """
    Classe para resolver o problema da dieta usando AMPL
    """
    
    def __init__(self):
        """Inicializa o solver AMPL"""
        try:
            self.ampl = ampl_notebook(
                modules=["coin"],
                license_uuid="default",
            )
            print("AMPL inicializado com sucesso!")
        except Exception as e:
            print(f"Erro ao inicializar AMPL: {e}")
            self.ampl = None
    
    def resolver_modelo(self, arquivo_mod, arquivo_dat, verbose=True):
        """
        Resolve um modelo específico
        
        Args:
            arquivo_mod (str): Caminho para o arquivo .mod
            arquivo_dat (str): Caminho para o arquivo .dat
            verbose (bool): Se True, exibe informações detalhadas
            
        Returns:
            dict: Resultados da otimização
        """
        if not self.ampl:
            print("AMPL não está disponível!")
            return None
        
        try:
            # Reset e carregamento do modelo
            self.ampl.reset()
            self.ampl.read(arquivo_mod)
            self.ampl.read_data(arquivo_dat)
            
            # Configurar solver
            self.ampl.option['solver'] = SOLVER_CONFIG['solver']
            
            if verbose:
                print(f"\nResolvendo modelo: {arquivo_mod}")
                print(f"Dados de entrada: {arquivo_dat}")
                print(f"Solver utilizado: {SOLVER_CONFIG['solver']}")
            
            # Resolver
            self.ampl.solve()
            
            # Verificar status da solução
            solve_result = self.ampl.get_value("solve_result")
            
            if verbose:
                print(f"Status da solução: {solve_result}")
            
            # Extrair resultados
            resultados = self._extrair_resultados(verbose)
            
            return resultados
            
        except Exception as e:
            print(f"Erro ao resolver modelo: {e}")
            return None
    
    def _extrair_resultados(self, verbose=True):
        """
        Extrai os resultados da otimização
        
        Args:
            verbose (bool): Se True, exibe informações detalhadas
            
        Returns:
            dict: Dicionário com os resultados
        """
        resultados = {
            'timestamp': datetime.now().isoformat(),
            'solve_result': self.ampl.get_value("solve_result"),
            'objetivo': None,
            'compras': {},
            'nutrientes_totais': {},
            'estatisticas': {}
        }
        
        try:
            # Valor da função objetivo
            resultados['objetivo'] = self.ampl.get_objective("Custo_Total").value()
            
            # Variáveis de compra
            compras_df = self.ampl.get_variable("Compra").get_values()
            for index, row in compras_df.iterrows():
                alimento = index[0] if isinstance(index, tuple) else index
                quantidade = row.iloc[0]
                resultados['compras'][alimento] = int(quantidade)
            
            # Calcular nutrientes totais
            resultados['nutrientes_totais'] = self._calcular_nutrientes_totais(resultados['compras'])
            
            # Estatísticas
            resultados['estatisticas'] = self._calcular_estatisticas(resultados['compras'])
            
            if verbose:
                self._exibir_resultados(resultados)
                
        except Exception as e:
            print(f"Erro ao extrair resultados: {e}")
            
        return resultados
    
    def _calcular_nutrientes_totais(self, compras):
        """
        Calcula o total de nutrientes consumidos
        
        Args:
            compras (dict): Dicionário com as quantidades compradas
            
        Returns:
            dict: Nutrientes totais
        """
        nutrientes_totais = {
            'energia': 0,
            'proteina': 0,
            'calcio': 0,
            'magnesio': 0,
            'vitaminaC': 0,
            'ferro': 0
        }
        
        for alimento, quantidade in compras.items():
            if quantidade > 0 and alimento in ALIMENTOS_DATA:
                dados = ALIMENTOS_DATA[alimento]
                for nutriente in nutrientes_totais:
                    nutrientes_totais[nutriente] += dados.get(nutriente, 0) * quantidade # Use .get with default 0 to handle missing keys gracefully
        
        return nutrientes_totais
    
    def _calcular_estatisticas(self, compras):
        """
        Calcula estatísticas da solução
        
        Args:
            compras (dict): Dicionário com as quantidades compradas
            
        Returns:
            dict: Estatísticas
        """
        alimentos_selecionados = sum(1 for q in compras.values() if q > 0)
        porcoes_totais = sum(compras.values())
        
        # Custo total dos alimentos selecionados para a dieta
        custo_total_alimentos_selecionados = sum(ALIMENTOS_DATA.get(alimento, {}).get('preco', 0) * quantidade
                                                 for alimento, quantidade in compras.items()
                                                 if quantidade > 0 and alimento in ALIMENTOS_DATA)
        
        custo_medio_porcao = custo_total_alimentos_selecionados / porcoes_totais if porcoes_totais > 0 else 0
        
        return {
            'alimentos_selecionados': alimentos_selecionados,
            'porcoes_totais': int(porcoes_totais),
            'custo_medio_porcao': round(custo_medio_porcao, 2)
        }
    
    def _exibir_resultados(self, resultados):
        """
        Exibe os resultados formatados
        
        Args:
            resultados (dict): Dicionário com os resultados
        """
        print("\n" + "="*60)
        print("RESULTADOS DA OTIMIZAÇÃO")
        print("="*60)
        
        print(f"Status: {resultados['solve_result']}")
        print(f"Custo Total: R$ {resultados['objetivo']:.2f}")
        
        print(f"\nAlimentos Selecionados ({resultados['estatisticas']['alimentos_selecionados']}):")
        print("-"*40)
        
        for alimento, quantidade in resultados['compras'].items():
            if quantidade > 0:
                preco_unitario = ALIMENTOS_DATA.get(alimento, {}).get('preco', 0)
                custo_total_alimento = preco_unitario * quantidade
                print(f"{alimento:<20}: {quantidade:2} porções (R$ {custo_total_alimento:5.2f})")
        
        print(f"\nNutrientes Totais:")
        print("-"*40)
        nutrientes = resultados['nutrientes_totais']
        print(f"Energia:     {nutrientes['energia']:7.1f} kcal")
        print(f"Proteína:    {nutrientes['proteina']:7.1f} g")
        print(f"Cálcio:      {nutrientes['calcio']:7.1f} mg")
        print(f"Magnésio:    {nutrientes['magnesio']:7.1f} mg")
        print(f"Vitamina C:  {nutrientes['vitaminaC']:7.1f} mg")
        print(f"Ferro:       {nutrientes['ferro']:7.1f} mg")
        
        print(f"\nEstatísticas:")
        print("-"*40)
        stats = resultados['estatisticas']
        print(f"Total de porções: {stats['porcoes_totais']}")
        print(f"Custo médio por porção: R$ {stats['custo_medio_porcao']:.2f}")
        
        print("="*60)
    
    def salvar_resultados(self, resultados, nome_arquivo):
        """
        Salva os resultados em arquivo JSON
        
        Args:
            resultados (dict): Resultados da otimização
            nome_arquivo (str): Nome do arquivo (sem extensão)
        """
        if resultados:
            try:
                with open(f"{nome_arquivo}.json", "w", encoding="utf-8") as f:
                    json.dump(resultados, f, indent=2, ensure_ascii=False)
                print(f"Resultados salvos em {nome_arquivo}.json")
            except Exception as e:
                print(f"Erro ao salvar resultados em {nome_arquivo}.json: {e}")
    
    def comparar_solucoes(self, resultados1, resultados2, nome1="Solução 1", nome2="Solução 2"):
        """
        Compara duas soluções
        
        Args:
            resultados1 (dict): Primeira solução
            resultados2 (dict): Segunda solução
            nome1 (str): Nome da primeira solução
            nome2 (str): Nome da segunda solução
        """
        print("\n" + "="*80)
        print("COMPARAÇÃO DE SOLUÇÕES")
        print("="*80)
        
        # Comparação de custos
        custo1 = resultados1.get('objetivo', 0)
        custo2 = resultados2.get('objetivo', 0)
        diferenca_custo = custo2 - custo1
        percentual_diferenca = (diferenca_custo / custo1) * 100 if custo1 != 0 else float('inf')
        
        print(f"{'Critério':<25} {nome1:<20} {nome2:<20}")
        print("-"*80)
        print(f"{'Custo Total (R$)':<25} {custo1:<20.2f} {custo2:<20.2f}")
        print(f"{'Diferença de Custo':<25} {'':<20} {diferenca_custo:<20.2f}")
        print(f"{'Variação (%)':<25} {'':<20} {percentual_diferenca:<20.1f}")
        
        # Comparação de diversidade
        alimentos1 = resultados1['estatisticas']['alimentos_selecionados'] if resultados1 and 'estatisticas' in resultados1 else 0
        alimentos2 = resultados2['estatisticas']['alimentos_selecionados'] if resultados2 and 'estatisticas' in resultados2 else 0
        
        print(f"{'Alimentos Únicos':<25} {alimentos1:<20} {alimentos2:<20}")
        
        # Comparação de porções
        porcoes1 = resultados1['estatisticas']['porcoes_totais'] if resultados1 and 'estatisticas' in resultados1 else 0
        porcoes2 = resultados2['estatisticas']['porcoes_totais'] if resultados2 and 'estatisticas' in resultados2 else 0
        
        print(f"{'Total de Porções':<25} {porcoes1:<20} {porcoes2:<20}")
        
        # Comparação de custo médio
        custo_medio1 = resultados1['estatisticas']['custo_medio_porcao'] if resultados1 and 'estatisticas' in resultados1 else 0
        custo_medio2 = resultados2['estatisticas']['custo_medio_porcao'] if resultados2 and 'estatisticas' in resultados2 else 0
        
        print(f"{'Custo Médio/Porção':<25} {custo_medio1:<20.2f} {custo_medio2:<20.2f}")
        
        print("="*80)
        
        # Análise qualitativa
        print("\nANÁLISE QUALITATIVA:")
        print("-"*40)
        
        if custo1 < custo2:
            print(f"• {nome1} é mais econômica (R$ {abs(diferenca_custo):.2f} de diferença)")
        else:
            print(f"• {nome2} é mais econômica (R$ {abs(diferenca_custo):.2f} de diferença)")
        
        if alimentos1 > alimentos2:
            print(f"• {nome1} oferece maior diversidade ({alimentos1} vs {alimentos2} alimentos)")
        elif alimentos2 > alimentos1:
            print(f"• {nome2} oferece maior diversidade ({alimentos2} vs {alimentos1} alimentos)")
        else:
            print("• Ambas as soluções têm a mesma diversidade")
        
        print("="*80)

def exemplo_uso():
    """
    Exemplo de como usar a classe DietSolver
    """
    solver = DietSolver()
    
    if solver.ampl:
        # Resolver modelo básico
        print("Resolvendo modelo básico...")
        resultados_basico = solver.resolver_modelo("dieta_basico.mod", "dieta_relaxado.dat")
        
        if resultados_basico:
            solver.salvar_resultados(resultados_basico, "resultados_basico")
        
        # Resolver modelo diversificado
        print("\nResolvendo modelo diversificado...")
        resultados_diversificado = solver.resolver_modelo("dieta_diversificado.mod", "dieta_relaxado.dat")
        
        if resultados_diversificado:
            solver.salvar_resultados(resultados_diversificado, "resultados_diversificado")
        
        # Comparar soluções
        if resultados_basico and resultados_diversificado:
            solver.comparar_solucoes(
                resultados_basico,
                resultados_diversificado,
                "Solução Ótima",
                "Solução Diversificada"
            )

if __name__ == "__main__":
    exemplo_uso()
