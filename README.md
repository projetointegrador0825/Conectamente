# Projeto-integrador-grupo26

# Tema do projeto: Mapeamento da Saúde Mental na Juventude

Integrantes:

Caio Gabriel Lemos Neris

Cinthia Pimentel da Silva

Livia Castro Alves da Silva

Ryan Alves de Araujo


# Objetivo: 

A saúde mental no Brasil enfrenta um cenário crítico, especialmente entre os jovens Dados da OMS mostram que o país lidera os rankings de ansiedade e depressão na América Latina, e essa população é a mais afetada. O objetivo é analisar a prevalência de transtornos mentais (ansiedade, depressão e estresse) em jovens de 15 a 29 anos para identificar quais subgrupos são mais vulneráveis.


# Planejamento das tarefas:

Tarefa um: Livia Castro

Transtornos como depressão, ansiedade, estresse e bipolaridade não afetam apenas o indivíduo, mas toda a estrutura social e acadêmica de um país. Este estudo dedica-se a verificar os índices dessas condições no Brasil, utilizando como base os dados oficiais do Portal de Microdados do IBGE (PNS) e as métricas de saúde mental da OPAS. Além disso, o trabalho explora a vulnerabilidade em contextos educacionais, utilizando técnicas de análise de dados aplicadas a perfis estudantis. O objetivo é transformar números e estatísticas em informações relevantes que auxiliem na compreensão da prevalência dessas doenças.

 PNS (Pesquisa Nacional de Saúde) Portal de Microdados https://www.ibge.gov.br/estatisticas/sociais/saude/9160-pesquisa-nacional-de-saude.html?=&t=microdados
 
 Saúde Mental de Estudantes - EDAhttps://www.kaggle.com/code/fecodelipe/sa-de-mental-de-estudantes-eda
 
 OPAS Saúde mentalhttps://www.paho.org/pt/topicos/saude-mental
 


Tarefa dois: Ryan Alves

Objetivo: coletar dados, em meta-análise, de estudos de prevalência de transtornos como depressão e ansiedade na população brasileira, tratá-los e apresentá-los por meio de ferramentas de análise.

Idades em amostragens: como o foco é na população jovem brasileira, o recorte dos dados se dará entre idivíduos de idades de 15 a 29 anos.

Links:

Para fundamentar minha meta-análise sobre a prevalência de transtornos mentais na população jovem brasileira (15 a 29 anos), extrairei deste artigo os dados comparativos da Pesquisa Nacional de Saúde (PNS) de 2013 e 2019, focando especificamente no recorte de adultos jovens (18 a 24 anos) que apresentou o crescimento mais acentuado de depressão no período, saltando de 3,7% para 10,3%. Coletarei as estatísticas obtidas via questionário PHQ-9 para alimentar minhas ferramentas de análise, correlacionando o aumento de 178,4% nessa faixa etária com variáveis como a falta de ocupação profissional, o ambiente urbano e comportamentos de risco (sedentarismo e tabagismo), permitindo uma visão precisa de como a recessão econômica impactou a saúde mental desse grupo demográfico específico.

https://www.scielo.br/j/csp/a/XBmqFfsR6wbLzMwrKgKG5sp/?format=html&lang=en

Outros links:

https://data.humdata.org/dataset/who-data-for-brazil/resource/abb9fb11-66a5-42ed-a5d7-e9dd6a3ceca8

https://link.springer.com/article/10.1186/s13104-023-06323-0

https://www.scielo.br/j/cadsc/a/B9rPYyB8NxTp8dghq4QnGnH/?format=html&lang=pt



Tarefa três: Cinthia Pimentel

Segundo o Informe II: Saúde Mental, segunda publicação do Ciclo de Informes sobre a situação da juventude brasileira, produzido por pesquisadores da Fiocruz.
A população jovem é a que mais sofre internações relacionadas a problemas de saúde mental no Brasil, mas também é a que menos busca atendimento na Atenção Primária
à Saúde (APS).Entre o jovens de 20 a 29 anos, a taxa de internação por transtornos mentais é mais alta do que a da população geral, em especial entre jovens de 25
a 29 anos, para os quais a taxa é de 719,7 casos para cada 100 mil habitantes.O objetivo é transformar esses dados em informações relevantes e apresentar de forma 
clara destacando a faixa etária mais afetada.

https://agencia.fiocruz.br/sites/agencia.fiocruz.br/files/Informe%20II%20-%20Sa%C3%BAde%20Mental%20-
%20Informes%20sobre%20situa%C3%A7%C3%A3o%20de%20sa%C3%BAde%20da%20juventude%20brasileira%20n2_2025%20(2).pdf




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


> **Status da Task**: ✅ Camada de Dados Consolidada | 🚧 Próxima Fase: Integração Streamlit

Tarefa,Status,Descrição
Extração PNS 2019,✅ Concluído,Scripts de automação para Tabelas 12.1 a 12.8.
Tratamento DataSUS,🚧 Em Andamento,Conversão de arquivos .dbc para análise.

-
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)




