import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import os
import base64

# ============================================================
# 1. CONFIGURAÇÃO DE PÁGINA & TEMA PREMIUM DARK GRAPHITE
# ============================================================
st.set_page_config(
    page_title="Urban Barn Find | V12 Tactical",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização de alto padrão para Dashboards de Fundos de Investimento
st.markdown("""
    <style>
    /* Fundo Grafite Profundo Moderno */
    .stApp { background-color: #0B0F17; color: #F8FAFC; }
    
    /* Títulos Elegantes */
    h1, h2, h3, h4 { 
        color: #F8FAFC !important; 
        font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }
    
    /* Cartões de Métricas Estilo KPI */
    div[data-testid="metric-container"] {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetricValue"] { color: #0EA5E9 !important; font-size: 32px !important; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #9CA3AF !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Linha divisória */
    hr { border-top: 1px solid #1F2937 !important; margin: 28px 0; }
    
    /* Dataframe customizado */
    .stDataFrame { 
        border: 1px solid #1F2937; 
        border-radius: 12px; 
        background-color: #111827;
        overflow: hidden; 
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 2. MOTOR DE CONVERSÃO BINÁRIA DE IMAGEM (BASE64)
# ============================================================
def converter_foto_para_base64(caminho_original):
    if pd.isna(caminho_original):
        return None
    
    # Isola o nome exato do arquivo (ex: Fiat_147_Taruma_02185.jpg)
    nome_arquivo = str(caminho_original).split('/')[-1].strip()
    caminho_local = f"fotos/{nome_arquivo}"
    
    # Se a foto existir na pasta do GitHub, converte ela em código binário de imagem
    if os.path.exists(caminho_local):
        try:
            with open(caminho_local, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded_string}"
        except:
            return None
    return None

@st.cache_data
def carregar_dados_periciais():
    csv_path = "achados.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # FILTRO ANTI-ERRO: Remove logs de falhas da API
        if 'Modelo_IA' in df.columns:
            df = df[~df['Modelo_IA'].astype(str).str.contains('Erro API', case=False, na=False)]
        if 'Evidencia_Visual' in df.columns:
            df = df[~df['Evidencia_Visual'].astype(str).str.contains('Error', case=False, na=False)]
            
        # Executa a mágica de conversão das fotos
        if 'Arquivo_Foto' in df.columns:
            df['Foto_Visual'] = df['Arquivo_Foto'].apply(converter_foto_para_base64)
            
        return df
    return pd.DataFrame()

df = carregar_dados_periciais()

# ============================================================
# 3. INTERFACE E GRÁFICOS
# ============================================================
st.title("Urban Barn Find")
st.caption("Intelligence Platform · Real Estate & Automotive Asset Scoping · Curitiba, PR")
st.markdown("<br>", unsafe_allow_html=True)

if not df.empty:
    # Métricas Comerciais
    total_varredura = 400
    confirmados = len(df)
    taxa_conversao = (confirmados / total_varredura) * 100
    total_lonas = int((df["Lona"].astype(str).str.lower() == "sim").sum()) if "Lona" in df.columns else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Propriedades Mapeadas", f"{total_varredura}+")
    m2.metric("Ativos Identificados", f"{confirmados}")
    m3.metric("Cobertos por Lona", f"{total_lonas}")
    m4.metric("Eficiência de Campo", f"{taxa_conversao:.1f}%")

    st.markdown("---")

    # Analytics sem a barra de 'Desconhecidos'
    st.subheader("Análise de Distribuição do Inventário")
    col_g1, col_g2 = st.columns(2)

    cor_principal = "#0EA5E9"
    cor_secundaria = "#1F2937"

    with col_g1:
        if 'Marca' in df.columns:
            df_filtrado_marcas = df[df['Marca'].astype(str).str.lower() != 'desconhecido']
            df_marcas = df_filtrado_marcas['Marca'].value_counts().reset_index()
            
            fig_marcas = px.bar(
                df_marcas, x='Marca', y='count',
                title="Modelos Validados por Fabricante",
                template="plotly_dark",
                color_discrete_sequence=[cor_principal]
            )
            fig_marcas.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                height=240, margin=dict(l=10, r=10, t=40, b=10),
                xaxis_title=None, yaxis_title=None
            )
            fig_marcas.update_xaxes(showgrid=False)
            fig_marcas.update_yaxes(showgrid=False)
            st.plotly_chart(fig_marcas, use_container_width=True, config={'displayModeBar': False})

    with col_g2:
        fig_lona = px.pie(
            df, names='Lona',
            title="Acessibilidade Visual do Ativo (Lona)",
            template="plotly_dark",
            hole=0.6,
            color_discrete_sequence=[cor_secundaria, warm_colors:=cor_principal]
        )
        fig_lona.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
            height=240, margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_lona, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # ============================================================
    # 4. MAPA TÁTICO
    # ============================================================
    st.subheader("📍 Disposição Geográfica dos Leads")
    
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
    # 5. TABELA COM RENDERIZAÇÃO DIRETA VIA BINÁRIO
    # ============================================================
    st.subheader("📄 Relatório Pericial Estruturado")
    
    colunas_finais = ["Foto_Visual", "Marca", "Modelo_IA", "Rua_Imovel", "Numero_Imovel", "Evidencia_Visual", "Lona"]
    cols_existentes = [c for c in colunas_finais if c in df.columns]
    
    st.dataframe(
        df[cols_existentes],
        column_config={
            "Foto_Visual": st.column_config.ImageColumn("Visual", width="small"),
            "Evidencia_Visual": st.column_config.TextColumn("Laudo Pericial (OpenAI Vision)", width="large"),
            "Marca": "Fabricante",
            "Modelo_IA": "Modelo"
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Aguardando upload do arquivo 'achados.csv' no GitHub...")
