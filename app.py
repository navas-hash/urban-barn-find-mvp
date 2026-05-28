import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os

# ============================================================
# 1. CONFIGURAÇÃO E DESIGN SYSTEM (APPLE HIG)
# ============================================================
st.set_page_config(
    page_title="Urban Barn Find | Investor Dashboard",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Minimalista / Light Theme / Responsivo
st.markdown("""
    <style>
    /* Fundo Off-white e tipografia limpa */
    .stApp { background-color: #F5F5F7; color: #1D1D1F; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* Cards das Métricas */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02), 0 1px 3px rgba(0,0,0,0.04);
        text-align: center;
    }
    div[data-testid="stMetricValue"] { font-size: 36px; font-weight: 700; color: #1D1D1F; }
    div[data-testid="stMetricLabel"] { font-size: 14px; color: #86868B; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Títulos e Divisores */
    h1, h2, h3 { color: #1D1D1F; font-weight: 600; }
    hr { border-top: 1px solid #D2D2D7; margin: 2rem 0; }
    
    /* Tabela Responsiva */
    .stDataFrame { border-radius: 14px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 2. CARREGAMENTO E LIMPEZA DOS DADOS (FILTRO ANTI-ERRO)
# ============================================================
@st.cache_data
def carregar_dados():
    csv_path = "achados.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # FILTRO SILENCIOSO: Remove qualquer linha que seja Erro de API da OpenAI
        if 'Modelo_IA' in df.columns:
            df = df[~df['Modelo_IA'].astype(str).str.contains('Erro API', case=False, na=False)]
        if 'Evidencia_Visual' in df.columns:
            df = df[~df['Evidencia_Visual'].astype(str).str.contains('Error', case=False, na=False)]
        
        # TRATAMENTO DE IMAGEM: Arruma o caminho da foto para o Streamlit ler a pasta local
        if 'Arquivo_Foto' in df.columns:
            # Troca o caminho do Colab pelo caminho relativo da pasta do GitHub
            df['Caminho_Limpo'] = df['Arquivo_Foto'].apply(
                lambda x: str(x).split('/')[-1] if pd.notna(x) else ""
            )
            df['Foto_Exibicao'] = "fotos/" + df['Caminho_Limpo']
            
        return df, "Dados Oficiais de Campo"
    
    return pd.DataFrame(), "Aguardando Sincronização..."

df, status = carregar_dados()

# ============================================================
# 3. INTERFACE DO PAINEL (CABEÇALHO E MÉTRICAS)
# ============================================================
st.title("Urban Barn Find")
st.caption(f"Status do Motor: **{status}** | Bairro Alvo: Água Verde, Curitiba")
st.markdown("<br>", unsafe_allow_html=True)

if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Propriedades Analisadas", value="400+")
    with col2:
        st.metric(label="Ativos Raros Encontrados", value=f"{len(df)}")
    with col3:
        lonas = len(df[df["Lona"] == "Sim"]) if "Lona" in df.columns else 0
        st.metric(label="Veículos Ocultos (Lona)", value=f"{lonas}")

    st.markdown("---")

    # ============================================================
    # 4. MAPA TÁTICO
    # ============================================================
    st.subheader("Radar de Ativos")
    
    # Pega o centro do mapa baseado no primeiro carro achado
    centro_lat = df.iloc[0]["Latitude"] if pd.notna(df.iloc[0]["Latitude"]) else -25.4542
    centro_lon = df.iloc[0]["Longitude"] if pd.notna(df.iloc[0]["Longitude"]) else -49.2854
    
    mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=15, tiles="CartoDB positron")

    for _, row in df.iterrows():
        if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
            icone = "eye-slash" if row.get("Lona") == "Sim" else "car"
            cor = "black" if row.get("Lona") == "Sim" else "blue"
            
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=folium.Popup(f"<b>{row.get('Marca', '')} {row.get('Modelo_IA', '')}</b><br>{row.get('Rua_Imovel', '')}, {row.get('Numero_Imovel', '')}", max_width=250),
                icon=folium.Icon(color=cor, icon=icone, prefix='fa')
            ).add_to(mapa)

    folium_static(mapa, width=1200, height=500)

    st.markdown("---")

    # ============================================================
    # 5. LAUDOS COM FOTOS REAIS (DATA EDITOR DO STREAMLIT)
    # ============================================================
    st.subheader("Evidências Periciais (GPT-4o Vision)")
    
    # Verifica se a pasta fotos existe e se o arquivo está nela para não quebrar o site
    df['Foto_Valida'] = df['Foto_Exibicao'].apply(lambda x: x if os.path.exists(x) else None)
    
    colunas_exibicao = ["Foto_Valida", "Marca", "Modelo_IA", "Rua_Imovel", "Numero_Imovel", "Evidencia_Visual", "Lona"]
    df_tabela = df[[c for c in colunas_exibicao if c in df.columns]].copy()
    
    # Exibe a tabela com a coluna de imagem renderizada magicamente
    st.dataframe(
        df_tabela,
        column_config={
            "Foto_Valida": st.column_config.ImageColumn("Foto de Campo", help="Captura do Google Street View"),
            "Marca": "Fabricante",
            "Modelo_IA": "Modelo",
            "Rua_Imovel": "Logradouro",
            "Numero_Imovel": "Nº",
            "Evidencia_Visual": "Laudo da IA",
            "Lona": "Sob Lona?"
        },
        use_container_width=True,
        hide_index=True,
        height=400
    )

else:
    st.info("Nenhum ativo detectado ainda ou aguardando upload do arquivo achados.csv.")
