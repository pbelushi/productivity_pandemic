import pandas as pd

print("A carregar os resultados do modelo contrafactual...")
df_final = pd.read_csv('results/analise_choque_pandemia.csv')

# Códigos habituais para o Comércio na base da OCDE
setores_comercio = ['G', 'G-I', 'G_I'] 

# Filtrar para os mesmos países em 2022
exemplo_comercio = df_final[
    (df_final['REF_AREA'].isin(['FRA', 'DEU', 'ITA', 'USA'])) & 
    (df_final['ACTIVITY'].isin(setores_comercio)) & 
    (df_final['TIME_PERIOD'] == 2022)
]

print("\n==================================================================")
print("TESTE 1: Choque Estrutural no Setor do Comércio em 2022")
print("==================================================================\n")

if not exemplo_comercio.empty:
    print(exemplo_comercio[['REF_AREA', 'ACTIVITY', 'TIME_PERIOD', 'Produtividade_Trabalho', 'Prod_Projetada_Contrafactual', 'Choque_Estrutural_Percentual']])
else:
    print("Códigos 'G' ou 'G-I' não encontrados exatamente com este nome.")
    print("Aqui estão os códigos de setores disponíveis na sua base para que possamos ajustar:")
    print(df_final['ACTIVITY'].unique())