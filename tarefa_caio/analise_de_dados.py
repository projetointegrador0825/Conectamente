import pandas as pd

# Carregar o arquivo CSV baixado no Kaggle
df = pd.read_csv("Student Mental Health.csv")

# Para ver o resultado no terminal:
# print(df.head())

# Verificar os valores mínimos, máximos e a média de idade
print(df['Age'].describe())

print(df['Age'].unique())

# Criando o filtro conforme o planejamento do projeto
df_juventude = df[(df['Age'] >= 15) & (df['Age'] <= 29)]

print(f"Total de registros na faixa de 15-29 anos: {len(df_juventude)}")
