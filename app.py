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
    background:
