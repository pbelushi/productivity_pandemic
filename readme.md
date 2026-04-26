# Choque de Produtividade na Pandemia: Uma Análise Cross-Country

Este repositório contém os dados e os scripts em Python desenvolvidos para expandir a pesquisa do *Working Paper* "O Enigma do Crescimento do PIB Brasileiro (2021-2025): Uma Análise Setorial da Produtividade do Trabalho". 

O objetivo deste projeto é investigar se a quebra estrutural e o salto de produtividade observados nos setores de Comércio e Serviços no Brasil (impulsionados pela digitalização forçada durante a pandemia de COVID-19) também ocorreram em economias desenvolvidas. Para isso, utilizamos dados harmonizados da OCDE (EUA, França, Alemanha e Itália).

## 🗂️ Estrutura do Repositório

* **`/data`**: Contém os dados brutos extraídos via API e as bases harmonizadas prontas para modelagem.
* **`/scripts`**: Códigos em Python para extração (ETL), processamento, modelagem contrafactual e visualização.
* **`/results`**: Tabelas finais contendo a quantificação do choque estrutural percentual por país e setor.
* **`/plots`**: Gráficos gerados para a análise visual da quebra estrutural.

## ⚙️ Fontes de Dados

Os dados internacionais foram extraídos da base **STAN (STructural ANalysis)** da **OCDE** via API (SDMX 3.0), focando nas seguintes variáveis:
* `B1G`: Gross Value Added (Valor Adicionado Bruto)
* `SAL`: Employees (Número de Empregados Salariados)

## 🚀 Como Replicar a Pesquisa

Para reproduzir os achados deste estudo, siga a ordem de execução dos scripts abaixo:

**1. Preparação do Ambiente:**

pip install -r requirements.txt

**2. Extração e Tratamento de Dados:**

python scripts/extract_oecd.py: Conecta à API da OCDE e extrai os dados brutos em formato .csv.

python scripts/process_oecd.py: Limpa os dados, estrutura a base (pivot table) e calcula a métrica principal: Produtividade do Trabalho (Valor Adicionado / Empregados).

**3. Modelagem Econômica:**

python scripts/model_counterfactual.py: Utiliza regressão linear nos dados de 2015-2019 para projetar a tendência contrafactual pré-pandemia e mede o choque estrutural efetivo a partir de 2020.

**4. Testes e Visualização:**

python scripts/test_comercio.py: Isola e testa os resultados específicos do Setor de Comércio (ISIC G).

python scripts/test_industria.py: Isola e testa os resultados específicos da Indústria de Transformação (ISIC C) para fins de controle e contraste empírico.

python scripts/plot_counterfactual.py: Gera os gráficos de séries temporais demonstrando o descolamento da produtividade real em relação à tendência histórica.

python scripts/format_spreadsheet.py: Formata os resultados finais numa planilha amigável (.xlsx) com padrões financeiros.

## 📊 Principais Descobertas

O modelo comprova internacionalmente a tese observada no Brasil: o setor de Comércio apresentou um forte choque estrutural positivo (ex: +19% nos EUA e +15% na França em 2022), enquanto a Indústria de Transformação permaneceu estagnada em relação à sua tendência histórica, evidenciando o impacto assimétrico da transformação digital global.

