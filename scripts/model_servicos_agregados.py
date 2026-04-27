import pandas as pd
import numpy as np
from scipy.stats import linregress

print("1. A carregar os dados base...")
df = pd.read_csv('data/ocde_produtividade_modelo.csv')

# Os 4 blocos geopolíticos
blocos = {
    'G7': ['USA', 'CAN', 'FRA', 'DEU', 'ITA', 'GBR', 'JPN'],
    'ZONA_EURO': ['AUT', 'BEL', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'NLD', 'PRT', 'SVK', 'SVN', 'ESP'],
    'PACIFICO': ['AUS', 'NZL', 'JPN', 'KOR', 'CHL'],
    'AMERICAS_OCDE': ['USA', 'CAN', 'MEX', 'CHL', 'COL', 'CRI']
}

# 2. Definir o Macro-setor: Todo o Terciário (H até U), EXCLUINDO o Comércio (G)
# Utilizamos apenas letras individuais para garantir que não há dupla contagem
setores_servicos = ['H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']

print(f"2. A agregar o macro-setor de Serviços (Letras H até U) para os 4 blocos...")
resultados_blocos = []

for nome_bloco, lista_paises in blocos.items():
    # Filtrar apenas os países do bloco E apenas os setores de serviços definidos
    df_filtrado = df[
        (df['REF_AREA'].isin(lista_paises)) & 
        (df['ACTIVITY'].isin(setores_servicos))
    ].copy()
    
    # AGREGAR TUDO: Somar VAB e Pessoal Ocupado de todos estes setores para cada ano
    df_bloco = df_filtrado.groupby('TIME_PERIOD')[['B1G', 'SAL']].sum().reset_index()
    
    # Calcular Produtividade do Macro-setor
    df_bloco['Produtividade_Trabalho'] = df_bloco['B1G'] / df_bloco['SAL']
    df_bloco['REF_AREA'] = nome_bloco
    df_bloco['ACTIVITY'] = 'SERVICOS_EXC_COMERCIO' # Criamos o nosso próprio rótulo
    
    # Limpar valores inválidos
    df_bloco = df_bloco.replace([np.inf, -np.inf], np.nan).dropna(subset=['Produtividade_Trabalho'])
    
    # Treinar o modelo contrafactual (2015-2019)
    df_pre = df_bloco[df_bloco['TIME_PERIOD'] <= 2019].copy()
    
    if len(df_pre) >= 3:
        x_pre = df_pre['TIME_PERIOD'].values
        y_pre = df_pre['Produtividade_Trabalho'].values
        
        slope, intercept, r_value, p_value, std_err = linregress(x_pre, y_pre)
        
        df_temp = df_bloco.copy()
        anos_totais = df_temp['TIME_PERIOD'].values
        df_temp['Prod_Projetada_Contrafactual'] = (slope * anos_totais) + intercept
        df_temp['Choque_Estrutural_Percentual'] = ((df_temp['Produtividade_Trabalho'] / df_temp['Prod_Projetada_Contrafactual']) - 1) * 100
        
        resultados_blocos.append(df_temp)

df_final = pd.concat(resultados_blocos, ignore_index=True)

print("\n==================================================================")
print("MACRO-SETOR: SERVIÇOS (Exceto Comércio) - Choque Agregado em 2022")
print("==================================================================\n")

analise_servicos = df_final[df_final['TIME_PERIOD'] == 2022]
print(analise_servicos[['REF_AREA', 'ACTIVITY', 'TIME_PERIOD', 'Produtividade_Trabalho', 'Choque_Estrutural_Percentual']])