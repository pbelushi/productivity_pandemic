import pandas as pd
import numpy as np
from scipy.stats import linregress
import os

print("1. A carregar os dados harmonizados...")
df = pd.read_csv('data/ocde_produtividade_modelo.csv')

# A SOLUÇÃO: Converter Infinitos em NaN, e depois apagar todas as linhas com NaN na Produtividade
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['Produtividade_Trabalho'])

print("2. A treinar os modelos de tendência pré-pandemia (2015-2019)...")
resultados = []

# Agrupar por País e Setor (ACTIVITY)
grupos = df.groupby(['REF_AREA', 'ACTIVITY']) 

for (pais, setor), dados_grupo in grupos:
    # Separar o período pré-pandemia (treino do modelo)
    df_pre = dados_grupo[dados_grupo['TIME_PERIOD'] <= 2019].copy()
    
    # Precisamos de pelo menos 3 anos de dados para traçar uma reta
    if len(df_pre) >= 3:
        x_pre = df_pre['TIME_PERIOD'].values
        y_pre = df_pre['Produtividade_Trabalho'].values
        
        # Treinar a regressão linear (Mínimos Quadrados)
        slope, intercept, r_value, p_value, std_err = linregress(x_pre, y_pre)
        
        # Projetar a tendência para todos os anos do grupo (incluindo pós-2020)
        df_temp = dados_grupo.copy()
        anos_totais = df_temp['TIME_PERIOD'].values
        df_temp['Prod_Projetada_Contrafactual'] = (slope * anos_totais) + intercept
        
        # Calcular o tamanho do choque estrutural em %
        df_temp['Choque_Estrutural_Percentual'] = ((df_temp['Produtividade_Trabalho'] / df_temp['Prod_Projetada_Contrafactual']) - 1) * 100
        
        resultados.append(df_temp)

# Unir tudo num único DataFrame final
df_final = pd.concat(resultados, ignore_index=True)

# 3. Guardar os resultados na pasta correspondente
os.makedirs('results', exist_ok=True)
caminho_resultados = 'results/analise_choque_pandemia.csv'
df_final.to_csv(caminho_resultados, index=False)

print(f"Sucesso! Modelo treinado sem erros. Resultados guardados em: {caminho_resultados}")

# =====================================================================
# 4. TESTE DA SUA TESE (Digitalização nos Serviços/Comércio)
# =====================================================================
# Vamos olhar para o Setor J (Informação e Comunicação) num ano pós-pandemia (2022)
print("\nVerificação da Tese: Choque Estrutural em Informação e Comunicação (Setor 'J') em 2022:")
exemplo = df_final[
    (df_final['REF_AREA'].isin(['FRA', 'DEU', 'ITA', 'USA'])) & 
    (df_final['ACTIVITY'] == 'J') & 
    (df_final['TIME_PERIOD'] == 2022)
]
print(exemplo[['REF_AREA', 'ACTIVITY', 'TIME_PERIOD', 'Produtividade_Trabalho', 'Prod_Projetada_Contrafactual', 'Choque_Estrutural_Percentual']])