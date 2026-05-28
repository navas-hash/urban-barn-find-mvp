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
            # Extrai apenas o nome do arquivo (ex: foto_1.jpg) e adiciona o prefixo da pasta
            df['Foto_Exibicao'] = df['Arquivo_Foto'].apply(
                lambda x: f"fotos/{str(x).split('/')[-1]}" if pd.notna(x) else None
            )
        return df
    return pd.DataFrame()

df = carregar_dados()

st.title("📡 Urban Barn Find | V12 Tactical")
st.markdown("---")

if not df.empty:
    # Métricas Estilo Dashboard
    m1, m2, m3 = st.columns(3)
    m1.metric("ALVOS VARRIDOS", "400+")
    m2.metric("CONFIRMADOS", f"{len(df)}")
    lonas = len(df[df["Lona"] ==
