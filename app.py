"""
Dashboard Premium — ICAI · Corredor del Bajío
Equipo 11 · Taller de Fundamentos para el Análisis de Datos
"""

import time
import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ICAI · Corredor del Bajío",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# SVG ICONS
# ─────────────────────────────────────────────────────────────────────
ICO = {
    "trophy": """<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M5 2h6v5a3 3 0 0 1-6 0V2z" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="round"/>
        <path d="M5 4H3v1a2 2 0 0 0 2 2" stroke="currentColor" stroke-width="1.3" fill="none"/>
        <path d="M11 4h2v1a2 2 0 0 1-2 2" stroke="currentColor" stroke-width="1.3" fill="none"/>
        <line x1="8" y1="10" x2="8" y2="13" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        <line x1="5" y1="14" x2="11" y2="14" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
    </svg>""",
}

def ico(name: str, color: str = "currentColor", size: int = 16) -> str:
    svg = ICO.get(name, "")
    return (svg
        .replace('width="16"',  f'width="{size}"')
        .replace('height="16"', f'height="{size}"')
        .replace("currentColor", color))


# ─────────────────────────────────────────────────────────────────────
# PALETA METÁLICA
# ─────────────────────────────────────────────────────────────────────
METAL       = "#94A3B8"
METAL_DARK  = "#475569"
METAL_DEEP  = "#1E293B"
METAL_LIGHT = "#CBD5E1"
GOLD        = "#D97706"
GOLD_LIGHT  = "#FBBF24"

STATE_COLORS = {
    "Jalisco":          "#60A5FA",
    "Guanajuato":       "#818CF8",
    "Querétaro":        "#34D399",
    "San Luis Potosí":  "#FBBF24",
    "Aguascalientes":   "#F472B6",
}

STATE_GRADIENT = {
    "Jalisco":          ("#1D4ED8", "#60A5FA", "rgba(96,165,250,0.45)"),
    "Guanajuato":       ("#4338CA", "#818CF8", "rgba(129,140,248,0.45)"),
    "Querétaro":        ("#047857", "#34D399", "rgba(52,211,153,0.45)"),
    "San Luis Potosí":  ("#92400E", "#FBBF24", "rgba(251,191,36,0.45)"),
    "Aguascalientes":   ("#9D174D", "#F472B6", "rgba(244,114,182,0.45)"),
}

METAL_SCALE = [
    [0.0,  "#0F172A"],
    [0.25, "#1E3A5F"],
    [0.55, "#2563EB"],
    [0.80, "#60A5FA"],
    [1.0,  "#BFDBFE"],
]


# ─────────────────────────────────────────────────────────────────────
# CSS — Tema Metálico Oscuro
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── BASE ──────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #CBD5E1 !important;
}
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none; }

/* ── FONDO ─────────────────────────────────────────────────────── */
.stApp {
    background: #080E1A !important;
    background-image:
        radial-gradient(ellipse 70% 40% at 15% 10%, rgba(96,165,250,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 88% 88%, rgba(217,119,6,0.05) 0%, transparent 55%) !important;
}

/* ── SIDEBAR ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1424 0%, #0D1E35 100%) !important;
    border-right: 1px solid rgba(148,163,184,0.1) !important;
    box-shadow: 4px 0 32px rgba(0,0,0,0.5) !important;
}
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] .stMarkdown p {
    color: #475569 !important;
    font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase;
}

/* ── MÉTRICAS ──────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0F1E30 0%, #152840 60%, #0F1E30 100%) !important;
    border: 1px solid rgba(148,163,184,0.1) !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    position: relative; overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.05),
                inset 0 -1px 0 rgba(0,0,0,0.2) !important;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg,
        transparent 0%, #334155 15%, #64748B 30%,
        #94A3B8 45%, #CBD5E1 50%,
        #94A3B8 55%, #64748B 70%, #334155 85%, transparent 100%);
    background-size: 200% auto;
    animation: chrome-slide 4s linear infinite;
    border-radius: 16px 16px 0 0;
}
[data-testid="stMetric"]::after {
    content: '';
    position: absolute; top: -20%; left: -60%; width: 40%; height: 140%;
    background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.03) 50%, transparent 60%);
    animation: card-sheen 6s ease-in-out infinite;
    pointer-events: none;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(148,163,184,0.28) !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5),
                0 0 0 1px rgba(203,213,225,0.08),
                inset 0 1px 0 rgba(255,255,255,0.08) !important;
    transform: translateY(-3px) !important;
}
[data-testid="stMetricLabel"] p {
    color: #475569 !important;
    font-size: 0.67rem !important;
    letter-spacing: 0.14em; text-transform: uppercase; font-weight: 600;
}
[data-testid="stMetricValue"] {
    color: #CBD5E1 !important;
    font-size: 1.5rem !important; font-weight: 700;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stMetricDelta"] { color: #334155 !important; font-size: 0.7rem !important; }

/* ── TABS ──────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(135deg, rgba(10,20,36,0.95), rgba(15,30,50,0.95));
    border-radius: 14px; padding: 5px; gap: 4px;
    border: 1px solid rgba(148,163,184,0.1);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 4px 20px rgba(0,0,0,0.35);
}
.stTabs [data-baseweb="tab"] {
    color: #475569;
    border-radius: 10px; font-size: 0.82rem; font-weight: 500;
    padding: 8px 18px; letter-spacing: 0.03em;
    transition: all 0.25s ease; border: 1px solid transparent;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #94A3B8; background: rgba(148,163,184,0.07);
    border-color: rgba(148,163,184,0.1);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a2f50 0%, #243d68 50%, #1a2f50 100%) !important;
    color: #CBD5E1 !important;
    border: 1px solid rgba(148,163,184,0.18) !important;
    box-shadow: 0 2px 14px rgba(0,0,0,0.45),
                inset 0 1px 0 rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 20px 0 0 0; }

/* ── BOTONES ───────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg,
        #1E293B 0%, #263548 25%, #334155 50%,
        #263548 75%, #1E293B 100%) !important;
    background-size: 200% 100% !important;
    color: #CBD5E1 !important;
    border: 1px solid rgba(148,163,184,0.2) !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.82rem !important; letter-spacing: 0.06em !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35),
                inset 0 1px 0 rgba(255,255,255,0.06) !important;
}
.stButton > button:hover {
    background-position: right center !important;
    color: #E2E8F0 !important;
    border-color: rgba(203,213,225,0.3) !important;
    box-shadow: 0 6px 28px rgba(0,0,0,0.45),
                inset 0 1px 0 rgba(255,255,255,0.1) !important;
    transform: translateY(-2px) !important;
}

/* ── SELECTBOX ─────────────────────────────────────────────────── */
[data-baseweb="select"] > div {
    background: linear-gradient(135deg, #0F1923, #152030) !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 10px !important;
    transition: border-color 0.25s, box-shadow 0.25s;
}
[data-baseweb="select"] > div:hover {
    border-color: rgba(148,163,184,0.3) !important;
    box-shadow: 0 0 0 3px rgba(100,116,139,0.1) !important;
}
[data-baseweb="select"] span { color: #94A3B8 !important; font-size: 0.88rem; }

/* ── DATAFRAME ─────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(148,163,184,0.12) !important;
    border-radius: 16px !important; overflow: hidden;
    box-shadow: 0 4px 32px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.03);
    background: linear-gradient(145deg, #0F1E30, #0A1525) !important;
    transition: box-shadow 0.3s ease;
}
[data-testid="stDataFrame"]:hover {
    box-shadow: 0 6px 40px rgba(0,0,0,0.5) !important;
}

/* ── CHECKBOX ──────────────────────────────────────────────────── */
[data-baseweb="checkbox"] span {
    background: rgba(15,25,35,0.9) !important;
    border: 1.5px solid rgba(148,163,184,0.25) !important;
    border-radius: 4px !important; transition: border-color 0.2s;
}

/* ── DOWNLOAD ──────────────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #0F1923, #152030) !important;
    color: #64748B !important;
    border: 1.5px solid rgba(148,163,184,0.18) !important;
    border-radius: 10px !important; font-weight: 600 !important;
    transition: all 0.25s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #152030, #1E2F48) !important;
    color: #CBD5E1 !important;
    border-color: rgba(148,163,184,0.35) !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35) !important;
}

/* ── DIVISOR ───────────────────────────────────────────────────── */
hr {
    border: none !important; height: 1px !important;
    background: linear-gradient(90deg,
        transparent,
        rgba(71,85,105,0.5) 30%, rgba(148,163,184,0.3) 50%,
        rgba(71,85,105,0.5) 70%, transparent) !important;
    margin: 1.4rem 0 !important;
}

/* ── ALERTS ────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    background: rgba(10,16,28,0.85) !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 12px !important;
}
[data-testid="stAlertContainer"] p { color: #94A3B8 !important; }

/* ── CODE ──────────────────────────────────────────────────────── */
code {
    background: rgba(10,16,28,0.9) !important;
    color: #94A3B8 !important; border-radius: 5px; padding: 2px 7px;
    border: 1px solid rgba(148,163,184,0.1);
}
[data-testid="stCode"] {
    background: rgba(8,14,26,0.97) !important;
    border: 1px solid rgba(148,163,184,0.1) !important;
    border-radius: 12px !important;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
}

/* ── TIPOGRAFÍA ────────────────────────────────────────────────── */
h2, h3 {
    color: #CBD5E1 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important; letter-spacing: -0.01em;
}
p, li  { color: #64748B !important; }
.stCaption p { color: #334155 !important; font-size: 0.74rem !important; }

/* ── NOTIFICACIONES ────────────────────────────────────────────── */
[data-baseweb="notification"] {
    background: rgba(5,20,12,0.75) !important;
    border: 1px solid rgba(22,163,74,0.22) !important; border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-baseweb="notification"] p { color: #4ADE80 !important; }

/* ── JSON ──────────────────────────────────────────────────────── */
[data-testid="stJson"] {
    background: rgba(8,14,26,0.97) !important;
    border: 1px solid rgba(148,163,184,0.1) !important; border-radius: 12px !important;
}

/* ── KEYFRAMES ─────────────────────────────────────────────────── */
@keyframes chrome-slide {
    0%   { background-position: 200% center; }
    100% { background-position: -200% center; }
}
@keyframes card-sheen {
    0%   { left: -60%; opacity: 0; }
    15%  { opacity: 1; }
    85%  { opacity: 1; }
    100% { left: 120%; opacity: 0; }
}
@keyframes txt-shine {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def api_get(endpoint: str, **params) -> dict:
    clean = {k: v for k, v in params.items() if v is not None}
    r = requests.get(f"{BASE_URL}{endpoint}", params=clean or None, timeout=5)
    r.raise_for_status()
    return r.json()


def check_api() -> bool:
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False


def hex_rgba(hex_color: str, alpha: float = 0.08) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def chart_layout(height: int = 400, title: str = "") -> dict:
    _axis = dict(
        gridcolor="rgba(71,85,105,0.18)",
        linecolor="rgba(71,85,105,0.22)",
        tickcolor="rgba(71,85,105,0.28)",
        tickfont=dict(color="#475569", size=11),
        title_font=dict(color="#64748B"),
        zeroline=False,
    )
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,14,26,0.65)",
        font=dict(color="#64748B", family="Inter, sans-serif", size=12),
        height=height,
        margin=dict(l=12, r=12, t=46 if title else 18, b=12),
        title=dict(
            text=title,
            font=dict(color="#94A3B8", size=13, family="Space Grotesk"),
            x=0.02, xanchor="left",
        ),
        legend=dict(
            bgcolor="rgba(8,14,26,0.88)",
            bordercolor="rgba(71,85,105,0.2)",
            borderwidth=1,
            font=dict(color="#64748B", size=11),
        ),
        hoverlabel=dict(
            bgcolor="rgba(8,14,26,0.97)",
            bordercolor="rgba(148,163,184,0.3)",
            font=dict(color="#CBD5E1", size=12),
        ),
        xaxis=_axis.copy(),
        yaxis=_axis.copy(),
    )


# ─────────────────────────────────────────────────────────────────────
# CONNECTION CHECK
# ─────────────────────────────────────────────────────────────────────
if not check_api():
    st.error("La API no responde. Ejecuta: `uvicorn main:app --reload`")
    st.stop()

info    = api_get("/")
ESTADOS = info["estados_disponibles"]
ANIOS   = list(range(2018, 2026))


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:9px;margin-bottom:3px;">
      <span style="color:#94A3B8;flex-shrink:0;">{ico("trophy","#94A3B8",18)}</span>
      <span style="font-family:Space Grotesk,sans-serif;font-size:1.05rem;font-weight:700;
        background:linear-gradient(90deg,#475569,#64748B,#94A3B8,#CBD5E1,#94A3B8,#64748B,#475569);
        background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
        animation:txt-shine 4s linear infinite;">
        ICAI · BAJÍO
      </span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Corredor industrial · 2018–2025")
    st.divider()

    st.markdown("**FILTROS**")
    estado_sel = st.selectbox("Estado", ["Todos"] + ESTADOS, label_visibility="collapsed")
    anio_sel   = st.selectbox("Año",    ["Todos"] + ANIOS,   label_visibility="collapsed")

    st.divider()
    st.markdown("**CONEXIÓN**")
    st.success(f"API activa — v{info['version']}")
    st.caption(BASE_URL)
    if st.button("Refrescar datos", width="stretch"):
        st.cache_data.clear()
        st.rerun()


# ─────────────────────────────────────────────────────────────────────
# HERO — Metálico oscuro
# ─────────────────────────────────────────────────────────────────────
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;600;700&family=Inter:wght@300;400&display=swap');

.hero-wrap {
    position:relative; width:100%; height:185px; overflow:hidden;
    display:flex; flex-direction:column; justify-content:center; padding:0 28px;
    background: linear-gradient(135deg, #080E1A 0%, #0D1B2A 35%, #111E32 65%, #0A1220 100%);
    border: 1px solid rgba(148,163,184,0.1); border-radius: 18px;
    box-shadow: 0 8px 48px rgba(0,0,0,0.55),
                inset 0 1px 0 rgba(255,255,255,0.04),
                inset 0 -1px 0 rgba(0,0,0,0.3);
}
.hero-wrap::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg,
        transparent 0%, #1E293B 10%, #334155 25%, #64748B 40%,
        #94A3B8 50%, #64748B 60%, #334155 75%, #1E293B 90%, transparent 100%);
    background-size:200% auto; animation:hero-chrome 6s linear infinite;
}
@keyframes hero-chrome { 0%{background-position:200% center} 100%{background-position:-200% center} }

.dot-grid {
    position:absolute; right:0; top:0; width:50%; height:100%;
    background-image: radial-gradient(circle, rgba(148,163,184,0.1) 1px, transparent 1px);
    background-size: 24px 24px;
    -webkit-mask-image: linear-gradient(to left, rgba(0,0,0,0.25), transparent);
    mask-image: linear-gradient(to left, rgba(0,0,0,0.25), transparent);
}
.scan-line {
    position:absolute; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent 0%, rgba(71,85,105,0.3) 20%,
        rgba(203,213,225,0.75) 50%, rgba(71,85,105,0.3) 80%, transparent 100%);
    top:0; pointer-events:none; animation: scan-down 7s ease-in-out infinite;
}
@keyframes scan-down { 0%{top:0;opacity:0} 5%{opacity:1} 93%{opacity:0.7} 100%{top:100%;opacity:0} }

.orb { position:absolute; border-radius:50%; filter:blur(65px); pointer-events:none; }
.o1  { width:320px;height:320px; background:radial-gradient(circle,rgba(96,165,250,0.055),transparent 70%);  top:-150px;right:30px;   animation:fl1 12s ease-in-out infinite; }
.o2  { width:200px;height:200px; background:radial-gradient(circle,rgba(148,163,184,0.04),transparent 70%);  top:-70px;right:370px;   animation:fl2 16s ease-in-out infinite; }
.o3  { width:160px;height:160px; background:radial-gradient(circle,rgba(217,119,6,0.055),transparent 70%);   bottom:-65px;right:190px; animation:fl3 10s ease-in-out infinite; }
.o4  { width:90px;height:90px;   background:radial-gradient(circle,rgba(129,140,248,0.04),transparent 70%);  bottom:15px;left:220px;  animation:fl2 11s ease-in-out infinite reverse; }
@keyframes fl1 { 0%,100%{transform:translate(0,0) scale(1)}   50%{transform:translate(-18px,-20px) scale(1.06)} }
@keyframes fl2 { 0%,100%{transform:translate(0,0) scale(1)}   50%{transform:translate(12px,-12px) scale(0.94)} }
@keyframes fl3 { 0%,100%{transform:translate(0,0)}            50%{transform:translate(-8px,12px)} }

.corn { position:absolute; width:18px; height:18px; }
.tl { top:6px;left:6px;    border-top:1.5px solid rgba(148,163,184,0.22); border-left:1.5px solid rgba(148,163,184,0.22); }
.tr { top:6px;right:6px;   border-top:1.5px solid rgba(148,163,184,0.22); border-right:1.5px solid rgba(148,163,184,0.22); }
.bl { bottom:6px;left:6px;  border-bottom:1.5px solid rgba(148,163,184,0.22); border-left:1.5px solid rgba(148,163,184,0.22); }
.br { bottom:6px;right:6px; border-bottom:1.5px solid rgba(148,163,184,0.22); border-right:1.5px solid rgba(148,163,184,0.22); }

.hero-title {
    font-family:'Space Grotesk',sans-serif;
    font-size:clamp(1.5rem,3vw,2.25rem); font-weight:700; line-height:1.1;
    background: linear-gradient(90deg,
        #334155 0%, #475569 10%, #64748B 22%, #94A3B8 35%,
        #CBD5E1 46%, #E2E8F0 50%, #CBD5E1 54%,
        #94A3B8 65%, #64748B 78%, #475569 90%, #334155 100%);
    background-size:200% auto;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    animation:silver-shine 5s linear infinite; position:relative; z-index:2;
}
@keyframes silver-shine { to { background-position:200% center } }

.hero-sub {
    font-family:'Inter',sans-serif; font-size:0.74rem; color:#334155; margin-top:8px;
    letter-spacing:0.2em; text-transform:uppercase; position:relative; z-index:2;
}
.badges { display:flex; gap:8px; margin-top:14px; position:relative; z-index:2; flex-wrap:wrap; }
.badge {
    display:inline-flex; align-items:center; gap:6px;
    background: linear-gradient(135deg, rgba(12,20,35,0.9), rgba(18,30,50,0.9));
    border: 1px solid rgba(148,163,184,0.14); border-radius:20px; padding:4px 12px;
    font-family:'Inter',sans-serif; font-size:0.67rem; color:#475569;
    letter-spacing:0.09em; white-space:nowrap;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 1px 4px rgba(0,0,0,0.3);
}
.live-dot {
    width:5px;height:5px;border-radius:50%; background:#4ADE80;
    box-shadow:0 0 7px rgba(74,222,128,0.65); animation:live-pulse 2s ease-in-out infinite;
}
.info-dot { width:5px;height:5px;border-radius:50%; background:#60A5FA; box-shadow:0 0 5px rgba(96,165,250,0.55); }
@keyframes live-pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.3;transform:scale(0.65)} }
</style>

<div class="hero-wrap">
  <div class="o1 orb"></div><div class="o2 orb"></div>
  <div class="o3 orb"></div><div class="o4 orb"></div>
  <div class="dot-grid"></div><div class="scan-line"></div>
  <div class="corn tl"></div><div class="corn tr"></div>
  <div class="corn bl"></div><div class="corn br"></div>
  <div class="hero-title">Índice de Atractividad Industrial</div>
  <div class="hero-sub">Corredor del Bajío &nbsp;·&nbsp; 2018 – 2025 &nbsp;·&nbsp; Equipo 11</div>
  <div class="badges">
    <span class="badge"><span class="live-dot"></span>API activa</span>
    <span class="badge"><span class="info-dot"></span>5 estados</span>
    <span class="badge"><span class="info-dot"></span>8 años</span>
    <span class="badge"><span class="info-dot"></span>5 dimensiones</span>
    <span class="badge"><span class="info-dot"></span>10 endpoints</span>
  </div>
</div>
""")


# ─────────────────────────────────────────────────────────────────────
# MÉTRICAS RÁPIDAS
# ─────────────────────────────────────────────────────────────────────
ranking_data = api_get("/icai/ranking")
df_rank      = pd.DataFrame(ranking_data["ranking"])

cols = st.columns(5)
for col, row in zip(cols, df_rank.itertuples()):
    col.metric(
        label=f"0{row.posicion}  {row.estado}",
        value=f"{row.ICAI_promedio:.1f}",
        delta="pts ICAI",
    )

st.divider()


# ─────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────
t_rank, t_icai, t_perfil, t_dim, t_datos, t_api = st.tabs([
    "  Ranking", "  ICAI", "  Perfil", "  Dimensiones", "  Datos", "  API",
])


# ══════════════════════════════════════════════════════════════════════
# RANKING
# ══════════════════════════════════════════════════════════════════════
with t_rank:
    st.subheader("Ranking ICAI promedio 2018–2025")
    col_g, col_t = st.columns([1.5, 1])

    with col_g:
        fig = go.Figure(go.Bar(
            x=df_rank["ICAI_promedio"], y=df_rank["estado"], orientation="h",
            marker=dict(
                color=df_rank["ICAI_promedio"], colorscale=METAL_SCALE,
                line=dict(color="rgba(148,163,184,0.15)", width=1),
            ),
            text=[f"{v:.2f} pts" for v in df_rank["ICAI_promedio"]],
            textposition="outside", textfont=dict(color="#64748B", size=12),
            hovertemplate="<b>%{y}</b><br>ICAI: %{x:.2f} pts<extra></extra>",
        ))
        fig.update_layout(**chart_layout(height=320, title="ICAI promedio del corredor"))
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(range=[0, df_rank["ICAI_promedio"].max() * 1.22])
        st.plotly_chart(fig, width="stretch")

    with col_t:
        bars_html = ""
        for idx, row in df_rank.iterrows():
            color        = STATE_COLORS.get(row["estado"], METAL)
            c1, c2, glow = STATE_GRADIENT.get(row["estado"], ("#1E293B", "#94A3B8", "rgba(148,163,184,0.35)"))
            pct          = row["ICAI_promedio"]
            delay        = idx * 0.15
            bars_html += f"""
            <div class="bcard">
              <div class="bheader">
                <span class="brank">0{int(row['posicion'])}</span>
                <span class="bname">{row['estado']}</span>
                <span class="bval" style="color:{color};">{row['ICAI_promedio']:.2f}</span>
              </div>
              <div class="btrack">
                <div class="bfill" style="--w:{pct:.2f}%;--c1:{c1};--c2:{c2};--glow:{glow};animation-delay:{delay:.2f}s;"></div>
              </div>
            </div>"""

        st.html(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500&display=swap');
        *{{margin:0;padding:0;box-sizing:border-box;}} body,div{{font-family:'Inter',sans-serif;}}
        .bcard {{
            margin-bottom:10px;
            background:linear-gradient(145deg,#0F1E30 0%,#0A1525 100%);
            border:1px solid rgba(148,163,184,0.1); border-radius:13px; padding:12px 16px;
            box-shadow:0 2px 10px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.03);
            transition:all 0.3s cubic-bezier(0.4,0,0.2,1); position:relative; overflow:hidden;
        }}
        .bcard::after {{
            content:''; position:absolute; top:0; left:-80%; width:40%; height:100%;
            background:linear-gradient(105deg,transparent 40%,rgba(255,255,255,0.025) 50%,transparent 60%);
            transition:left 0.55s ease; pointer-events:none;
        }}
        .bcard:hover {{ border-color:rgba(148,163,184,0.22); box-shadow:0 6px 24px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.05); transform:translateX(4px); }}
        .bcard:hover::after {{ left:130%; }}
        .bheader{{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}}
        .brank{{font-size:0.62rem;color:#334155;min-width:22px;letter-spacing:0.1em;font-weight:600;}}
        .bname{{font-size:0.82rem;color:#64748B;font-weight:500;flex:1;margin-left:9px;}}
        .bval{{font-family:'Space Grotesk',sans-serif;font-size:1rem;font-weight:700;}}
        .btrack{{height:3px;background:rgba(15,30,50,0.9);border-radius:3px;overflow:hidden;}}
        .bfill{{
            height:100%;width:0%;
            background:linear-gradient(90deg,var(--c1),var(--c2));
            border-radius:3px; box-shadow:0 0 8px var(--glow);
            animation:grow-bar 1.3s cubic-bezier(0.22,1,0.36,1) forwards;
        }}
        @keyframes grow-bar{{from{{width:0%}}to{{width:var(--w)}}}}
        </style>
        {bars_html}
        """)

    st.caption(
        "Metodología: Normalización Min-Max · "
        "Ponderaciones: IED 25% · Exportaciones 25% · Manufactura 25% · Crédito 15% · INPC 10%"
    )


# ══════════════════════════════════════════════════════════════════════
# ICAI TEMPORAL
# ══════════════════════════════════════════════════════════════════════
with t_icai:
    st.subheader("Evolución del ICAI por estado")

    params_i: dict = {}
    if estado_sel != "Todos": params_i["estado"] = estado_sel
    if anio_sel   != "Todos": params_i["anio"]   = anio_sel

    data  = api_get("/icai", **params_i)
    df_ic = pd.DataFrame(data["datos"])

    if anio_sel == "Todos":
        fig = go.Figure()
        for estado in (df_ic["entidad"].unique() if estado_sel == "Todos" else [estado_sel]):
            sub   = df_ic[df_ic["entidad"] == estado]
            color = STATE_COLORS.get(estado, METAL)
            fig.add_trace(go.Scatter(
                x=sub["anio"], y=sub["ICAI"], mode="lines+markers", name=estado,
                line=dict(color=color, width=2.5),
                marker=dict(color=color, size=7, line=dict(color="#080E1A", width=2)),
                fill="tozeroy", fillcolor=hex_rgba(color, 0.07),
                hovertemplate=f"<b>{estado}</b><br>%{{x}}: %{{y:.2f}} pts<extra></extra>",
            ))
        fig.update_layout(**chart_layout(height=430, title="ICAI 2018–2025 — Evolución temporal"))
        fig.update_xaxes(dtick=1)
    else:
        colors_bar = [STATE_COLORS.get(e, METAL) for e in df_ic["entidad"]]
        fig = go.Figure(go.Bar(
            x=df_ic["entidad"], y=df_ic["ICAI"],
            marker=dict(color=colors_bar, line=dict(color="rgba(148,163,184,0.12)", width=1)),
            text=[f"{v:.2f}" for v in df_ic["ICAI"]],
            textposition="outside", textfont=dict(color="#64748B"),
            hovertemplate="<b>%{x}</b><br>ICAI: %{y:.2f} pts<extra></extra>",
        ))
        fig.update_layout(**chart_layout(height=430, title=f"ICAI — Año {anio_sel}"))
        fig.update_yaxes(range=[0, df_ic["ICAI"].max() * 1.22])

    st.plotly_chart(fig, width="stretch")
    st.dataframe(df_ic, hide_index=True, width="stretch")


# ══════════════════════════════════════════════════════════════════════
# PERFIL DIMENSIONAL
# ══════════════════════════════════════════════════════════════════════
with t_perfil:
    st.subheader("Perfil dimensional por estado")

    _polar_style = dict(
        bgcolor="rgba(8,14,26,0.7)",
        radialaxis=dict(
            visible=True, range=[0, 25],
            gridcolor="rgba(71,85,105,0.2)",
            tickfont=dict(color="#334155", size=9),
            linecolor="rgba(71,85,105,0.2)",
        ),
        angularaxis=dict(
            gridcolor="rgba(71,85,105,0.15)",
            tickfont=dict(color="#64748B", size=11),
            linecolor="rgba(71,85,105,0.18)",
        ),
    )

    if estado_sel == "Todos":
        st.info("Radar comparativo de los 5 estados. Selecciona uno en el panel lateral para ver el perfil detallado.")
        fig = go.Figure()
        for estado in ESTADOS:
            try:
                pd_data = api_get(f"/icai/perfil/{estado}")
                perf    = pd_data["contribucion_por_dimension"]
                color   = STATE_COLORS.get(estado, METAL)
                vals    = list(perf.values())
                keys    = list(perf.keys())
                fig.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]], theta=keys + [keys[0]], fill="toself", name=estado,
                    line=dict(color=color, width=2.2), fillcolor=hex_rgba(color, 0.07),
                    hovertemplate=f"<b>{estado}</b><br>%{{theta}}: %{{r:.2f}} pts<extra></extra>",
                ))
            except Exception:
                pass
        fig.update_layout(**chart_layout(height=500, title="Perfil dimensional comparativo"))
        fig.update_layout(polar=_polar_style)
        st.plotly_chart(fig, width="stretch")
    else:
        pd_data = api_get(f"/icai/perfil/{estado_sel}")
        perf    = pd_data["contribucion_por_dimension"]
        color   = STATE_COLORS.get(estado_sel, METAL)
        vals    = list(perf.values())
        keys    = list(perf.keys())

        c1, c2, c3 = st.columns(3)
        c1.metric("Estado",           pd_data["estado"])
        c2.metric("ICAI promedio",    f"{pd_data['ICAI_promedio']:.2f} pts")
        c3.metric("Posición ranking", f"0{pd_data['posicion_ranking']} de 5")
        st.caption(pd_data["interpretacion"])

        col_b, col_r = st.columns(2)
        with col_b:
            fig = go.Figure(go.Bar(
                x=keys, y=vals,
                marker=dict(color=vals, colorscale=METAL_SCALE,
                            line=dict(color="rgba(148,163,184,0.15)", width=1)),
                text=[f"{v:.2f}" for v in vals],
                textposition="outside", textfont=dict(color="#64748B"),
                hovertemplate="<b>%{x}</b><br>Contribución: %{y:.2f} pts<extra></extra>",
            ))
            fig.update_layout(**chart_layout(height=370, title="Contribución por dimensión"))
            fig.update_yaxes(range=[0, max(vals) * 1.3])
            st.plotly_chart(fig, width="stretch")
        with col_r:
            fig = go.Figure(go.Scatterpolar(
                r=vals + [vals[0]], theta=keys + [keys[0]],
                fill="toself", fillcolor=hex_rgba(color, 0.1),
                line=dict(color=color, width=2.5),
                marker=dict(color=color, size=8, line=dict(color="#080E1A", width=2)),
                name=estado_sel,
                hovertemplate="<b>%{theta}</b><br>%{r:.2f} pts<extra></extra>",
            ))
            fig.update_layout(**chart_layout(height=370, title="Radar dimensional"))
            fig.update_layout(polar=_polar_style)
            st.plotly_chart(fig, width="stretch")


# ══════════════════════════════════════════════════════════════════════
# DIMENSIONES
# ══════════════════════════════════════════════════════════════════════
with t_dim:
    st.subheader("Variables del ICAI")

    params_e: dict = {}
    if estado_sel != "Todos":
        params_e["estado"] = estado_sel

    s_ied, s_exp, s_mfg, s_cred, s_inpc = st.tabs(
        ["IED", "Exportaciones", "Manufactura", "Crédito", "INPC"]
    )

    def _lines(df, x_col, y_col, hov_fmt=",.1f") -> go.Figure:
        fig = go.Figure()
        for estado in df["entidad"].unique():
            sub   = df[df["entidad"] == estado]
            color = STATE_COLORS.get(estado, METAL)
            fig.add_trace(go.Scatter(
                x=sub[x_col], y=sub[y_col], mode="lines+markers", name=estado,
                line=dict(color=color, width=2.4),
                marker=dict(color=color, size=7, line=dict(color="#080E1A", width=2)),
                fill="tozeroy", fillcolor=hex_rgba(color, 0.06),
                hovertemplate=f"<b>{estado}</b><br>%{{x}}: %{{y:{hov_fmt}}}<extra></extra>",
            ))
        return fig

    def _bars(df, x_col, y_col, hov_fmt=",.1f") -> go.Figure:
        fig = go.Figure()
        for estado in df["entidad"].unique():
            sub   = df[df["entidad"] == estado]
            color = STATE_COLORS.get(estado, METAL)
            fig.add_trace(go.Bar(
                x=sub[x_col], y=sub[y_col], name=estado,
                marker=dict(color=color, line=dict(color="rgba(148,163,184,0.1)", width=1)),
                hovertemplate=f"<b>{estado}</b><br>%{{x}}: %{{y:{hov_fmt}}}<extra></extra>",
            ))
        return fig

    with s_ied:
        d  = api_get("/ied", **params_e)
        df = pd.DataFrame(d["serie_anual"])
        fig = _bars(df, "anio", "ied_usd", ",.1f")
        fig.update_layout(**chart_layout(height=390, title="Inversión Extranjera Directa (Millones USD)"), barmode="group")
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Fuente: {d['fuente']} — Unidad: {d['unidad']}")
        st.dataframe(pd.DataFrame(d["resumen_por_estado"]), hide_index=True, width="stretch")

    with s_exp:
        d  = api_get("/exportaciones", **params_e)
        df = pd.DataFrame(d["serie_anual"])
        fig = _lines(df, "anio", "exportaciones_usd", ",.0f")
        fig.update_layout(**chart_layout(height=390, title="Exportaciones anuales (Miles USD)"))
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Fuente: {d['fuente']} — Unidad: {d['unidad']}")
        st.dataframe(pd.DataFrame(d["resumen_por_estado"]), hide_index=True, width="stretch")

    with s_mfg:
        d   = api_get("/manufactura", **params_e)
        df  = pd.DataFrame(d["serie_anual"])
        c1_, c2_ = st.columns(2)
        with c1_:
            fig = _lines(df, "anio", "personal_ocupado", ",.0f")
            fig.update_layout(**chart_layout(height=360, title="Personal ocupado (personas)"))
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, width="stretch")
        with c2_:
            fig = _lines(df, "anio", "valor_produccion", ",.0f")
            fig.update_layout(**chart_layout(height=360, title="Valor de producción (miles MXN)"))
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, width="stretch")
        st.caption(f"Fuente: {d['fuente']}")

    with s_cred:
        d  = api_get("/credito", **params_e)
        df = pd.DataFrame(d["serie_anual"])
        fig = _bars(df, "anio", "credito_pesos", ",.0f")
        fig.update_layout(**chart_layout(height=390, title="Crédito comercial empresarial (Millones MXN)"), barmode="group")
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Fuente: {d['fuente']} — Nota: {d['nota_metodologica']}")

    with s_inpc:
        d  = api_get("/inpc")
        df = pd.DataFrame(d["serie_anual"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["anio"], y=df["inpc_general"], mode="lines+markers", name="INPC General",
            line=dict(color="#60A5FA", width=2.5),
            marker=dict(color="#60A5FA", size=7, line=dict(color="#080E1A", width=2)),
            fill="tozeroy", fillcolor="rgba(96,165,250,0.07)",
            hovertemplate="<b>INPC General</b><br>%{x}: %{y:.2f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=df["anio"], y=df["inpc_energia"], mode="lines+markers", name="INPC Energía",
            line=dict(color="#FBBF24", width=2.5, dash="dot"),
            marker=dict(color="#FBBF24", size=7, line=dict(color="#080E1A", width=2)),
            hovertemplate="<b>INPC Energía</b><br>%{x}: %{y:.2f}<extra></extra>",
        ))
        fig.update_layout(**chart_layout(height=390, title="INPC — General y Energéticos"))
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Fuente: {d['fuente']} — Base: {d['unidad']} — {d['nota']}")


# ══════════════════════════════════════════════════════════════════════
# DATOS COMPLETOS
# ══════════════════════════════════════════════════════════════════════
with t_datos:
    st.subheader("Panel de datos completo")

    params_d: dict = {}
    if estado_sel != "Todos": params_d["estado"] = estado_sel
    if anio_sel   != "Todos": params_d["anio"]   = anio_sel

    datos = api_get("/datos", **params_d)
    df_d  = pd.DataFrame(datos["datos"])

    parts = [f"**{datos['total_registros']}** registros"]
    if estado_sel != "Todos": parts.append(f"Estado: {estado_sel}")
    if anio_sel   != "Todos": parts.append(f"Año: {anio_sel}")
    st.caption(" · ".join(parts))

    st.dataframe(df_d, hide_index=True, width="stretch")
    st.download_button(
        "Descargar CSV",
        data=df_d.to_csv(index=False).encode("utf-8"),
        file_name="panel_bajio_filtrado.csv",
        mime="text/csv",
    )


# ══════════════════════════════════════════════════════════════════════
# API EXPLORER
# ══════════════════════════════════════════════════════════════════════
with t_api:
    st.subheader("API Explorer")
    st.caption("Ejecuta cualquier endpoint en tiempo real y examina la respuesta JSON completa.")

    endpoint_sel = st.selectbox("Endpoint", info["endpoints"])
    params_api: dict = {}
    url_path = endpoint_sel

    if "{estado}" in endpoint_sel:
        e = st.selectbox("Estado (en URL)", ESTADOS, key="api_url_e")
        url_path = endpoint_sel.replace("{estado}", e)
    else:
        if endpoint_sel not in ["/", "/estados", "/inpc", "/icai/ranking"]:
            if st.checkbox("Filtrar por estado", key="api_e_chk"):
                params_api["estado"] = st.selectbox("Estado", ESTADOS, key="api_e2")
        if endpoint_sel in ["/datos", "/icai"]:
            if st.checkbox("Filtrar por año", key="api_a_chk"):
                params_api["anio"] = st.selectbox("Año", ANIOS, key="api_a2")

    qs       = "&".join(f"{k}={v}" for k, v in params_api.items())
    full_url = f"{BASE_URL}{url_path}" + (f"?{qs}" if qs else "")
    st.code(f"GET  {full_url}", language="bash")

    if st.button("Ejecutar", type="primary"):
        t0   = time.perf_counter()
        resp = requests.get(full_url, timeout=5)
        ms   = (time.perf_counter() - t0) * 1000

        c1, c2, c3 = st.columns(3)
        c1.metric("Status HTTP",         resp.status_code)
        c2.metric("Tiempo de respuesta", f"{ms:.0f} ms")
        c3.metric("Tamaño respuesta",    f"{len(resp.content) / 1024:.1f} KB")

        st.json(resp.json())
