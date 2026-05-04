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




Tarefa quatro: Caio Gabriel

Saúde Mental da Juventude (15-29 anos)

Objetivo: Transformar dados epidemiológicos em informações estratégicas para políticas públicas de saúde mental, focando em transtornos de humor, depressão e ansiedade no Brasil.
Eixos de Análise:

Idade: Divisão em três subgrupos (15-19, 20-24 e 25-29 anos), com pico de gravidade na fase adulta jovem.

Gênero: Homens (maior índice de internação por substâncias); Mulheres (maior busca por atenção básica e transtornos de humor).

Geografia: Foco na Região Sul e DF, que superam as médias nacionais de internação.

Interseccionalidade: Vulnerabilidade crítica de jovens indígenas (suicídio) e negros (acesso ao serviço).

Base de Dados: Cruzamento de dados do DataSUS (SIH, SIM e SISAB) para internações e óbitos, com a PNS/IBGE para autodeclarações e diagnósticos.

Fontes:

http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sia/cnv/qabr.def

https://datasus.saude.gov.br/informacoes-de-saude-tabnet/

https://pysus.readthedocs.io/en/latest/

https://pysus.readthedocs.io/en/latest/databases/CNES.html




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




