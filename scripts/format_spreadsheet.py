import pandas as pd
import os

print("A carregar os resultados do modelo...")
# 1. Carregar os dados que o modelo gerou
df = pd.read_csv('results/analise_choque_pandemia.csv')

# 2. Renomear as colunas para espelhar a estrutura da sua planilha original
df = df.rename(columns={
    'REF_AREA': 'País',
    'ACTIVITY': 'Setor (ISIC)',
    'TIME_PERIOD': 'Ano',
    'B1G': 'Valor adicionado',
    'SAL': 'Pessoal ocupado',
    'Produtividade_Trabalho': 'Relação VA/PO (Efetiva)',
    'Prod_Projetada_Contrafactual': 'Relação VA/PO (Projetada)',
    'Choque_Estrutural_Percentual': 'Variação produtividade (Choque %)'
})

# 3. Funções de formatação para o padrão brasileiro (R$ / US$, pontos e vírgulas)
def formata_moeda(valor):
    if pd.isna(valor): return ""
    # Formata com 2 casas decimais, troca vírgula por ponto (milhares) e ponto por vírgula (decimais)
    return f"US$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formata_numero(valor):
    if pd.isna(valor): return ""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formata_perc(valor):
    if pd.isna(valor): return ""
    return f"{valor:,.2f}%".replace(".", ",")

print("A aplicar as formatações financeiras e percentuais...")

# 4. Aplicar a formatação nas respetivas colunas
df['Valor adicionado'] = df['Valor adicionado'].apply(formata_moeda)
df['Relação VA/PO (Efetiva)'] = df['Relação VA/PO (Efetiva)'].apply(formata_numero)
df['Relação VA/PO (Projetada)'] = df['Relação VA/PO (Projetada)'].apply(formata_numero)
df['Variação produtividade (Choque %)'] = df['Variação produtividade (Choque %)'].apply(formata_perc)

# 5. Ordenar as colunas de forma lógica
colunas_finais = [
    'Ano', 'País', 'Setor (ISIC)', 'Valor adicionado', 'Pessoal ocupado', 
    'Relação VA/PO (Efetiva)', 'Relação VA/PO (Projetada)', 'Variação produtividade (Choque %)'
]
df_final = df[colunas_finais]

# Vamos focar apenas nos anos da sua pesquisa (por exemplo, 2015 em diante)
df_final = df_final.sort_values(by=['País', 'Setor (ISIC)', 'Ano'])

# 6. Guardar como ficheiro Excel (.xlsx)
# Caso não tenha a biblioteca openpyxl instalada, o terminal avisará (basta correr: pip install openpyxl)
caminho_saida = 'results/Produtividade_OCDE_Planilha.xlsx'
df_final.to_excel(caminho_saida, index=False)

print(f"\nSucesso! Planilha formatada e guardada em: {caminho_saida}")