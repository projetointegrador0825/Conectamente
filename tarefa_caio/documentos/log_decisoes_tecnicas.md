# Relatório de Decisões Técnicas e Engenharia de Dados

## 1. Escolha da Stack Tecnológica (Python vs Mobile)
A proposta inicial de viabilidade sugeria o uso de React Native. No entanto, durante a Tarefa 04, optou-se pela migração integral para **Python (Pandas & PySUS)**. 
**Justificativa:** Aplicativos móveis não possuem suporte nativo eficiente para o processamento e cross-referencing de microdados epidemiológicos pesados (arquivos .dbc e .xlsx extensos). O ecossistema Python permitiu a normalização de dados complexos que serão consumidos pelo Dashboard Streamlit.

## 2. Tratamento de Dependências e Erros de Ambiente
Durante a configuração do ambiente no Windows, enfrentamos falhas na instalação da biblioteca `pyreaddbc`, essencial para a leitura de dados do DataSUS.
**Solução:** Foi necessária a instalação e configuração das **Build Tools do Visual Studio (C++)** para permitir a compilação de bibliotecas legacy de baixo nível, garantindo a integridade da extração.

## 3. Arquitetura de Extração (Separação por Abas)
As tabelas da PNS 2019 são distribuídas em abas com hierarquias geográficas distintas. Para evitar poluição de dados e garantir a performance, os scripts foram separados:
- **Aba 1 (Idades):** Foco em subgrupos geracionais.
- **Aba 2 (Regiões e UF):** Foco no mapeamento geográfico detalhado.
Essa separação facilita a integração futura com as taxas de internação (Cinthia) e indicadores de severidade PHQ-9 (Ryan).

## 4. Normalização de Caminhos (Windows Pathing)
Devido ao uso de diretórios com espaços e caracteres especiais no Windows, implementamos o uso de **Raw Strings (`r""`)** em todos os scripts de ETL para prevenir erros de `SyntaxError` e `FileNotFoundError`.