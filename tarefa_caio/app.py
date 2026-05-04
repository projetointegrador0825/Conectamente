import streamlit as st
import pandas as pd
import os

# Título
st.title("🧠 ConectaMente: Dashboard de Saúde Mental")

# Caminho Base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note se a pasta é 'dados' ou 'Dados' (o Windows às vezes ignora, mas é bom ser exato)
folder_path = os.path.join(BASE_DIR, "dados", "processados")
file_name = "Tabelas_12_Consolidadas_Regioes_UF.xlsx"
DATA_PATH = os.path.join(folder_path, file_name)

# --- DIAGNÓSTICO ---
if not os.path.exists(folder_path):
    st.error(f"A pasta não foi encontrada: {folder_path}")
else:
    arquivos_na_pasta = os.listdir(folder_path)
    if file_name not in arquivos_na_pasta:
        st.warning(f"Pasta encontrada, mas o arquivo não está lá. Arquivos disponíveis: {arquivos_na_pasta}")
    else:
        try:
            df = pd.read_excel(DATA_PATH)
            st.success("Dados carregados com sucesso!")
            st.write(df.head())
        except Exception as e:
            st.error(f"Erro ao ler o Excel: {e}")