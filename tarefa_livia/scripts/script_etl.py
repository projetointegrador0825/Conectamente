# Primeiro, avisamos ao computador que vamos usar a ferramenta de tabelas (Pandas)
import pandas as pd

# Agora, damos o endereço do seu arquivo para o Python
# É como dizer: "Vá na pasta tarefa_livia, depois na pasta dados e pegue esse arquivo"
caminho_do_arquivo = 'tarefa_livia/dados/Student Mental Health.csv'

# Mandamos o Pandas ler o arquivo e guardar em uma variável chamada 'dados'
dados = pd.read_csv(caminho_do_arquivo)

# Pedimos para ele nos mostrar apenas as 5 primeiras linhas para ver se deu certo
print("Aqui estão os primeiros dados que encontramos:")
print(dados.head())

# Pedimos para ele listar os nomes das colunas (os títulos das tabelas)
print("\nEssas são as perguntas/colunas da nossa base:")
print(dados.columns)

import pandas as pd

# 1. EXTRAÇÃO (Você já venceu essa parte!)
caminho_do_arquivo = 'tarefa_livia/dados/Student Mental Health.csv'
dados = pd.read_csv(caminho_do_arquivo)

# 2. TRANSFORMAÇÃO (Vamos arrumar a casa)

# Criamos um "dicionário" para traduzir os nomes das colunas
# De um lado o nome antigo (inglês), do outro o nome novo (português)
traducao = {
    'Choose your gender': 'Genero',
    'Age': 'Idade',
    'What is your course?': 'Curso',
    'Your current year of Study': 'Ano_Estudo',
    'Do you have Depression?': 'Depressao',
    'Do you have Anxiety?': 'Ansiedade',
    'Do you have Panic attack?': 'Ataque_Panico',
    'Did you seek any specialist for a treatment?': 'Buscou_Tratamento'
}

# Aplicamos a tradução
dados_limpos = dados.rename(columns=traducao)

# Vamos manter apenas as colunas que realmente importam para o dashboard
colunas_selecionadas = ['Genero', 'Idade', 'Curso', 'Ano_Estudo', 'Depressao', 'Ansiedade', 'Ataque_Panico', 'Buscou_Tratamento']
dados_finais = dados_limpos[colunas_selecionadas]

# 3. CARGA (Salvar o arquivo pronto para o Dashboard)
# Vamos salvar um novo CSV, já bonitinho, dentro da sua pasta
dados_finais.to_csv('tarefa_livia/dados/dados_estudantes_limpos.csv', index=False)

print("Transformação concluída com sucesso!")
print("Novo arquivo 'dados_estudantes_limpos.csv' criado na pasta dados.")
print("\nVeja como ficaram as colunas agora:")
print(dados_finais.columns)