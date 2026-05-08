import streamlit as st
import os
import sys

# Auto-génération si déploiement cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.load_model import verifier_ou_generer
verifier_ou_generer()

st.set_page_config(
    page_title="ResistIA — Global Biotek",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════
# LANGUE
# ═══════════════════════════════════════════════════

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

TEXT = {
    "Français": {
        "sidebar_desc": "Plateforme IA de Recommandation<br>Thérapeutique — Afrique de l'Ouest",
        "title": "Plateforme IA de Recommandation Thérapeutique<br>contre la Résistance aux Antibiotiques",
        "subtitle": "Développée dans le cadre du projet <strong>Global Biotek</strong> — Afrique de l'Ouest",
        "warning": "⚠️ <strong>Avertissement médical :</strong> ResistIA est un outil d'aide à la décision clinique fondé sur des données épidémiologiques régionales. Les recommandations générées ne remplacent pas l'avis d'un professionnel de santé qualifié. Tout traitement doit être prescrit par un médecin.",
        "database": "📊 Base de données ResistIA",
        "antibiograms": "🧫 Antibiogrammes",
        "bacteria": "🦠 Bactéries ESKAPE",
        "antibiotics": "💊 Antibiotiques",
        "countries": "🌍 Pays ECOWAS",
        "modules_title": "🗺️ Modules de la plateforme",
        "module_reco_title": "🔬 Recommandation Thérapeutique",
        "module_reco_desc": "Saisissez une bactérie, un pays et un site de prélèvement. Obtenez instantanément les antibiotiques classés par efficacité et les cocktails thérapeutiques suggérés.",
        "module_gemma_title": "🤖 Assistant Gemma",
        "module_gemma_desc": "Génère une synthèse clinique contrôlée et une explication complémentaire à partir des recommandations ResistIA, sans remplacer la décision médicale.",
        "module_heatmap_title": "🗺️ Heatmap Régionale",
        "module_heatmap_desc": "Carte interactive de résistance bactérie × antibiotique pour les 8 pays ECOWAS. Filtrage par pays disponible.",
        "module_stats_title": "📊 Statistiques",
        "module_stats_desc": "Distribution S/I/R, top pathogènes résistants, efficacité des antibiotiques par région et évolution temporelle 2019–2024.",
        "module_about_title": "ℹ️ À propos",
        "module_about_desc": "Méthodologie, sources de données, architecture IA, rôle de Gemma, équipe projet et avertissement légal complet.",
        "footer": "ResistIA v1.0 — Global Biotek © 2026<br>Données : CARD v4.0.1 + Dataset synthétique ECOWAS calibré GLASS/OMS 2022",
    },
    "English": {
        "sidebar_desc": "AI-Powered Therapeutic<br>Recommendation Platform — West Africa",
        "title": "AI-Powered Therapeutic Recommendation Platform<br>against Antimicrobial Resistance",
        "subtitle": "Developed as part of the <strong>Global Biotek</strong> project — West Africa",
        "warning": "⚠️ <strong>Medical disclaimer:</strong> ResistIA is a clinical decision-support tool based on regional epidemiological data. Its recommendations do not replace the advice of a qualified healthcare professional. Any treatment must be prescribed by a physician.",
        "database": "📊 ResistIA Knowledge Base",
        "antibiograms": "🧫 Antibiograms",
        "bacteria": "🦠 ESKAPE Bacteria",
        "antibiotics": "💊 Antibiotics",
        "countries": "🌍 ECOWAS Countries",
        "modules_title": "🗺️ Platform Modules",
        "module_reco_title": "🔬 Therapeutic Recommendation",
        "module_reco_desc": "Select a bacterium, country, and specimen site. Instantly obtain antibiotics ranked by estimated effectiveness and suggested therapeutic combinations.",
        "module_gemma_title": "🤖 Gemma Assistant",
        "module_gemma_desc": "Generates a controlled clinical synthesis and complementary explanation from ResistIA recommendations without replacing medical decision-making.",
        "module_heatmap_title": "🗺️ Regional Heatmap",
        "module_heatmap_desc": "Interactive bacteria × antibiotic resistance map across 8 ECOWAS countries with country-level filtering.",
        "module_stats_title": "📊 Statistics",
        "module_stats_desc": "S/I/R distribution, top resistant pathogens, antibiotic effectiveness by region, and temporal trends from 2019 to 2024.",
        "module_about_title": "ℹ️ About",
        "module_about_desc": "Methodology, data sources, AI architecture, Gemma’s role, project team, and full medical disclaimer.",
        "footer": "ResistIA v1.0 — Global Biotek © 2026<br>Data: CARD v4.0.1 + Synthetic ECOWAS dataset calibrated with WHO GLASS 2022",
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
    background-color: rgba(255,255,255,0.08);
    border-radius: 8px;
    transition: all 0.3s ease;
}

.logo-container {
    animation: fadeIn 1.2s ease-in-out;
    text-align: center;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

.sidebar-desc {
    font-size: 0.8rem;
    color: #AED6F1;
    text-align: center;
    margin-top: 6px;
}

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.1);
}

.stButton > button {
    background-color: #1E8449;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 2rem;
    font-weight: bold;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #27AE60;
    transform: scale(1.02);
}

.module-card {
    background: #F8F9FA;
    border: 1px solid #DEE2E6;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    border-left: 4px solid #1A5276;
    transition: all 0.2s ease;
}

.module-card:hover {
    background: #EBF5FB;
    border-left: 4px solid #1E8449;
    transform: translateY(-2px);
}

.avertissement {
    background: #FDEBD0;
    border-left: 5px solid #D35400;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# CHEMINS LOGOS
# ═══════════════════════════════════════════════════

APP_DIR = os.path.dirname(os.path.abspath(__file__))
logo_banner = os.path.join(APP_DIR, "logo_resistia_banner.png")
logo_blanc = os.path.join(APP_DIR, "logo_resistia.png")
logo_icon = os.path.join(APP_DIR, "logo_resistia_icon.png")

# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════

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

    t = TEXT[st.session_state["lang"]]

    st.markdown(
        f"<div class='sidebar-desc'>{t['sidebar_desc']}</div>",
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# PAGE ACCUEIL
# ═══════════════════════════════════════════════════

t = TEXT[st.session_state["lang"]]

if os.path.exists(logo_banner):
    st.image(logo_banner, use_container_width=True)
else:
    st.title("🧬 ResistIA")

st.markdown("")

st.markdown(
    f"<h2 style='color:#1A5276; margin-top:0;'>{t['title']}</h2>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='color:#555; font-size:1rem;'>{t['subtitle']}</p>",
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="avertissement">
{t["warning"]}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── KPIs ─────────────────────────────────────────
st.subheader(t["database"])

col1, col2, col3, col4 = st.columns(4)
col1.metric(t["antibiograms"], "64 000")
col2.metric(t["bacteria"], "9")
col3.metric(t["antibiotics"], "23")
col4.metric(t["countries"], "8")

st.markdown("---")

# ── Modules ───────────────────────────────────────
st.subheader(t["modules_title"])

col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown(f"""
    <div class="module-card">
        <strong>{t["module_reco_title"]}</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        {t["module_reco_desc"]}
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="module-card">
        <strong>{t["module_gemma_title"]}</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        {t["module_gemma_desc"]}
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="module-card">
        <strong>{t["module_heatmap_title"]}</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        {t["module_heatmap_desc"]}
        </span>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="module-card">
        <strong>{t["module_stats_title"]}</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        {t["module_stats_desc"]}
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="module-card">
        <strong>{t["module_about_title"]}</strong><br>
        <span style='color:#555; font-size:0.9rem;'>
        {t["module_about_desc"]}
        </span>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([1, 2, 1])

with col_f2:
    if os.path.exists(logo_icon):
        st.image(logo_icon, width=90)

    st.markdown(
        f"<p style='text-align:center; color:#888; font-size:0.8rem;'>{t['footer']}</p>",
        unsafe_allow_html=True
    )