import pandas as pd
import requests
import io
import os

# O seu URL exato
url_ocde = "https://sdmx.oecd.org/public/rest/data/OECD.STI.PIE,DSD_STAN@DF_STAN_2025,1.0/A.AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA..B1G+SAL..?startPeriod=2015&dimensionAtObservation=AllDimensions&format=csv"

print("A estabelecer ligação à nova API da OCDE...")

try:
    # 1. Definimos um 'User-Agent' para simular que somos um navegador web humano
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 2. Fazemos o pedido HTTPS usando a biblioteca requests
    resposta = requests.get(url_ocde, headers=headers)
    
    # Verificamos se o pedido foi bem-sucedido
    resposta.raise_for_status() 
    
    # 3. Lemos o texto da resposta com o pandas
    df_oecd = pd.read_csv(io.StringIO(resposta.text))
    
    print("\nDados extraídos com sucesso!")
    print(f"Dimensões do dataset: {df_oecd.shape}")
    
    print("\nA guardar os dados na pasta 'data'...")
    
    # 4. Garantir que a pasta 'data' existe (cria se não existir)
    os.makedirs('data', exist_ok=True)
    
    # 5. Guardar o ficheiro em formato CSV
    caminho_ficheiro = 'data/ocde_stan_raw.csv'
    df_oecd.to_csv(caminho_ficheiro, index=False)
    
    print(f"Sucesso! Ficheiro guardado fisicamente em: {caminho_ficheiro}")

except requests.exceptions.HTTPError as err:
    print(f"\nErro HTTP: {err}")
except Exception as e:
    print(f"\nErro geral ao descarregar ou processar os dados: {e}")