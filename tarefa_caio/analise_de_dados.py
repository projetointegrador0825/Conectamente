import pandas as pd
from pysus.online_data import SIH

# 1. Definição das Regiões de Foco (Sul e DF) conforme o planejamento [2]
# PR = Paraná, SC = Santa Catarina, RS = Rio Grande do Sul, DF = Distrito Federal
estados_foco = ['PR', 'SC', 'RS', 'DF']

# Definindo o período (exemplo: ano de 2023)
ano_analise = 2023
meses_analise = [3-5] # Primeiro trimestre para teste rápido

# Lista para consolidar os dados de todos os estados filtrados
lista_dataframes = []

print("--- INICIANDO EXTRAÇÃO PARA SUL E DF ---")

for uf in estados_foco:
    try:
        print(f"Extraindo dados de internação (SIH) para: {uf}...")
        # Extração via PySUS [1]
        df_estado = SIH.download(states=uf, years=ano_analise, months=meses_analise)
        lista_dataframes.append(df_estado)
    except Exception as e:
        print(f"Erro ao baixar dados de {uf}: {e}")

# 2. Unificação dos dados em um único DataFrame do Pandas
if lista_dataframes:
    df_sul_df = pd.concat(lista_dataframes, ignore_index=True)
    
    # 3. Filtro Etário Estratégico (15 a 29 anos) [6]
    # No SIH, a coluna de idade geralmente é 'IDADE'
    if 'IDADE' in df_sul_df.columns:
        # Convertendo para numérico caso necessário
        df_sul_df['IDADE'] = pd.to_numeric(df_sul_df['IDADE'], errors='coerce')
        
        # Aplicando o filtro da Juventude (15-29 anos) [4, 6]
        df_final = df_sul_df[(df_sul_df['IDADE'] >= 15) & (df_sul_df['IDADE'] <= 29)]
        
        print("\n--- RESULTADO DA EXTRAÇÃO ---")
        print(f"Total de internações processadas: {len(df_final)}")
        
        # Separando pelos subgrupos planejados para o Dashboard [1, 6]
        print(f"15-19 anos: {len(df_final[df_final['IDADE'] <= 19])}")
        print(f"20-24 anos: {len(df_final[(df_final['IDADE'] >= 20) & (df_final['IDADE'] <= 24)])}")
        print(f"25-29 anos: {len(df_final[df_final['IDADE'] >= 25])}")
    else:
        print("Aviso: Coluna 'IDADE' não encontrada nos dados brutos do SIH.")
else:
    print("Nenhum dado foi extraído. Verifique sua conexão e os parâmetros.")
