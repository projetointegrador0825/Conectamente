import pandas as pd

# --- 1. LIMPANDO O KAGGLE ---
print("Limpando dados do Kaggle...")
df_estudantes = pd.read_csv('tarefa_livia/dados/Student Mental Health.csv')
traducao = {
    'Do you have Depression?': 'Depressao',
    'Do you have Anxiety?': 'Ansiedade',
    'Do you have Panic attack?': 'Ataque_Panico'
}
df_kaggle = df_estudantes.rename(columns=traducao)[['Depressao', 'Ansiedade', 'Ataque_Panico']]
df_kaggle['Origem'] = 'Mundo (Kaggle)' # Adicionamos uma etiqueta para saber de onde veio

# --- 2. LIMPANDO O BRASIL (Excel) ---
print("Limpando dados do Brasil...")
try:
    # Lendo o Excel (xlsx)
    df_br = pd.read_excel('tarefa_livia/dados/saude_mental_brasil_estudantes.xlsx')
    
    # IMPORTANTE: Se os nomes das colunas no seu Excel forem diferentes, 
    # o código vai avisar no erro abaixo.
    df_br_limpo = df_br[['Depressao', 'Ansiedade', 'Ataque_Panico']].copy()
    df_br_limpo['Origem'] = 'Brasil (IBGE/Pesquisa)'
except Exception as e:
    print(f"Aviso: Não consegui ler o Excel do Brasil. Erro: {e}")
    df_br_limpo = pd.DataFrame()

# --- 3. UNIFICANDO ---
df_final = pd.concat([df_kaggle, df_br_limpo], ignore_index=True)

# Salva o arquivo final que o Dashboard vai usar
df_final.to_csv('tarefa_livia/dados/dados_unificados.csv', index=False)
print("✅ Sucesso! Arquivo 'dados_unificados.csv' criado.")