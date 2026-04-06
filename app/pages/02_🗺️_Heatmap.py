# ═══════════════════════════════════════════════════
# pages/02_🗺️_Heatmap.py
# Module M3 — Heatmap Régionale
# ═══════════════════════════════════════════════════
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.recommender import PAYS

st.set_page_config(
    page_title="Heatmap — ResistIA",
    page_icon="🗺️",
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
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, "..", "data", "processed")

@st.cache_data
def charger_donnees():
  df = pd.read_csv(os.path.join(DATA_DIR, "dataset_complet.csv"))
  return df

df = charger_donnees()

# ── EN-TÊTE ──
st.title("🗺️ Heatmap Régionale de Résistance")
st.markdown("*Taux de résistance par paire bactérie × antibiotique — Afrique de l'Ouest ECOWAS*")
st.markdown("---")

# ── Filtres ──
col1, col2 = st.columns([1, 2])
with col1:
    pays_options = ["Tous les pays"] + sorted(df["country"].unique().tolist())
    pays_selectionne = st.selectbox("🌍 Filtrer par pays", options=pays_options)

with col2:
    st.markdown("""
    <div style='background:#D6EAF8; border-left:4px solid #1A5276;
                padding:0.6rem 1rem; border-radius:6px; margin-top:0.3rem;'>
    🟢 <strong>Vert</strong> = Résistance faible (antibiotique efficace) &nbsp;|&nbsp;
    🔴 <strong>Rouge</strong> = Résistance élevée (antibiotique à éviter)
    </div>
    """, unsafe_allow_html=True)

# ── Filtrer ──
if pays_selectionne != "Tous les pays":
    df_filtre = df[df["country"] == pays_selectionne]
else:
    df_filtre = df.copy()

# ── Calcul pivot ──
pivot = df_filtre.groupby(
    ["bacteria_name", "antibiotic"]
)["is_resistant"].mean().reset_index()
pivot.columns = ["Bactérie", "Antibiotique", "Taux_Résistance"]

pivot_table = pivot.pivot(
    index="Bactérie",
    columns="Antibiotique",
    values="Taux_Résistance"
).fillna(0)

# Abréger noms bactéries
def abreger(nom):
    parts = nom.split()
    return f"{parts[0][0]}. {parts[1]}" if len(parts) >= 2 else nom

pivot_table.index = [abreger(b) for b in pivot_table.index]

# ── Heatmap Plotly ──
fig = go.Figure(data=go.Heatmap(
    z=pivot_table.values * 100,
    x=pivot_table.columns.tolist(),
    y=pivot_table.index.tolist(),
    colorscale=[
        [0.0,  "#1E8449"],
        [0.25, "#58D68D"],
        [0.5,  "#F9E79F"],
        [0.75, "#E67E22"],
        [1.0,  "#C0392B"],
    ],
    zmin=0, zmax=100,
    hoverongaps=False,
    hovertemplate=(
        "<b>%{y}</b> × <b>%{x}</b><br>"
        "Taux de résistance : <b>%{z:.1f}%</b><extra></extra>"
    ),
    colorbar=dict(
        title="Résistance (%)",
        ticksuffix="%",
        thickness=15,
        len=0.8,
    ),
    text=[[f"{v*100:.0f}%" for v in row] for row in pivot_table.values],
    texttemplate="%{text}",
    textfont=dict(size=10),
))

fig.update_layout(
    title=dict(
        text=f"Résistance bactérie × antibiotique — {pays_selectionne}",
        font=dict(size=15, color="#1A5276"),
        x=0.5
    ),
    xaxis=dict(
        title="Antibiotique",
        tickangle=-35,
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        title="Bactérie",
        tickfont=dict(size=11),
        autorange="reversed",
    ),
    height=480,
    margin=dict(l=20, r=20, t=60, b=120),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

st.plotly_chart(fig, use_container_width=True)

# ── Top 5 résistances ──
st.markdown("---")
col_top1, col_top2 = st.columns(2)

with col_top1:
    st.markdown("### 🔴 Top 5 — Paires les plus résistantes")
    top_resist = pivot.sort_values("Taux_Résistance", ascending=False).head(5).copy()
    top_resist["Taux_Résistance"] = (top_resist["Taux_Résistance"] * 100).round(1).astype(str) + "%"
    top_resist.columns = ["Bactérie", "Antibiotique", "Taux Résistance"]
    st.dataframe(top_resist, use_container_width=True, hide_index=True)

with col_top2:
    st.markdown("### 🟢 Top 5 — Antibiotiques les plus efficaces")
    top_eff = pivot.groupby("Antibiotique")["Taux_Résistance"].mean()
    top_eff = (1 - top_eff).sort_values(ascending=False).head(5).reset_index()
    top_eff.columns = ["Antibiotique", "Efficacité Moyenne"]
    top_eff["Efficacité Moyenne"] = (top_eff["Efficacité Moyenne"] * 100).round(1).astype(str) + "%"
    st.dataframe(top_eff, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown(f"""
<div style='text-align:center; color:#555; font-size:0.85rem;'>
Données : {len(df_filtre):,} antibiogrammes — {pays_selectionne} |
Source : CARD v4.0.1 + Dataset ECOWAS calibré GLASS/OMS 2022
</div>
""", unsafe_allow_html=True)