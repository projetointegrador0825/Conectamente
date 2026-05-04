# 🧠 Projeto ConectaMente: Inteligência em Saúde Mental

O **ConectaMente** é uma plataforma analítica desenvolvida para transformar microdados epidemiológicos em inteligência estratégica, focando no cenário crítico da saúde mental infantojuvenil no Brasil.

---

## 🛠️ Engenharia de Dados e ETL (Tarefa 04 - Caio Lemos)

Nesta etapa, a arquitetura do projeto evoluiu de uma proposta mobile inicial para uma infraestrutura robusta de análise de dados. O foco foi a extração, limpeza e normalização de microdados da **PNS 2019** para alimentar o ecossistema analítico.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google_BigQuery-4285F4?style=for-the-badge&logo=google-bigquery&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

### 📊 Dados Analisados
Trabalhamos com a **Série 12 da PNS 2019**, focada em indicadores de saúde mental e estilo de vida:
*   **Recorte Geracional**: Jovens de 15 a 29 anos, subdivididos para identificar transições de risco.
*   **Indicadores**: Sentimentos de tristeza, solidão e padrões de diagnóstico.
*   **Granularidade**: Grandes Regiões, Unidades da Federação (UF) e Capitais.

### 🏗️ O que foi feito
1.  **Migração Tecnológica**: Transição estratégica para o ecossistema **Python** para permitir o processamento de arquivos `.dbc` (DataSUS) e `.xlsx` (IBGE).
2.  **Pipeline de ETL**: Desenvolvimento de scripts especializados para automação da consolidação de dados por hierarquia geográfica (Regiões, Estados e Capitais).
3.  **Normalização**: Estruturação de uma base de dados única, pronta para o cruzamento com indicadores de severidade **PHQ-9** e taxas de internação.

---

## 🖥️ Design de Inteligência do Dashboard (Concept)

O dashboard está sendo projetado para oferecer uma visão profunda sobre a saúde mental, dividida em quatro módulos fundamentais:

### 1. Panorama de Morbidade e Autodeclaração
*   **Visualização**: Gráficos de rosca e barras horizontais.
*   **Métrica**: Distribuição percentual de transtornos de humor e indicadores de sofrimento psíquico extraídos da PNS 2019.

### 2. Geolocalização e Áreas de Risco Crítico
*   **Visualização**: Mapas de calor interativos (*Choropleth Maps*).
*   **Foco Regional**: Análise comparativa nacional com destaque prioritário para a **Região Sul e Distrito Federal**.

### 3. Recorte Geracional e Interseccionalidade
*   **Visualização**: Histogramas e pirâmides de dados segmentadas.
*   **Público-Alvo**: Foco estrito na faixa de **15 a 29 anos**, observando padrões distintos por gênero e etnia.

### 4. Eficiência da Rede de Apoio (CAPS)
*   **Visualização**: Gráficos de tendência e KPIs de performance.
*   **Análise**: Correlação entre os níveis de severidade (**PHQ-9**) e a taxa de cobertura efetiva nos Centros de Atenção Psicossocial.

---

## 📂 Documentação de Engenharia (Caio Lemos)
Para detalhes sobre o processo de desenvolvimento e decisões técnicas, acesse:
*   [📄 Dicionário de Dados](./tarefa_caio/documentos/dicionario_dados.md)
*   [📑 Log de Decisões Técnicas](./tarefa_caio/documentos/log_decisoes_tecnicas.md)
*   [📓 Engineering Log (Daily)](./tarefa_caio/Daily.txt)

> 04/05/2026: **Status da Task**: ✅ Camada de Dados Consolidada | 🚧 Próxima Fase: Integração Streamlit


## 🛠️ Engenharia de Dados e ETL (Tarefa 04 - Caio Lemos)

Nesta etapa, a arquitetura do projeto evoluiu de uma proposta mobile inicial para uma infraestrutura robusta de análise de dados. O foco foi a extração e normalização de microdados da **PNS 2019 (Pesquisa Nacional de Saúde)** para alimentar o dashboard de saúde mental.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![BigQuery](https://img.shields.io/badge/Google_BigQuery-4285F4?style=for-the-badge&logo=google-bigquery&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

### 📊 Dados Analisados
Estamos trabalhando com a **Série 12 da PNS 2019**, focada em indicadores de saúde mental e estilo de vida.
*   **Recorte Geracional:** Jovens de 15 a 29 anos.
*   **Indicadores:** Sentimentos de tristeza, solidão, ideação suicida e padrões de diagnóstico.
*   **Granularidade:** Grandes Regiões, Unidades da Federação (UF) e Capitais.

### 🏗️ O que foi feito
1.  **Migração Tecnológica:** Transição estratégica para o ecossistema Python para permitir o processamento de arquivos `.dbc` (DataSUS) e `.xlsx` (IBGE).
2.  **Pipeline de ETL:** Desenvolvimento de scripts especializados para automação da limpeza e consolidação de dados:
    *   `consolidar_tabelas_12_regioes.py`
    *   `consolidar_tabelas_12_states.py`
    *   `consolidar_tabelas_12_capitais.py`
3.  **Normalização:** Estruturação de uma base de dados única, facilitando o cruzamento com as metas de meta-análise e taxas de internação.

### 📂 Documentação Técnica
Para detalhes profundos sobre a engenharia desta tarefa, acesse:
*   [📄 Dicionário de Dados](./tarefa_caio/documentos/dicionario_dados.md)
*   [📑 Log de Decisões Técnicas](./tarefa_caio/documentos/log_decisoes_tecnicas.md)
*   [📓 Engineering Log (Daily)](./tarefa_caio/Daily.txt)

> **Status da Task:** ✅ Camada de Dados Consolidada | 🚧 Próxima Fase: Integração Streamlit