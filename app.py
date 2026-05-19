import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="ICAI - Atractividad Industrial del Bajio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SVG Icons ─────────────────────────────────────────────────────────
SVG_CHART = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="12" width="4" height="9" rx="1" fill="#0A9396"/>
  <rect x="10" y="7" width="4" height="14" rx="1" fill="#0A9396" opacity="0.7"/>
  <rect x="17" y="3" width="4" height="18" rx="1" fill="#0A9396" opacity="0.4"/>
  <line x1="3" y1="21" x2="21" y2="21" stroke="#0A9396" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""

SVG_TROPHY = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 3h12v7a6 6 0 01-12 0V3z" stroke="#F4A261" stroke-width="1.8" fill="none"/>
  <path d="M6 6H3a2 2 0 002 2h1M18 6h3a2 2 0 01-2 2h-1" stroke="#F4A261" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M12 16v4M8 20h8" stroke="#F4A261" stroke-width="1.8" stroke-linecap="round"/>
</svg>"""

SVG_TARGET = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="9" stroke="#EE6C4D" stroke-width="1.8"/>
  <circle cx="12" cy="12" r="5" stroke="#EE6C4D" stroke-width="1.8"/>
  <circle cx="12" cy="12" r="1.5" fill="#EE6C4D"/>
</svg>"""

SVG_MONEY = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="2" y="6" width="20" height="13" rx="2" stroke="#0A9396" stroke-width="1.8"/>
  <circle cx="12" cy="12" r="3" stroke="#0A9396" stroke-width="1.8"/>
  <path d="M6 9v6M18 9v6" stroke="#0A9396" stroke-width="1.8" stroke-linecap="round"/>
</svg>"""

SVG_FACTORY = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M2 20V8l6 4V8l6 4V6h8v14H2z" stroke="#6B7EBF" stroke-width="1.8" stroke-linejoin="round"/>
  <rect x="14" y="14" width="3" height="6" rx="0.5" stroke="#6B7EBF" stroke-width="1.5"/>
  <rect x="5" y="14" width="3" height="4" rx="0.5" stroke="#6B7EBF" stroke-width="1.5"/>
</svg>"""

SVG_BANK = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 10l9-7 9 7" stroke="#A78BFA" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="3" y="18" width="18" height="3" rx="1" stroke="#A78BFA" stroke-width="1.5"/>
  <line x1="6" y1="10" x2="6" y2="18" stroke="#A78BFA" stroke-width="1.8"/>
  <line x1="10" y1="10" x2="10" y2="18" stroke="#A78BFA" stroke-width="1.8"/>
  <line x1="14" y1="10" x2="14" y2="18" stroke="#A78BFA" stroke-width="1.8"/>
  <line x1="18" y1="10" x2="18" y2="18" stroke="#A78BFA" stroke-width="1.8"/>
</svg>"""

SVG_TREND_DOWN = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 6l6 8 4-4 8 8" stroke="#EE6C4D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M15 18h6v-6" stroke="#EE6C4D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

SVG_TABLE = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="3" width="18" height="18" rx="2" stroke="#0A9396" stroke-width="1.8"/>
  <line x1="3" y1="9" x2="21" y2="9" stroke="#0A9396" stroke-width="1.5"/>
  <line x1="3" y1="15" x2="21" y2="15" stroke="#0A9396" stroke-width="1.5"/>
  <line x1="9" y1="9" x2="9" y2="21" stroke="#0A9396" stroke-width="1.5"/>
</svg>"""

SVG_GLOBE = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/>
  <path d="M12 3c-2 3-3 5.5-3 9s1 6 3 9M12 3c2 3 3 5.5 3 9s-1 6-3 9" stroke="currentColor" stroke-width="1.5"/>
  <line x1="3" y1="12" x2="21" y2="12" stroke="currentColor" stroke-width="1.5"/>
  <path d="M4.5 7.5h15M4.5 16.5h15" stroke="currentColor" stroke-width="1.2"/>
</svg>"""

# ── CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: linear-gradient(135deg, #060d1a 0%, #0a1628 40%, #0d1f3c 70%, #071220 100%);
    font-family: 'Space Grotesk', sans-serif;
}

/* Animated mesh background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(10,147,150,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(238,108,77,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 50% 50%, rgba(107,126,191,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: meshShift 12s ease-in-out infinite alternate;
}

@keyframes meshShift {
    0%   { opacity: 0.6; transform: scale(1) rotate(0deg); }
    50%  { opacity: 1;   transform: scale(1.05) rotate(1deg); }
    100% { opacity: 0.7; transform: scale(0.98) rotate(-1deg); }
}

/* Main header */
.dash-header {
    background: linear-gradient(135deg,
        rgba(10,147,150,0.15) 0%,
        rgba(107,126,191,0.08) 50%,
        rgba(238,108,77,0.08) 100%);
    border: 1px solid rgba(10,147,150,0.25);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    animation: fadeSlideDown 0.6s ease-out;
}

.dash-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #0A9396, #6B7EBF, #EE6C4D, transparent);
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}

@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.dash-title {
    font-size: 26px;
    font-weight: 700;
    background: linear-gradient(135deg, #e8f4f5 0%, #0A9396 50%, #6B7EBF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}

.dash-sub {
    font-size: 13px;
    color: rgba(200,220,230,0.6);
    font-weight: 400;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.3px;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.04) 0%,
        rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeSlideUp 0.5s ease-out both;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border-color: rgba(10,147,150,0.4);
    box-shadow: 0 8px 32px rgba(10,147,150,0.15);
}

.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    background: var(--accent, linear-gradient(90deg, #0A9396, #6B7EBF));
    border-radius: 0 0 14px 14px;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}

.kpi-card:hover::after { transform: scaleX(1); }

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.kpi-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: rgba(180,210,220,0.5);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.kpi-value {
    font-size: 30px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #e8f4f5;
    line-height: 1;
    margin-bottom: 6px;
    letter-spacing: -1px;
}

.kpi-delta-pos {
    font-size: 12px;
    color: #4ade80;
    font-family: 'JetBrains Mono', monospace;
    display: flex; align-items: center; gap: 3px;
}
.kpi-delta-neg {
    font-size: 12px;
    color: #f87171;
    font-family: 'JetBrains Mono', monospace;
    display: flex; align-items: center; gap: 3px;
}

.badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 4px;
}
.badge-alto    { background: rgba(74,222,128,0.15); color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
.badge-medio   { background: rgba(250,204,21,0.15); color: #facc15; border: 1px solid rgba(250,204,21,0.3); }
.badge-bajo    { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }

/* Section headers */
.section-hdr {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.section-hdr-text {
    font-size: 14px;
    font-weight: 600;
    color: rgba(200,230,240,0.85);
    letter-spacing: 0.2px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080f1e 0%, #0a1628 100%);
    border-right: 1px solid rgba(10,147,150,0.15);
}

section[data-testid="stSidebar"] .stMarkdown p {
    color: rgba(180,210,220,0.7);
    font-size: 13px;
}

.sidebar-logo {
    background: linear-gradient(135deg, rgba(10,147,150,0.12), rgba(107,126,191,0.08));
    border: 1px solid rgba(10,147,150,0.2);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.sidebar-logo::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 70%, rgba(10,147,150,0.1) 100%);
    animation: rotateBg 8s linear infinite;
}
@keyframes rotateBg {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
.sidebar-logo-title {
    font-size: 18px;
    font-weight: 700;
    background: linear-gradient(135deg, #0A9396, #6B7EBF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}
.sidebar-logo-sub {
    font-size: 10px;
    color: rgba(180,210,220,0.4);
    letter-spacing: 1px;
    text-transform: uppercase;
    position: relative;
    z-index: 1;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
}

.weight-pill {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 7px 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    margin-bottom: 6px;
    transition: all 0.2s ease;
}
.weight-pill:hover {
    background: rgba(10,147,150,0.08);
    border-color: rgba(10,147,150,0.2);
}
.weight-name { font-size: 12px; color: rgba(200,220,230,0.7); }
.weight-val  { font-size: 12px; font-weight: 700; color: #0A9396; font-family: 'JetBrains Mono', monospace; }

/* Divider */
.grad-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(10,147,150,0.3), rgba(107,126,191,0.2), transparent);
    margin: 20px 0;
}

/* Metrics override */
div[data-testid="stMetric"] {
    background: transparent !important;
    padding: 0 !important;
}

/* Plotly charts dark bg */
.js-plotly-plot { border-radius: 12px; }

/* Animated counter */
@keyframes countUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animated-val {
    animation: countUp 0.5s ease-out both;
}
</style>
""", unsafe_allow_html=True)


# ── Datos ─────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    panel = pd.read_csv("panel_bajio.csv")
    def minmax(s):     return (s - s.min()) / (s.max() - s.min())
    def minmax_inv(s): return 1 - minmax(s)
    panel["norm_ied"]           = minmax(panel["ied_usd"])
    panel["norm_exportaciones"] = minmax(panel["exportaciones_usd"])
    panel["norm_manufactura"]   = minmax(panel["personal_ocupado"])
    panel["norm_credito"]       = minmax(panel["credito_pesos"])
    panel["norm_inpc"]          = minmax_inv(panel["inpc_general"])
    panel["ICAI"] = (
        panel["norm_ied"]           * 0.25 +
        panel["norm_exportaciones"] * 0.25 +
        panel["norm_manufactura"]   * 0.25 +
        panel["norm_credito"]       * 0.15 +
        panel["norm_inpc"]          * 0.10
    ) * 100
    panel["ICAI"] = panel["ICAI"].round(2)
    return panel

panel = cargar_datos()
ESTADOS = sorted(panel["entidad"].unique().tolist())
ANIOS   = sorted(panel["anio"].unique().tolist())

COLORES = {
    "San Luis Potosi": "#0A9396", "San Luis Potosí": "#0A9396",
    "Jalisco":         "#EE6C4D",
    "Guanajuato":      "#F4A261",
    "Queretaro":       "#6B7EBF", "Querétaro": "#6B7EBF",
    "Aguascalientes":  "#A78BFA",
}
def get_color(e): return COLORES.get(e, "#888")

def nivel_icai(v):
    if v >= 40: return "Medio-Alto", "badge-alto"
    if v >= 20: return "Intermedio", "badge-medio"
    return "Bajo", "badge-bajo"

def plot_cfg(fig, h=320):
    fig.update_layout(
        height=h,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(family="Space Grotesk, sans-serif", color="rgba(200,220,230,0.75)", size=11),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=10, color="rgba(200,220,230,0.7)")
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)", title_font=dict(size=11)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)", title_font=dict(size=11)),
    )
    return fig


# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-title">ICAI</div>
        <div class="sidebar-logo-sub">Corredor del Bajío · 2018–2025</div>
    </div>
    """, unsafe_allow_html=True)

    estado_sel = st.selectbox("Estado de enfoque", ESTADOS,
        index=ESTADOS.index("San Luis Potosí") if "San Luis Potosí" in ESTADOS else 0)

    anio_rango = st.slider("Rango de años",
        min_value=min(ANIOS), max_value=max(ANIOS),
        value=(min(ANIOS), max(ANIOS)))

    st.markdown('<div class="grad-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:11px;font-weight:600;letter-spacing:0.8px;text-transform:uppercase;color:rgba(180,210,220,0.4);margin-bottom:10px;">Ponderaciones ICAI</div>', unsafe_allow_html=True)

    pesos_sidebar = [
        ("IED", "25%"), ("Exportaciones", "25%"), ("Manufactura", "25%"),
        ("Crédito", "15%"), ("INPC", "10%")
    ]
    for nombre, pct in pesos_sidebar:
        st.markdown(f"""
        <div class="weight-pill">
            <span class="weight-name">{nombre}</span>
            <span class="weight-val">{pct}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="grad-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:rgba(180,210,220,0.3);line-height:1.6;font-family:JetBrains Mono,monospace;">SE · INEGI · CNBV · Banxico<br>Equipo 11 · Análisis de Datos</div>', unsafe_allow_html=True)


# ── Filtros ───────────────────────────────────────────────────────────
panel_filt   = panel[(panel["anio"] >= anio_rango[0]) & (panel["anio"] <= anio_rango[1])]
datos_estado = panel_filt[panel_filt["entidad"] == estado_sel]
icai_prom    = datos_estado["ICAI"].mean()
icai_last    = datos_estado[datos_estado["anio"] == datos_estado["anio"].max()]["ICAI"].values
icai_prev    = datos_estado[datos_estado["anio"] == datos_estado["anio"].max() - 1]["ICAI"].values
icai_best    = datos_estado["ICAI"].max()
anio_best    = datos_estado[datos_estado["ICAI"] == icai_best]["anio"].values[0]
ranking      = panel_filt.groupby("entidad")["ICAI"].mean().sort_values(ascending=False).reset_index()
ranking.columns = ["entidad", "ICAI_prom"]
pos          = ranking[ranking["entidad"] == estado_sel].index[0] + 1
nivel, badge = nivel_icai(icai_prom)
delta_last   = float(icai_last[0] - icai_prev[0]) if len(icai_last) > 0 and len(icai_prev) > 0 else 0.0
diferencia   = icai_prom - ranking["ICAI_prom"].mean()


# ── Header ────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <div class="dash-title">Índice Compuesto de Atractividad Industrial</div>
    <div class="dash-sub">Corredor del Bajío &nbsp;·&nbsp; {estado_sel} &nbsp;·&nbsp; {anio_rango[0]}–{anio_rango[1]} &nbsp;·&nbsp; Metodología Min-Max + Ponderación Económica</div>
</div>
""", unsafe_allow_html=True)


# ── KPIs ──────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

def kpi_delta_html(val, suffix=""):
    color = "kpi-delta-pos" if val >= 0 else "kpi-delta-neg"
    arrow = "▲" if val >= 0 else "▼"
    return f'<div class="{color}">{arrow} {abs(val):.1f}{suffix}</div>'

with k1:
    st.markdown(f"""
    <div class="kpi-card" style="--accent: linear-gradient(90deg,#0A9396,#6B7EBF);">
        <div class="kpi-label">{SVG_CHART} ICAI Promedio</div>
        <div class="kpi-value animated-val">{icai_prom:.1f}</div>
        <div style="font-size:10px;color:rgba(180,210,220,0.4);margin-bottom:4px;">pts / 100</div>
        <span class="badge {badge}">{nivel}</span>
    </div>""", unsafe_allow_html=True)

with k2:
    icai_last_str = f"{icai_last[0]:.1f}" if len(icai_last) > 0 else "N/D"
    st.markdown(f"""
    <div class="kpi-card" style="--accent: linear-gradient(90deg,#EE6C4D,#F4A261);">
        <div class="kpi-label">{SVG_TREND_DOWN} ICAI {max(ANIOS)}</div>
        <div class="kpi-value animated-val">{icai_last_str}</div>
        <div style="font-size:10px;color:rgba(180,210,220,0.4);margin-bottom:4px;">pts / 100</div>
        {kpi_delta_html(delta_last, ' vs ant.')}
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card" style="--accent: linear-gradient(90deg,#6B7EBF,#A78BFA);">
        <div class="kpi-label">{SVG_TROPHY} Posición</div>
        <div class="kpi-value animated-val">{pos}°</div>
        <div style="font-size:10px;color:rgba(180,210,220,0.4);margin-bottom:4px;">de {len(ESTADOS)} estados</div>
        <div style="font-size:11px;color:rgba(180,210,220,0.5);">Ranking regional</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card" style="--accent: linear-gradient(90deg,#F4A261,#EE6C4D);">
        <div class="kpi-label">{SVG_TARGET} Mejor Año</div>
        <div class="kpi-value animated-val">{anio_best}</div>
        <div style="font-size:10px;color:rgba(180,210,220,0.4);margin-bottom:4px;">&nbsp;</div>
        <div class="kpi-delta-pos">▲ {icai_best:.1f} pts</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card" style="--accent: linear-gradient(90deg,#A78BFA,#6B7EBF);">
        <div class="kpi-label">{SVG_GLOBE} vs. Corredor</div>
        <div class="kpi-value animated-val">{icai_prom:.1f}</div>
        <div style="font-size:10px;color:rgba(180,210,220,0.4);margin-bottom:4px;">pts</div>
        {kpi_delta_html(diferencia, ' vs prom.')}
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="grad-divider"></div>', unsafe_allow_html=True)


# ── Evolución + Ranking ───────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(f'<div class="section-hdr">{SVG_CHART}<span class="section-hdr-text">Evolución del ICAI por estado</span></div>', unsafe_allow_html=True)
    fig_evol = go.Figure()
    for e in ESTADOS:
        de = panel_filt[panel_filt["entidad"] == e].sort_values("anio")
        sel = (e == estado_sel)
        fig_evol.add_trace(go.Scatter(
            x=de["anio"], y=de["ICAI"].round(1), name=e,
            mode="lines+markers",
            line=dict(color=get_color(e), width=3 if sel else 1.2,
                      dash="solid" if sel else "dot"),
            marker=dict(size=8 if sel else 4,
                        symbol="circle",
                        line=dict(width=2 if sel else 0, color="white")),
            opacity=1.0 if sel else 0.4,
            hovertemplate=f"<b>{e}</b><br>%{{x}}: %{{y:.1f}} pts<extra></extra>"
        ))
    fig_evol = plot_cfg(fig_evol, 320)
    fig_evol.update_layout(
        xaxis=dict(tickmode="array", tickvals=list(range(anio_rango[0], anio_rango[1]+1)),
                   gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.04)"),
    )
    st.plotly_chart(fig_evol, use_container_width=True)

with col2:
    st.markdown(f'<div class="section-hdr">{SVG_TROPHY}<span class="section-hdr-text">Ranking ICAI promedio</span></div>', unsafe_allow_html=True)
    fig_rank = go.Figure(go.Bar(
        x=ranking["ICAI_prom"].round(1),
        y=ranking["entidad"],
        orientation="h",
        marker=dict(
            color=[get_color(e) for e in ranking["entidad"]],
            opacity=0.85,
            line=dict(width=0)
        ),
        text=ranking["ICAI_prom"].round(1),
        textposition="outside",
        textfont=dict(size=12, color="rgba(200,230,240,0.8)"),
        hovertemplate="<b>%{y}</b><br>ICAI: %{x:.1f} pts<extra></extra>"
    ))
    fig_rank = plot_cfg(fig_rank, 320)
    fig_rank.update_layout(
        xaxis=dict(range=[0, 85]),
        yaxis=dict(autorange="reversed"),
        bargap=0.35,
    )
    st.plotly_chart(fig_rank, use_container_width=True)


# ── Perfil dimensional ────────────────────────────────────────────────
st.markdown(f'<div class="section-hdr">{SVG_TARGET}<span class="section-hdr-text">Perfil dimensional de {estado_sel} vs. promedio del corredor</span></div>', unsafe_allow_html=True)

dims    = ["IED", "Exportaciones", "Manufactura", "Crédito", "INPC"]
pesos_d = [0.25, 0.25, 0.25, 0.15, 0.10]
cols_n  = ["norm_ied","norm_exportaciones","norm_manufactura","norm_credito","norm_inpc"]
vals_e  = [datos_estado[c].mean() * p * 100 for c, p in zip(cols_n, pesos_d)]
vals_c  = [panel_filt[c].mean()   * p * 100 for c, p in zip(cols_n, pesos_d)]

fig_dim = go.Figure()
fig_dim.add_trace(go.Bar(
    name="Promedio corredor", x=dims,
    y=[round(v,2) for v in vals_c],
    marker=dict(color="rgba(255,255,255,0.12)", line=dict(width=0)),
    text=[f"{v:.1f}" for v in vals_c], textposition="outside",
    textfont=dict(size=11, color="rgba(180,210,220,0.6)"),
    hovertemplate="Promedio: %{y:.1f} pts<extra></extra>"
))
fig_dim.add_trace(go.Bar(
    name=estado_sel, x=dims,
    y=[round(v,2) for v in vals_e],
    marker=dict(
        color=[get_color(estado_sel)]*5,
        opacity=0.85, line=dict(width=0)
    ),
    text=[f"{v:.1f}" for v in vals_e], textposition="outside",
    textfont=dict(size=12, color="rgba(220,240,245,0.9)", family="JetBrains Mono"),
    hovertemplate=f"{estado_sel}: %{{y:.1f}} pts<extra></extra>"
))
fig_dim = plot_cfg(fig_dim, 300)
fig_dim.update_layout(
    barmode="group", bargap=0.25, bargroupgap=0.08,
    yaxis=dict(range=[0, 20], title="Contribución al ICAI (pts)"),
)
st.plotly_chart(fig_dim, use_container_width=True)

st.markdown('<div class="grad-divider"></div>', unsafe_allow_html=True)


# ── IED + Exportaciones ───────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown(f'<div class="section-hdr">{SVG_MONEY}<span class="section-hdr-text">Inversión Extranjera Directa</span></div>', unsafe_allow_html=True)
    fig_ied = go.Figure()
    for e in ESTADOS:
        de = panel_filt[panel_filt["entidad"]==e].sort_values("anio")
        sel = (e == estado_sel)
        r,g,b = int(get_color(e)[1:3],16), int(get_color(e)[3:5],16), int(get_color(e)[5:7],16)
        trace_ied = dict(
            x=de["anio"], y=de["ied_usd"].round(1), name=e,
            mode="lines+markers",
            line=dict(color=get_color(e), width=2.5 if sel else 1),
            marker=dict(size=6 if sel else 3),
            opacity=1.0 if sel else 0.4,
            hovertemplate=f"<b>{e}</b><br>%{{x}}: %{{y:.1f}} mill. USD<extra></extra>"
        )
        if sel:
            trace_ied["fill"] = "tozeroy"
            trace_ied["fillcolor"] = f"rgba({r},{g},{b},0.06)"
        fig_ied.add_trace(go.Scatter(**trace_ied))
    fig_ied = plot_cfg(fig_ied, 260)
    fig_ied.update_layout(yaxis_title="Mill. USD")
    st.plotly_chart(fig_ied, use_container_width=True)

with col4:
    st.markdown(f'<div class="section-hdr">{SVG_GLOBE}<span class="section-hdr-text">Exportaciones por estado</span></div>', unsafe_allow_html=True)
    panel_exp = panel_filt.copy()
    panel_exp["exp_b"] = (panel_exp["exportaciones_usd"] / 1e6).round(2)
    fig_exp = go.Figure()
    for e in ESTADOS:
        de = panel_exp[panel_exp["entidad"]==e].sort_values("anio")
        sel = (e == estado_sel)
        fig_exp.add_trace(go.Bar(
            x=de["anio"], y=de["exp_b"], name=e,
            marker=dict(color=get_color(e), opacity=0.85 if sel else 0.35, line=dict(width=0)),
            hovertemplate=f"<b>{e}</b><br>%{{x}}: %{{y:.2f}} miles de mill. USD<extra></extra>"
        ))
    fig_exp = plot_cfg(fig_exp, 260)
    fig_exp.update_layout(barmode="group", bargap=0.2, yaxis_title="Miles de mill. USD")
    st.plotly_chart(fig_exp, use_container_width=True)


# ── Manufactura + Crédito ─────────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown(f'<div class="section-hdr">{SVG_FACTORY}<span class="section-hdr-text">Personal ocupado en manufactura</span></div>', unsafe_allow_html=True)
    panel_man = panel_filt.copy()
    panel_man["personal_k"] = (panel_man["personal_ocupado"]/1000).round(1)
    fig_man = go.Figure()
    for e in ESTADOS:
        de = panel_man[panel_man["entidad"]==e].sort_values("anio")
        sel = (e == estado_sel)
        r,g,b = int(get_color(e)[1:3],16), int(get_color(e)[3:5],16), int(get_color(e)[5:7],16)
        fig_man.add_trace(go.Scatter(
            x=de["anio"], y=de["personal_k"], name=e,
            mode="lines",
            line=dict(color=get_color(e), width=2.5 if sel else 1),
            fill="tozeroy",
            fillcolor=f"rgba({r},{g},{b},{0.15 if sel else 0.03})",
            opacity=1.0 if sel else 0.5,
            hovertemplate=f"<b>{e}</b><br>%{{x}}: %{{y:.1f}}k personas<extra></extra>"
        ))
    fig_man = plot_cfg(fig_man, 260)
    fig_man.update_layout(yaxis_title="Miles de personas")
    st.plotly_chart(fig_man, use_container_width=True)

with col6:
    st.markdown(f'<div class="section-hdr">{SVG_BANK}<span class="section-hdr-text">Crédito comercial empresarial</span></div>', unsafe_allow_html=True)
    panel_cred = panel_filt.copy()
    panel_cred["cred_k"] = (panel_cred["credito_pesos"]/1000).round(1)
    fig_cred = go.Figure()
    for e in ESTADOS:
        de = panel_cred[panel_cred["entidad"]==e].sort_values("anio")
        sel = (e == estado_sel)
        fig_cred.add_trace(go.Scatter(
            x=de["anio"], y=de["cred_k"], name=e,
            mode="lines+markers",
            line=dict(color=get_color(e), width=2.5 if sel else 1, dash="solid" if sel else "dash"),
            marker=dict(size=5 if sel else 3),
            opacity=1.0 if sel else 0.4,
            hovertemplate=f"<b>{e}</b><br>%{{x}}: %{{y:.1f}} miles de mill. pesos<extra></extra>"
        ))
    fig_cred = plot_cfg(fig_cred, 260)
    fig_cred.update_layout(yaxis_title="Miles de mill. pesos")
    st.plotly_chart(fig_cred, use_container_width=True)


# ── INPC + Tabla ──────────────────────────────────────────────────────
col7, col8 = st.columns(2)

with col7:
    st.markdown(f'<div class="section-hdr">{SVG_TREND_DOWN}<span class="section-hdr-text">INPC general vs. subíndice energéticos</span></div>', unsafe_allow_html=True)
    inpc_data = panel_filt[["anio","inpc_general","inpc_energia"]].drop_duplicates().sort_values("anio")
    fig_inpc = go.Figure()
    fig_inpc.add_trace(go.Scatter(
        x=inpc_data["anio"], y=inpc_data["inpc_general"].round(2),
        name="INPC General", mode="lines+markers",
        line=dict(color="#0A9396", width=2.5),
        marker=dict(size=6, symbol="circle"),
        fill="tozeroy", fillcolor="rgba(10,147,150,0.06)",
        hovertemplate="INPC General %{x}: %{y:.2f}<extra></extra>"
    ))
    fig_inpc.add_trace(go.Scatter(
        x=inpc_data["anio"], y=inpc_data["inpc_energia"].round(2),
        name="Energéticos", mode="lines+markers",
        line=dict(color="#EE6C4D", width=2, dash="dot"),
        marker=dict(size=5, symbol="diamond"),
        hovertemplate="Energéticos %{x}: %{y:.2f}<extra></extra>"
    ))
    fig_inpc = plot_cfg(fig_inpc, 260)
    fig_inpc.update_layout(yaxis_title="Índice (base Jul 2018=100)")
    st.plotly_chart(fig_inpc, use_container_width=True)

with col8:
    st.markdown(f'<div class="section-hdr">{SVG_TABLE}<span class="section-hdr-text">Datos del ICAI — {estado_sel}</span></div>', unsafe_allow_html=True)
    tabla = datos_estado[["anio","ICAI","ied_usd","exportaciones_usd","credito_pesos","personal_ocupado"]].copy()
    tabla.columns = ["Año","ICAI","IED (mill. USD)","Exportaciones (miles USD)","Crédito (mill. pesos)","Personal manuf."]
    tabla["ICAI"] = tabla["ICAI"].round(1)
    tabla["IED (mill. USD)"] = tabla["IED (mill. USD)"].round(1)
    tabla["Exportaciones (miles USD)"] = tabla["Exportaciones (miles USD)"].apply(lambda x: f"{x:,.0f}")
    tabla["Crédito (mill. pesos)"] = tabla["Crédito (mill. pesos)"].round(1)
    tabla["Personal manuf."] = tabla["Personal manuf."].apply(lambda x: f"{x:,.0f}")
    tabla = tabla.sort_values("Año", ascending=False).reset_index(drop=True)
    st.dataframe(tabla, use_container_width=True, height=260, hide_index=True)


# ── Footer ────────────────────────────────────────────────────────────
st.markdown('<div class="grad-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:12px 0;font-size:10px;
    color:rgba(180,210,220,0.25);font-family:'JetBrains Mono',monospace;letter-spacing:0.5px;">
    ICAI — Índice Compuesto de Atractividad Industrial del Corredor del Bajío &nbsp;·&nbsp;
    Equipo 11 · Taller de Fundamentos para el Análisis de Datos &nbsp;·&nbsp;
    SE · INEGI (EMIM, ETEF) · CNBV · Banxico-SIE
</div>
""", unsafe_allow_html=True)
