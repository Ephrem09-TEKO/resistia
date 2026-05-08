# ═══════════════════════════════════════════════════
# pages/03_🗺️_Heatmap.py
# Module — Regional Heatmap / Heatmap Régionale
# ═══════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Heatmap — ResistIA",
    page_icon="🗺️",
    layout="wide"
)

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

TEXT = {
    "Français": {
        "sidebar_desc": "Plateforme IA de Recommandation<br>Thérapeutique — Afrique de l'Ouest",
        "title": "🗺️ Heatmap Régionale de Résistance",
        "subtitle": "*Visualisation des taux de résistance par paire bactérie × antibiotique en Afrique de l’Ouest.*",
        "objective": "<strong>Objectif :</strong> identifier rapidement les zones critiques de résistance. Le vert indique une faible résistance, tandis que le rouge signale une résistance élevée.",
        "filters": "🎛️ Filtres d’analyse",
        "country_filter": "🌍 Filtrer par pays",
        "all_countries": "Tous les pays",
        "legend": "🟢 <strong>Vert</strong> = résistance faible / antibiotique plus efficace<br>🟡 <strong>Jaune</strong> = résistance intermédiaire<br>🔴 <strong>Rouge</strong> = résistance élevée / antibiotique à éviter",
        "antibiograms": "🧫 Antibiogrammes",
        "bacteria": "🦠 Bactéries",
        "antibiotics": "💊 Antibiotiques",
        "context": "🌍 Contexte",
        "heatmap_title": "🔥 Carte de résistance bactérie × antibiotique",
        "plot_title": "Résistance bactérie × antibiotique",
        "xaxis": "Antibiotique",
        "yaxis": "Bactérie",
        "colorbar": "Résistance (%)",
        "hover_resistance": "Taux de résistance",
        "top_resistant": "### 🔴 Top 5 — Paires les plus résistantes",
        "top_effective": "### 🟢 Top 5 — Antibiotiques les plus efficaces",
        "col_bacteria": "Bactérie",
        "col_antibiotic": "Antibiotique",
        "col_resistance": "Taux Résistance",
        "col_eff": "Efficacité Moyenne",
        "quick_read": "Lecture rapide",
        "quick_text": "Sur le périmètre <strong>{country}</strong>, le taux moyen de résistance observé est de <strong>{mean:.1f}%</strong>. La paire la plus critique est <strong>{pair}</strong>. L’antibiotique avec la meilleure efficacité moyenne est <strong>{best}</strong>.",
        "footer": "Données : {n:,} antibiogrammes — {country} | Source : CARD v4.0.1 + Dataset ECOWAS calibré GLASS/OMS 2022",
    },
    "English": {
        "sidebar_desc": "AI-Powered Therapeutic<br>Recommendation Platform — West Africa",
        "title": "🗺️ Regional Resistance Heatmap",
        "subtitle": "*Visualization of resistance rates by bacterium × antibiotic pair across West Africa.*",
        "objective": "<strong>Goal:</strong> quickly identify critical resistance patterns. Green indicates low resistance, while red indicates high resistance.",
        "filters": "🎛️ Analysis filters",
        "country_filter": "🌍 Filter by country",
        "all_countries": "All countries",
        "legend": "🟢 <strong>Green</strong> = low resistance / more effective antibiotic<br>🟡 <strong>Yellow</strong> = intermediate resistance<br>🔴 <strong>Red</strong> = high resistance / antibiotic to avoid",
        "antibiograms": "🧫 Antibiograms",
        "bacteria": "🦠 Bacteria",
        "antibiotics": "💊 Antibiotics",
        "context": "🌍 Context",
        "heatmap_title": "🔥 Bacterium × antibiotic resistance map",
        "plot_title": "Bacterium × antibiotic resistance",
        "xaxis": "Antibiotic",
        "yaxis": "Bacterium",
        "colorbar": "Resistance (%)",
        "hover_resistance": "Resistance rate",
        "top_resistant": "### 🔴 Top 5 — Most resistant pairs",
        "top_effective": "### 🟢 Top 5 — Most effective antibiotics",
        "col_bacteria": "Bacterium",
        "col_antibiotic": "Antibiotic",
        "col_resistance": "Resistance Rate",
        "col_eff": "Average Effectiveness",
        "quick_read": "Quick read",
        "quick_text": "For <strong>{country}</strong>, the average observed resistance rate is <strong>{mean:.1f}%</strong>. The most critical pair is <strong>{pair}</strong>. The antibiotic with the best average effectiveness is <strong>{best}</strong>.",
        "footer": "Data: {n:,} antibiograms — {country} | Source: CARD v4.0.1 + ECOWAS dataset calibrated with WHO GLASS 2022",
    }
}

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A5276 0%, #0B1F33 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebarNav"] > div:first-child { display: none; }
[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(255,255,255,0.10);
    border-radius: 8px;
    transition: all 0.25s ease;
}
h1, h2 { color: #1A5276 !important; }
h3 { color: #1E8449 !important; }

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
.legend-card {
    background: #F8F9FA;
    border: 1px solid #DEE2E6;
    border-left: 5px solid #1E8449;
    padding: 0.85rem 1.1rem;
    border-radius: 10px;
    margin-top: 0.2rem;
    line-height: 1.8;
}
.data-card {
    background: #F8F9FA;
    border: 1px solid #DEE2E6;
    border-radius: 12px;
    padding: 1rem;
    border-left: 4px solid #1A5276;
    transition: all 0.25s ease;
}
.data-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}
hr {
    border: none;
    height: 1px;
    background: #EAECEE;
}
</style>
""", unsafe_allow_html=True)

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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

@st.cache_data
def charger_donnees():
    return pd.read_csv(os.path.join(DATA_DIR, "dataset_complet.csv"))

df = charger_donnees()
tx = TEXT[st.session_state["lang"]]

st.title(tx["title"])
st.markdown(tx["subtitle"])

st.markdown(f"""
<div class="info-card">
{tx["objective"]}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.subheader(tx["filters"])

col1, col2 = st.columns([1, 2])

with col1:
    pays_options = [tx["all_countries"]] + sorted(df["country"].unique().tolist())
    pays_selectionne = st.selectbox(tx["country_filter"], options=pays_options)

with col2:
    st.markdown(
        f"<div class='legend-card'>{tx['legend']}</div>",
        unsafe_allow_html=True
    )

if pays_selectionne != tx["all_countries"]:
    df_filtre = df[df["country"] == pays_selectionne]
else:
    df_filtre = df.copy()

pivot = df_filtre.groupby(
    ["bacteria_name", "antibiotic"]
)["is_resistant"].mean().reset_index()

pivot.columns = [tx["col_bacteria"], tx["col_antibiotic"], "Taux_Résistance"]

pivot_table = pivot.pivot(
    index=tx["col_bacteria"],
    columns=tx["col_antibiotic"],
    values="Taux_Résistance"
).fillna(0)

def abreger(nom):
    parts = nom.split()
    return f"{parts[0][0]}. {parts[1]}" if len(parts) >= 2 else nom

pivot_table.index = [abreger(b) for b in pivot_table.index]

st.markdown("---")

col_k1, col_k2, col_k3, col_k4 = st.columns(4)
col_k1.metric(tx["antibiograms"], f"{len(df_filtre):,}")
col_k2.metric(tx["bacteria"], pivot[tx["col_bacteria"]].nunique())
col_k3.metric(tx["antibiotics"], pivot[tx["col_antibiotic"]].nunique())
col_k4.metric(tx["context"], pays_selectionne)

st.markdown("---")
st.subheader(tx["heatmap_title"])

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
    zmin=0,
    zmax=100,
    hoverongaps=False,
    hovertemplate=(
        "<b>%{y}</b> × <b>%{x}</b><br>"
        f"{tx['hover_resistance']} : <b>%{{z:.1f}}%</b><extra></extra>"
    ),
    colorbar=dict(
        title=tx["colorbar"],
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
        text=f"{tx['plot_title']} — {pays_selectionne}",
        font=dict(size=15, color="#1A5276"),
        x=0.5
    ),
    xaxis=dict(title=tx["xaxis"], tickangle=-35, tickfont=dict(size=11)),
    yaxis=dict(title=tx["yaxis"], tickfont=dict(size=11), autorange="reversed"),
    height=520,
    margin=dict(l=20, r=20, t=60, b=120),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col_top1, col_top2 = st.columns(2)

with col_top1:
    st.markdown(tx["top_resistant"])

    top_resist = pivot.sort_values("Taux_Résistance", ascending=False).head(5).copy()
    top_resist["Taux_Résistance"] = (
        top_resist["Taux_Résistance"] * 100
    ).round(1).astype(str) + "%"

    top_resist.columns = [tx["col_bacteria"], tx["col_antibiotic"], tx["col_resistance"]]

    st.markdown("<div class='data-card'>", unsafe_allow_html=True)
    st.dataframe(top_resist, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_top2:
    st.markdown(tx["top_effective"])

    top_eff = pivot.groupby(tx["col_antibiotic"])["Taux_Résistance"].mean()
    top_eff = (1 - top_eff).sort_values(ascending=False).head(5).reset_index()
    top_eff.columns = [tx["col_antibiotic"], tx["col_eff"]]
    top_eff[tx["col_eff"]] = (
        top_eff[tx["col_eff"]] * 100
    ).round(1).astype(str) + "%"

    st.markdown("<div class='data-card'>", unsafe_allow_html=True)
    st.dataframe(top_eff, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

moy_resistance = pivot["Taux_Résistance"].mean() * 100
pire_ligne = pivot.sort_values("Taux_Résistance", ascending=False).iloc[0]
meilleur_atb = top_eff.iloc[0][tx["col_antibiotic"]]

pair_critique = f"{pire_ligne[tx['col_bacteria']]} × {pire_ligne[tx['col_antibiotic']]}"

st.markdown(f"""
<div class="info-card">
<strong>{tx["quick_read"]}:</strong><br>
{tx["quick_text"].format(
    country=pays_selectionne,
    mean=moy_resistance,
    pair=pair_critique,
    best=meilleur_atb
)}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align:center; color:#555; font-size:0.85rem;'>
{tx["footer"].format(n=len(df_filtre), country=pays_selectionne)}
</div>
""", unsafe_allow_html=True)