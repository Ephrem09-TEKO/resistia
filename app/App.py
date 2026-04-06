import streamlit as st
import os

# Auto-génération si déploiement cloud
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.load_model import verifier_ou_generer
verifier_ou_generer()

st.set_page_config(
    page_title  = "ResistIA — Global Biotek",
    page_icon   = "🧬",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)

# ── CSS ──────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A5276 0%, #0D2137 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebarNav"] { padding-top: 0 !important; }

    h1 { color: #1A5276 !important; }
    h2 { color: #1A5276 !important; }
    h3 { color: #1E8449 !important; }

    .stButton > button {
        background-color: #1E8449; color: white;
        border-radius: 8px; border: none;
        padding: 0.6rem 2rem; font-weight: bold;
        font-size: 1rem; width: 100%;
    }
    .stButton > button:hover { background-color: #196F3D; }

    [data-testid="metric-container"] {
        background: #D6EAF8;
        border-left: 5px solid #1A5276;
        border-radius: 8px; padding: 1rem;
    }
    .avertissement {
        background: #FDEBD0;
        border-left: 5px solid #D35400;
        padding: 0.8rem 1.2rem;
        border-radius: 6px; margin-bottom: 1rem;
    }
    .module-card {
        background: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #1A5276;
    }
    .module-card:hover {
        background: #EBF5FB;
        border-left: 4px solid #1E8449;
    }
    .footer-credit {
        display: flex; align-items: center;
        justify-content: center; gap: 10px;
        color: #888; font-size: 0.8rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Chemins logos ─────────────────────────────────
APP_DIR    = os.path.dirname(os.path.abspath(__file__))
logo_banner   = os.path.join(APP_DIR, "logo_resistia_banner.png")
logo_blanc    = os.path.join(APP_DIR, "logo_resistia.png")
logo_icon     = os.path.join(APP_DIR, "logo_resistia_icon.png")
logo_gbiotek  = os.path.join(APP_DIR, "logo_globalbiotek.jpg")

# ── SIDEBAR ───────────────────────────────────────
with st.sidebar:
    # ── Logo ResistIA fond blanc ──
    if os.path.exists(logo_blanc):
        st.image(logo_blanc, width=220)

    # ── Description ──
    st.markdown(
        "<p style='font-size:0.82rem; color:#AED6F1; text-align:center; margin-top:4px;'>"
        "Plateforme IA de Recommandation<br>Thérapeutique — Afrique de l'Ouest"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ── Label Navigation ──
    st.markdown(
        "<p style='font-size:0.78rem; color:#85C1E9; "
        "font-weight:bold; letter-spacing:1px;'>"
        "NAVIGATION</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ── Crédit Global Biotek en bas ──
    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.72rem; color:#7FB3D3; "
        "text-align:center; margin-bottom:4px; margin-top:40px;'>"
        "Un projet</p>",
        unsafe_allow_html=True
    )
    if os.path.exists(logo_gbiotek):
        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            st.image(logo_gbiotek, width=75)
    st.markdown(
        "<p style='font-size:0.68rem; color:#7FB3D3; text-align:center;'>"
        "v1.0 — VivaTech Paris 2026</p>",
        unsafe_allow_html=True
    )

# ── PAGE ACCUEIL ──────────────────────────────────

# Banner ResistIA pleine largeur
if os.path.exists(logo_banner):
    st.image(logo_banner, use_container_width=True)
else:
    st.title("🧬 ResistIA")

st.markdown("")

# Sous-titre + description
st.markdown(
    "<h2 style='color:#1A5276; margin-top:0;'>"
    "Plateforme IA de Recommandation Thérapeutique<br>"
    "contre la Résistance aux Antibiotiques</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color:#555; font-size:1rem;'>"
    "Développée dans le cadre du projet <strong>Global Biotek</strong> "
    "— Afrique de l'Ouest &nbsp;|&nbsp; "
    "<strong>VivaTech Paris, Juin 2026</strong></p>",
    unsafe_allow_html=True
)

# Avertissement
st.markdown("""
<div class="avertissement">
⚠️ <strong>Avertissement médical :</strong> ResistIA est un outil d'aide à la décision
clinique fondé sur des données épidémiologiques régionales. Les recommandations générées
ne remplacent pas l'avis d'un professionnel de santé qualifié. Tout traitement doit être
prescrit par un médecin.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── KPIs ─────────────────────────────────────────
st.subheader("📊 Base de données ResistIA")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧫 Antibiogrammes",   "64 000")
col2.metric("🦠 Bactéries ESKAPE", "9")
col3.metric("💊 Antibiotiques",    "23")
col4.metric("🌍 Pays ECOWAS",      "8")

st.markdown("---")

# ── Modules ───────────────────────────────────────
st.subheader("🗺️ Modules de la plateforme")

col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown("""
    <div class="module-card">
        <strong>🔬 Recommandation Thérapeutique</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        Saisissez une bactérie, un pays et un site de prélèvement.
        Obtenez instantanément les antibiotiques classés par efficacité
        et les cocktails thérapeutiques suggérés.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <strong>🗺️ Heatmap Régionale</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        Carte interactive de résistance bactérie × antibiotique
        pour les 8 pays ECOWAS. Filtrage par pays disponible.
        </span>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div class="module-card">
        <strong>📊 Statistiques</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        Distribution S/I/R, top pathogènes résistants, efficacité
        des antibiotiques par région et évolution temporelle 2019–2024.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <strong>ℹ️ À propos</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        Méthodologie, sources de données (CARD, GLASS/OMS),
        équipe projet et avertissement légal complet.
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Footer ────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
with col_f2:
    if os.path.exists(logo_icon):
        st.image(logo_icon, width=60)
    st.markdown(
        "<p style='text-align:center; color:#888; font-size:0.8rem;'>"
        "ResistIA v1.0 — Global Biotek © 2026<br>"
        "Données : CARD v4.0.1 + Dataset synthétique ECOWAS calibré GLASS/OMS 2022"
        "</p>",
        unsafe_allow_html=True
    )