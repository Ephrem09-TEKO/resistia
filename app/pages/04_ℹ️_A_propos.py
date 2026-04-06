# ═══════════════════════════════════════════════════
# pages/04_ℹ️_A_propos.py
# Module M5 — À propos
# ═══════════════════════════════════════════════════
import streamlit as st
import os

st.set_page_config(
    page_title="À propos — ResistIA",
    page_icon="ℹ️",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebar"] { background: linear-gradient(180deg,#1A5276 0%,#154360 100%); }
[data-testid="stSidebar"] * { color: white !important; }
h1, h2 { color: #1A5276 !important; }
h3     { color: #1E8449 !important; }
</style>
""", unsafe_allow_html=True)

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

st.title("ℹ️ À propos de ResistIA")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Le projet")
    st.markdown("""
    **ResistIA** est une plateforme IA développée dans le cadre d'un stage de bioinformatique
    au sein de **Global Biotek**, projet de biotechnologie et d'analyse de données biologiques
    basé à Lomé, Togo.

    Le projet a été développé de **Mars à Mai 2026**.
    """)

    st.markdown("### 🔬 Méthodologie")
    st.markdown("""
    **A1 — Collecte des données :** Base CARD v4.0.1 (13 379 gènes de résistance)
    + dataset synthétique de 64 000 antibiogrammes calibré sur GLASS/OMS 2022 et RESAOLAB,
    couvrant 9 bactéries ESKAPE, 23 antibiotiques et 8 pays ECOWAS (2019-2024).

    **A2 — Prétraitement :** Nettoyage, encodage, feature engineering (taux de résistance
    par paire bactérie × antibiotique comme feature principale).

    **A3 — Modèle IA :** Gradient Boosting (Scikit-learn) avec scoring probabiliste
    en 3 zones de confiance. Le moteur de recommandation est fondé sur les taux historiques
    de résistance par paire, approche plus robuste qu'une prédiction binaire.

    **A4 — Plateforme :** Interface Streamlit avec 4 modules fonctionnels déployée
    sur Streamlit Community Cloud.
    """)

    st.markdown("### 📚 Sources de données")
    st.markdown("""
    - **CARD** (Comprehensive Antibiotic Resistance Database) — McMaster University, v4.0.1
    - **GLASS** (Global AMR Surveillance System) — Organisation Mondiale de la Santé, 2022
    - **RESAOLAB** — Réseau des Laboratoires d'Afrique de l'Ouest
    - **Dataset synthétique ECOWAS** — généré et calibré par l'équipe ResistIA, Mars 2026
    """)

with col2:
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo_globalbiotek.jpg")
    if os.path.exists(logo_path):
        st.image(logo_path, width=220)

    st.markdown("### 👨‍💻 Équipe")
    st.markdown("""
    **TEKO Koffi Ephrem Diano**  
    Biomedical Analyst — Bioinformatique & Data Analytics  
    📧 ephremteko@gmail.com  
    📱 +228 99 30 15 77
    """)

    st.markdown("### 🏢 Structure")
    st.markdown("""
    **Global Biotek**  
    Projet de Bioinformatique  
    Lomé, Togo — 2026
    """)

st.markdown("---")
st.markdown("""
<div style='background:#FADBD8; border-left:5px solid #C0392B;
            padding:1rem 1.2rem; border-radius:8px;'>
⚠️ <strong>Avertissement légal :</strong> ResistIA est un outil d'aide à la décision
clinique fondé sur des données épidémiologiques régionales. Les recommandations générées
<strong>ne constituent pas un acte médical</strong> et ne remplacent en aucun cas l'avis
d'un professionnel de santé qualifié. Tout traitement antibiotique doit être prescrit
et supervisé par un médecin.
</div>
""", unsafe_allow_html=True)