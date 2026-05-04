import streamlit as st
import pandas as pd
import os
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="ConectaMente Dashboard", layout="wide")

# 2. Caminhos Dinâmicos (Prevenção de erro de diretório)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ajuste 'dados' e 'processados' para bater exatamente com suas pastas
DATA_PATH = os.path.join(BASE_DIR, "dados", "processados", "Tabelas_12_Consolidadas_Regioes_UF.xlsx")

# 3. Função para Carregar Dados
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    else:
        return None

df = load_data()

# --- INTERFACE ---
st.title("🧠 ConectaMente: Dashboard de Saúde Mental")

if df is not None:
    # 4. Sidebar - Filtros Interativos
    st.sidebar.header("Filtros de Pesquisa")
    
    # Filtro de Região
    lista_regioes = sorted(df['Regiao'].unique().tolist())
    regiao_selecionada = st.sidebar.selectbox("Selecione a Região", lista_regioes)
    
    # Filtro de Métrica (Tristeza, Solidão, etc)
    lista_metricas = sorted(df['NOME_METRICA'].unique().tolist())
    metrica_selecionada = st.sidebar.multiselect("Selecione os Indicadores", lista_metricas, default=lista_metricas[0])

    # 5. Filtragem do DataFrame
    df_filtrado = df[(df['Regiao'] == regiao_selecionada) & (df['NOME_METRICA'].isin(metrica_selecionada))]

    # 6. Layout de Colunas para Métricas Principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Indicadores em: {regiao_selecionada}")
        # Gráfico de Barras com Plotly para ser interativo
        fig = px.bar(df_filtrado, 
                     x='NOME_METRICA', 
                     y='rc', 
                     error_y='Limite_superior', # Exemplo de barra de erro
                     title=f"Prevalência (%) - {regiao_selecionada}",
                     labels={'rc': 'Porcentagem (%)', 'NOME_METRICA': 'Indicador'},
                     color='NOME_METRICA')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Dados Detalhados")
        st.dataframe(df_filtrado[['NOME_METRICA', 'rc', 'Limite_inferior', 'Limite_superior']], hide_index=True)

    # 7. Nota de Rodapé Técnica
    st.info("💡 Dados extraídos da PNS 2019 - Série 12. Os limites superiores indicam a margem de erro estatística.")

else:
    st.error(f"Arquivo não encontrado em: {DATA_PATH}")
    st.info("Verifique se o nome do arquivo e das pastas 'dados' e 'processados' estão corretos no VS Code.")