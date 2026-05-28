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
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Minimalista / Light Theme Premium
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
# 2. CARREGAMENTO COM FALLBACK DE PREVIEW AUTOMÁTICO
# ============================================================
@st.cache_data
def carregar_dados():
    csv_path = "achados.csv"
    
    # Se o arquivo existir no GitHub, tenta validar os dados reais
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            # Remove linhas de erros da OpenAI para proteger o layout
            if 'Modelo_IA' in df.columns:
                df = df[~df['Modelo_IA'].astype(str).str.contains('Erro API', case=False, na=False)]
            if 'Evidencia_Visual' in df.columns:
                df = df[~df['Evidencia_Visual'].astype(str).str.contains('Error', case=False, na=False)]
            
            # Se tiver dados reais válidos pós-filtro, usa eles!
            if not df.empty:
                if 'Arquivo_Foto' in df.columns:
                    df['Caminho_Limpo'] = df['Arquivo_Foto'].apply(lambda x: str(x).split('/')[-1] if pd.notna(x) else "")
                    df['Foto_Valida'] = "fotos/" + df['Caminho_Limpo']
                else:
                    df['Foto_Valida'] = None
                return df, "Dados Oficiais de Campo (Produção)"
        except:
            pass

    # SE ESTIVER VAZIO OU SEM ARQUIVO: Entra o Mágico de Oz com imagens reais da web para o Preview
    dados_mock = {
        "Bairro": ["Água Verde", "Água Verde", "Água Verde"],
        "Latitude": [-25.4542, -25.4610, -25.4495],
        "Longitude": [-49.2854, -49.2912, -49.2789],
        "Rua_Imovel": ["Rua Bispo Dom José", "Rua José Cadilhe", "Av. República Argentina"],
        "Numero_Imovel": [2061, 777, 1420],
        "Marca": ["Volkswagen", "Chevrolet", "Ford"],
        "Modelo_IA": ["Fusca 1300", "Opala Comodoro", "Maverick V8"],
        "Evidencia_Visual": [
            "Lanternas traseiras redondas, para-choques cromados lâmina única e vincos originais de capô.",
            "Grade frontal larga com filetes horizontais, coluna C larga típica de cupê e calotas cromadas.",
            "Capô longo com vincos pronunciados, traseira fastback clássica e grade em colmeia."
        ],
        "Lona": ["Não", "Não", "Sim"],
        # Fotos reais do Unsplash para testarmos a coluna de imagem agora mesmo!
        "Foto_Valida": [
            "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=150", 
            "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=150",
            "https://images.unsplash.com/photo-1617469767053-d3b508a0d1e5?w=150"
        ]
    }
    return pd.DataFrame(dados_mock), "Modo Demonstração (Ambiente de Homologação)"

df, status = carregar_dados()

# ============================================================
# 3. INTERFACE PRINCIPAL
# ============================================================
st.title("Urban Barn Find")
st.caption(f"Status do Sistema: **{status}** | Região Alvo: Curitiba, PR")
st.markdown("<br>", unsafe_allow_html=True)

# Bloco de Métricas KPI
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Propriedades Varridas", value="400+", delta="Foco Comercial")
with col2:
    st.metric(label="Ativos Confirmados por IA", value=f"{len(df)}")
with col3:
    lonas = len(df[df["Lona"].str.lower() == "sim"]) if "Lona" in df.columns else 0
    st.metric(label="Veículos Sob Lona", value=f"{lonas}", delta="Visão Computacional")

st.markdown("---")

# Mapa Interativo
st.subheader("Radar de Oportunidades")
centro_lat = df.iloc[0]["Latitude"] if not df.empty else -25.4542
centro_lon = df.iloc[0]["Longitude"] if not df.empty else -49.2854
mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=14, tiles="CartoDB positron")

for _, row in df.iterrows():
    icone = "eye-slash" if row.get("Lona") == "Sim" else "car"
    cor = "black" if row.get("Lona") == "Sim" else "blue"
    
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"<b>{row.get('Marca', '')} {row.get('Modelo_IA', '')}</b><br>{row.get('Rua_Imovel', '')}, nº {row.get('Numero_Imovel', '')}",
        icon=folium.Icon(color=cor, icon=icone, prefix='fa')
    ).add_to(mapa)

folium_static(mapa, width=1200, height=450)

st.markdown("---")

# Tabela Pericial de Evidências com Miniaturas de Imagem
st.subheader("Laudos Periciais Estruturados (GPT-4o Vision)")

colunas_exibicao = ["Foto_Valida", "Marca", "Modelo_IA", "Rua_Imovel", "Numero_Imovel", "Evidencia_Visual", "Lona"]
df_tabela = df[[c for c in colunas_exibicao if c in df.columns]]

st.dataframe(
    df_tabela,
    column_config={
        "Foto_Valida": st.column_config.ImageColumn("Foto de Campo", help="Recorte visual feito pela Lente Sniper"),
        "Marca": "Fabricante",
        "Modelo_IA": "Modelo Identificado",
        "Rua_Imovel": "Logradouro",
        "Numero_Imovel": "Nº",
        "Evidencia_Visual": "Análise de Evidências Visuais",
        "Lona": "Oculto?"
    },
    use_container_width=True,
    hide_index=True
)
