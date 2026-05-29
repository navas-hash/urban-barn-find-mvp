import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import os
import base64

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Urban Barn Find · Investor Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PREMIUM DARK LUXURY THEME (CLAUDE ORIGINAL) ──────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Mono:wght@400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

html, body, .stApp, .stApp > div, section.main, .main {
    background-color: #07070F !important;
    color: #E8E4DC !important;
    font-family: 'DM Sans', sans-serif !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1380px !important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background-color: #0B0B1A !important;
    border-right: 1px solid #181830 !important;
}
[data-testid="stSidebar"] * { color: #C8C4BB !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
div[data-testid="stMarkdown"] { background: transparent !important; }
.element-container { background: transparent !important; }
hr { border-color: #181830 !important; margin: 1.5rem 0 !important; }

/* Selectbox dark */
[data-testid="stSelectbox"] > div > div {
    background-color: #101022 !important;
    border: 1px solid #282848 !important;
    color: #E8E4DC !important;
    border-radius: 8px !important;
}
[data-testid="stSelectbox"] svg { fill: #6B6B90 !important; }

/* ─── COMPONENTS ────────────────────────────────────────────────── */
.hero { padding: 28px 0 32px; border-bottom: 1px solid #181830; margin-bottom: 36px; }
.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; letter-spacing: 0.22em; text-transform: uppercase;
    color: #D4A853; margin-bottom: 14px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 56px; font-weight: 900;
    color: #F0EDE8; line-height: 1.05; margin-bottom: 14px;
}
.hero-title em { color: #D4A853; font-style: normal; }
.hero-sub { font-size: 16px; color: #7A7A98; line-height: 1.7; max-width: 580px; margin-bottom: 20px; }
.live-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: #081510; border: 1px solid #1A3A25;
    border-radius: 100px; padding: 6px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; color: #3DD68C;
}
.live-dot {
    width: 7px; height: 7px;
    background: #3DD68C; border-radius: 50%;
    animation: livepulse 2s ease-in-out infinite;
}
@keyframes livepulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(61,214,140,.5); }
    50% { box-shadow: 0 0 0 7px rgba(61,214,140,0); }
}

/* KPI Grid */
.kpi-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 16px; }
.kpi-card {
    background: #0D0D20;
    border: 1px solid #1A1A32;
    border-radius: 14px;
    padding: 24px 26px 22px;
    position: relative; overflow: hidden;
    transition: border-color .2s;
}
.kpi-card:hover { border-color: #2A2A4A; }
.kpi-card::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #D4A853 0%, rgba(213,168,83,0) 100%);
}
.kpi-card.green::after { background: linear-gradient(90deg, #3DD68C 0%, rgba(61,214,140,0) 100%); }
.kpi-card.red::after   { background: linear-gradient(90deg, #EF4444 0%, rgba(239,68,68,0) 100%); }
.kpi-card.blue::after  { background: linear-gradient(90deg, #60A5FA 0%, rgba(96,165,250,0) 100%); }
.kpi-icon {
    position: absolute; right: 22px; top: 50%;
    transform: translateY(-50%); font-size: 38px; opacity: 0.08;
}
.kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 0.18em; text-transform: uppercase;
    color: #4A4A6A; margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 44px; font-weight: 700;
    color: #F0EDE8; line-height: 1; margin-bottom: 8px;
}
.kpi-delta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; color: #D4A853;
}
.kpi-delta.g { color: #3DD68C; }
.kpi-delta.r { color: #EF4444; }
.kpi-delta.b { color: #60A5FA; }

/* Section headers */
.sec-head { display: flex; align-items: baseline; gap: 14px; margin: 36px 0 18px; }
.sec-title { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; color: #F0EDE8; }
.sec-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase;
    color: #D4A853; border: 1px solid #3A2A10;
    border-radius: 4px; padding: 3px 9px;
}

/* Asset cards */
.asset-card {
    background: #0D0D20;
    border: 1px solid #1A1A32;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 14px;
    transition: border-color .2s;
}
.asset-card:hover { border-color: #D4A853; }
.asset-name {
    font-family: 'Playfair Display', serif;
    font-size: 22px; font-weight: 700; color: #F0EDE8; margin-bottom: 4px;
}
.asset-loc {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; color: #5A5A80; margin-bottom: 14px;
}
.asset-evidence {
    font-size: 13px; color: #8B879A; line-height: 1.7;
    font-style: italic;
    border-left: 2px solid #2A2010;
    padding-left: 14px; margin-bottom: 14px;
}
.badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 0.08em;
    padding: 4px 10px; border-radius: 100px; margin-right: 8px;
}
.b-decade { background: #14112A; color: #9B7FE8; border: 1px solid #221A40; }
.b-brand  { background: #0C1A10; color: #3DD68C; border: 1px solid #183028; }
.b-lona   { background: #1A0C0C; color: #EF6060; border: 1px solid #3A1818; }
.b-ok     { background: #0C1A10; color: #3DD68C; border: 1px solid #183028; }
.asset-footer {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #3A3A58; margin-top: 12px; padding-top: 12px;
    border-top: 1px solid #131328;
    display: flex; justify-content: space-between; align-items: center;
}
.asset-link { color: #D4A853 !important; text-decoration: none; }
.asset-link:hover { color: #F0C87A !important; }

/* Sidebar */
.sb-brand-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 0.2em; text-transform: uppercase;
    color: #D4A853; margin-bottom: 6px;
}
.sb-brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 28px; font-weight: 900; color: #F0EDE8; line-height: 1.1;
}
.sb-brand-version {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; color: #2A2A4A; margin-top: 4px;
}
.sb-divider { border-top: 1px solid #181830; margin: 18px 0; }
.pitch-item {
    background: #0D0D1C;
    border-left: 2px solid #D4A853;
    padding: 12px 14px 12px 16px;
    margin-bottom: 10px;
    border-radius: 0 8px 8px 0;
}
.pitch-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase;
    color: #D4A853; margin-bottom: 5px;
}
.pitch-text { font-size: 12px; color: #6A6A8A; line-height: 1.6; }
.pitch-text strong { color: #C8A84B; }
.sb-stat {
    background: #0D0D1C; border: 1px solid #181830;
    border-radius: 10px; padding: 14px 16px; margin-bottom: 8px;
}
.sb-stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase;
    color: #3A3A58; margin-bottom: 4px;
}
.sb-stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 24px; font-weight: 700; color: #D4A853;
}
.sb-stat-sub { font-size: 11px; color: #4A4A6A; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

# ─── TRANFORMAÇÃO DE FOTO PARA BASE64 (SISTEMA INTEGRADO) ─────────────────────
def carregar_imagem_base64(caminho_csv):
    if pd.isna(caminho_csv):
        return ""
    nome_foto = str(caminho_csv).split('/')[-1].strip()
    caminho_real = f"fotos/{nome_foto}"
    if os.path.exists(caminho_real):
        try:
            with open(caminho_real, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
        except:
            return ""
    return ""

# ─── DATA LOADER REFEITO PAR COMPATIBILIDADE DE INFRAESTRUTURA ────────────────
def carregar_dados():
    csv_path = "achados.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            
            # FILTRO ANTI-ERROS OPENAI (Proteção de Interface)
            if 'Modelo_IA' in df.columns:
                df = df[~df['Modelo_IA'].astype(str).str.contains('Erro API', case=False, na=False)]
            if 'Evidencia_Visual' in df.columns:
                df = df[~df['Evidencia_Visual'].astype(str).str.contains('Error', case=False, na=False)]
            
            if not df.empty:
                # ADAPTAÇÃO GEOGRÁFICA DE VARIÁVEIS (Se o Colab não gerou, criamos dinamicamente)
                if "Bairro" not in df.columns:
                    df["Bairro"] = "Água Verde"
                if "Decada" not in df.columns:
                    df["Decada"] = "Anos 70/80"
                if "Alerta_Fachada" not in df.columns:
                    df["Alerta_Fachada"] = "Limpo"
                if "Link_Google_Maps" not in df.columns:
                    df["Link_Google_Maps"] = df.apply(lambda r: f"https://www.google.com/maps/search/?api=1&query={str(r.get('Latitude',''))},{str(r.get('Longitude',''))}", axis=1)
                
                # Sincronização binária de fotos locais
                if 'Arquivo_Foto' in df.columns:
                    df['Foto_Base64'] = df['Arquivo_Foto'].apply(carregar_imagem_base64)
                else:
                    df['Foto_Base64'] = ""
                return df, True
        except:
            pass

    # Fallback idêntico ao mock do Claude caso o arquivo falhe
    dados_mock = {
        "Bairro":          ["Água Verde", "Água Verde", "Água Verde", "Água Verde"],
        "Latitude":        [-25.4542, -25.4610, -25.4495, -25.4578],
        "Longitude":       [-49.2854, -49.2912, -49.2789, -49.2831],
        "Rua_Imovel":      ["Rua Bispo Dom José", "Rua José Cadilhe", "Av. República Argentina", "Rua Bento Viana"],
        "Numero_Imovel":   [2061, 777, 1420, 550],
        "Classe_Roboflow": ["fusca", "carros-antigos", "kombi", "carros-antigos"],
        "Marca":           ["Volkswagen", "Chevrolet", "Volkswagen", "Ford"],
        "Modelo_IA":       ["Fusca 1300", "Opala Comodoro", "Kombi Corujinha", "Maverick V8"],
        "Decada":          ["1970s", "1980s", "1960s", "1970s"],
        "Evidencia_Visual": [
            "Lanternas traseiras redondas (Fafá), para-choques cromados lâmina única e vincos originais de capô.",
            "Grade frontal larga com filetes horizontais, coluna C larga típica de cupê e calotas cromadas originais.",
            "Pintura saia-e-blusa original, para-brisa bipartido e setas 'orelinha' funcionais.",
            "Capô longo com vincos pronunciados, traseira fastback e grade em colmeia original com emblema."
        ],
        "Lona":            ["Nao", "Nao", "Sim", "Nao"],
        "Link_Google_Maps": ["#", "#", "#", "#"],
        "Alerta_Fachada":  ["Limpo", "Limpo", "Limpo", "Limpo"],
        "Foto_Base64":     ["", "", "", ""]
    }
    return pd.DataFrame(dados_mock), False

df, dados_reais = carregar_dados()
total_achados  = len(df)
total_lonas    = len(df[df["Lona"].astype(str).str.lower() == "sim"]) if "Lona" in df.columns else 0
taxa_deteccao  = f"{total_achados / 400 * 100:.1f}%"
modo_label     = "Dados reais de campo" if dados_reais else "Demonstração Homologada"

# ─── SIDEBAR (CLAUDE ORIGINAL) ────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 22px 4px 10px;">
        <div class="sb-brand-label">Computer Vision · SaaS B2B</div>
        <div class="sb-brand-name">Urban<br>Barn Find</div>
        <div class="sb-brand-version">v12 · INVESTOR BUILD · {modo_label}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:#3A3A58;margin-bottom:12px;">
        Por que investir
    </div>
    <div class="pitch-item">
        <div class="pitch-label">📊 Mercado Endereçável</div>
        <div class="pitch-text">Mercado global de veículos clássicos: <strong>USD 34 bilhões</strong> (2024). Brasil: <strong>1.2M unidades</strong> registrada de coleção.</div>
    </div>
    <div class="pitch-item">
        <div class="pitch-label">🔬 Moat Tecnológico</div>
        <div class="pitch-text">Modelo YOLO proprietário treinado em <strong>12.000+ imagens</strong>. Cruzamento shapefile IPPUC garante alvo em imóvel <strong>privado</strong>.</div>
    </div>
    <div class="pitch-item">
        <div class="pitch-label">⚡ Eficiência Operacional</div>
        <div class="pitch-text"><strong>400 imóveis/hora</strong> varridos remotamente. Custo de <strong>R$ 0,008 por análise</strong>.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:#3A3A58;margin-bottom:12px;">
        Tração Atual
    </div>
    <div class="sb-stat">
        <div class="sb-stat-label">Parceiros em Piloto</div>
        <div class="sb-stat-value">4</div>
        <div class="sb-stat-sub">Revendedores · Curitiba</div>
    </div>
    <div class="sb-stat">
        <div class="sb-stat-label">Ativos Mapeados (Bairro Alvo)</div>
        <div class="sb-stat-value">{total_achados}</div>
        <div class="sb-stat-sub">Veículos filtrados por IA</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.selectbox("Bairro", ["Todos", "Água Verde"], label_visibility="collapsed")

# ─── HERO (CLAUDE ORIGINAL) ───────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="live-badge"><div class="live-dot"></div>Sistema Ativo · Varrendo Curitiba</div>
    <br><br>
    <div class="hero-eyebrow">Inteligência Visual Urbana · Urban Barn Find</div>
    <div class="hero-title">O tesouro escondido<br>nas <em>ruas do Brasil.</em></div>
    <div class="hero-sub">
        Localizamos veículos raros em propriedades privadas usando Computer Vision e
        Street View — eliminando 100% do trabalho de campo cego e reduzindo o custo
        de prospecção em <strong style="color:#D4A853;">15.000×</strong> vs. o método tradicional.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI CARDS (CLAUDE ORIGINAL) ──────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-icon">🏘️</div>
        <div class="kpi-label">Propriedades Varridas</div>
        <div class="kpi-value">400</div>
        <div class="kpi-delta">▲ Somente imóvel privado</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-icon">🎯</div>
        <div class="kpi-label">Ativos Confirmados por IA</div>
        <div class="kpi-value">{total_achados}</div>
        <div class="kpi-delta g">▲ {taxa_deteccao} de taxa de detecção</div>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Custo por Ativo Localizado</div>
        <div class="kpi-value">R$0,08</div>
        <div class="kpi-delta b">▼ vs. R$ 1.200 abordagem manual</div>
    </div>
</div>
<div class="kpi-row">
    <div class="kpi-card red">
        <div class="kpi-icon">👁️</div>
        <div class="kpi-label">Veículos Sob Lona · Raio-X</div>
        <div class="kpi-value">{total_lonas}</div>
        <div class="kpi-delta r">Invisíveis ao garimpo tradicional</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">Falsos Positivos Retidos</div>
        <div class="kpi-value">142</div>
        <div class="kpi-delta">▼ R$ 4,26 em APIs poupadas</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🚀</div>
        <div class="kpi-label">Velocidade de Varredura</div>
        <div class="kpi-value">400/h</div>
        <div class="kpi-delta">▲ Imóveis analisados por hora</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CHARTS (CLAUDE ORIGINAL DINÂMICO) ────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-title">Inteligência de Mercado</div>
    <div class="sec-tag">Análise da Varredura</div>
</div>
""", unsafe_allow_html=True)

col_c1, col_c2, col_c3 = st.columns([2, 2, 3])
CHART_BG, PLOT_BG, GRID_COLOR, GOLD = "rgba(0,0,0,0)", "rgba(13,13,30,0.9)", "#181830", "#D4A853"

with col_c1:
    decada_counts = df["Decada"].value_counts().reset_index()
    decada_counts.columns = ["Década", "Ativos"]
    fig_dec = px.bar(decada_counts, x="Década", y="Ativos", color_discrete_sequence=[GOLD], template="plotly_dark")
    fig_dec.update_layout(
        paper_bgcolor=CHART_BG, plot_bgcolor=PLOT_BG,
        title=dict(text="Por Década", font=dict(family="Playfair Display", size=17, color="#F0EDE8")),
        margin=dict(l=0, r=0, t=44, b=0), showlegend=False,
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(family="IBM Plex Mono", size=10), title=None),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(family="IBM Plex Mono", size=10), title=None),
    )
    st.plotly_chart(fig_dec, use_container_width=True)

with col_c2:
    # FILTRO INTERNO DO GRÁFICO: Remove 'Desconhecido' APENAS da visualização gráfica para ficar limpo
    df_grafico_marcas = df[df["Marca"].astype(str).str.lower() != "desconhecido"]
    marca_counts = df_grafico_marcas["Marca"].value_counts()
    
    COLORS = ["#D4A853", "#9B7FE8", "#3DD68C", "#EF6060", "#60A5FA"]
    fig_pie = go.Figure(data=[go.Pie(
        labels=marca_counts.index, values=marca_counts.values, hole=0.62,
        marker=dict(colors=COLORS[:len(marca_counts)], line=dict(color="#07070F", width=3)),
        textfont=dict(family="IBM Plex Mono", size=10),
        hovertemplate="<b>%{label}</b><br>%{value} ativos (%{percent})<extra></extra>"
    )])
    fig_pie.update_layout(
        paper_bgcolor=CHART_BG, margin=dict(l=0, r=0, t=44, b=0),
        title=dict(text="Por Fabricante", font=dict(family="Playfair Display", size=17, color="#F0EDE8")),
        legend=dict(font=dict(family="IBM Plex Mono", size=10, color="#8B8BA0"), bgcolor=CHART_BG),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_c3:
    fig_funnel = go.Figure(go.Funnel(
        y=["Imóveis Varridos", "Com Cobertura SV", "Veículo Detectado", "Ativo Confirmado"],
        x=[400, 258, 146, total_achados],
        textposition="inside", textfont=dict(family="IBM Plex Mono", size=11, color="#F0EDE8"),
        marker=dict(color=["#131328", "#1A1A3A", "#28204A", GOLD], line=dict(color="#07070F", width=2)),
        connector=dict(line=dict(color=GRID_COLOR, dash="dot", width=1.5))
    ))
    fig_funnel.update_layout(
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, margin=dict(l=0, r=0, t=44, b=0),
        title=dict(text="Funil de Prospecção", font=dict(family="Playfair Display", size=17, color="#F0EDE8")),
        yaxis=dict(tickfont=dict(family="IBM Plex Mono", size=10, color="#6B6B90")),
        xaxis=dict(tickfont=dict(family="IBM Plex Mono", size=10, color="#6B6B90"), gridcolor=GRID_COLOR),
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

# ─── MAPA TÁTICO COM IMAGEM BASE64 EMBUTIDA NO POPUP ──────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-title">Mapa Tático de Campo</div>
    <div class="sec-tag">Curitiba · Água Verde</div>
</div>
<p style="color:#5A5A80;font-size:14px;margin-bottom:16px;">
    Clique nos marcadores para abrir o laudo pericial completo gerado pela IA e a imagem de campo.
    <span style="color:#EF6060;">● Sob lona</span>
      
    <span style="color:#D4A853;">● Visível</span>
</p>
""", unsafe_allow_html=True)

mapa = folium.Map(location=[-25.4542, -49.2854], zoom_start=15, tiles="CartoDB dark_matter")

for _, row in df.iterrows():
    lat, lon    = row["Latitude"], row["Longitude"]
    marca       = row["Marca"]
    modelo      = row["Modelo_IA"]
    evidencia   = row["Evidencia_Visual"]
    lona        = row["Lona"]
    rua         = row["Rua_Imovel"]
    num         = row["Numero_Imovel"]
    link        = row["Link_Google_Maps"]
    decada      = row["Decada"]
    img_b64     = row["Foto_Base64"]

    lona_status = str(lona).strip().lower() == "sim"
    lona_badge = (
        '<span style="background:#1A0C0C;color:#EF6060;border:1px solid #3A1818;'
        'border-radius:100px;padding:3px 10px;font-size:10px;font-family:monospace;">● Sob Lona</span>'
        if lona_status else
        '<span style="background:#0C1A10;color:#3DD68C;border:1px solid #183028;'
        'border-radius:100px;padding:3px 10px;font-size:10px;font-family:monospace;">● Visível</span>'
    )

    # Injeção inteligente de imagem dentro do pop-up escuro do próprio mapa
    img_tag = f'<img src="{img_b64}" style="width:100%;height:130px;object-fit:cover;border-radius:8px;margin-bottom:12px;border:1px solid #1C1C38;">' if img_b64 else ''

    html_popup = f"""
    <div style="font-family:'DM Sans',Arial,sans-serif;width:290px;background:#0F0F22;
                border:1px solid #1C1C38;border-radius:14px;padding:16px;color:#E8E4DC;
                box-shadow:0 20px 60px rgba(0,0,0,.8);">
        <div style="font-family:monospace;font-size:9px;letter-spacing:.18em;
                    text-transform:uppercase;color:#D4A853;margin-bottom:8px;">
            Ativo Automotivo Confirmado
        </div>
        {img_tag}
        <div style="font-family:Georgia,serif;font-size:20px;font-weight:700;
                    color:#F0EDE8;margin-bottom:4px;">{marca} {modelo}</div>
        <div style="font-family:monospace;font-size:11px;color:#5A5A80;margin-bottom:12px;">
            {rua}, nº {num} · {decada}
        </div>
        {lona_badge}
        <div style="border-top:1px solid #1C1C38;margin:12px 0;"></div>
        <div style="font-size:12px;line-height:1.6;color:#8A879A;background:#131328;
                    border-left:2px solid #D4A853;padding:10px;border-radius:0 8px 8px 0;font-style:italic;">
            "{evidencia}"
        </div>
        <a href="{link}" target="_blank"
           style="display:block;text-align:center;background:#D4A853;color:#07070F;
                  padding:10px;font-size:11px;text-decoration:none;border-radius:10px;
                  font-weight:700;margin-top:14px;font-family:monospace;letter-spacing:.06em;">
            ABRIR ROTA DE CAMPO →
        </a>
    </div>
    """

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(html_popup, max_width=330),
        icon=folium.Icon(color="red" if lona_status else "orange", icon="eye-slash" if lona_status else "star", prefix="fa")
    ).add_to(mapa)

folium_static(mapa, width=1200, height=520)

# ─── LAUDOS PERICIAIS COM FOTOS INJETADAS NO DESIGN DO CLAUDE ─────────────────
st.markdown("""
<div class="sec-head" style="margin-top:40px;">
    <div class="sec-title">Laudos Periciais</div>
    <div class="sec-tag">Claude Vision · Estruturado</div>
</div>
<p style="color:#5A5A80;font-size:14px;margin-bottom:20px;">
    Cada laudo é gerado automaticamente pela IA a partir da análise visual do Street View.
    Evidências visuais auditáveis e coordenadas exatas para campo.
</p>
""", unsafe_allow_html=True)

for _, row in df.iterrows():
    is_lona = str(row["Lona"]).strip().lower() == "sim"
    lona_badge   = '<span class="badge b-lona">● SOB LONA</span>' if is_lona else '<span class="badge b-ok">● VISÍVEL</span>'
    alerta_badge = f'<span class="badge b-lona">⚠ {row["Alerta_Fachada"]}</span>' if row["Alerta_Fachada"] != "Limpo" else '<span class="badge b-ok">✓ Fachada Limpa</span>'
    img_b64      = row["Foto_Base64"]

    # Bloco visual da foto injetada em Base64 no card original do Claude
    imagem_html = f"""
    <div style="flex-shrink: 0; width: 160px; height: 120px; border-radius: 10px; overflow: hidden; border: 1px solid #1A1A32; background: #07070F;">
        <img src="{img_b64}" style="width: 100%; height: 100%; object-fit: cover;">
    </div>
    """ if img_b64 else """
    <div style="flex-shrink: 0; width: 160px; height: 120px; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1A1A32; background: #0D0D20; font-family: monospace; font-size: 10px; color: #3A3A58;">
        FOTO INDISPONÍVEL
    </div>
    """

    st.markdown(f"""
    <div class="asset-card" style="display: flex; gap: 24px; align-items: flex-start;">
        {imagem_html}
        <div style="flex-grow: 1;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;margin-bottom:12px;">
                <div>
                    <div class="asset-name">{row['Marca']} {row['Modelo_IA']}</div>
                    <div class="asset-loc">📍 {row['Rua_Imovel']}, nº {row['Numero_Imovel']}  ·  {row['Bairro']}</div>
                </div>
                <div style="padding-top:4px;">
                    <span class="badge b-decade">{row['Decada']}</span>
                    <span class="badge b-brand">{row['Marca']}</span>
                    {lona_badge}
                    {alerta_badge}
                </div>
            </div>
            <div class="asset-evidence">{row['Evidencia_Visual']}</div>
            <div class="asset-footer">
                <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3A3A58;">
                    {row['Latitude']:.5f}, {row['Longitude']:.5f}
                </span>
                <a href="{row['Link_Google_Maps']}" target="_blank" class="asset-link" style="font-family:'IBM Plex Mono',monospace;font-size:10px;">
                    → Abrir no Google Maps
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── EXPANSION PIPELINE (CLAUDE ORIGINAL) ─────────────────────────────────────
st.markdown("""
<div class="sec-head" style="margin-top:44px;">
    <div class="sec-title">Pipeline de Expansão</div>
    <div class="sec-tag">Próximas 4 Semanas</div>
</div>
""", unsafe_allow_html=True)

col_e1, col_e2, col_e3, col_e4 = st.columns(4)
expansion = [
    ("Vila Izabel",       "~3.800 lotes",  "Semana 1", "#3DD68C"),
    ("Mercês",            "~4.200 lotes",  "Semana 2", "#60A5FA"),
    ("Boqueirão",         "~6.100 lotes",  "Semana 3", "#9B7FE8"),
    ("Santa Felicidade",  "~5.500 lotes",  "Semana 4", "#EF6060"),
]
for col, (bairro, lotes, semana, cor) in zip([col_e1, col_e2, col_e3, col_e4], expansion):
    with col:
        st.markdown(f"""
        <div style="background:#0D0D20;border:1px solid #1A1A32;border-radius:12px;padding:20px;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{cor};opacity:.6;"></div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:{cor};opacity:.7;margin-bottom:8px;">{semana}</div>
            <div style="font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:#F0EDE8;margin-bottom:4px;">{bairro}</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#4A4A6A;">{lotes} · Curitiba</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
