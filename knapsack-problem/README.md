# Problema da Mochila - Cenário RPG 🎮

Este projeto implementa diferentes solucionadores para o **Problema da Mochila** usando um cenário de RPG onde um aventureiro deve escolher quais tesouros carregar em sua mochila para maximizar o valor total, respeitando o limite de peso de 10kg.

## 📁 Estrutura dos Arquivos

```
├── knapsack_data.py          # Dados do problema (itens, pesos, valores)
├── ampl_files_generator.py   # Gerador de arquivos AMPL (.mod, .dat, .run)
├── ampl_solver.py           # Solucionador usando AMPL
├── alternative_solver.py    # Solucionador usando Programação Dinâmica
├── main.py                  # Arquivo principal com menu interativo
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

## 🎯 Descrição do Problema

**Cenário**: Um aventureiro encontrou 10 tesouros valiosos durante uma caça ao tesouro, mas sua mochila só suporta **10kg**. Qual combinação de itens maximiza o valor total?

### 🏺 Itens Disponíveis

| Item               | Peso (kg) | Valor ($) | Descrição                                                           |
|--------------------|-----------|-----------|---------------------------------------------------------------------|
| Moeda Antiga       | 1.0       | 300       | Moeda de ouro rara, valiosa para colecionadores                     |
| Diamante           | 2.0       | 1500      | Pedra preciosa encontrada em um baú misterioso                      |
| Barra de Ouro      | 5.0       | 2500      | Barra de ouro puro, mas muito pesada                                |
| Colar de Prata     | 1.5       | 800       | Colar de prata decorado com pedras preciosas                        |
| Poção Mágica       | 3.0       | 1200      | Poção mágica de valor inestimável para alquimistas                  |
| Livro Antigo       | 2.5       | 500       | Livro antigo contendo segredos perdidos da civilização              |
| Coroa              | 4.0       | 2200      | Coroa real incrustada com rubis e safiras                           |
| Estátua de Jade    | 6.0       | 2800      | Estatueta de jade sagrado, venerada por povos antigos               |
| Anel de Safira     | 0.5       | 900       | Anel de safira que pertencia a um rei lendário                      |
| Mapa do Tesouro    | 1.0       | 1100      | Mapa que leva a um tesouro escondido, valioso para caçadores        |

## 🚀 Como Executar

### Execução Simples
```bash
python main.py
```

### Executar Módulos Individualmente

1. **Ver dados do problema:**
```bash
python knapsack_data.py
```

2. **Gerar arquivos AMPL:**
```bash
python ampl_files_generator.py
```

3. **Executar solucionador alternativo:**
```bash
python alternative_solver.py
```

4. **Executar solucionador AMPL (se disponível):**
```bash
python ampl_solver.py
```

## 🔧 Instalação

### Dependências Básicas
O projeto funciona apenas com a biblioteca padrão do Python (sem dependências externas).

### Dependências Opcionais
Para usar o solucionador AMPL:
```bash
pip install amplpy
```

## 📊 Métodos de Solução

### 1. **Solucionador AMPL** (`ampl_solver.py`)
- Usa modelagem matemática profissional
- Requer instalação do `amplpy`
- Gera arquivos .mod, .dat e .run automaticamente
- Garante solução ótima

### 2. **Programação Dinâmica** (`alternative_solver.py`)
- Implementação pura em Python
- Algoritmo clássico para o problema da mochila
- Complexidade: O(n × W)
- Garante solução ótima
- Não requer dependências externas

### 3. **Algoritmo Guloso** (para comparação)
- Seleciona itens por maior valor/peso
- Rápido mas não garante otimalidade
- Usado para comparação com a solução ótima

## 🎮 Menu Interativo

O arquivo `main.py` oferece um menu com as seguintes opções:

```
1. Ver informações do dataset
2. Resolver com AMPL (se disponível)
3. Resolver com Programação Dinâmica  
4. Comparar soluções (DP vs Guloso)
5. Gerar arquivos AMPL
6. Executar análise completa
0. Sair
```

## 📈 Resultados Esperados

**Solução Ótima:**
- **Valor Total:** $6.800
- **Peso Total:** 9.0 kg
- **Itens Selecionados:**
  - Anel de Safira (0.5 kg, $900)
  - Colar de Prata (1.5 kg, $800)
  - Coroa (4.0 kg, $2200)
  - Diamante (2.0 kg, $1500)
  - Mapa do Tesouro (1.0 kg, $1100)
  - Moeda Antiga (1.0 kg, $300)

## 🔬 Modelo Matemático

**Função Objetivo:**
```
Maximizar: Σ (valor[i] × incluir[i])
```

**Restrições:**
```
Σ (peso[i] × incluir[i]) ≤ 10 kg
incluir[i] ∈ {0, 1}
```

Onde `incluir[i]` é uma variável binária que indica se o item `i` foi selecionado.

## 📝 Arquivos AMPL Gerados

- **mochila.mod**: Modelo matemático
- **mochila.dat**: Dados do problema  
- **mochila.run**: Script de execução com relatórios

## 🤝 Contribuições

Este projeto foi criado como material educacional para demonstrar diferentes abordagens para resolver o Problema da Mochila.

## 📄 Autor

**José Brito** - Implementação e documentação do cenário RPG

---

*Divirta-se explorando diferentes algoritmos de otimização! 🎯*