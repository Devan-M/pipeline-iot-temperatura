import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


# ============================================================
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Pipeline IoT | Dashboard",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       CONFIGURAÇÃO GERAL
       ====================================================== */

    .stApp {
        background-color: #f5f7fb;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #ffffff;
    }


    /* ======================================================
       CABEÇALHO
       ====================================================== */

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #1d4ed8 0%,
            #2563eb 55%,
            #3b82f6 100%
        );

        padding: 2rem 2.2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;

        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
    }

    .dashboard-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }

    .dashboard-header p {
        color: #dbeafe;
        font-size: 1rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }


    /* ======================================================
       STATUS DO BANCO
       ====================================================== */

    .database-status {
        display: inline-block;

        background-color: rgba(255, 255, 255, 0.15);

        color: #ffffff;

        padding: 0.35rem 0.75rem;

        border-radius: 999px;

        font-size: 0.8rem;

        margin-top: 1rem;
    }


    /* ======================================================
       CARDS
       ====================================================== */

    .metric-card {
        background-color: #ffffff;

        padding: 1.3rem 1.4rem;

        border-radius: 14px;

        border: 1px solid #e5e7eb;

        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);

        min-height: 125px;
    }

    .metric-title {
        color: #6b7280;

        font-size: 0.85rem;

        font-weight: 600;

        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: #111827;

        font-size: 1.8rem;

        font-weight: 700;

        line-height: 1.2;
    }

    .metric-description {
        color: #9ca3af;

        font-size: 0.75rem;

        margin-top: 0.5rem;
    }


    /* ======================================================
       SEÇÕES
       ====================================================== */

    .section-title {
        color: #111827;

        font-size: 1.25rem;

        font-weight: 700;

        margin-top: 1.8rem;

        margin-bottom: 0.2rem;
    }

    .section-description {
        color: #6b7280;

        font-size: 0.85rem;

        margin-bottom: 1rem;
    }


    /* ======================================================
       RODAPÉ
       ====================================================== */

    .footer {
        text-align: center;

        color: #9ca3af;

        font-size: 0.75rem;

        padding-top: 2rem;

        border-top: 1px solid #e5e7eb;

        margin-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONEXÃO COM O BANCO
# ============================================================

@st.cache_resource
def create_database_engine():
    """Cria a conexão com o PostgreSQL."""

    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    port = os.getenv("POSTGRES_PORT", "5432")

    if not all([database, user, password]):
        raise ValueError(
            "Variáveis de conexão com o PostgreSQL não configuradas."
        )

    database_url = (
        f"postgresql+psycopg2://"
        f"{user}:{password}"
        f"@localhost:{port}/{database}"
    )

    return create_engine(database_url)


engine = create_database_engine()


# ============================================================
# CONSULTAS
# ============================================================

@st.cache_data
def load_avg_temperature():
    """Carrega a temperatura média por localização."""

    query = """
        SELECT
            location,
            avg_temperature,
            total_readings
        FROM avg_temp_por_localizacao
        ORDER BY location;
    """

    return pd.read_sql(query, engine)


@st.cache_data
def load_readings_by_hour():
    """Carrega a quantidade de leituras por hora."""

    query = """
        SELECT
            hora,
            total_readings
        FROM leituras_por_hora
        ORDER BY hora;
    """

    return pd.read_sql(query, engine)


@st.cache_data
def load_daily_temperature():
    """Carrega as temperaturas por dia."""

    query = """
        SELECT
            data,
            temperatura_minima,
            temperatura_maxima,
            temperatura_media
        FROM temp_max_min_por_dia
        ORDER BY data;
    """

    return pd.read_sql(query, engine)


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

df_avg = load_avg_temperature()
df_hour = load_readings_by_hour()
df_daily = load_daily_temperature()


# ============================================================
# CÁLCULO DOS INDICADORES
# ============================================================

total_readings = int(df_avg["total_readings"].sum())

avg_temperature = (
    df_avg["avg_temperature"] * df_avg["total_readings"]
).sum() / total_readings

max_temperature = int(df_daily["temperatura_maxima"].max())

min_temperature = int(df_daily["temperatura_minima"].min())

first_date = pd.to_datetime(df_daily["data"].min()).strftime("%d/%m/%Y")

last_date = pd.to_datetime(df_daily["data"].max()).strftime("%d/%m/%Y")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🌡️ Pipeline IoT")

    st.markdown("---")

    st.markdown("### Sobre o projeto")

    st.markdown(
        """
        Pipeline de dados desenvolvido para coleta,
        processamento, armazenamento e visualização
        de dados provenientes de dispositivos IoT.
        """
    )

    st.markdown("### Tecnologias")

    st.markdown(
        """
        - 🐍 Python
        - 🐼 Pandas
        - 🐘 PostgreSQL
        - 🐳 Docker
        - 📊 Plotly
        - 🎈 Streamlit
        """
    )

    st.markdown("---")

    st.markdown("### Período analisado")

    st.markdown(
        f"**{first_date}** até **{last_date}**"
    )

    st.markdown("---")

    st.caption(
        "Pipeline de Dados com IoT e Docker"
    )


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">
        <h1>🌡️ Pipeline de Dados com IoT</h1>
        <p>
            Monitoramento e análise das leituras de temperatura
            provenientes de dispositivos IoT.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.success("● PostgreSQL conectado")

# ============================================================
# INDICADORES
# ============================================================

st.markdown(
    '<div class="section-title">Visão geral</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Principais indicadores encontrados no conjunto de dados.'
    '</div>',
    unsafe_allow_html=True,
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total de leituras",
        value=f"{total_readings:,}".replace(",", "."),
        help="Quantidade total de registros processados.",
    )

with col2:
    st.metric(
        label="🌡️ Temperatura média",
        value=f"{avg_temperature:.2f} °C",
        help="Temperatura média considerando todas as leituras.",
    )

with col3:
    st.metric(
        label="🔥 Temperatura máxima",
        value=f"{max_temperature} °C",
        help="Maior temperatura registrada no dataset.",
    )

with col4:
    st.metric(
        label="❄️ Temperatura mínima",
        value=f"{min_temperature} °C",
        help="Menor temperatura registrada no dataset.",
    )

# ============================================================
# GRÁFICO 1 — EVOLUÇÃO DA TEMPERATURA
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Evolução da temperatura ao longo do tempo'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Temperaturas mínima, média e máxima registradas diariamente.'
    '</div>',
    unsafe_allow_html=True,
)


fig_daily = go.Figure()


fig_daily.add_trace(
    go.Scatter(
        x=df_daily["data"],
        y=df_daily["temperatura_maxima"],
        mode="lines",
        name="Máxima",
        line=dict(width=2),
    )
)


fig_daily.add_trace(
    go.Scatter(
        x=df_daily["data"],
        y=df_daily["temperatura_media"],
        mode="lines",
        name="Média",
        line=dict(width=3),
    )
)


fig_daily.add_trace(
    go.Scatter(
        x=df_daily["data"],
        y=df_daily["temperatura_minima"],
        mode="lines",
        name="Mínima",
        line=dict(width=2),
    )
)


fig_daily.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis=dict(
        title="Data",
        gridcolor="#e5e7eb",
    ),
    yaxis=dict(
        title="Temperatura (°C)",
        gridcolor="#e5e7eb",
    ),
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
)


st.plotly_chart(
    fig_daily,
    use_container_width=True,
)


# ============================================================
# GRÁFICOS 2 E 3 — ANÁLISES COMPLEMENTARES
# ============================================================

col_left, col_right = st.columns(2)


# ============================================================
# GRÁFICO 2 — TEMPERATURA MÉDIA POR LOCALIZAÇÃO
# ============================================================

with col_left:

    st.markdown(
        '<div class="section-title">'
        'Temperatura média por localização'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Comparação entre leituras classificadas como In e Out.'
        '</div>',
        unsafe_allow_html=True,
    )


    fig_avg = px.bar(
        df_avg,
        x="location",
        y="avg_temperature",
        text="avg_temperature",
        labels={
            "location": "Localização",
            "avg_temperature": "Temperatura média (°C)",
        },
    )


    fig_avg.update_traces(
        texttemplate="%{text:.2f} °C",
        textposition="outside",
    )


    fig_avg.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(
            title="Temperatura média (°C)",
            gridcolor="#e5e7eb",
        ),
        xaxis=dict(
            title="",
        ),
    )


    st.plotly_chart(
        fig_avg,
        use_container_width=True,
    )


# ============================================================
# GRÁFICO 3 — LEITURAS POR HORA
# ============================================================

with col_right:

    st.markdown(
        '<div class="section-title">'
        'Distribuição das leituras por hora'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Quantidade de registros realizada em cada hora do dia.'
        '</div>',
        unsafe_allow_html=True,
    )


    fig_hour = px.bar(
        df_hour,
        x="hora",
        y="total_readings",
        labels={
            "hora": "Hora",
            "total_readings": "Leituras",
        },
    )


    fig_hour.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            title="Hora do dia",
            tickmode="linear",
            dtick=1,
        ),
        yaxis=dict(
            title="Quantidade de leituras",
            gridcolor="#e5e7eb",
        ),
    )


    st.plotly_chart(
        fig_hour,
        use_container_width=True,
    )

# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer">
        Pipeline de Dados com IoT e Docker<br>
        Dados provenientes do dataset
        <b>Temperature Readings: IoT Devices</b>.
    </div>
    """,
    unsafe_allow_html=True,
)
