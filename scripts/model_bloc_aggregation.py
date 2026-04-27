import pandas as pd
import numpy as np
from scipy.stats import linregress
import os

print("1. A carregar e agregar os dados das economias desenvolvidas...")
df = pd.read_csv('data/ocde_produtividade_modelo.csv')

# 1.1 Definir os países que formarão o nosso bloco
paises_bloco = ['USA', 'FRA', 'DEU', 'ITA']
df_filtrado = df[df['REF_AREA'].isin(paises_bloco)].copy()

# 1.2 O PASSO CRUCIAL: Somar o Valor Adicionado e o Pessoal Ocupado por Ano e Setor
# Isto cria o nosso "País Único" pesando o tamanho de cada economia corretamente
df_bloco = df_filtrado.groupby(['TIME_PERIOD', 'ACTIVITY'])[['B1G', 'SAL']].sum().reset_index()

# 1.3 Recalcular a produtividade real do bloco
df_bloco['Produtividade_Trabalho'] = df_bloco['B1G'] / df_bloco['SAL']
df_bloco['REF_AREA'] = 'BLOCO_OCDE' # Damos um nome ao nosso novo "país"

# Limpar infinitos e nulos (boa prática)
df_bloco = df_bloco.replace([np.inf, -np.inf], np.nan).dropna(subset=['Produtividade_Trabalho'])

print("2. A treinar o modelo contrafactual para o Bloco OCDE (2015-2019)...")
resultados_bloco = []

# Agrupar apenas por setor, já que o país agora é apenas um (BLOCO_OCDE)
grupos = df_bloco.groupby('ACTIVITY')

for setor, dados_grupo in grupos:
    df_pre = dados_grupo[dados_grupo['TIME_PERIOD'] <= 2019].copy()
    
    if len(df_pre) >= 3:
        x_pre = df_pre['TIME_PERIOD'].values
        y_pre = df_pre['Produtividade_Trabalho'].values
        
        slope, intercept, r_value, p_value, std_err = linregress(x_pre, y_pre)
        
        df_temp = dados_grupo.copy()
        anos_totais = df_temp['TIME_PERIOD'].values
        df_temp['Prod_Projetada_Contrafactual'] = (slope * anos_totais) + intercept
        df_temp['Choque_Estrutural_Percentual'] = ((df_temp['Produtividade_Trabalho'] / df_temp['Prod_Projetada_Contrafactual']) - 1) * 100
        
        df_temp['REF_AREA'] = 'BLOCO_OCDE'
        resultados_bloco.append(df_temp)

df_final_bloco = pd.concat(resultados_bloco, ignore_index=True)

# Guardar os resultados do bloco num CSV separado
os.makedirs('results', exist_ok=True)
caminho_resultados = 'results/analise_bloco_ocde.csv'
df_final_bloco.to_csv(caminho_resultados, index=False)

print("\n==================================================================")
print("TESTE EM BLOCO: Choque de Produtividade em 2022")
print("==================================================================\n")

# Vamos olhar para o Comércio (G), Informação/Comunicação (J) e Indústria (C)
setores_alvo = ['G', 'J', 'C'] 
analise_2022 = df_final_bloco[
    (df_final_bloco['TIME_PERIOD'] == 2022) & 
    (df_final_bloco['ACTIVITY'].isin(setores_alvo))
]

print(analise_2022[['REF_AREA', 'ACTIVITY', 'TIME_PERIOD', 'Produtividade_Trabalho', 'Prod_Projetada_Contrafactual', 'Choque_Estrutural_Percentual']])