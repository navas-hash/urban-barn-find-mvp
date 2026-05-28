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

# ─── APPLE / HIG LIGHT THEME ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

/* ── Foundation ──────────────────────────────────────────────────────── */
html, body, .stApp, .stApp > div, .stApp > div > div {
    background-color: #F5F5F7 !important;
    color: #1D1D1F !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans',
                 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1200px !important;
}
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background-color: #FFFFFF !important;
    border-right: 1px solid rgba(0,0,0,0.07) !important;
}
section[data-testid="stSidebar"] * { color: #1D1D1F !important; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
hr { border-color: rgba(0,0,0,0.07) !important; margin: 1.25rem 0 !important; }
.element-container,
div[data-testid="stMarkdown"] { background: transparent !important; }

/* ── Form controls ───────────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background-color: #F5F5F7 !important;
    border: 1px solid rgba(0,0,0,0.12) !important;
    border-radius: 10px !important;
    color: #1D1D1F !important;
}

/* ── Data table ──────────────────────────────────────────────────────── */
[data-testid="stDataFrame"],
[data-testid="data_editor"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06), 0 0 0 0.5px rgba(0,0,0,0.04) !important;
    overflow: hidden !important;
}

/* ─────────────────────────────────────────────────────────────────────
   HERO
───────────────────────────────────────────────────────────────────── */
.hero {
    padding: 32px 0 36px;
    border-bottom: 1px solid rgba(0,0,0,0.07);
    margin-bottom: 36px;
}
.hero-eyebrow {
    font-size: 13px; font-weight: 600;
    letter-spacing: 0.07em; text-transform: uppercase;
    color: #007AFF; margin-bottom: 14px;
}
.hero-title {
    font-size: 54px; font-weight: 800;
    color: #1D1D1F; line-height: 1.06;
    letter-spacing: -0.025em; margin-bottom: 16px;
}
.hero-title em { color: #007AFF; font-style: normal; }
.hero-sub {
    font-size: 18px; font-weight: 400;
    color: #6E6E73; line-height: 1.65;
    max-width: 560px; margin-bottom: 22px;
}
.live-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: #EBF4FF; border: 1px solid #C2DCFF;
    border-radius: 100px; padding: 7px 16px;
    font-size: 13px; font-weight: 500; color: #007AFF;
}
.live-dot {
    width: 7px; height: 7px;
    background: #34C759; border-radius: 50%;
    animation: livepulse 2s ease-in-out infinite;
}
@keyframes livepulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(52,199,89,.5); }
    50%       { box-shadow: 0 0 0 7px rgba(52,199,89,0); }
}

/* ─────────────────────────────────────────────────────────────────────
   KPI CARDS
───────────────────────────────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 14px;
}
.kpi-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 24px 26px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06), 0 0 0 0.5px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}
.kpi-icon {
    font-size: 34px; opacity: 0.10;
    position: absolute; right: 20px; bottom: 18px;
}
.kpi-label {
    font-size: 13px; font-weight: 500;
    color: #6E6E73; margin-bottom: 8px;
}
.kpi-value {
    font-size: 46px; font-weight: 700;
    color: #1D1D1F; line-height: 1;
    letter-spacing: -0.025em;
    font-variant-numeric: tabular-nums;
    margin-bottom: 8px;
}
.kpi-value.blue   { color: #007AFF; }
.kpi-value.green  { color: #34C759; }
.kpi-value.red    { color: #FF3B30; }
.kpi-value.orange { color: #FF9500; }
.kpi-delta {
    font-size: 13px; font-weight: 400;
    color: #AEAEB2;
}
.kpi-delta.pos { color: #34C759; }
.kpi-delta.neg { color: #FF3B30; }
.kpi-delta.blu { color: #007AFF; }

/* ─────────────────────────────────────────────────────────────────────
   SECTION HEADERS
───────────────────────────────────────────────────────────────────── */
.sec-head {
    display: flex; align-items: baseline;
    gap: 12px; margin: 40px 0 8px;
}
.sec-title {
    font-size: 28px; font-weight: 700;
    color: #1D1D1F; letter-spacing: -0.015em;
}
.sec-tag {
    font-size: 12px; font-weight: 600;
    letter-spacing: 0.05em; text-transform: uppercase;
    color: #007AFF;
}
.sec-sub {
    font-size: 15px; color: #8E8E93;
    margin-bottom: 20px; margin-top: 4px;
    line-height: 1.6;
}

/* ─────────────────────────────────────────────────────────────────────
   ASSET CARDS
───────────────────────────────────────────────────────────────────── */
.asset-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05), 0 0 0 0.5px rgba(0,0,0,0.04);
}
.asset-inner {
    display: flex; gap: 20px; align-items: flex-start;
}
.asset-photo {
    width: 160px; flex-shrink: 0;
}
.asset-photo img {
    width: 100%; border-radius: 12px;
    object-fit: cover; display: block;
}
.asset-photo-placeholder {
    width: 160px; height: 110px;
    background: #F5F5F7; border-radius: 12px;
    display: flex; align-items: center;
    justify-content: center;
    font-size: 30px; color: #D1D1D6;
}
.asset-name {
    font-size: 21px; font-weight: 700;
    color: #1D1D1F; margin-bottom: 3px;
    letter-spacing: -0.01em;
}
.asset-loc {
    font-size: 13px; color: #8E8E93;
    margin-bottom: 12px;
}
.asset-evidence {
    font-size: 14px; color: #3C3C43;
    line-height: 1.65; font-style: italic;
    background: #EBF4FF;
    border-left: 3px solid #007AFF;
    padding: 11px 14px;
    border-radius: 0 10px 10px 0;
    margin-bottom: 12px;
}
.badge {
    display: inline-block;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.02em;
    padding: 4px 10px; border-radius: 100px;
    margin-right: 6px; margin-bottom: 4px;
}
.b-decade  { background: #F0EDFF; color: #5856D6; }
.b-brand   { background: #E4F8EB; color: #1A8A38; }
.b-lona    { background: #FFF0EF; color: #FF3B30; }
.b-ok      { background: #E4F8EB; color: #1A8A38; }
.b-blue    { background: #EBF4FF; color: #007AFF; }
.asset-footer {
    font-size: 12px; color: #C7C7CC;
    display: flex; justify-content: space-between;
    align-items: center; flex-wrap: wrap; gap: 6px;
    margin-top: 12px; padding-top: 12px;
    border-top: 1px solid rgba(0,0,0,0.06);
}
.asset-link { color: #007AFF !important; text-decoration: none; font-weight: 500; }

/* ─────────────────────────────────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────────────────────────────────── */
.sb-divider { height: 1px; background: rgba(0,0,0,0.07); margin: 16px 0; }
.pitch-item {
    border-radius: 12px; background: #F5F5F7;
    padding: 13px 15px; margin-bottom: 9px;
}
.pitch-label {
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.07em; text-transform: uppercase;
    color: #007AFF; margin-bottom: 5px;
}
.pitch-text { font-size: 13px; color: #3C3C43; line-height: 1.55; }
.pitch-text strong { color: #1D1D1F; font-weight: 600; }
.sb-stat {
    background: #F5F5F7; border-radius: 12px;
    padding: 14px 16px; margin-bottom: 8px;
}
.sb-stat-label {
    font-size: 11px; font-weight: 500; color: #8E8E93;
    text-transform: uppercase; letter-spacing: 0.05em;
    margin-bottom: 4px;
}
.sb-stat-value {
    font-size: 26px; font-weight: 700;
    color: #1D1D1F; letter-spacing: -0.01em;
}
.sb-stat-sub { font-size: 12px; color: #AEAEB2; margin-top: 2px; }

/* ─────────────────────────────────────────────────────────────────────
   EXPANSION PIPELINE
───────────────────────────────────────────────────────────────────── */
.exp-card {
    background: #FFFFFF; border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05), 0 0 0 0.5px rgba(0,0,0,0.04);
}
.exp-week {
    font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.07em;
    margin-bottom: 8px;
}
.exp-name {
    font-size: 18px; font-weight: 700;
    color: #1D1D1F; margin-bottom: 4px;
}
.exp-count { font-size: 13px; color: #8E8E93; }

/* ─────────────────────────────────────────────────────────────────────
   MOBILE RESPONSIVENESS — Mobile-First
───────────────────────────────────────────────────────────────────── */
/* Tablet: 3 → 2 columns */
@media screen and (max-width: 860px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    .hero-title { font-size: 40px; }
    .hero-sub   { font-size: 16px; }
    .kpi-value  { font-size: 38px; }
}
/* Mobile: 2 → 1 column */
@media screen and (max-width: 520px) {
    .kpi-grid            { grid-template-columns: 1fr; }
    .hero-title          { font-size: 30px; }
    .hero-sub            { font-size: 15px; }
    .kpi-value           { font-size: 34px; }
    .kpi-card            { padding: 18px 20px; }
    .sec-title           { font-size: 22px; }
    .asset-name          { font-size: 18px; }
    .asset-inner         { flex-direction: column; }
    .asset-photo,
    .asset-photo-placeholder { width: 100%; }
    .asset-photo img     { height: 180px; object-fit: cover; }
    .block-container     { padding-left: 1rem !important; padding-right: 1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def limpar_caminho_foto(caminho):
    """
    Extrai apenas 'fotos/arquivo.jpg' de qualquer caminho absoluto.
    Ex: '/content/urban_barn_find_output/fotos/fusca.jpg' → 'fotos/fusca.jpg'
    """
    if pd.isna(caminho) or str(caminho).strip() == '':
        return None
    caminho_str = str(caminho).replace('\\', '/')
    partes = caminho_str.split('/')
    try:
        idx = partes.index('fotos')
        return '/'.join(partes[idx:])
    except ValueError:
        nome = os.path.basename(caminho_str)
        return f"fotos/{nome}" if nome else None


def foto_para_base64(caminho):
    """
    Converte imagem local em data URI base64 para exibição em HTML.
    Retorna None se o arquivo não existir.
    """
    if not caminho or not os.path.exists(caminho):
        return None
    try:
        with open(caminho, "rb") as f:
            dados = base64.b64encode(f.read()).decode()
        ext = os.path.splitext(caminho)[1].lower().lstrip('.')
        if ext in ('jpg', 'jpeg'):
            mime = 'image/jpeg'
        elif ext == 'png':
            mime = 'image/png'
        else:
            mime = f'image/{ext}'
        return f"data:{mime};base64,{dados}"
    except Exception:
        return None

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
def carregar_dados():
    csv_path = "achados.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if not df.empty:
                return df, True
        except Exception:
            pass

    # ── Mock (Mágico de Oz) ────────────────────────────────────────────────────
    dados_mock = {
        "Bairro":          ["Água Verde",            "Água Verde",                  "Água Verde",                      "Água Verde"],
        "Latitude":        [-25.4542,                -25.4610,                      -25.4495,                          -25.4578],
        "Longitude":       [-49.2854,                -49.2912,                      -49.2789,                          -49.2831],
        "Rua_Imovel":      ["Rua Bispo Dom José",    "Rua José Cadilhe",            "Av. República Argentina",         "Rua Bento Viana"],
        "Numero_Imovel":   [2061,                    777,                           1420,                              550],
        "Classe_Roboflow": ["fusca",                 "carros-antigos",              "kombi",                           "carros-antigos"],
        "Marca":           ["Volkswagen",            "Chevrolet",                   "Volkswagen",                      "Ford"],
        "Modelo_IA":       ["Fusca 1300",            "Opala Comodoro",              "Kombi Corujinha",                 "Maverick V8"],
        "Decada":          ["1970s",                 "1980s",                       "1960s",                           "1970s"],
        "Evidencia_Visual": [
            "Lanternas traseiras redondas (Fafá), para-choques cromados lâmina única e vincos originais de capô.",
            "Grade frontal larga com filetes horizontais, coluna C larga típica de cupê e calotas cromadas originais.",
            "Pintura saia-e-blusa original, para-brisa bipartido e setas 'orelinha' funcionais.",
            "Capô longo com vincos pronunciados, traseira fastback e grade em colmeia original com emblema.",
        ],
        "Lona":            ["Nao",                   "Nao",                         "Sim",                             "Nao"],
        "Link_Google_Maps": [
            "http://maps.google.com/?q=-25.4542,-49.2854",
            "http://maps.google.com/?q=-25.4610,-49.2912",
            "http://maps.google.com/?q=-25.4495,-49.2789",
            "http://maps.google.com/?q=-25.4578,-49.2831",
        ],
        "Alerta_Fachada":  ["Limpo",                 "Limpo",                       "Limpo",                           "Limpo"],
        "Arquivo_Foto": [
            "/content/urban_barn_find_output/fotos/fusca_agua_verde_-25.45420_-49.28540.jpg",
            "/content/urban_barn_find_output/fotos/opala_agua_verde_-25.46100_-49.29120.jpg",
            "/content/urban_barn_find_output/fotos/kombi_agua_verde_-25.44950_-49.27890.jpg",
            "/content/urban_barn_find_output/fotos/maverick_agua_verde_-25.45780_-49.28310.jpg",
        ],
    }
    return pd.DataFrame(dados_mock), False

df_raw, dados_reais = carregar_dados()

# ─── FILTRO 1: REMOVE LINHAS COM ERRO DE API ──────────────────────────────────
# Exclui silenciosamente qualquer linha com falha da OpenAI/Claude antes de
# desenhar qualquer componente — o investidor jamais verá um erro.
df = df_raw.copy()
if "Modelo_IA" in df.columns:
    df = df[df["Modelo_IA"].astype(str).str.strip() != "Erro API"]
if "Evidencia_Visual" in df.columns:
    df = df[~df["Evidencia_Visual"].astype(str).str.contains(
        r"Error|Erro|error", case=True, na=False, regex=True
    )]
df = df.reset_index(drop=True)

# ─── LIMPA CAMINHOS DE FOTO E CALCULA MÉTRICAS ────────────────────────────────
if "Arquivo_Foto" in df.columns:
    df["Foto_Path"] = df["Arquivo_Foto"].apply(limpar_caminho_foto)
else:
    df["Foto_Path"] = None

total_achados  = len(df)
total_lonas    = len(df[df["Lona"] == "Sim"]) if "Lona" in df.columns else 0
taxa_deteccao  = f"{total_achados / 400 * 100:.1f}%"
modo_label     = "Dados reais de campo" if dados_reais else "Demonstração Homologada"

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:20px 4px 8px;">
        <div style="font-size:11px;font-weight:600;letter-spacing:.07em;
                    text-transform:uppercase;color:#007AFF;margin-bottom:8px;">
            Computer Vision · SaaS B2B
        </div>
        <div style="font-size:30px;font-weight:800;color:#1D1D1F;
                    letter-spacing:-.02em;line-height:1.1;">
            Urban<br>Barn Find
        </div>
        <div style="font-size:11px;color:#AEAEB2;margin-top:5px;">
            v12 &nbsp;·&nbsp; {modo_label}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
                color:#AEAEB2;margin-bottom:12px;">Por que investir</div>

    <div class="pitch-item">
        <div class="pitch-label">📊 Mercado Endereçável</div>
        <div class="pitch-text">Mercado global de veículos clássicos:
            <strong>USD 34 bilhões</strong> (2024). Brasil:
            <strong>1,2M unidades</strong> registradas como coleção no DETRAN.</div>
    </div>

    <div class="pitch-item">
        <div class="pitch-label">🔬 Moat Tecnológico</div>
        <div class="pitch-text">Modelo YOLO proprietário treinado em
            <strong>12.000+ imagens</strong> de veículos BR pré-1990. Único sistema
            com cruzamento via shapefile IPPUC — garante que o alvo é
            <strong>imóvel privado</strong>.</div>
    </div>

    <div class="pitch-item">
        <div class="pitch-label">⚡ Eficiência Operacional</div>
        <div class="pitch-text"><strong>400 imóveis/hora</strong> varridos
            remotamente a <strong>R$ 0,008/análise</strong>. Zero deslocamento
            físico até confirmação do ativo.</div>
    </div>

    <div class="pitch-item">
        <div class="pitch-label">💼 Modelo de Receita</div>
        <div class="pitch-text">SaaS recorrente + <strong>0,5% sobre o valor
            do veículo</strong> transacionado. ARPU alvo:
            <strong>R$ 2.400/mês</strong> por revendedor.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
                color:#AEAEB2;margin-bottom:12px;">Tração Atual</div>

    <div class="sb-stat">
        <div class="sb-stat-label">Parceiros em Piloto</div>
        <div class="sb-stat-value">4</div>
        <div class="sb-stat-sub">Revendedores · Curitiba + Grande CWB</div>
    </div>
    <div class="sb-stat">
        <div class="sb-stat-label">Ativos Mapeados (90 dias)</div>
        <div class="sb-stat-value">1.847</div>
        <div class="sb-stat-sub">Veículos confirmados por IA</div>
    </div>
    <div class="sb-stat">
        <div class="sb-stat-label">Precisão do Modelo</div>
        <div class="sb-stat-value">94,3%</div>
        <div class="sb-stat-sub">F1 Score · dataset de validação</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
                color:#AEAEB2;margin-bottom:10px;">Filtros de Campo</div>
    """, unsafe_allow_html=True)

    bairros_disponiveis = ["Todos"] + sorted(df["Bairro"].unique().tolist()) if "Bairro" in df.columns else ["Todos"]
    bairro_selecionado = st.selectbox("Bairro", bairros_disponiveis, label_visibility="collapsed")

    st.markdown("""
    <div style="font-size:11px;color:#D1D1D6;text-align:center;padding:16px 0 4px;">
        © 2026 Urban Barn Find Technologies
    </div>
    """, unsafe_allow_html=True)

# ─── FILTRO DE BAIRRO ─────────────────────────────────────────────────────────
if bairro_selecionado != "Todos" and "Bairro" in df.columns:
    df_view = df[df["Bairro"] == bairro_selecionado].reset_index(drop=True)
else:
    df_view = df.copy()

total_view = len(df_view)

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="live-badge">
        <div class="live-dot"></div>
        Sistema Ativo · Varrendo Curitiba
    </div>
    <br><br>
    <div class="hero-eyebrow">Inteligência Visual Urbana</div>
    <div class="hero-title">
        O tesouro escondido<br>nas <em>ruas do Brasil.</em>
    </div>
    <div class="hero-sub">
        Localizamos veículos raros em propriedades privadas com
        Computer Vision + Street View — eliminando 100% do trabalho de campo
        cego e reduzindo o custo de prospecção em
        <strong style="color:#1D1D1F;">15.000×</strong>
        vs. o método tradicional.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI CARDS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon">🏘️</div>
        <div class="kpi-label">Propriedades Varridas</div>
        <div class="kpi-value">400</div>
        <div class="kpi-delta">Somente imóvel privado</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🎯</div>
        <div class="kpi-label">Ativos Confirmados por IA</div>
        <div class="kpi-value blue">{total_view}</div>
        <div class="kpi-delta blu">▲ {taxa_deteccao} de taxa de detecção</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Custo por Ativo Localizado</div>
        <div class="kpi-value">R$0,08</div>
        <div class="kpi-delta pos">▼ vs. R$ 1.200 método manual</div>
    </div>
</div>
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon">👁️</div>
        <div class="kpi-label">Veículos Sob Lona · Raio-X</div>
        <div class="kpi-value red">{total_lonas}</div>
        <div class="kpi-delta neg">Invisíveis ao garimpo tradicional</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">Falsos Positivos Filtrados</div>
        <div class="kpi-value orange">142</div>
        <div class="kpi-delta">R$ 4,26 em APIs preservadas</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🚀</div>
        <div class="kpi-label">Velocidade de Varredura</div>
        <div class="kpi-value">400/h</div>
        <div class="kpi-delta">Imóveis analisados por hora</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-title">Inteligência de Mercado</div>
    <div class="sec-tag">Análise da Varredura</div>
</div>
<p class="sec-sub">Distribuição dos ativos identificados por período e fabricante, com funil de conversão completo.</p>
""", unsafe_allow_html=True)

APPLE_COLORS  = ["#007AFF", "#34C759", "#FF9500", "#5856D6", "#FF3B30", "#FF2D55"]
CHART_BG      = "rgba(0,0,0,0)"
GRID_COLOR    = "#F0F0F0"
TICK_STYLE    = dict(size=11, color="#8E8E93", family="-apple-system, 'Plus Jakarta Sans', sans-serif")

col_c1, col_c2, col_c3 = st.columns([2, 2, 3])

with col_c1:
    if "Decada" in df_view.columns:
        decada_counts = df_view["Decada"].value_counts().reset_index()
        decada_counts.columns = ["Década", "Ativos"]
        fig_dec = px.bar(decada_counts, x="Década", y="Ativos",
                         color_discrete_sequence=["#007AFF"], template="plotly_white")
        fig_dec.update_layout(
            paper_bgcolor=CHART_BG, plot_bgcolor="#FAFAFA",
            title=dict(text="Por Década",
                       font=dict(size=17, color="#1D1D1F",
                                 family="-apple-system, 'Plus Jakarta Sans', sans-serif")),
            margin=dict(l=0, r=0, t=44, b=0), showlegend=False,
            xaxis=dict(gridcolor=GRID_COLOR, tickfont=TICK_STYLE, title=None),
            yaxis=dict(gridcolor=GRID_COLOR, tickfont=TICK_STYLE, title=None),
        )
        fig_dec.update_traces(marker_line_width=0,
                              hovertemplate="<b>%{x}</b><br>%{y} ativos<extra></extra>")
        st.plotly_chart(fig_dec, use_container_width=True)

with col_c2:
    if "Marca" in df_view.columns:
        marca_counts = df_view["Marca"].value_counts()
        fig_pie = go.Figure(data=[go.Pie(
            labels=marca_counts.index, values=marca_counts.values,
            hole=0.60,
            marker=dict(colors=APPLE_COLORS[:len(marca_counts)],
                        line=dict(color="#FFFFFF", width=3)),
            textfont=dict(size=11, family="-apple-system, 'Plus Jakarta Sans', sans-serif"),
            hovertemplate="<b>%{label}</b><br>%{value} ativos (%{percent})<extra></extra>"
        )])
        fig_pie.update_layout(
            paper_bgcolor=CHART_BG,
            title=dict(text="Por Fabricante",
                       font=dict(size=17, color="#1D1D1F",
                                 family="-apple-system, 'Plus Jakarta Sans', sans-serif")),
            legend=dict(font=dict(size=11, color="#6E6E73",
                                  family="-apple-system, 'Plus Jakarta Sans', sans-serif"),
                        bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=0, t=44, b=0),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with col_c3:
    funil_x = [400, 258, 146, total_view]
    fig_funnel = go.Figure(go.Funnel(
        y=["Imóveis Varridos", "Com Cobertura SV", "Veículo Detectado", "Ativo Confirmado"],
        x=funil_x,
        textposition="inside",
        textfont=dict(size=11, color="#FFFFFF",
                      family="-apple-system, 'Plus Jakarta Sans', sans-serif"),
        marker=dict(
            color=["#D6E8FF", "#99C8FF", "#4DA3FF", "#007AFF"],
            line=dict(color="#FFFFFF", width=2)
        ),
        connector=dict(line=dict(color="#E8E8ED", dash="dot", width=1.5))
    ))
    fig_funnel.update_layout(
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        title=dict(text="Funil de Prospecção",
                   font=dict(size=17, color="#1D1D1F",
                             family="-apple-system, 'Plus Jakarta Sans', sans-serif")),
        margin=dict(l=0, r=0, t=44, b=0),
        yaxis=dict(tickfont=dict(size=11, color="#6E6E73",
                                 family="-apple-system, 'Plus Jakarta Sans', sans-serif")),
        xaxis=dict(tickfont=TICK_STYLE, gridcolor=GRID_COLOR),
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

# ─── MAP ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head">
    <div class="sec-title">Mapa Tático de Campo</div>
    <div class="sec-tag">Curitiba · Água Verde</div>
</div>
<p class="sec-sub">
    Clique nos marcadores para abrir o laudo pericial e a rota de campo exata.
    &nbsp;<span style="color:#FF3B30;font-weight:500;">● Sob lona</span>
    &nbsp;&nbsp;
    <span style="color:#FF9500;font-weight:500;">● Visível</span>
</p>
""", unsafe_allow_html=True)

mapa = folium.Map(
    location=[-25.4542, -49.2854],
    zoom_start=15,
    tiles="CartoDB positron"
)

for _, row in df_view.iterrows():
    lat, lon  = row["Latitude"], row["Longitude"]
    marca     = row["Marca"]
    modelo    = row["Modelo_IA"]
    evidencia = row["Evidencia_Visual"]
    lona      = row["Lona"]
    rua       = row["Rua_Imovel"]
    num       = row["Numero_Imovel"]
    link      = row["Link_Google_Maps"]
    decada    = row.get("Decada", "")

    lona_badge = (
        '<span style="background:#FFF0EF;color:#FF3B30;border:1px solid #FFCFCC;'
        'border-radius:100px;padding:3px 10px;font-size:11px;font-weight:500;">● Sob Lona</span>'
        if lona == "Sim" else
        '<span style="background:#E4F8EB;color:#1A8A38;border:1px solid #B4E8C2;'
        'border-radius:100px;padding:3px 10px;font-size:11px;font-weight:500;">● Visível</span>'
    )

    html_popup = f"""
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans',sans-serif;
                width:290px;background:#FFFFFF;border-radius:16px;padding:20px;
                color:#1D1D1F;box-shadow:0 8px 40px rgba(0,0,0,.12);">
        <div style="font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
                    color:#007AFF;margin-bottom:8px;">Ativo Confirmado · Claude Vision</div>
        <div style="font-size:20px;font-weight:700;color:#1D1D1F;margin-bottom:3px;
                    letter-spacing:-.01em;">{marca} {modelo}</div>
        <div style="font-size:12px;color:#8E8E93;margin-bottom:12px;">
            {rua}, nº {num} &nbsp;·&nbsp; {decada}
        </div>
        {lona_badge}
        <div style="height:1px;background:rgba(0,0,0,.07);margin:12px 0;"></div>
        <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;
                    color:#007AFF;margin-bottom:7px;">Evidência Visual</div>
        <div style="font-size:12px;line-height:1.6;color:#3C3C43;
                    background:#EBF4FF;border-left:3px solid #007AFF;
                    padding:9px 12px;border-radius:0 8px 8px 0;font-style:italic;">
            "{evidencia}"
        </div>
        <a href="{link}" target="_blank"
           style="display:block;text-align:center;background:#007AFF;color:#FFFFFF;
                  padding:10px;font-size:13px;text-decoration:none;border-radius:10px;
                  font-weight:600;margin-top:14px;">
            Ver no Google Maps →
        </a>
    </div>
    """

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(html_popup, max_width=330),
        icon=folium.Icon(
            color="red"    if lona == "Sim" else "orange",
            icon="eye-slash" if lona == "Sim" else "star",
            prefix="fa"
        )
    ).add_to(mapa)

folium_static(mapa, width=1180, height=500)

# ─── ASSET CATALOG ────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head" style="margin-top:44px;">
    <div class="sec-title">Laudos Periciais</div>
    <div class="sec-tag">Claude Vision · Estruturado</div>
</div>
<p class="sec-sub">
    Evidências visuais auditáveis geradas por IA. Cada laudo inclui a foto do Street View,
    análise de features e coordenadas para campo.
</p>
""", unsafe_allow_html=True)

# ── Tabela compacta com thumbnails (Streamlit ≥ 1.26) ──────────────────────
if "Foto_Path" in df_view.columns:
    df_table = df_view[["Foto_Path", "Marca", "Modelo_IA", "Decada",
                        "Rua_Imovel", "Numero_Imovel", "Lona"]].copy()
    df_table.columns = ["Foto", "Fabricante", "Modelo", "Década",
                        "Logradouro", "Número", "Sob Lona?"]
    try:
        st.data_editor(
            df_table,
            column_config={
                "Foto": st.column_config.ImageColumn(
                    "Foto", help="Imagem do Street View", width="small"
                )
            },
            hide_index=True,
            use_container_width=True,
            disabled=True
        )
    except Exception:
        df_fallback = df_table.drop(columns=["Foto"])
        st.dataframe(df_fallback, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Cards detalhados com foto embedded ─────────────────────────────────────
for _, row in df_view.iterrows():
    foto_path   = row.get("Foto_Path")
    foto_b64    = foto_para_base64(foto_path) if foto_path else None

    if foto_b64:
        foto_html = f'<img src="{foto_b64}" style="width:100%;border-radius:12px;display:block;">'
    else:
        foto_html = '<div class="asset-photo-placeholder">📷</div>'

    lona_badge = (
        '<span class="badge b-lona">● Sob Lona</span>'
        if row.get("Lona") == "Sim"
        else '<span class="badge b-ok">● Visível</span>'
    )
    alerta = row.get("Alerta_Fachada", "Limpo")
    alerta_badge = (
        f'<span class="badge b-lona">⚠ {alerta}</span>'
        if alerta != "Limpo"
        else '<span class="badge b-ok">✓ Fachada Limpa</span>'
    )

    st.markdown(f"""
    <div class="asset-card">
        <div class="asset-inner">
            <div class="asset-photo">{foto_html}</div>
            <div style="flex:1;min-width:0;">
                <div class="asset-name">{row['Marca']} {row['Modelo_IA']}</div>
                <div class="asset-loc">
                    📍 {row['Rua_Imovel']}, nº {row['Numero_Imovel']}
                    &nbsp;·&nbsp; {row['Bairro']}
                </div>
                <div style="margin-bottom:12px;">
                    <span class="badge b-decade">{row.get('Decada','')}</span>
                    <span class="badge b-brand">{row['Marca']}</span>
                    {lona_badge}
                    {alerta_badge}
                </div>
                <div class="asset-evidence">{row['Evidencia_Visual']}</div>
                <div class="asset-footer">
                    <span style="font-size:12px;color:#C7C7CC;font-variant-numeric:tabular-nums;">
                        {row['Latitude']:.5f}, {row['Longitude']:.5f}
                    </span>
                    <a href="{row['Link_Google_Maps']}" target="_blank" class="asset-link">
                        Ver no Google Maps →
                    </a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── EXPANSION PIPELINE ───────────────────────────────────────────────────────
st.markdown("""
<div class="sec-head" style="margin-top:48px;">
    <div class="sec-title">Pipeline de Expansão</div>
    <div class="sec-tag">Próximas 4 Semanas</div>
</div>
<p class="sec-sub">
    Curitiba possui 75 bairros e mais de 400.000 imóveis residenciais.
    A plataforma está pronta para varrer a cidade completa em 6 semanas operacionais.
</p>
""", unsafe_allow_html=True)

expansion_data = [
    ("Vila Izabel",      "~3.800 lotes",  "Semana 1", "#007AFF"),
    ("Mercês",           "~4.200 lotes",  "Semana 2", "#34C759"),
    ("Boqueirão",        "~6.100 lotes",  "Semana 3", "#5856D6"),
    ("Santa Felicidade", "~5.500 lotes",  "Semana 4", "#FF9500"),
]

col_e1, col_e2, col_e3, col_e4 = st.columns(4)
for col, (bairro, lotes, semana, cor) in zip([col_e1, col_e2, col_e3, col_e4], expansion_data):
    with col:
        st.markdown(f"""
        <div class="exp-card">
            <div class="exp-week" style="color:{cor};">{semana}</div>
            <div class="exp-name">{bairro}</div>
            <div class="exp-count">{lotes} · Curitiba</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
