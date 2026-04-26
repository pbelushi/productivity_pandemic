import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração de estilo para gráficos académicos
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12, 'axes.titlesize': 14})

print("A carregar os dados para gerar os gráficos...")
df_final = pd.read_csv('results/analise_choque_pandemia.csv')

# Vamos focar no Comércio (G) dos EUA e da França
paises_analise = ['USA', 'FRA']
setor = 'G'

df_plot = df_final[(df_final['REF_AREA'].isin(paises_analise)) & (df_final['ACTIVITY'] == setor)].copy()

# Criar a figura com dois gráficos lado a lado
fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=False)
fig.suptitle(f'Choque Estrutural de Produtividade no Comércio (Setor {setor})', fontweight='bold')

for idx, pais in enumerate(paises_analise):
    ax = axes[idx]
    df_pais = df_plot[df_plot['REF_AREA'] == pais].sort_values('TIME_PERIOD')
    
    # Linha da Produtividade Real
    ax.plot(df_pais['TIME_PERIOD'], df_pais['Produtividade_Trabalho'], 
            marker='o', linewidth=2.5, color='#1f77b4', label='Produtividade Efetiva (Real)')
    
    # Linha do Cenário Contrafactual (Tendência)
    ax.plot(df_pais['TIME_PERIOD'], df_pais['Prod_Projetada_Contrafactual'], 
            linestyle='--', linewidth=2, color='#d62728', label='Cenário Contrafactual (Tendência 2015-2019)')
    
    # Realçar o período da pandemia (área sombreada a partir de 2020)
    ax.axvspan(2019.5, df_pais['TIME_PERIOD'].max() + 0.5, color='gray', alpha=0.1, label='Período Pós-Choque')
    
    ax.set_title(f'País: {pais}')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Produtividade do Trabalho (VAB / Empregados)')
    ax.legend(loc='best', fontsize=10)
    
    # Remover bordas desnecessárias
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()

# Guardar o gráfico numa pasta 'plots'
os.makedirs('plots', exist_ok=True)
caminho_grafico = 'plots/grafico_choque_comercio.png'
plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')

print(f"\nSucesso! Gráfico guardado em: {caminho_grafico}")
plt.show()  # Abre a janela com o gráfico para você ver na hora!