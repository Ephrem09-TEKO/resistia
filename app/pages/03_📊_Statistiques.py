# ═══════════════════════════════════════════════════
# pages/03_📊_Statistiques.py
# Module M4 — Statistiques
# ═══════════════════════════════════════════════════
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Statistiques — ResistIA",
    page_icon="📊",
    layout="wide"
)

# ── CSS ──
st.markdown("""
<style>
[data-testid="stSidebar"] { background: linear-gradient(180deg,#1A5276 0%,#154360 100%); }
[data-testid="stSidebar"] * { color: white !important; }
h1, h2 { color: #1A5276 !important; }
h3     { color: #1E8449 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    APP_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_blanc  = os.path.join(APP_DIR, "logo_resistia.png")
    logo_gbiotek= os.path.join(APP_DIR, "logo_globalbiotek.jpg")

    if os.path.exists(logo_blanc):
        st.image(logo_blanc, width=220)

    st.markdown(
        "<p style='font-size:0.82rem; color:#AED6F1; text-align:center; margin-top:4px;'>"
        "Plateforme IA de Recommandation<br>Thérapeutique — Afrique de l'Ouest"
        "</p>", unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.78rem; color:#85C1E9; "
        "font-weight:bold; letter-spacing:1px;'>NAVIGATION</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.72rem; color:#7FB3D3; "
        "text-align:center; margin-bottom:4px; margin-top:40px;'>"
        "Un projet</p>", unsafe_allow_html=True
    )
    if os.path.exists(logo_gbiotek):
        col_l, col_m, col_r = st.columns([1,2,1])
        with col_m:
            st.image(logo_gbiotek, width=75)
    st.markdown(
        "<p style='font-size:0.68rem; color:#7FB3D3; text-align:center;'>"
        "v1.0 — Avril 2026</p>", unsafe_allow_html=True
    )

# ── Charger données ──
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

@st.cache_data
def charger_donnees():
    return pd.read_csv(os.path.join(DATA_DIR, "dataset_complet.csv"))

df = charger_donnees()

# ── EN-TÊTE ──
st.title("📊 Tableau de Bord Statistiques")
st.markdown("*Vue d'ensemble épidémiologique — Résistance aux antibiotiques en Afrique de l'Ouest*")
st.markdown("---")

# ── KPIs ──
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🧫 Antibiogrammes", f"{len(df):,}")
col2.metric("🦠 Bactéries", df["bacteria_name"].nunique())
col3.metric("💊 Antibiotiques", df["antibiotic"].nunique())
col4.metric("🌍 Pays", df["country"].nunique())
taux_global = df["is_resistant"].mean()
col5.metric("📈 Taux résistance global", f"{taux_global*100:.1f}%")

st.markdown("---")

# ── Ligne 1 : Distribution S/I/R + Top bactéries ──
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("### 🔬 Distribution S / I / R")
    dist = df["resistance"].value_counts()
    colors = {"S": "#1E8449", "I": "#E67E22", "R": "#C0392B"}
    fig1 = go.Figure(go.Pie(
        labels=["Sensible (S)", "Résistant (R)", "Intermédiaire (I)"],
        values=[dist.get("S", 0), dist.get("R", 0), dist.get("I", 0)],
        marker_colors=[colors["S"], colors["R"], colors["I"]],
        hole=0.45,
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>%{value:,} cas (%{percent})<extra></extra>",
    ))
    fig1.update_layout(
        height=320, margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="white",
        annotations=[dict(text=f"{len(df):,}<br>cas", x=0.5, y=0.5,
                          font_size=14, showarrow=False)]
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.markdown("### 🦠 Bactéries par taux de résistance")
    bact_resist = df.groupby("bacteria_name")["is_resistant"].mean().sort_values()
    bact_labels = [b.split()[0][0] + ". " + b.split()[1] for b in bact_resist.index]
    bact_colors = ["#C0392B" if v >= 0.5 else "#E67E22" if v >= 0.35
                   else "#1E8449" for v in bact_resist.values]
    fig2 = go.Figure(go.Bar(
        x=bact_resist.values * 100,
        y=bact_labels,
        orientation="h",
        marker_color=bact_colors,
        text=[f"{v*100:.1f}%" for v in bact_resist.values],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Taux résistance : %{x:.1f}%<extra></extra>",
    ))
    fig2.update_layout(
        xaxis_title="Taux de résistance (%)",
        height=320,
        margin=dict(l=10, r=60, t=30, b=40),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    fig2.update_xaxes(range=[0, 90], showgrid=True, gridcolor="#EEEEEE")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Ligne 2 : Efficacité antibiotiques + Distribution par pays ──
col_g3, col_g4 = st.columns(2)

with col_g3:
    st.markdown("### 💊 Antibiotiques — Efficacité moyenne")
    atb_eff = (1 - df.groupby("antibiotic")["is_resistant"].mean()).sort_values()
    atb_colors = ["#1E8449" if v >= 0.8 else "#E67E22" if v >= 0.6
                  else "#C0392B" for v in atb_eff.values]
    fig3 = go.Figure(go.Bar(
        x=atb_eff.values * 100,
        y=atb_eff.index.tolist(),
        orientation="h",
        marker_color=atb_colors,
        text=[f"{v*100:.1f}%" for v in atb_eff.values],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Efficacité : %{x:.1f}%<extra></extra>",
    ))
    fig3.add_vline(x=80, line_dash="dash", line_color="#1E8449")
    fig3.update_layout(
        xaxis_title="Efficacité estimée (%)",
        height=400,
        margin=dict(l=10, r=80, t=30, b=40),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    fig3.update_xaxes(range=[0, 115], showgrid=True, gridcolor="#EEEEEE")
    st.plotly_chart(fig3, use_container_width=True)

with col_g4:
    st.markdown("### 🌍 Résistance par pays ECOWAS")
    pays_resist = df.groupby("country")["is_resistant"].mean().sort_values(ascending=False)
    pays_colors = ["#C0392B" if v >= 0.5 else "#E67E22" if v >= 0.4
                   else "#1E8449" for v in pays_resist.values]
    fig4 = go.Figure(go.Bar(
        x=pays_resist.index.tolist(),
        y=pays_resist.values * 100,
        marker_color=pays_colors,
        text=[f"{v*100:.1f}%" for v in pays_resist.values],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Taux résistance : %{y:.1f}%<extra></extra>",
    ))
    fig4.update_layout(
        yaxis_title="Taux de résistance (%)",
        height=400,
        margin=dict(l=20, r=20, t=30, b=80),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    fig4.update_yaxes(range=[0, 60], showgrid=True, gridcolor="#EEEEEE")
    fig4.update_xaxes(tickangle=-30)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── Ligne 3 : Évolution temporelle ──
st.markdown("### 📈 Évolution du taux de résistance global (2019–2024)")
evolution = df.groupby("year")["is_resistant"].mean().reset_index()
fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=evolution["year"],
    y=evolution["is_resistant"] * 100,
    mode="lines+markers",
    line=dict(color="#1A5276", width=3),
    marker=dict(size=8, color="#1A5276"),
    fill="tozeroy",
    fillcolor="rgba(26,82,118,0.1)",
    hovertemplate="<b>%{x}</b><br>Taux résistance : %{y:.2f}%<extra></extra>",
    name="Taux global"
))
fig5.update_layout(
    xaxis_title="Année",
    yaxis_title="Taux de résistance (%)",
    height=280,
    margin=dict(l=20, r=20, t=20, b=40),
    plot_bgcolor="white", paper_bgcolor="white",
    showlegend=False,
)
fig5.update_xaxes(dtick=1, showgrid=True, gridcolor="#EEEEEE")
fig5.update_yaxes(range=[40, 55], showgrid=True, gridcolor="#EEEEEE")
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#555; font-size:0.85rem;'>
Source : CARD v4.0.1 + Dataset synthétique ECOWAS calibré GLASS/OMS 2022 |
ResistIA v1.0 — Global Biotek © 2026
</div>
""", unsafe_allow_html=True)