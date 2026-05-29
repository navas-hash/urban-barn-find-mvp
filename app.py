import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import os

# ============================================================
# 1. CONFIGURAÇÃO DE PÁGINA & TEMA ORIGINAL DARK PREMIUM
# ============================================================
st.set_page_config(
    page_title="Urban Barn Find | V12 Tactical",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injeção de CSS focada para NÃO quebrar a visibilidade das tabelas
st.markdown("""
    <style>
    /* Fundo Escuro Industrial */
    .stApp { background-color: #0E1117; }
    
    /* Textos de Markdown e Parágrafos fora de tabelas em Branco */
    .stMarkdown p, .stMarkdown span, caption { color: #FFFFFF !important; }
    
    /* Títulos em Azul Neon Hacker */
    h1, h2, h3, h4 { 
        color: #00D1FF !important; 
        font-family: 'Courier New', monospace !important;
        font-weight: 700 !important; 
    }
    
    /* Cartões das Métricas Originais */
    div[data-testid="metric-container"] {
        background-color: #1A1C24;
        border: 1px solid #2D2F39;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }
    div[data-testid="stMetricValue"] { color: #00D1FF !important; font-size: 36px !important; }
    div[data-testid="stMetricLabel"] { color: #86868B !important; font-size: 12px !important; }
    
    /* Ajuste de Linha Divisória */
    hr { border-top: 1px solid #2D2F39 !important; }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 2. CARREGAMENTO E FILTRAGEM DE DADOS (FOCO EM FUNCIONAMENTO)
# ============================================================
@st.cache_data
def carregar_dados_blindados():
    csv_path = "achados.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # FILTRO ANTI-ERRO: Remove de forma invisível as linhas com falha 429 da API
        if 'Modelo_IA' in df.columns:
            df = df[~df['Modelo_IA'].astype(str).str.contains('Erro API', case=False, na=False)]
        if 'Evidencia_Visual' in df.columns:
            df = df[~df['Evidencia_Visual'].astype(str).str.contains('Error', case=False, na=False)]
            
        # CORREÇÃO DO CAMINHO DAS FOTOS: Remove caminhos do Colab e padroniza para o GitHub
        if 'Arquivo_Foto' in df.columns:
            df['Foto_Visual'] = df['Arquivo_Foto'].apply(
                lambda x: f"fotos/{str(x).split('/')[-1].strip()}" if pd.notna(x) else None
            )
        return df
    return pd.DataFrame()

df = carregar_dados_blindados()

# ============================================================
# 3. INTERFACE E GRÁFICOS (A PERFUMARIA DO CLAUDE DE VOLTA)
# ============================================================
st.title("📡 Urban Barn Find | V12 Tactical Dashboard")
st.markdown("---")

if not df.empty:
    # 4 Cards de Métricas Originais
    total_varredura = 400
    confirmados = len(df)
    taxa_conversao = (confirmados / total_varredura) * 100
    total_lonas = int((df["Lona"].astype(str).str.lower() == "sim").sum()) if "Lona" in df.columns else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ALVOS VARRIDOS", f"{total_varredura}+")
    m2.metric("CONFIRMADOS IA", f"{confirmados}")
    m3.metric("VEÍCULOS SOB LONA", f"{total_lonas}")
    m4.metric("RENDIMENTO EM CAMPO", f"{taxa_conversao:.1f}%")

    st.markdown("---")

    # Bloco de Gráficos Originais (Lado a Lado)
    st.subheader("📊 Volumetria e Estatísticas de Campo")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        df_marcas = df['Marca'].value_counts().reset_index()
        fig_marcas = px.bar(
            df_marcas, x='Marca', y='count',
            title="Modelos Detectados por Fabricante",
            template="plotly_dark",
            color_discrete_sequence=['#00D1FF']
        )
        fig_marcas.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=240)
        fig_marcas.update_xaxes(showgrid=False)
        fig_marcas.update_yaxes(showgrid=False)
        st.plotly_chart(fig_marcas, use_container_width=True)

    with col_g2:
        fig_lona = px.pie(
            df, names='Lona',
            title="Proporção: Veículos Ocultos (Lona)",
            template="plotly_dark",
            hole=0.4,
            color_discrete_sequence=['#2D2F39', '#00D1FF']
        )
        fig_lona.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=240)
        st.plotly_chart(fig_lona, use_container_width=True)

    st.markdown("---")

    # ============================================================
    # 4. MAPA TÁTICO (MODO NOTURNO)
    # ============================================================
    st.subheader("📍 Radar Geográfico de Oportunidades")
    
    centro_lat = df['Latitude'].mean() if 'Latitude' in df.columns else -25.4542
    centro_lon = df['Longitude'].mean() if 'Longitude' in df.columns else -49.2854
    
    m = folium.Map(location=[centro_lat, centro_lon], zoom_start=15, tiles="CartoDB dark_matter")
    
    for _, row in df.iterrows():
        if pd.notna(row.get("Latitude")) and pd.notna(row.get("Longitude")):
            is_lona = str(row.get("Lona", "Não")).strip().lower() == "sim"
            folium.Marker(
                [row["Latitude"], row["Longitude"]],
                popup=f"<b>{row.get('Marca','')} {row.get('Modelo_IA','')}</b>",
                icon=folium.Icon(color="black" if is_lona else "blue", icon="car", prefix="fa")
            ).add_to(m)
            
    folium_static(m, width=1200, height=450)

    st.markdown("---")

    # ============================================================
    # 5. TABELA DE EVIDÊNCIAS (CORREÇÃO DE CONTRASTE E IMAGEM)
    # ============================================================
    st.subheader("📄 Relatório Pericial de Evidências Visuais")
    
    colunas_finais = ["Foto_Visual", "Marca", "Modelo_IA", "Rua_Imovel", "Numero_Imovel", "Evidencia_Visual", "Lona"]
    cols_existentes = [c for c in colunas_finais if c in df.columns]
    
    st.dataframe(
        df[cols_existentes],
        column_config={
            "Foto_Visual": st.column_config.ImageColumn("Visual", width="small"),
            "Evidencia_Visual": st.column_config.TextColumn("Laudo de Análise da IA", width="large"),
            "Marca": "Fabricante",
            "Modelo_IA": "Modelo"
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Aguardando upload do arquivo 'achados.csv' no GitHub...")
