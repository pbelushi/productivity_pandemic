import pandas as pd
import numpy as np
from scipy.stats import linregress
import os

print("1. A carregar os dados base...")
df = pd.read_csv('data/ocde_produtividade_modelo.csv')

# Definir os países que compõem cada bloco (baseado nos países disponíveis na sua extração da OCDE)
blocos = {
    'G7': ['USA', 'CAN', 'FRA', 'DEU', 'ITA', 'GBR', 'JPN'],
    'ZONA_EURO': ['AUT', 'BEL', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'NLD', 'PRT', 'SVK', 'SVN', 'ESP'],
    'PACIFICO': ['AUS', 'NZL', 'JPN', 'KOR', 'CHL'] # Principais economias da Bacia do Pacífico na OCDE
}

print("2. A agregar e treinar modelos para cada bloco...")
resultados_blocos = []

for nome_bloco, lista_paises in blocos.items():
    # Filtrar os países do bloco atual
    df_filtrado = df[df['REF_AREA'].isin(lista_paises)].copy()
    
    # Agregar: Somar VAB e Pessoal Ocupado
    df_bloco = df_filtrado.groupby(['TIME_PERIOD', 'ACTIVITY'])[['B1G', 'SAL']].sum().reset_index()
    
    # Calcular Produtividade Agregada
    df_bloco['Produtividade_Trabalho'] = df_bloco['B1G'] / df_bloco['SAL']
    df_bloco['REF_AREA'] = nome_bloco
    
    # Limpar valores inválidos
    df_bloco = df_bloco.replace([np.inf, -np.inf], np.nan).dropna(subset=['Produtividade_Trabalho'])
    
    # Treinar o contrafactual (2015-2019)
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
            
            resultados_blocos.append(df_temp)

# Unir todos os resultados num único DataFrame
df_final = pd.concat(resultados_blocos, ignore_index=True)

# Guardar os resultados
os.makedirs('results', exist_ok=True)
caminho_saida = 'results/analise_multi_blocos.csv'
df_final.to_csv(caminho_saida, index=False)

print(f"\nModelos treinados com sucesso! Guardado em: {caminho_saida}")

print("\n==================================================================")
print("COMPARAÇÃO DE BLOCOS: Choque de Produtividade no Comércio (G) em 2022")
print("==================================================================\n")

# Vamos comparar especificamente o setor do Comércio (G) entre os três blocos
analise_comercio = df_final[
    (df_final['TIME_PERIOD'] == 2022) & 
    (df_final['ACTIVITY'] == 'G')
]
print(analise_comercio[['REF_AREA', 'ACTIVITY', 'TIME_PERIOD', 'Produtividade_Trabalho', 'Choque_Estrutural_Percentual']])


print("\n==================================================================")
print("COMPARAÇÃO DE BLOCOS: Choque de Produtividade na Indústria (C) em 2022")
print("==================================================================\n")

# Comparação da Indústria de Transformação (C)
analise_industria = df_final[
    (df_final['TIME_PERIOD'] == 2022) & 
    (df_final['ACTIVITY'] == 'C')
]
print(analise_industria[['REF_AREA', 'ACTIVITY', 'TIME_PERIOD', 'Produtividade_Trabalho', 'Choque_Estrutural_Percentual']])