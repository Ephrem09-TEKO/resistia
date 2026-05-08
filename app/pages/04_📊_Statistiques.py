# ═══════════════════════════════════════════════════
# pages/04_📊_Statistiques.py
# Module — Statistics / Statistiques
# ═══════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Statistics — ResistIA",
    page_icon="📊",
    layout="wide"
)

# ═══════════════════════════════════════════════════
# LANGUAGE
# ═══════════════════════════════════════════════════

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

TEXT = {
    "Français": {
        "sidebar_desc": "Plateforme IA de Recommandation<br>Thérapeutique — Afrique de l'Ouest",
        "title": "📊 Tableau de Bord Statistiques",
        "subtitle": "*Vue d’ensemble épidémiologique de la résistance aux antibiotiques en Afrique de l’Ouest.*",
        "objective": "<strong>Objectif :</strong> fournir une lecture rapide des tendances de résistance : distribution S/I/R, bactéries prioritaires, efficacité des antibiotiques, comparaison par pays et évolution temporelle.",
        "kpi_title": "📌 Indicateurs clés",
        "antibiograms": "🧫 Antibiogrammes",
        "bacteria": "🦠 Bactéries",
        "antibiotics": "💊 Antibiotiques",
        "countries": "🌍 Pays",
        "global_resistance": "📈 Résistance globale",
        "sir_dist": "### 🔬 Distribution S / I / R",
        "susceptible": "Sensible (S)",
        "resistant": "Résistant (R)",
        "intermediate": "Intermédiaire (I)",
        "cases": "cas",
        "bacteria_resistance": "### 🦠 Bactéries par taux de résistance",
        "resistance_rate": "Taux de résistance",
        "antibiotic_eff": "### 💊 Antibiotiques — efficacité moyenne",
        "effectiveness": "Efficacité",
        "estimated_eff": "Efficacité estimée (%)",
        "country_resistance": "### 🌍 Résistance par pays ECOWAS",
        "temporal": "### 📈 Évolution du taux de résistance global (2019–2024)",
        "year": "Année",
        "quick_read": "Lecture rapide",
        "quick_text": "Le taux global de résistance observé est de <strong>{global_rate:.1f}%</strong>. La bactérie présentant le profil le plus critique est <strong>{bact_max}</strong>. L’antibiotique ayant la meilleure efficacité moyenne est <strong>{atb_best}</strong>. Le pays avec le taux moyen le plus élevé dans ce dataset est <strong>{pays_max}</strong>.",
        "footer": "Source : CARD v4.0.1 + Dataset synthétique ECOWAS calibré GLASS/OMS 2022 | ResistIA v1.0 — Global Biotek © 2026",
    },

    "English": {
        "sidebar_desc": "AI-Powered Therapeutic<br>Recommendation Platform — West Africa",
        "title": "📊 Statistics Dashboard",
        "subtitle": "*Epidemiological overview of antibiotic resistance across West Africa.*",
        "objective": "<strong>Goal:</strong> provide a fast overview of resistance trends: S/I/R distribution, priority bacteria, antibiotic effectiveness, country comparison, and temporal evolution.",
        "kpi_title": "📌 Key indicators",
        "antibiograms": "🧫 Antibiograms",
        "bacteria": "🦠 Bacteria",
        "antibiotics": "💊 Antibiotics",
        "countries": "🌍 Countries",
        "global_resistance": "📈 Global resistance",
        "sir_dist": "### 🔬 S / I / R distribution",
        "susceptible": "Susceptible (S)",
        "resistant": "Resistant (R)",
        "intermediate": "Intermediate (I)",
        "cases": "cases",
        "bacteria_resistance": "### 🦠 Bacteria by resistance rate",
        "resistance_rate": "Resistance rate",
        "antibiotic_eff": "### 💊 Antibiotics — average effectiveness",
        "effectiveness": "Effectiveness",
        "estimated_eff": "Estimated effectiveness (%)",
        "country_resistance": "### 🌍 Resistance by ECOWAS country",
        "temporal": "### 📈 Global resistance trend (2019–2024)",
        "year": "Year",
        "quick_read": "Quick read",
        "quick_text": "The observed global resistance rate is <strong>{global_rate:.1f}%</strong>. The bacterium with the most critical profile is <strong>{bact_max}</strong>. The antibiotic with the best average effectiveness is <strong>{atb_best}</strong>. The country with the highest average rate in this dataset is <strong>{pays_max}</strong>.",
        "footer": "Source: CARD v4.0.1 + ECOWAS dataset calibrated with WHO GLASS 2022 | ResistIA v1.0 — Global Biotek © 2026",
    }
}

# ═══════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A5276 0%, #0B1F33 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebarNav"] > div:first-child {
    display: none;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(255,255,255,0.10);
    border-radius: 8px;
    transition: all 0.25s ease;
}

h1, h2 {
    color: #1A5276 !important;
}

h3 {
    color: #1E8449 !important;
}

.logo-container {
    animation: fadeIn 1s ease-in-out;
    text-align: center;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-8px); }
    to { opacity: 1; transform: translateY(0); }
}

.sidebar-desc {
    font-size: 0.8rem;
    color: #AED6F1;
    text-align: center;
    margin-top: 6px;
}

.info-card {
    background: #EBF5FB;
    border-left: 5px solid #1A5276;
    padding: 1rem 1.2rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.chart-card {
    background: #F8F9FA;
    border: 1px solid #DEE2E6;
    border-left: 4px solid #1A5276;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
}

.chart-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}

[data-testid="metric-container"] {
    background: #D6EAF8;
    border-left: 5px solid #1A5276;
    border-radius: 10px;
    padding: 1rem;
}

hr {
    border: none;
    height: 1px;
    background: #EAECEE;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo_blanc = os.path.join(APP_DIR, "logo_resistia.png")

with st.sidebar:
    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)

    if os.path.exists(logo_blanc):
        st.image(logo_blanc, width=200)

    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state["lang"] = st.selectbox(
        "🌍 Language / Langue",
        options=["English", "Français"],
        index=0 if st.session_state["lang"] == "English" else 1
    )

    tx = TEXT[st.session_state["lang"]]

    st.markdown(
        f"<div class='sidebar-desc'>{tx['sidebar_desc']}</div>",
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

@st.cache_data
def charger_donnees():
    return pd.read_csv(os.path.join(DATA_DIR, "dataset_complet.csv"))

df = charger_donnees()
tx = TEXT[st.session_state["lang"]]

# ═══════════════════════════════════════════════════
# PAGE
# ═══════════════════════════════════════════════════

st.title(tx["title"])
st.markdown(tx["subtitle"])

st.markdown(f"""
<div class="info-card">
{tx["objective"]}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── KPIs ─────────────────────────────────────────
st.subheader(tx["kpi_title"])

taux_global = df["is_resistant"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(tx["antibiograms"], f"{len(df):,}")
col2.metric(tx["bacteria"], df["bacteria_name"].nunique())
col3.metric(tx["antibiotics"], df["antibiotic"].nunique())
col4.metric(tx["countries"], df["country"].nunique())
col5.metric(tx["global_resistance"], f"{taux_global*100:.1f}%")

st.markdown("---")

# ── Ligne 1 ──────────────────────────────────────
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown(tx["sir_dist"])

    dist = df["resistance"].value_counts()
    colors = {"S": "#1E8449", "I": "#E67E22", "R": "#C0392B"}

    fig1 = go.Figure(go.Pie(
        labels=[tx["susceptible"], tx["resistant"], tx["intermediate"]],
        values=[dist.get("S", 0), dist.get("R", 0), dist.get("I", 0)],
        marker_colors=[colors["S"], colors["R"], colors["I"]],
        hole=0.48,
        textinfo="label+percent",
        hovertemplate=f"<b>%{{label}}</b><br>%{{value:,}} {tx['cases']} (%{{percent}})<extra></extra>",
    ))

    fig1.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="white",
        annotations=[dict(
            text=f"{len(df):,}<br>{tx['cases']}",
            x=0.5,
            y=0.5,
            font_size=14,
            showarrow=False
        )]
    )

    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.markdown(tx["bacteria_resistance"])

    bact_resist = df.groupby("bacteria_name")["is_resistant"].mean().sort_values()
    bact_labels = [b.split()[0][0] + ". " + b.split()[1] for b in bact_resist.index]

    bact_colors = [
        "#C0392B" if v >= 0.5 else "#E67E22" if v >= 0.35 else "#1E8449"
        for v in bact_resist.values
    ]

    fig2 = go.Figure(go.Bar(
        x=bact_resist.values * 100,
        y=bact_labels,
        orientation="h",
        marker_color=bact_colors,
        text=[f"{v*100:.1f}%" for v in bact_resist.values],
        textposition="outside",
        hovertemplate=f"<b>%{{y}}</b><br>{tx['resistance_rate']} : %{{x:.1f}}%<extra></extra>",
    ))

    fig2.update_layout(
        xaxis_title=f"{tx['resistance_rate']} (%)",
        height=340,
        margin=dict(l=10, r=70, t=30, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig2.update_xaxes(range=[0, 90], showgrid=True, gridcolor="#EEEEEE")

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Ligne 2 ──────────────────────────────────────
col_g3, col_g4 = st.columns(2)

with col_g3:
    st.markdown(tx["antibiotic_eff"])

    atb_eff = (1 - df.groupby("antibiotic")["is_resistant"].mean()).sort_values()

    atb_colors = [
        "#1E8449" if v >= 0.8 else "#E67E22" if v >= 0.6 else "#C0392B"
        for v in atb_eff.values
    ]

    fig3 = go.Figure(go.Bar(
        x=atb_eff.values * 100,
        y=atb_eff.index.tolist(),
        orientation="h",
        marker_color=atb_colors,
        text=[f"{v*100:.1f}%" for v in atb_eff.values],
        textposition="outside",
        hovertemplate=f"<b>%{{y}}</b><br>{tx['effectiveness']} : %{{x:.1f}}%<extra></extra>",
    ))

    fig3.add_vline(x=80, line_dash="dash", line_color="#1E8449")

    fig3.update_layout(
        xaxis_title=tx["estimated_eff"],
        height=430,
        margin=dict(l=10, r=90, t=30, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig3.update_xaxes(range=[0, 115], showgrid=True, gridcolor="#EEEEEE")

    st.plotly_chart(fig3, use_container_width=True)

with col_g4:
    st.markdown(tx["country_resistance"])

    pays_resist = df.groupby("country")["is_resistant"].mean().sort_values(ascending=False)

    pays_colors = [
        "#C0392B" if v >= 0.5 else "#E67E22" if v >= 0.4 else "#1E8449"
        for v in pays_resist.values
    ]

    fig4 = go.Figure(go.Bar(
        x=pays_resist.index.tolist(),
        y=pays_resist.values * 100,
        marker_color=pays_colors,
        text=[f"{v*100:.1f}%" for v in pays_resist.values],
        textposition="outside",
        hovertemplate=f"<b>%{{x}}</b><br>{tx['resistance_rate']} : %{{y:.1f}}%<extra></extra>",
    ))

    fig4.update_layout(
        yaxis_title=f"{tx['resistance_rate']} (%)",
        height=430,
        margin=dict(l=20, r=20, t=30, b=80),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig4.update_yaxes(range=[0, 60], showgrid=True, gridcolor="#EEEEEE")
    fig4.update_xaxes(tickangle=-30)

    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── Évolution temporelle ─────────────────────────
st.markdown(tx["temporal"])

evolution = df.groupby("year")["is_resistant"].mean().reset_index()

fig5 = go.Figure()

fig5.add_trace(go.Scatter(
    x=evolution["year"],
    y=evolution["is_resistant"] * 100,
    mode="lines+markers",
    line=dict(color="#1A5276", width=3),
    marker=dict(size=9, color="#1A5276"),
    fill="tozeroy",
    fillcolor="rgba(26,82,118,0.1)",
    hovertemplate=f"<b>%{{x}}</b><br>{tx['resistance_rate']} : %{{y:.2f}}%<extra></extra>",
    name="Global rate"
))

fig5.update_layout(
    xaxis_title=tx["year"],
    yaxis_title=f"{tx['resistance_rate']} (%)",
    height=320,
    margin=dict(l=20, r=20, t=20, b=40),
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
)

fig5.update_xaxes(dtick=1, showgrid=True, gridcolor="#EEEEEE")
fig5.update_yaxes(range=[40, 55], showgrid=True, gridcolor="#EEEEEE")

st.plotly_chart(fig5, use_container_width=True)

# ── Synthèse finale ──────────────────────────────
st.markdown("---")

bact_max = df.groupby("bacteria_name")["is_resistant"].mean().sort_values(ascending=False).index[0]
atb_best = (1 - df.groupby("antibiotic")["is_resistant"].mean()).sort_values(ascending=False).index[0]
pays_max = df.groupby("country")["is_resistant"].mean().sort_values(ascending=False).index[0]

st.markdown(f"""
<div class="info-card">
<strong>{tx["quick_read"]}:</strong><br>
{tx["quick_text"].format(
    global_rate=taux_global*100,
    bact_max=bact_max,
    atb_best=atb_best,
    pays_max=pays_max
)}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align:center; color:#555; font-size:0.85rem;'>
{tx["footer"]}
</div>
""", unsafe_allow_html=True)