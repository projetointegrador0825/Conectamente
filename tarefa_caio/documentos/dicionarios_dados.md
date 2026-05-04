# Dicionário de Dados - Consolidação PNS 2019 (Série 12)

Este documento descreve as colunas presentes nos arquivos consolidados resultantes do processo de ETL das tabelas de saúde mental da Pesquisa Nacional de Saúde (PNS 2019).

## Estrutura da Tabela

| Coluna | Descrição | Tipo |
| :--- | :--- | :--- |
| **TABELA_ORIGEM** | Identificador da tabela original no IBGE (ex: 12.1.1 para Faixa Etária, 12.1.2 para Regiões/UF). | Texto |
| **NOME_METRICA** | Nome simplificado do indicador de saúde mental (ex: TRISTEZA, SOZINHO, PENSAMENTO_MORTE). | Texto |
| **Faixa_Etaria** | Recorte geracional analisado (13-17 anos, 13-15 anos, 16-17 anos). *Apenas Aba 1*. | Texto |
| **Regiao** | Grande Região do Brasil (Norte, Nordeste, Sudeste, Sul, Centro-Oeste) ou Brasil. | Texto |
| **Unidade_Federacao** | Nome do estado (UF) correspondente. *Apenas Aba 2*. | Texto |
| **rc** | Coeficiente de variação ou prevalência estimada em valores percentuais (%). | Numérico |
| **Limite_inferior** | Valor mínimo do Intervalo de Confiança (IC) de 95%. | Numérico |
| **Limite_superior** | Valor máximo do Intervalo de Confiança (IC) de 95%. | Numérico |
| **rc_Homem/Mulher** | Prevalência segmentada por gênero. | Numérico |
| **rc_Publica/Privada**| Prevalência segmentada por tipo de rede de ensino. | Numérico |

## Notas Técnicas
- Todos os valores percentuais foram arredondados para duas casas decimais para garantir precisão analítica.
- Valores nulos (`None`) indicam que a segmentação não estava disponível para aquele recorte geográfico específico.