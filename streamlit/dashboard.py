"""
╔══════════════════════════════════════════════════════════════════════════╗
║           DASHBOARD IBGE — Análise Regional de Métricas                 ║
║                                                                          ║
║  Como rodar:                                                             ║
║    streamlit run dashboard.py                                            ║
║                                                                          ║
║  Estrutura do arquivo (navegue pelos blocos):                            ║
║    [1] IMPORTS & CONFIGURAÇÕES GLOBAIS                                   ║
║    [2] CONEXÃO COM O BIGQUERY E CARREGAMENTO DE DADOS                   ║
║    [3] COMPONENTES REUTILIZÁVEIS (filtros, botão voltar)                 ║
║    [4] PÁGINAS DOS GRÁFICOS                                              ║
║        → pagina_genero()                                                 ║
║        → pagina_dependencia()                                            ║
║        → pagina_faixa_etaria()                                           ║
║        → pagina_pizza_estados()                                          ║
║    [5] PÁGINA INICIAL (HOME) com botões de navegação                     ║
║    [6] ROTEADOR — decide qual página exibir                              ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════
# [1] IMPORTS & CONFIGURAÇÕES GLOBAIS
# ══════════════════════════════════════════════════════════════════════════

import streamlit as st          # Framework principal da aplicação web
import pandas as pd             # Manipulação de dados em tabelas (DataFrames)
import plotly.express as px     # Geração de gráficos interativos

from google.cloud import bigquery               # Cliente do BigQuery (banco de dados Google)
from google.oauth2 import service_account       # Autenticação com conta de serviço Google

# ── Credenciais via Streamlit Secrets ─────────────────────────────────────
# As credenciais são lidas de .streamlit/secrets.toml (localmente) ou dos
# Secrets configurados no Streamlit Community Cloud (em produção).
# O arquivo secrets.toml e o JSON original NUNCA devem ser commitados —
# ambos estão listados no .gitignore.
# Padrão recomendado em:
#   https://docs.streamlit.io/develop/tutorials/databases/bigquery
GCP_CREDENTIALS = st.secrets["gcp_service_account"]

# ── Query SQL que será executada no BigQuery ──────────────────────────────
# Busca todas as colunas necessárias para os três gráficos do dashboard.
QUERY_SQL = """
SELECT
    regiao,
    faixa_etaria,
    nome_metrica,
    pc,
    pc_homem,
    pc_mulher,
    pc_depen_publica,
    pc_depen_privada
FROM `projeto-integrador-sm.dados_ibge.regioes`
"""

# ── Query SQL — Prevalência por ESTADO ───────────────────────────────────
# Tabela com colunas confirmadas:
#   tabela_origem, nome_metrica, faixa_etaria, regiao, estado,
#   pc, limite_inferior, limite_superior,
#   pc_homem, limite_inf_homem, limite_sup_homem, pc_mulher
# Selecionamos apenas o necessário para o gráfico de pizza.
QUERY_SQL_ESTADOS = """
SELECT
    estado,
    nome_metrica,
    faixa_etaria,
    pc
FROM `projeto-integrador-sm.dados_ibge.estados`
WHERE estado IS NOT NULL
  AND pc     IS NOT NULL
"""

# ── Query SQL — Prevalência por CAPITAL ──────────────────────────────────
# Tabela com colunas confirmadas:
#   tabela_origem, nome_metrica, faixa_etaria, capital,
#   pc, limite_inferior, limite_superior,
#   pc_homem, limite_inf_homem, limite_sup_homem,
#   pc_mulher, limite_inf_mulher, limite_sup_mulher
# Tabela separada da de estados — capital é a coluna de localidade aqui.
QUERY_SQL_CAPITAIS = """
SELECT
    capital,
    nome_metrica,
    faixa_etaria,
    pc
FROM `projeto-integrador-sm.dados_ibge.capitais`
WHERE capital IS NOT NULL
  AND pc       IS NOT NULL
"""

# ── Metadados das páginas disponíveis ────────────────────────────────────
# Cada dicionário representa um botão/página na Home.
# Para ADICIONAR uma nova página, basta inserir um novo item aqui
# e criar a função correspondente mais abaixo.
PAGINAS = [
    {
        "chave":     "genero",          # identificador interno da página
        "emoji":     "⚧️",
        "titulo":    "Gênero × Métrica",
        "descricao": "Compara indicadores entre homens e mulheres.",
    },
    {
        "chave":     "dependencia",
        "emoji":     "🏫",
        "titulo":    "Dependência × Métrica",
        "descricao": "Compara redes de ensino pública e privada.",
    },
    {
        "chave":     "faixa_etaria",
        "emoji":     "📅",
        "titulo":    "Faixa Etária × Métrica",
        "descricao": "Mostra métricas distribuídas por faixa etária.",
    },
    {
        "chave":     "pizza_estados",
        "emoji":     "🗺️",
        "titulo":    "Prevalência por Estado / Capital",
        "descricao": "Distribuição dos transtornos pelos 26 estados e DF e suas capitais.",
    },
]

# ══════════════════════════════════════════════════════════════════════════
# [2] CONEXÃO COM O BIGQUERY E CARREGAMENTO DE DADOS
# ══════════════════════════════════════════════════════════════════════════

# O decorator @st.cache_data faz com que o Streamlit guarde o resultado
# desta função na memória. Assim, o BigQuery só é consultado UMA VEZ
# por sessão — se o usuário trocar de página ou mexer nos filtros,
# os dados já estão em cache e a tela atualiza instantaneamente.
@st.cache_data(show_spinner="⏳ Carregando dados do BigQuery…")
def carregar_dados() -> pd.DataFrame:
    """
    Autentica no Google Cloud, executa a query SQL e retorna
    um DataFrame limpo e tipado.

    Retorno
    -------
    pd.DataFrame com as colunas:
        regiao, faixa_etaria, nome_metrica,
        pc_regiao (float), pc_homem (float), pc_mulher (float),
        pc_depen_publica (float), pc_depen_privada (float)
    """

    # Lê as credenciais a partir do secrets.toml (via st.secrets)
    credenciais = service_account.Credentials.from_service_account_info(
        GCP_CREDENTIALS
    )

    # Cria o cliente do BigQuery usando as credenciais acima
    cliente = bigquery.Client(
        credentials=credenciais,
        project=credenciais.project_id
    )

    # Executa a query e converte o resultado para DataFrame do pandas
    df = cliente.query(QUERY_SQL).to_dataframe()

    # ── Converte colunas numéricas ────────────────────────────────────
    # errors='coerce' transforma valores inválidos (texto, None) em NaN
    # em vez de lançar um erro que quebraria o app.
    colunas_numericas = ["pc", "pc_homem", "pc_mulher",
                         "pc_depen_publica", "pc_depen_privada"]

    for coluna in colunas_numericas:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    # Cria alias "pc_regiao" como cópia numérica da coluna principal "pc"
    df["pc_regiao"] = df["pc"]

    # ── Remove linhas com dados obrigatórios ausentes ─────────────────
    # Uma linha sem região, faixa etária, métrica ou percentual principal
    # não tem utilidade nos gráficos; é melhor descartá-la aqui do que
    # tratar erros depois.
    mascara_valida = (
        df["regiao"].notnull()       & (df["regiao"] != "")       &
        df["faixa_etaria"].notnull() & (df["faixa_etaria"] != "") &
        df["nome_metrica"].notnull() & (df["nome_metrica"] != "") &
        df["pc_regiao"].notnull()
    )
    df = df[mascara_valida]

    return df


@st.cache_data(show_spinner="⏳ Carregando dados por estado…")
def carregar_dados_estados() -> pd.DataFrame:
    """
    Carrega a tabela de prevalência por estado do BigQuery.

    Colunas retornadas: estado, nome_metrica, faixa_etaria, pc (float).

    O @st.cache_data guarda o resultado em memória — o BigQuery só é
    consultado uma vez por sessão, mesmo que o usuário troque de filtro
    várias vezes na mesma página.
    """
    credenciais = service_account.Credentials.from_service_account_info(
        GCP_CREDENTIALS
    )
    cliente = bigquery.Client(
        credentials=credenciais,
        project=credenciais.project_id
    )

    df = cliente.query(QUERY_SQL_ESTADOS).to_dataframe()

    # Garante que pc seja numérico (o BigQuery pode retornar NUMERIC/FLOAT64,
    # mas pd.to_numeric é uma segurança extra contra tipos inesperados).
    df["pc"] = pd.to_numeric(df["pc"], errors="coerce")

    # Descarta linhas incompletas que não têm utilidade no gráfico
    df = df[
        df["estado"].notnull()       & (df["estado"] != "")       &
        df["nome_metrica"].notnull() & (df["nome_metrica"] != "") &
        df["pc"].notnull()
    ]

    return df


@st.cache_data(show_spinner="⏳ Carregando dados por capital…")
def carregar_dados_capitais() -> pd.DataFrame:
    """
    Carrega a tabela de prevalência por capital do BigQuery.

    Colunas retornadas: capital, nome_metrica, faixa_etaria, pc (float).

    Tabela separada da de estados — a coluna de localidade aqui é
    'capital', não 'estado'. Por isso usamos uma query e um cache
    independentes.
    """
    credenciais = service_account.Credentials.from_service_account_info(
        GCP_CREDENTIALS
    )
    cliente = bigquery.Client(
        credentials=credenciais,
        project=credenciais.project_id
    )

    df = cliente.query(QUERY_SQL_CAPITAIS).to_dataframe()

    df["pc"] = pd.to_numeric(df["pc"], errors="coerce")

    df = df[
        df["capital"].notnull()      & (df["capital"] != "")      &
        df["nome_metrica"].notnull() & (df["nome_metrica"] != "") &
        df["pc"].notnull()
    ]

    return df


# ══════════════════════════════════════════════════════════════════════════
# [3] COMPONENTES REUTILIZÁVEIS
# ══════════════════════════════════════════════════════════════════════════

def renderizar_filtros(df: pd.DataFrame) -> tuple:
    """
    Exibe dois menus suspensos (selectboxes) no topo da página:
    um para Região e outro para Faixa Etária.

    Como funciona um selectbox no Streamlit:
      - st.selectbox(label, options) mostra um menu suspenso.
      - O valor escolhido pelo usuário é retornado pela função.
      - Sempre que o usuário troca a opção, o Streamlit re-executa
        o script inteiro do zero — por isso salvamos seleções
        importantes no session_state quando necessário.

    Parâmetros
    ----------
    df : pd.DataFrame
        Dataset completo, usado para popular as opções dos menus.

    Retorno
    -------
    tuple: (regiao_selecionada: str, faixa_etaria_selecionada: str)
    """

    # st.columns(n) divide a tela em n colunas lado a lado.
    # Aqui criamos 3 colunas; a terceira fica vazia só para dar espaço.
    col1, col2, _ = st.columns([2, 2, 1])

    with col1:
        # sorted() organiza as opções em ordem alfabética
        regiao = st.selectbox(
            label="🗺️ Região:",
            options=sorted(df["regiao"].unique().tolist()),
            key="filtro_regiao",   # chave única — evita conflito se houver
                                   # outro selectbox com o mesmo label
        )

    with col2:
        faixa_etaria = st.selectbox(
            label="📅 Faixa Etária:",
            options=sorted(df["faixa_etaria"].unique().tolist()),
            key="filtro_faixa",
        )

    # Linha horizontal separando filtros do gráfico
    st.divider()

    return regiao, faixa_etaria


def botao_voltar() -> None:
    """
    Exibe um botão "← Voltar" que redireciona para a Home.

    Como funciona a navegação no Streamlit:
      O Streamlit não tem "páginas" nativas com URLs diferentes (a menos
      que você use a pasta pages/ nativa). Aqui usamos session_state para
      simular navegação:
        1. Guardamos a página atual em st.session_state["pagina"].
        2. Ao clicar em um botão, alteramos esse valor.
        3. Chamamos st.rerun() para forçar o Streamlit a re-executar
           o script — na próxima execução, o roteador lerá o novo valor
           e exibirá a página correta.
    """
    if st.button("← Voltar ao início", key="btn_voltar"):
        st.session_state["pagina"] = "home"
        st.rerun()   # força re-execução imediata do script


# ══════════════════════════════════════════════════════════════════════════
# [4] PÁGINAS DOS GRÁFICOS
# ══════════════════════════════════════════════════════════════════════════
# Cada função abaixo é uma "página" completa.
# Elas recebem o DataFrame já filtrado por região e faixa etária
# (a filtragem acontece no roteador [6], evitando repetição de código).
# ──────────────────────────────────────────────────────────────────────────

# ── 4a. Gênero × Métrica ──────────────────────────────────────────────────

def pagina_genero(df_filtrado: pd.DataFrame) -> None:
    """
    Exibe o gráfico de barras comparando percentuais de homens e mulheres
    para cada métrica educacional.

    Parâmetros
    ----------
    df_filtrado : pd.DataFrame
        Dados já filtrados por região e faixa etária.
    """
    botao_voltar()   # botão de retorno no topo da página

    st.markdown("## ⚧️ Gênero × Métrica")
    st.caption(
        "Percentual médio de cada indicador educacional, "
        "separado por gênero, para a região e faixa etária selecionadas."
    )

    # ── Verificações de segurança ─────────────────────────────────────
    # Antes de tentar montar o gráfico, verificamos se os dados existem.
    # Isso evita erros feios na tela do usuário.

    colunas_necessarias = ["pc_homem", "pc_mulher", "nome_metrica"]
    colunas_ausentes    = [c for c in colunas_necessarias if c not in df_filtrado.columns]

    if colunas_ausentes:
        # st.warning() exibe uma caixa amarela de aviso
        st.warning(f"⚠️ Colunas ausentes no dataset: {colunas_ausentes}")
        return   # encerra a função sem tentar gerar o gráfico

    if df_filtrado.empty:
        # st.info() exibe uma caixa azul informativa
        st.info("ℹ️ Sem dados para os filtros selecionados.")
        return

    # ── Preparação dos dados ──────────────────────────────────────────
    # groupby('nome_metrica') agrupa todas as linhas com a mesma métrica.
    # .mean() calcula a média de pc_homem e pc_mulher dentro de cada grupo.
    # .reset_index() transforma o índice de volta em coluna normal.
    df_agrupado = (
        df_filtrado
        .groupby("nome_metrica")[["pc_homem", "pc_mulher"]]
        .mean()
        .reset_index()
    )

    # .melt() "derrete" o DataFrame de formato largo para formato longo:
    # Antes: | nome_metrica | pc_homem | pc_mulher |
    # Depois: | nome_metrica | genero   | pc        |
    # O formato longo é necessário para px.bar com a opção color=.
    df_longo = df_agrupado.melt(
        id_vars=["nome_metrica"],   # coluna que permanece fixa
        var_name="genero",          # nova coluna com os nomes das variáveis
        value_name="pc",            # nova coluna com os valores
    )

    # Substitui os nomes internos por rótulos legíveis
    df_longo["genero"] = df_longo["genero"].map({
        "pc_homem": "Homem",
        "pc_mulher": "Mulher",
    })

    if df_longo.empty:
        st.warning("⚠️ Sem dados após processamento.")
        return

    # ── Construção do gráfico ─────────────────────────────────────────
    # px.bar() cria um gráfico de barras interativo.
    # barmode='group' coloca as barras de cada métrica lado a lado
    # (em vez de empilhadas).
    fig = px.bar(
        df_longo,
        x="genero",                 # eixo horizontal
        y="pc",                     # eixo vertical (altura das barras)
        color="nome_metrica",       # cada métrica recebe uma cor diferente
        barmode="group",            # barras agrupadas (não empilhadas)
        text="pc",                  # mostra o valor em cima de cada barra
        labels={                    # renomeia os eixos e legenda
            "pc":           "PC (%)",
            "genero":       "Gênero",
            "nome_metrica": "Métrica",
        },
        title="Gênero × Métrica — Percentual médio por indicador",
    )

    # Fixa o eixo Y entre 0 e 100 para facilitar comparação visual
    fig.update_yaxes(range=[0, 100], title_text="Percentual (%)")

    # Formata os rótulos em cima das barras com 2 casas decimais + "%"
    fig.update_traces(textposition="outside", texttemplate="%{text:.2f}%")

    # Ajusta altura do gráfico e tamanho da fonte na legenda
    fig.update_layout(
        height=460,
        hovermode="closest",         # tooltip aparece na barra mais próxima
        legend=dict(font=dict(size=9)),
    )

    # st.plotly_chart() renderiza o gráfico Plotly dentro do Streamlit.
    # use_container_width=True faz o gráfico ocupar toda a largura disponível.
    st.plotly_chart(fig, use_container_width=True)


# ── 4b. Dependência Administrativa × Métrica ──────────────────────────────

def pagina_dependencia(df_filtrado: pd.DataFrame) -> None:
    """
    Exibe o gráfico de barras comparando percentuais de escolas
    públicas e privadas para cada métrica educacional.

    Parâmetros
    ----------
    df_filtrado : pd.DataFrame
        Dados já filtrados por região e faixa etária.
    """
    botao_voltar()

    st.markdown("## 🏫 Dependência Administrativa × Métrica")
    st.caption(
        "Percentual médio de cada indicador educacional, "
        "separado por tipo de rede (pública × privada)."
    )

    # ── Verificações de segurança ─────────────────────────────────────
    colunas_necessarias = ["pc_depen_publica", "pc_depen_privada", "nome_metrica"]
    colunas_ausentes    = [c for c in colunas_necessarias if c not in df_filtrado.columns]

    if colunas_ausentes:
        st.warning(f"⚠️ Colunas ausentes no dataset: {colunas_ausentes}")
        return

    if df_filtrado.empty:
        st.info("ℹ️ Sem dados para os filtros selecionados.")
        return

    # ── Preparação dos dados ──────────────────────────────────────────
    # Mesma lógica de groupby + melt explicada em pagina_genero(),
    # mas agora para as colunas de dependência administrativa.
    df_agrupado = (
        df_filtrado
        .groupby("nome_metrica")[["pc_depen_publica", "pc_depen_privada"]]
        .mean()
        .reset_index()
    )

    df_longo = df_agrupado.melt(
        id_vars=["nome_metrica"],
        var_name="dependencia",
        value_name="pc",
    )

    df_longo["dependencia"] = df_longo["dependencia"].map({
        "pc_depen_publica": "Pública",
        "pc_depen_privada": "Privada",
    })

    if df_longo.empty:
        st.warning("⚠️ Sem dados após processamento.")
        return

    # ── Construção do gráfico ─────────────────────────────────────────
    fig = px.bar(
        df_longo,
        x="dependencia",
        y="pc",
        color="nome_metrica",
        barmode="group",
        text="pc",
        labels={
            "pc":           "PC (%)",
            "dependencia":  "Dependência Administrativa",
            "nome_metrica": "Métrica",
        },
        title="Dependência Administrativa × Métrica — Percentual médio",
    )

    fig.update_yaxes(range=[0, 100], title_text="Percentual (%)")
    fig.update_traces(textposition="outside", texttemplate="%{text:.2f}%")
    fig.update_layout(
        height=460,
        hovermode="closest",
        legend=dict(font=dict(size=9)),
    )

    st.plotly_chart(fig, use_container_width=True)


# ── 4c. Faixa Etária × Métrica ────────────────────────────────────────────

def pagina_faixa_etaria(df_filtrado: pd.DataFrame) -> None:
    """
    Exibe o gráfico de barras com o percentual regional médio
    por faixa etária e por métrica educacional.

    Parâmetros
    ----------
    df_filtrado : pd.DataFrame
        Dados já filtrados por região e faixa etária.
    """
    botao_voltar()

    st.markdown("## 📅 Faixa Etária × Métrica")
    st.caption(
        "Percentual médio regional de cada indicador educacional "
        "distribuído por faixa etária."
    )

    # ── Verificações de segurança ─────────────────────────────────────
    colunas_necessarias = ["faixa_etaria", "nome_metrica", "pc_regiao"]
    colunas_ausentes    = [c for c in colunas_necessarias if c not in df_filtrado.columns]

    if colunas_ausentes:
        st.warning(f"⚠️ Colunas ausentes no dataset: {colunas_ausentes}")
        return

    if df_filtrado.empty:
        st.info("ℹ️ Sem dados para os filtros selecionados.")
        return

    # ── Preparação dos dados ──────────────────────────────────────────
    # Agrupa por DUAS colunas: faixa etária e métrica.
    # Para cada combinação, calcula a média do percentual regional.
    df_agrupado = (
        df_filtrado
        .groupby(["faixa_etaria", "nome_metrica"])["pc_regiao"]
        .mean()
        .reset_index()
    )

    if df_agrupado.empty:
        st.warning("⚠️ Sem dados após processamento.")
        return

    # ── Construção do gráfico ─────────────────────────────────────────
    fig = px.bar(
        df_agrupado,
        x="faixa_etaria",
        y="pc_regiao",
        color="nome_metrica",
        barmode="group",
        text="pc_regiao",
        labels={
            "pc_regiao":    "PC (%)",
            "faixa_etaria": "Faixa Etária",
            "nome_metrica": "Métrica",
        },
        title="Faixa Etária × Métrica — Percentual médio regional",
    )

    fig.update_yaxes(range=[0, 100], title_text="Percentual (%)")
    fig.update_traces(textposition="outside", texttemplate="%{text:.2f}%")
    fig.update_layout(
        height=460,
        hovermode="closest",
        legend=dict(font=dict(size=9)),
        xaxis_tickangle=-30,         # inclina os rótulos do eixo X para não sobrepor
    )

    st.plotly_chart(fig, use_container_width=True)


# ── 4d. Pizza — Prevalência por Estado / Capital ─────────────────────────

def pagina_pizza_estados(df_estados: pd.DataFrame, df_capitais: pd.DataFrame) -> None:
    """
    Exibe gráficos de pizza com a distribuição proporcional da prevalência
    de um transtorno, podendo alternar entre visão por Estado e por Capital.

    Como a tabela de estados e a de capitais são SEPARADAS no BigQuery
    (cada uma com sua própria coluna de localidade), esta função recebe
    os dois DataFrames já carregados e usa o correto conforme a escolha
    do usuário no radio button.

    Controles disponíveis:
      • Selectbox de transtorno/métrica
      • Selectbox de faixa etária (opcional — "Todas" agrega tudo)
      • Radio button: Estado × Capital
      • Dois gráficos de pizza lado a lado
      • Tabela de dados brutos recolhível

    Parâmetros
    ----------
    df_estados  : pd.DataFrame  — colunas: estado, nome_metrica, faixa_etaria, pc
    df_capitais : pd.DataFrame  — colunas: capital, nome_metrica, faixa_etaria, pc
    """
    botao_voltar()

    st.markdown("## 🗺️ Prevalência de Transtornos por Estado e Capital")
    st.caption(
        "Selecione um transtorno e escolha se deseja ver a distribuição "
        "pelos 26 estados + DF ou pelas capitais de cada estado."
    )

    # ══════════════════════════════════════════════════════════════════
    # CONTROLES DO USUÁRIO
    # ══════════════════════════════════════════════════════════════════

    col_visao, col_metrica, col_faixa = st.columns([1.5, 2, 2])

    with col_visao:
        # st.radio() → seleção exclusiva entre duas opções.
        # A escolha define qual DataFrame e qual coluna de localidade usar.
        visao = st.radio(
            label="📍 Visualizar por:",
            options=["Estado", "Capital"],
            horizontal=False,
            key="pizza_visao",
        )

    # Define qual DataFrame e qual coluna de localidade usar
    # com base na escolha do radio button acima.
    if visao == "Estado":
        df_ativo      = df_estados    # tabela correta para estados
        col_local     = "estado"      # coluna de localidade nesta tabela
        titulo_local  = "Estado"
    else:
        df_ativo      = df_capitais   # tabela correta para capitais
        col_local     = "capital"     # coluna de localidade nesta tabela
        titulo_local  = "Capital"

    # Verificação: se o DataFrame estiver vazio, avisa e encerra
    if df_ativo.empty:
        st.info(f"ℹ️ Sem dados disponíveis para a visão por {titulo_local}.")
        return

    with col_metrica:
        # Lista de transtornos do DataFrame ativo (estado ou capital)
        metricas_raw = sorted(df_ativo["nome_metrica"].unique().tolist())

        # Formata os nomes para exibição: troca "_" por espaço e aplica
        # sentence case (só a primeira letra maiúscula). O valor interno
        # continua sendo o original — usamos um dicionário de mapeamento
        # para recuperar o valor bruto após a seleção do usuário.
        def formatar_metrica(nome: str) -> str:
            return nome.replace("_", " ").capitalize()

        mapa_exibicao = {formatar_metrica(m): m for m in metricas_raw}
        metricas_formatadas = [formatar_metrica(m) for m in metricas_raw]

        # st.selectbox() → menu suspenso. Retorna o valor escolhido como string.
        metrica_exibida = st.selectbox(
            label="🧠 Transtorno / Indicador:",
            options=metricas_formatadas,
            key="pizza_metrica",
        )

        # Recupera o valor original (com underscore) para filtrar o DataFrame
        metrica_selecionada = mapa_exibicao[metrica_exibida]

    with col_faixa:
        # Faixa etária — inclui a opção "Todas" para agregar sem filtro
        faixas = ["Todas"] + sorted(df_ativo["faixa_etaria"].unique().tolist())

        faixa_selecionada = st.selectbox(
            label="📅 Faixa Etária:",
            options=faixas,
            key="pizza_faixa",
        )

    st.divider()

    # ══════════════════════════════════════════════════════════════════
    # FILTRAGEM DOS DADOS
    # ══════════════════════════════════════════════════════════════════

    # Filtra pelo transtorno selecionado — sempre obrigatório
    df_filtrado = df_ativo[df_ativo["nome_metrica"] == metrica_selecionada].copy()

    # Filtra pela faixa etária, somente se não for "Todas"
    if faixa_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["faixa_etaria"] == faixa_selecionada]

    if df_filtrado.empty:
        st.warning(
            f"⚠️ Sem dados para '{metrica_selecionada}'"
            + (f" na faixa '{faixa_selecionada}'." if faixa_selecionada != "Todas" else ".")
        )
        return

    # ── Agrupamento ───────────────────────────────────────────────────
    # groupby(col_local) agrupa todas as linhas com o mesmo estado/capital.
    # .mean() calcula a MÉDIA de pc — mais adequado que soma quando há
    # múltiplas faixas etárias agregadas em "Todas".
    df_agrupado = (
        df_filtrado
        .groupby(col_local)["pc"]
        .mean()
        .reset_index()
        .sort_values("pc", ascending=False)
        .rename(columns={"pc": "prevalencia"})   # renomeia para clareza interna
    )

    if df_agrupado.empty:
        st.warning("⚠️ Sem dados após agrupamento.")
        return

    # ══════════════════════════════════════════════════════════════════
    # TÍTULO DA SEÇÃO
    # ══════════════════════════════════════════════════════════════════

    sufixo_faixa = f" — Faixa: {faixa_selecionada}" if faixa_selecionada != "Todas" else " — Todas as faixas etárias"
    st.markdown(f"#### {metrica_selecionada} por {titulo_local}{sufixo_faixa}")

    # ══════════════════════════════════════════════════════════════════
    # GRÁFICOS LADO A LADO
    # ══════════════════════════════════════════════════════════════════

    col_esq, col_dir = st.columns(2)

    # ── Gráfico esquerdo — Participação relativa (%) ──────────────────
    # Mostra o PESO de cada estado/capital dentro do total do indicador.
    # Útil para ver quais localidades concentram mais o transtorno.
    with col_esq:
        st.markdown("**Participação relativa no conjunto**")
        st.caption(
            "Cada fatia representa a proporção daquele "
            f"{titulo_local.lower()} em relação à soma de todos os outros."
        )

        # px.pie() — gráfico de pizza Plotly.
        #   values= define o TAMANHO de cada fatia (usa prevalencia média).
        #   names=  define o RÓTULO de cada fatia (nome do estado/capital).
        #   hole=   valor entre 0 e 1; cria buraco central (estilo "donut").
        fig_rel = px.pie(
            df_agrupado,
            values="prevalencia",
            names=col_local,
            hole=0.38,
            title=f"Participação relativa — {metrica_selecionada}",
        )

        # update_traces() ajusta como os rótulos aparecem nas fatias.
        # textinfo="percent+label" mostra: "SP\n18,4%"
        fig_rel.update_traces(
            textinfo="percent+label",
            textposition="inside",
            insidetextorientation="auto",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Participação: %{percent}<br>"
                "Prevalência média: %{value:.2f}%"
                "<extra></extra>"     # remove o bloco secundário do tooltip
            ),
        )
        fig_rel.update_layout(
            height=540,
            legend=dict(font=dict(size=9), orientation="v"),
        )
        st.plotly_chart(fig_rel, use_container_width=True)

    # ── Gráfico direito — Valor real de prevalência (pc%) ─────────────
    # Mostra o PERCENTUAL REAL registrado no dataset, não a participação.
    # Útil para comparar magnitudes absolutas entre localidades.
    with col_dir:
        st.markdown("**Prevalência média real (pc%)**")
        st.caption(
            "Cada fatia exibe o valor médio de pc% registrado "
            f"para aquela {titulo_local.lower()} no indicador selecionado."
        )

        fig_abs = px.pie(
            df_agrupado,
            values="prevalencia",
            names=col_local,
            hole=0.38,
            title=f"Prevalência real (pc%) — {metrica_selecionada}",
        )

        # texttemplate permite formatar livremente o texto dentro da fatia.
        # %{label} = nome do estado/capital
        # %{value:.2f} = valor numérico com 2 casas decimais
        fig_abs.update_traces(
            texttemplate="%{label}<br>%{value:.2f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Prevalência: %{value:.2f}%"
                "<extra></extra>"
            ),
        )
        fig_abs.update_layout(
            height=540,
            showlegend=False,   # a legenda já está no gráfico da esquerda
        )
        st.plotly_chart(fig_abs, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════
    # TABELA DE DADOS BRUTOS (RECOLHÍVEL)
    # ══════════════════════════════════════════════════════════════════

    # st.expander() cria uma seção colapsável — começa fechada,
    # o usuário clica para expandir e ver os dados detalhados.
    with st.expander("📋 Ver tabela de dados desta seleção"):
        df_exibir = df_agrupado.rename(columns={
            col_local:      titulo_local,
            "prevalencia":  f"Prevalência média — {metrica_selecionada} (%)",
        })
        # st.dataframe() renderiza a tabela com barra de rolagem,
        # ordenação por coluna ao clicar no cabeçalho e busca interna.
        st.dataframe(
            df_exibir.style.format(
                {f"Prevalência média — {metrica_selecionada} (%)": "{:.2f}%"}
            ),
            use_container_width=True,
            hide_index=True,
        )


# ══════════════════════════════════════════════════════════════════════════
# [5] PÁGINA INICIAL — HOME
# ══════════════════════════════════════════════════════════════════════════

def pagina_home() -> None:
    """
    Página inicial do dashboard.

    Exibe título, descrição e um cartão com botão para cada gráfico.
    Clicar em um botão salva a página destino em session_state
    e chama st.rerun() para que o roteador [6] exiba a nova página.

    Como o session_state funciona:
      st.session_state é um dicionário persistente durante a sessão
      do usuário (até fechar o navegador). Diferente de variáveis Python
      normais, ele sobrevive às re-execuções do script que o Streamlit
      faz automaticamente cada vez que o usuário interage com algo.
    """

    # ── Texto introdutório ────────────────────────────────────────────
    # st.title() exibe um título grande no topo da página (equivalente a <h1>).
    st.title("🌱 Introdução: Saúde Mental no Brasil")

    # st.markdown() interpreta a string como Markdown:
    #   **texto**   → negrito
    #   ### Título  → subtítulo nível 3
    #   * item      → lista com marcador
    #   1. item     → lista numerada
    #   ---         → linha horizontal
    #   *texto*     → itálico
    st.markdown("""
### Contextualização do Projeto

Este trabalho é fruto do **Projeto Integrador** e tem como objetivo central analisar o cenário da saúde mental no Brasil através de dados reais e tecnologia de ponta.

A saúde mental deixou de ser apenas a ausência de transtornos para se tornar uma prioridade de saúde pública. Com o aumento dos casos de depressão e ansiedade, entender como esses indicadores se distribuem pelo território nacional é fundamental para o planejamento de políticas eficazes.

### Base de Dados e Tecnologia

Para esta análise, utilizamos:
* **PNS 2019 (IBGE):** A Pesquisa Nacional de Saúde é a fonte mais completa de indicadores de saúde e estilos de vida da população brasileira.
* **Google BigQuery:** Os microdados foram processados em nuvem, permitindo o cruzamento de milhões de linhas com alta performance.
* **Streamlit & Python:** Ferramentas utilizadas para transformar dados complexos em visualizações interativas e acessíveis.

### Objetivos da Análise

Nesta plataforma, você encontrará visualizações divididas em:
1.  **Indicadores Regionais:** Comparativo de prevalência entre as 5 regiões do Brasil.
2.  **Recortes Demográficos:** Análise por gênero, faixa etária e tipo de dependência de saúde (Pública vs. Privada).
3.  **Distribuição Proporcional:** Gráficos que facilitam a compreensão da participação de cada região no cenário nacional.

---
*Este dashboard serve como ferramenta de apoio à decisão e visualização acadêmica sobre a realidade da saúde mental brasileira.*
""")

    st.divider()   # linha horizontal separando a introdução dos botões de navegação

    # ── Integrantes do grupo ──────────────────────────────────────────
    st.markdown("""
### 👥 Integrantes do Grupo

* Caio Gabriel Lemos Neris
* Cinthia Pimentel da Silva
* Livia Castro Alves da Silva
* Ryan Alves de Araujo
""")

    st.divider()

    # ── Cartões de navegação ──────────────────────────────────────────
    # Criamos uma coluna para cada página definida em PAGINAS (no topo).
    # len(PAGINAS) retorna o número de páginas — assim se você adicionar
    # um novo item em PAGINAS, a Home se ajusta automaticamente.
    colunas = st.columns(len(PAGINAS))

    for coluna, pagina in zip(colunas, PAGINAS):
        # zip() emparelha cada coluna com seus metadados de página
        with coluna:
            # ── Cartão visual ─────────────────────────────────────
            # Usamos HTML/CSS inline para criar um cartão estilizado.
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #1f77b4, #0d4f8c);
                    border-radius: 12px;
                    padding: 24px 16px;
                    text-align: center;
                    color: white;
                    margin-bottom: 10px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                ">
                    <div style="font-size:2rem;">{pagina['emoji']}</div>
                    <h3 style="margin:8px 0 6px 0; font-size:1.1rem;">
                        {pagina['titulo']}
                    </h3>
                    <p style="margin:0; font-size:0.85rem; opacity:0.85;">
                        {pagina['descricao']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ── Botão de navegação ────────────────────────────────
            # st.button() cria um botão clicável.
            # Quando clicado, retorna True — usamos isso para navegar.
            # key= é obrigatório quando há múltiplos botões; deve ser único.
            # use_container_width=True estica o botão até a borda da coluna.
            if st.button(
                label=f"Abrir →",
                key=f"btn_{pagina['chave']}",
                use_container_width=True,
            ):
                # Salva a página destino no session_state
                st.session_state["pagina"] = pagina["chave"]

                # st.rerun() força o Streamlit a re-executar o script
                # agora — o roteador [6] lerá o novo valor e abrirá
                # a página correta.
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════
# [6] CONFIGURAÇÃO INICIAL E ROTEADOR PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════
# Tudo abaixo deste ponto é executado a cada re-render do Streamlit.
# O Streamlit re-executa o script inteiro sempre que:
#   • O usuário clica em um botão
#   • O usuário muda um selectbox, slider, etc.
#   • st.rerun() é chamado explicitamente
# ──────────────────────────────────────────────────────────────────────────

# ── Configuração da aba do navegador ─────────────────────────────────────
# Deve ser a PRIMEIRA chamada st.* do script, senão o Streamlit lança erro.
st.set_page_config(
    page_title="Dashboard IBGE",
    page_icon="📊",
    layout="wide",           # "wide" usa toda a largura da janela
)

# ── CSS global ────────────────────────────────────────────────────────────
# Limita a largura dos menus suspensos (selectbox) para não ficarem enormes.
st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        max-width: 380px !important;
        min-width: 120px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── Inicialização da navegação ────────────────────────────────────────────
# Na primeira abertura do app, session_state está vazio.
# Definimos "home" como página padrão usando o operador setdefault(),
# que só insere o valor se a chave ainda não existir.
st.session_state.setdefault("pagina", "home")

# ── Carrega os dados (resultado vem do cache na maioria das vezes) ─────────
# Cada função de carregamento tem seu próprio cache independente.
df_completo = carregar_dados()

# ── Roteador: decide qual função de página chamar ────────────────────────
# Lemos a página atual do session_state e chamamos a função correspondente.

pagina_atual = st.session_state["pagina"]

if pagina_atual == "home":
    # Exibe a página inicial com os botões de navegação
    pagina_home()

elif pagina_atual in ("genero", "dependencia", "faixa_etaria"):
    # Para as páginas de gráfico, primeiro renderizamos os filtros
    # e depois passamos o DataFrame já filtrado para a página correta.

    # renderizar_filtros() exibe os dois selectboxes e retorna os valores
    regiao_selecionada, faixa_selecionada = renderizar_filtros(df_completo)

    # Aplica os filtros: mantém apenas linhas que batem com as seleções
    df_filtrado = df_completo[
        (df_completo["regiao"]      == regiao_selecionada) &
        (df_completo["faixa_etaria"] == faixa_selecionada)
    ]

    # Chama a função da página correta com os dados filtrados
    if pagina_atual == "genero":
        pagina_genero(df_filtrado)

    elif pagina_atual == "dependencia":
        pagina_dependencia(df_filtrado)

    elif pagina_atual == "faixa_etaria":
        pagina_faixa_etaria(df_filtrado)

elif pagina_atual == "pizza_estados":
    # Esta página usa DUAS tabelas separadas do BigQuery:
    #   - dados_ibge.estados  → coluna de localidade: "estado"
    #   - dados_ibge.capitais → coluna de localidade: "capital"
    # Carregamos as duas aqui e passamos para a função da página,
    # que decide qual usar conforme o radio button do usuário.
    df_estados  = carregar_dados_estados()
    df_capitais = carregar_dados_capitais()
    pagina_pizza_estados(df_estados, df_capitais)

else:
    # Página desconhecida — redireciona para a Home com mensagem de erro
    st.error(f"Página desconhecida: '{pagina_atual}'. Redirecionando…")
    st.session_state["pagina"] = "home"
    st.rerun()
