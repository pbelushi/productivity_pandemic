# Choque de Produtividade na Pandemia: Uma Análise Cross-Country

Este repositório contém os dados e os scripts em Python desenvolvidos para expandir a pesquisa do *Working Paper* "O Enigma do Crescimento do PIB Brasileiro (2021-2025): Uma Análise Setorial da Produtividade do Trabalho". 

O objetivo deste projeto é investigar se a quebra estrutural e o salto de produtividade observados nos setores de Comércio e Serviços no Brasil (impulsionados pela digitalização forçada durante a pandemia de COVID-19) também ocorreram em economias desenvolvidas. Para isso, utilizamos dados harmonizados da OCDE (EUA, França, Alemanha e Itália).

## 🗂️ Estrutura do Repositório

* **`/data`**: Contém os dados brutos extraídos via API e as bases harmonizadas.
* **`/scripts`**: 
    * `extract_oecd.py`: Extração via API SDMX da OCDE.
    * `process_oecd.py`: Limpeza e cálculo da Produtividade do Trabalho.
    * `model_counterfactual.py`: Modelagem de tendência pré-pandemia por país/setor.
    * `model_bloc_aggregation.py`: Agregação das 4 maiores economias (EUA, FRA, DEU, ITA) num bloco único.
    * `model_multi_blocos.py`: Análise comparativa entre G7, Zona do Euro e Zona do Pacífico.
    * `model_americas.py`: Foco específico nas economias da OCDE no continente americano.
    * `model_servicos_blocos.py`: Decomposição do choque nos serviços de Informação (J) e Finanças (K).
    * `model_servicos_agregados.py`: Análise do macro-setor de serviços (H-U), excluindo o comércio.
    * `plot_counterfactual.py`: Geração de gráficos de quebra estrutural.
    * `format_spreadsheet.py`: Exportação dos resultados em formato Excel profissional.
* **`/results`**: Tabelas finais de choques percentuais e planilhas formatadas.
* **`/plots`**: Visualizações das "bocas de jacaré" (descolamento da produtividade).

## ⚙️ Fontes de Dados

Os dados internacionais foram extraídos da base **STAN (STructural ANalysis)** da **OCDE** via API (SDMX 3.0), focando nas seguintes variáveis:
* `B1G`: Gross Value Added (Valor Adicionado Bruto)
* `SAL`: Employees (Número de Empregados Salariados)

## 🚀 Como Replicar a Pesquisa

Para reproduzir os achados deste estudo, siga a ordem de execução dos scripts abaixo:

**1. Preparação do Ambiente:**

pip install -r requirements.txt

**2. Execução do Pipeline:**

1. Execute python scripts/extract_oecd.py para baixar os dados.

2. Execute python scripts/process_oecd.py para gerar a base produtividade.

3. Para análises de blocos (o coração da expansão internacional), execute os scripts iniciados por model_....

## 📊 Principais Descobertas

A expansão internacional validou a tese brasileira:

* **Comércio (Setor G):** Apresentou um choque estrutural positivo global, com destaque para o bloco das Américas (+20,3%) e G7 (+15%).

* **Tecnologia (Setor J):** Registou choque negativo ou estagnação em todos os blocos, evidenciando um inchaço nas contratações (labor hoarding) que superou os ganhos de produtividade.

* **Finanças (Setor K):** Foi o grande vencedor da digitalização nos serviços corporativos, com saltos de produtividade superiores a 12% no G7.

* **Indústria (Setor C):** Demonstrou estagnação ou crescimento limitado devido aos gargalos logísticos globais.

