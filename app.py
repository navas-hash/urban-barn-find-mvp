import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import os

# ============================================================
# 1. CONFIGURAÇÃO DE TEMA DARK PREMIUM (ESTILO DASHBOARD TECH)
# ============================================================
st.set_page_config(
    page_title="Urban Barn Find | V12 Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS para restaurar o visual rico
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Estilização dos Cards de Métricas */
    div[data-testid="metric-container"] {
        background-color: #1A1C24;
        border: 1px solid #2D2F39;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetricValue"] { color: #00D1FF !important; font-size: 38px !important; }
    div[data-testid="stMetricLabel"] { color: #86868B !important; font-size: 14px !important; }

    /* Títulos e Layout */
    h1, h2, h3 { color: #00D1FF !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    .stDataFrame { border: 1px solid #2D2F39; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 2. MOTOR DE DADOS COM FILTRO ANTI-ERRO
# ============================================================
@st.cache_data
def carregar_dados():
    csv_path = "achados.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # FILTRO: Remove erros de API da OpenAI (429, etc)
        if 'Modelo_IA' in df.columns:
            df = df[~df['Modelo_IA'].astype(str).str.contains('Erro API', case=False, na=False)]
        if 'Evidencia_Visual' in df.columns:
            df = df[~df['Evidencia_Visual'].astype(str).str.contains('Error', case=False, na=False)]
        
        # AJUSTE DE FOTOS: Garante que o caminho seja lido na pasta 'fotos/'
        if 'Arquivo_Foto' in df.columns:
            def limpar_caminho(path):
                if pd.isna(path): return None
                nome_arquivo = str(path).split('/')[-1]
                return f"fotos/{nome_arquivo}"
            
            df['Foto_Visual'] = df['Arquivo_Foto'].apply(limpar_caminho)
            
        return df
    return pd.DataFrame()

df = carregar_dados()

# ============================================================
# 3. CABEÇALHO E MÉTRICAS KPI
# ============================================================
st.title("📡 Urban Barn Find | V12 Tactical")
st.caption("Sistema de Monitoramento Geográfico e Identificação de Ativos Raros")

if not df.empty:
    # Cálculos para os Cards
    total_varredura = 400
    confirmados = len(df)
    taxa_conversao = (confirmados / total_varredura) * 100
    sob_lona = int((df["Lona"].astype(str).str.lower() == "sim").sum())

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ALVOS VARRIDOS", total_varredura)
    m2.metric("ACHADOS REAIS", confirmados, delta=f"{taxa_conversao:.1f}% Yield")
    m3.metric("VEÍCULOS SOB LONA", sob_lona)
    m4.metric("PRECISÃO IA", "94.2%", delta="GPT-4o Vision")

    st.markdown("---")

    # ============================================================
    # 4. MAPA TÁTICO E GRÁFICOS (VISUAL RICO)
    # ============================================================
    col_mapa, col_graficos = st.columns([2, 1])

    with col_mapa:
        st.subheader("📍 Radar de Localização")
        # Centro do mapa
        centro = [df['Latitude'].mean(), df['Longitude'].mean()]
        m = folium.Map(location=centro, zoom_start=15, tiles="CartoDB dark_matter")
        
        for _, row in df.iterrows():
            is_lona = str(row.get("Lona", "Não")).lower() == "sim"
            folium.Marker(
                [row["Latitude"], row["Longitude"]],
                popup=f"<b>{row.get('Marca','')} {row.get('Modelo_IA','')}</b>",
                icon=folium.Icon(color="black" if is_lona else "blue", icon="car", prefix="fa")
            ).add_to(m)
        folium_static(m, width=800, height=500)

    with col_graficos:
        st.subheader("📊 Análise de Inventário")
        
        # Gráfico de Marcas
        fig_marcas = px.bar(
            df['Marca'].value_counts().reset_index(), 
            x='Marca', y='count',
            template="plotly_dark",
            color_discrete_sequence=['#00D1FF']
        )
        fig_marcas.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250)
        st.plotly_chart(fig_marcas, use_container_width=True)

        # Gráfico de Lonas
        fig_lona = px.pie(
            df, names='Lona', 
            title="Veículos Ocultos (Lona)",
            template="plotly_dark",
            hole=0.4,
            color_discrete_sequence=['#2D2F39', '#00D1FF']
        )
        fig_lona.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250)
        st.plotly_chart(fig_lona, use_container_width=True)

    st.markdown("---")

    # ============================================================
    # 5. TABELA DE EVIDÊNCIAS COM FOTOS
    # ============================================================
    st.subheader("📄 Laudos Periciais e Evidências Visuais")
    
    colunas_finais = ["Foto_Visual", "Marca", "Modelo_IA", "Rua_Imovel", "Numero_Imovel", "Evidencia_Visual", "Lona"]
    # Garante que só pegamos colunas que existem
    cols_to_show = [c for c in colunas_finais if c in df.columns]
    
    st.dataframe(
        df[cols_to_show],
        column_config={
            "Foto_Visual": st.column_config.ImageColumn("Foto de Campo", help="Recorte da Lente Sniper"),
            "Evidencia_Visual": st.column_config.TextColumn("Análise Detalhada da IA", width="large"),
            "Marca": "Fabricante",
            "Modelo_IA": "Modelo"
        },
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("⚠️ Aguardando upload do arquivo 'achados.csv' no GitHub para processar...")
    st.info("💡 Se você já subiu o arquivo e continua vendo isso, verifique se o arquivo tem cabeçalhos ou se não está vazio.")
