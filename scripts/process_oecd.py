import pandas as pd
import os

print("1. A carregar os dados brutos...")
df_raw = pd.read_csv('data/ocde_stan_raw.csv')

# Descobrindo o nome exato da coluna de setor na nova API
colunas_disponiveis = df_raw.columns.tolist()
# O ERRO ESTAVA AQUI: O comentário agora tem a hashtag (#) correta
coluna_setor = 'ACTIVITY' if 'ACTIVITY' in colunas_disponiveis else 'SECTOR' # Se não for nenhum dos dois, na OCDE geralmente é ACTIVITY

print(f"Coluna de setor identificada como: {coluna_setor}")

# Incluímos o setor nas colunas de interesse
colunas_interesse = ['REF_AREA', coluna_setor, 'MEASURE', 'TIME_PERIOD', 'OBS_VALUE']
df_clean = df_raw[colunas_interesse].copy()

print("2. A reestruturar os dados (Pivot Table com Setores)...")
df_pivot = df_clean.pivot_table(
    index=['REF_AREA', coluna_setor, 'TIME_PERIOD'], 
    columns='MEASURE',
    values='OBS_VALUE',
    aggfunc='first'
).reset_index()

print("3. A limpar dados em falta e calcular a Produtividade...")
df_modelo = df_pivot.dropna(subset=['B1G', 'SAL']).copy()

# O Cálculo da Produtividade
df_modelo['Produtividade_Trabalho'] = df_modelo['B1G'] / df_modelo['SAL']

df_modelo = df_modelo.sort_values(by=['REF_AREA', coluna_setor, 'TIME_PERIOD'])

caminho_processado = 'data/ocde_produtividade_modelo.csv'
df_modelo.to_csv(caminho_processado, index=False)

print("\nVeja como a base ficou muito mais consistente agora:")
print(df_modelo[df_modelo['REF_AREA'] == 'FRA'].head())