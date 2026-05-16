# Projeto-integrador-grupo26

# Tema do projeto: Mapeamento da Saúde Mental na Juventude

Integrantes:

* Caio Gabriel Lemos Neris
* Cinthia Pimentel da Silva
* Livia Castro Alves da Silva
* Ryan Alves de Araujo


# Objetivo: 

A saúde mental no Brasil enfrenta um cenário crítico, especialmente entre os jovens Dados da OMS mostram que o país lidera os rankings de ansiedade e depressão na América Latina, e essa população é a mais afetada. O objetivo é analisar a prevalência de transtornos mentais (ansiedade, depressão e estresse) em jovens de 15 a 29 anos para identificar quais subgrupos são mais vulneráveis.


# Planejamento das tarefas ---------------------------------------------

Tarefa um: Livia Castro

Transtornos como depressão, ansiedade, estresse e bipolaridade não afetam apenas o indivíduo, mas toda a estrutura social e acadêmica de um país. Este estudo dedica-se a verificar os índices dessas condições no Brasil, utilizando como base os dados oficiais do Portal de Microdados do IBGE (PNS) e as métricas de saúde mental da OPAS. Além disso, o trabalho explora a vulnerabilidade em contextos educacionais, utilizando técnicas de análise de dados aplicadas a perfis estudantis. O objetivo é transformar números e estatísticas em informações relevantes que auxiliem na compreensão da prevalência dessas doenças.

Tarefa dois: Ryan Alves

Objetivo: coletar dados, em meta-análise, de estudos de prevalência de transtornos como depressão e ansiedade na população brasileira, tratá-los e apresentá-los por meio de ferramentas de análise.
Idades em amostragens: como o foco é na população jovem brasileira, o recorte dos dados se dará entre idivíduos de idades de 15 a 29 anos.
Para fundamentar minha meta-análise sobre a prevalência de transtornos mentais na população jovem brasileira (15 a 29 anos), extrairei deste artigo os dados comparativos da Pesquisa Nacional de Saúde (PNS) de 2013 e 2019, focando especificamente no recorte de adultos jovens (18 a 24 anos) que apresentou o crescimento mais acentuado de depressão no período, saltando de 3,7% para 10,3%. Coletarei as estatísticas obtidas via questionário PHQ-9 para alimentar minhas ferramentas de análise, correlacionando o aumento de 178,4% nessa faixa etária com variáveis como a falta de ocupação profissional, o ambiente urbano e comportamentos de risco (sedentarismo e tabagismo), permitindo uma visão precisa de como a recessão econômica impactou a saúde mental desse grupo demográfico específico.


Tarefa três: Cinthia Pimentel

Segundo o Informe II: Saúde Mental, segunda publicação do Ciclo de Informes sobre a situação da juventude brasileira, produzido por pesquisadores da Fiocruz.
A população jovem é a que mais sofre internações relacionadas a problemas de saúde mental no Brasil, mas também é a que menos busca atendimento na Atenção Primária
à Saúde (APS).Entre o jovens de 20 a 29 anos, a taxa de internação por transtornos mentais é mais alta do que a da população geral, em especial entre jovens de 25
a 29 anos, para os quais a taxa é de 719,7 casos para cada 100 mil habitantes.O objetivo é transformar esses dados em informações relevantes e apresentar de forma 
clara destacando a faixa etária mais afetada.




Tarefa quatro: Caio Gabriel

Saúde Mental da Juventude (15-29 anos)

Objetivo: Transformar dados epidemiológicos em informações estratégicas para políticas públicas de saúde mental, focando em transtornos de humor, depressão e ansiedade no Brasil.
Eixos de Análise:

Idade: Divisão em três subgrupos (15-19, 20-24 e 25-29 anos), com pico de gravidade na fase adulta jovem.

Gênero: Homens (maior índice de internação por substâncias); Mulheres (maior busca por atenção básica e transtornos de humor).

Geografia: Foco na Região Sul e DF, que superam as médias nacionais de internação.

Interseccionalidade: Vulnerabilidade crítica de jovens indígenas (suicídio) e negros (acesso ao serviço).

Base de Dados: Cruzamento de dados do DataSUS (SIH, SIM e SISAB) para internações e óbitos, com a PNS/IBGE para autodeclarações e diagnósticos.



------------------------------------------------------------------------------

# Ideia inicial do dashboard:

1 - Tipos de transtorno (porcentagem):

- Definir quais transtornos vamos colocar baseado em dados do SUS/CAPS [fontes acima]

2 - Quantidade de pessoas afetadas no Brasil:

• dados na OMS/SUS/CAPS

• Verificar por regiões (Norte, sul, suldestes, nordeste e cetro-oeste)

3 - Faixa Etarias mais atingidas:

• Faixa etária do projeto de 15 a 29

4 - Taxa de atendimento:

• Atendimento em CAPS / acesso a tratamento

Tarefa,Status,Descrição
Extração PNS 2019,✅ Concluído,Scripts de automação para Tabelas 12.1 a 12.8.
Tratamento DataSUS,🚧 Em Andamento,Conversão de arquivos .dbc para análise.

-
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)


---------------------------------------------------

## 👥 Equipe e Divisão de Linhas de Pesquisa

O sucesso da consolidação da camada de dados do **Projeto ConectaMente** é o resultado da integração de diferentes frentes de estudo e análise epidemiológica dos integrantes do **Grupo 26**:

*   **Livia Castro Alves da Silva (Tarefa 01):** Análise de base e contextualização dos índices oficiais de depressão, ansiedade e estresse a partir do Portal de Microdados do IBGE (PNS) e métricas da OPAS, com foco na vulnerabilidade de perfis estudantis e contextos educacionais.
*   **Ryan Alves de Araujo (Tarefa 02):** Condução da meta-análise de prevalência de transtornos. Responsável pelo cruzamento histórico dos dados da PNS (2013 vs. 2019) utilizando o questionário PHQ-9 para correlacionar o salto de 178,4% na depressão de adultos jovens com variáveis socioeconômicas e comportamentais.
*   **Cinthia Pimentel da Silva (Tarefa 03):** Análise do fluxo de ocupação da rede de saúde, mapeando as taxas de internação hospitalar na juventude com base nos Informes de Saúde Mental da Fiocruz, evidenciando o pico crítico de internações na faixa dos 25 a 29 anos (719,7 casos por 100 mil hab.).
*   **Caio Gabriel Lemos Neris (Tarefa 04):** Engenharia de dados, ETL e modelagem dimensional. Responsável pelo desenvolvimento dos pipelines em Python para extração de arquivos `.dbc` (DataSUS/Tabnet) e `.xlsx` (IBGE), unificação dos recortes geográficos e estruturação da base analítica final.

---

## 🗄️ Armazenamento e Disponibilidade dos Dados (BigQuery)

Para garantir escalabilidade, alta performance nas consultas do dashboard (Streamlit) e permitir que os cruzamentos entre a **PNS 2019**, os dados de internação da **Fiocruz/DataSUS** e as métricas do **PHQ-9** ocorressem sem gargalos, toda a camada de dados limpa e normalizada foi integrada ao ecossistema de dados do Google Cloud.

A base de dados oficial e consolidada do projeto está publicamente disponível e hospedada no **Google BigQuery**. Você pode acessar o repositório de dados, visualizar o esquema das tabelas e executar queries estruturadas diretamente pelo link abaixo:

🔗 [**Acessar Banco de Dados ConectaMente no Google BigQuery**](https://console.cloud.google.com/bigquery?project=conectamente-grupo26)

### 📊 Estrutura das Tabelas Disponíveis no Data Lake:
*   `conectamente-grupo26.pns_2019.consolidado_regioes`: Indicadores de autodeclaração, tristeza e solidão divididos pelas Grandes Regiões.
*   `conectamente-grupo26.pns_2019.consolidado_estados`: Dados refinados por Unidade da Federação (UF), com foco analítico na Região Sul e Distrito Federal.
*   `conectamente-grupo26.pns_2019.consolidado_capitais`: Granularidade a nível municipal/capitais para cruzamento com a cobertura local dos CAPS.
*   `conectamente-grupo26.meta_analise.prevalencia_phq9`: Dados de severidade e evolução temporal da depressão na faixa de 15 a 29 anos.
*   `conectamente-grupo26.fiocruz.taxas_internacao`: Histórico de morbidade e internações hospitalares por transtornos mentais e uso de substâncias.

---

## 🚀 Próximos Passos e Cronograma Atualizado

Com a arquitetura de dados finalizada e os dados devidamente povoados no BigQuery, o projeto avança para a sua última etapa de engenharia e design.

| Tarefa / Linha de Entrega | Status | Descrição |
| :--- | :--- | :--- |
| Extração e Normalização PNS 2019 | ✅ Concluído | Scripts de automação para Tabelas 12 executados com sucesso. |
| Tratamento e Carga DataSUS (SIH/SIM) | ✅ Concluído | Dados de internação e óbitos integrados à base. |
| Modelagem e Carga no BigQuery | ✅ Concluído | Data Lake estruturado e pronto para consumo. |
| **Integração e Interface Streamlit** | ✅ Concluído | Conexão do BigQuery ao dashboard interativo em Python. |

## 🚀 Alterações feitas ao longo do projeto:

Devido a falta de informações de alguns dados, optamos por uma nova linha de pesquisa. Dessa forma a faixa etária dos jovens estudados nesse projeto foram entre 13-17 anos.
Foi utilizado a PNS 2019 como base de dados final.

---
🛠️ **Tecnologias Utilizadas na Camada de Dados:**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![Google BigQuery](https://img.shields.io/badge/Google%20BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

## LINK FINAL DO PROJETO:
* https://projeto-integrador-grupo26-g8zzyr98qhfptz3cb7shhu.streamlit.app




