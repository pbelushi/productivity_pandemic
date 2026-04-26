import pandas as pd

print("A carregar os resultados do modelo contrafactual...")
df_final = pd.read_csv('results/analise_choque_pandemia.csv')

# Códigos habituais para a Indústria (C = Manufacturing / Indústria de Transformação)
setores_industria = ['C', 'B-E', 'B_E'] 

# Filtrar para os mesmos países em 2022
exemplo_industria = df_final[
    (df_final['REF_AREA'].isin(['FRA', 'DEU', 'ITA', 'USA'])) & 
    (df_final['ACTIVITY'].isin(setores_industria)) & 
    (df_final['TIME_PERIOD'] == 2022)
]

print("\n==================================================================")
print("TESTE 2: Choque Estrutural na Indústria (Transformação) em 2022")
print("==================================================================\n")

if not exemplo_industria.empty:
    print(exemplo_industria[['REF_AREA', 'ACTIVITY', 'TIME_PERIOD', 'Produtividade_Trabalho', 'Prod_Projetada_Contrafactual', 'Choque_Estrutural_Percentual']])
else:
    print("Códigos de Indústria ('C' ou 'B-E') não encontrados exatamente com este nome.")
    print("Aqui estão os códigos de setores disponíveis na sua base para que possamos ajustar:")
    print(df_final['ACTIVITY'].unique())