import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import os

# ============================================================
# 1. CONFIGURAÇÃO DE PÁGINA & DESIGN SYSTEM (APPLE HIG)
# ============================================================
st.set_page_config(
    page_title="Urban Barn Find",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para emular uma interface nativa de aplicativo Apple (Light Mode)
st.markdown("""
    <style>
    /* Fundo Canvas da Apple e tipografia do sistema */
    .stApp {
        background-color: #F5F5F7;
        color: #1D1D1F;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Títulos refinados */
    h1, h2, h3 {
        color: #1D1D1F !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    /* Widgets de Métricas (Estilo Ajustado iOS) */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E5EA;
        border-radius: 12px;
        padding: 14px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    div[data-testid="stMetricValue"] {
        color: #1D1D1F !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #86868B !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Divisores sutis */
    hr {
        border: 0;
        border-top: 1px solid #D2D2D7;
        margin: 24px 0;
    }

    /* Customização do Data Grid */
    .stDataFrame {
        border: 1px solid #E5E5EA;
        border-radius: 12px;
        background-color: #FFFFFF;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 2. CARREGAMENTO DE DADOS COM FILTROS INVISÍVEIS
# ============================================================
@st.cache_data
def carregar_dados_oficiais():
    csv_path = "achados.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)

        # Filtro Silencioso: Remove linhas com falhas da API OpenAI
        if 'Modelo_IA' in df.columns:
            df = df[~df['Modelo_IA'].astype(str).str.contains('Erro API', case=False, na=False)]
        if 'Evidencia_Visual' in df.columns:
            df = df[~df['Evidencia_Visual'].astype(str).str.contains('Error', case=False, na=False)]

        # Tratamento do caminho das fotos para ler do repositório local
        if 'Arquivo_Foto' in df.columns:
            def isolar_foto(caminho_completo):
                if pd.isna(caminho_completo): return None
                nome_arquivo = str(caminho_completo).split('/')[-1]
                return f"fotos/{nome_arquivo}"
            
            df['Foto_Visual'] = df['Arquivo_Foto'].apply(isolar_foto)

        return df
    return pd.DataFrame()

df = carregar_dados_oficiais()

# ============================================================
# 3. INTERFACE DO WEB APP
# ============================================================
st.title("Urban Barn Find")
st.caption("Mapeamento Geográfico Inteligente de Ativos Automotivos Raros · Curitiba, PR")
st.markdown("<br>", unsafe_allow_html=True)

if not df.empty:
    # --------------------------------------------------------
    # MÓDULO 1: Linha de Widgets de Métricas (Métricas de Operação)
    # --------------------------------------------------------
    total_varredura = 400
    confirmados = len(df)
    taxa_conversao = (confirmados / total_varredura) * 100
    total_lonas = int((df["Lona"].astype(str).str.lower() == "sim").sum()) if "Lona" in df.columns else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Imóveis Analisados", f"{total_varredura}+")
    with m2:
        st.metric("Alvos Confirmados", f"{confirmados}")
    with m3:
        st.metric("Veículos Sob Lona", f"{total_lonas}")
    with m4:
        st.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")

    st.markdown("<hr>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # MÓDULO 2: Gráficos Discretos (A "Perfumaria" no Estilo Apple)
    # --------------------------------------------------------
    st.subheader("Análise Analítica do Inventário")
    col_g1, col_g2 = st.columns(2)

    # Cor padrão Apple: Azul San Francisco (#0071E3) e tons neutros de cinza
    cor_apple_blue = "#0071E3"
    cor_apple_gray = "#E5E5EA"

    with col_g1:
        # Gráfico de Barras Minimalista (Marcas mais encontradas)
        df_marcas = df['Marca'].value_counts().reset_index()
        fig_marcas = px.bar(
            df_marcas, x='Marca', y='count',
            title="Volume por Fabricante",
            template="plotly_white",
            color_discrete_sequence=[cor_apple_blue]
        )
        fig_marcas.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=220,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="-apple-system, BlinkMacSystemFont, sans-serif",
            font_color="#1D1D1F",
            xaxis_title=None,
            yaxis_title=None
        )
        fig_marcas.update_xaxes(showgrid=False)
        fig_marcas.update_yaxes(showgrid=False)
        st.plotly_chart(fig_marcas, use_container_width=True, config={'displayModeBar': False})

    with col_g2:
        # Gráfico Donut Discreto (Proporção de Lonas)
        fig_lona = px.pie(
            df, names='Lona',
            title="Status de Visibilidade (Ocultos por Lona)",
            template="plotly_white",
            hole=0.6,
            color_discrete_sequence=[cor_apple_gray, cor_apple_blue]
        )
        fig_lona.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=220,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="-apple-system, BlinkMacSystemFont, sans-serif",
            font_color="#1D1D1F"
        )
        st.plotly_chart(fig_lona, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<hr>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # MÓDULO 3: Janela do Mapa (O Herói da Aplicação)
    # --------------------------------------------------------
    st.subheader("Visualização Espacial dos Ativos")
    
    centro_lat = df['Latitude'].mean() if 'Latitude' in df.columns else -25.4542
    centro_lon = df['Longitude'].mean() if 'Longitude' in df.columns else -49.2854
    
    mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=15, tiles="CartoDB positron")

    for _, row in df.iterrows():
        if 'Latitude' in row and 'Longitude' in row and pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            is_lona = str(row.get("Lona", "Não")).strip().lower() == "sim"
            cor_marcador = "black" if is_lona else "blue"
            icone_marcador = "eye-slash" if is_lona else "car"
            
            folium.Marker(
                [row["Latitude"], row["Longitude"]],
                popup=f"<b>{row.get('Marca', '')} {row.get('Modelo_IA', '')}</b><br>{row.get('Rua_Imovel', '')}, nº {row.get('Numero_Imovel', '')}",
                icon=folium.Icon(color=cor_marcador, icon=icone_marcador, prefix="fa")
            ).add_to(mapa)
            
    folium_static(mapa, width=1200, height=450)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # MÓDULO 4: Repositório de Evidências Periciais
    # --------------------------------------------------------
    st.subheader("Painel Pericial de Evidências")
    
    colunas_alvo = ["Foto_Visual", "Marca", "Modelo_IA", "Rua_Imovel", "Numero_Imovel", "Evidencia_Visual", "Lona"]
    colunas_existentes = [c for c in colunas_alvo if c in df.columns]

    st.dataframe(
        df[colunas_existentes],
        column_config={
            "Foto_Visual": st.column_config.ImageColumn("Visual", width="small", help="Captura real isolada pelo algoritmo"),
            "Marca": "Fabricante",
            "Modelo_IA": "Modelo",
            "Rua_Imovel": "Logradouro",
            "Numero_Imovel": "Nº",
            "Evidencia_Visual": "Laudo de Análise Estruturada (GPT-4o)",
            "Lona": "Sob Lona?"
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Aguardando inserção de dados no arquivo 'achados.csv' para inicializar a aplicação.")
