import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os

# CONFIGURAÇÃO DE TEMA DARK
st.set_page_config(
    page_title="Urban Barn Find | Inteligência de Campo",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização Dark "Hacker" Original
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    [data-testid="metric-container"] {
        background-color: #1A1C24;
        border: 1px solid #2D2F39;
        border-radius: 10px;
        padding: 15px;
    }
    .stDataFrame { border: 1px solid #2D2F39; border-radius: 10px; }
    h1, h2, h3 { color: #00D1FF !important; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    csv_path = "achados.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # Limpeza de Erros 429 e outros
        if 'Modelo_IA' in df.columns:
            df = df[~df['Modelo_IA'].astype(str).str.contains('Erro API', case=False, na=False)]
        if 'Evidencia_Visual' in df.columns:
            df = df[~df['Evidencia_Visual'].astype(str).str.contains('Error', case=False, na=False)]
        
        # CORREÇÃO DA IMAGEM: Garante que o caminho aponte para a pasta 'fotos' no GitHub
        if 'Arquivo_Foto' in df.columns:
            df['Foto_Exibicao'] = df['Arquivo_Foto'].apply(
                lambda x: f"fotos/{str(x).split('/')[-1]}" if pd.notna(x) else None
            )
        return df
    return pd.DataFrame()

df = carregar_dados()

st.title("📡 Urban Barn Find | V12 Tactical")
st.markdown("---")

if not df.empty:
    # Contagem de lonas refeita de forma 100% segura e sem colchetes duplos
    if "Lona" in df.columns:
        total_lonas = int((df["Lona"].astype(str).str.lower() == "sim").sum())
    else:
        total_lonas = 0

    # Métricas Estilo Dashboard
    m1, m2, m3 = st.columns(3)
    m1.metric("ALVOS VARRIDOS", "400+")
    m2.metric("CONFIRMADOS", f"{len(df)}")
    m3.metric("SOB LONA", f"{total_lonas}")

    st.markdown("### 📍 Mapa de Localização")
    centro = [-25.4542, -49.2854]
    m = folium.Map(location=centro, zoom_start=15, tiles="CartoDB dark_matter")
    
    for _, row in df.iterrows():
        lona_status = str(row.get("Lona", "Não")).strip().lower()
        cor_marcador = "black" if lona_status == "sim" else "blue"
        icone_marcador = "eye-slash" if lona_status == "sim" else "car"
        
        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup=f"{row.get('Marca', '')} {row.get('Modelo_IA', '')}",
            icon=folium.Icon(color=cor_marcador, icon=icone_marcador, prefix="fa")
        ).add_to(m)
    folium_static(m, width=1200)

    st.markdown("---")
    st.markdown("### 📄 Relatório de Evidências")
    
    colunas_necessarias = ["Foto_Exibicao", "Marca", "Modelo_IA", "Rua_Imovel", "Numero_Imovel", "Evidencia_Visual", "Lona"]
    colunas_existentes = [c for c in colunas_necessarias if c in df.columns]
    
    st.dataframe(
        df[colunas_existentes],
        column_config={
            "Foto_Exibicao": st.column_config.ImageColumn("Visual", width="small"),
            "Evidencia_Visual": st.column_config.TextColumn("Análise da IA", width="large")
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Aguardando sincronização do arquivo 'achados.csv' no GitHub...")
