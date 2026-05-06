import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração Básica
st.set_page_config(page_title="Saúde Mental Unificada", layout="wide")

st.title("📊 Dashboard Unificado: Saúde Mental Estudantil")
st.markdown("Análise integrada de dados globais e indicadores nacionais.")

# 2. Carregar o arquivo que você criou no ETL
df = pd.read_csv('tarefa_livia/dados/dados_unificados.csv')

# 3. Criar abas para organizar o conteúdo
tab1, tab2 = st.tabs(["📈 Porcentagens Gerais", "🗺️ Comparação Brasil vs Mundo"])

with tab1:
    st.subheader("Frequência Geral de Transtornos")
    
    # Preparamos os dados para o gráfico horizontal
    # Transformamos Yes em 1 e No em 0 para calcular a média/porcentagem
    resumo = df[['Depressao', 'Ansiedade', 'Ataque_Panico']].apply(lambda x: (x == 'Yes').mean() * 100)
    resumo_df = resumo.reset_index()
    resumo_df.columns = ['Transtorno', 'Porcentagem']

    # Gráfico de Barras Horizontais
    fig_geral = px.bar(resumo_df, 
                       y='Transtorno', 
                       x='Porcentagem', 
                       orientation='h',
                       text='Porcentagem',
                       color='Transtorno', 
                       color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig_geral.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig_geral, use_container_width=True)

with tab2:
    st.subheader("Diferença entre Bases de Dados (Brasil vs Mundo)")
    
    # Calculando porcentagem por origem
    df_comp = df.groupby('Origem')[['Depressao', 'Ansiedade', 'Ataque_Panico']].apply(lambda x: (x == 'Yes').mean() * 100).reset_index()
    df_comp = df_comp.melt(id_vars='Origem', var_name='Transtorno', value_name='Porcentagem')

    # Gráfico Comparativo Horizontal
    fig_comp = px.bar(df_comp, 
                      y='Transtorno', 
                      x='Porcentagem', 
                      color='Origem', 
                      barmode='group',
                      orientation='h',
                      text='Porcentagem')
    
    fig_comp.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig_comp, use_container_width=True)

st.divider()
st.info(f"Total de registros integrados: {len(df)}")