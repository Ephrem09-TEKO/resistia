# ═══════════════════════════════════════════════════
# pages/05_ℹ️_A_propos.py
# Module — About / À propos
# ═══════════════════════════════════════════════════

import streamlit as st
import os

st.set_page_config(
    page_title="About — ResistIA",
    page_icon="ℹ️",
    layout="wide"
)

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

TEXT = {
    "Français": {
        "sidebar_desc": "Plateforme IA de Recommandation<br>Thérapeutique — Afrique de l'Ouest",
        "title": "ℹ️ À propos de ResistIA",
        "subtitle": "*Plateforme IA d’aide à la décision contre la résistance aux antibiotiques.*",
        "hero_title": "🧬 ResistIA Hackathon Edition",
        "hero_text": "ResistIA est une plateforme d’aide à la décision clinique conçue pour aider les soignants à interpréter les profils de résistance aux antibiotiques et à identifier les options thérapeutiques les plus pertinentes dans les contextes à ressources limitées.<br><br>Cette version intègre <strong>Gemma via Ollama</strong> comme moteur d’explication complémentaire : ResistIA produit la recommandation structurée, et Gemma aide à formuler une synthèse lisible, contrôlée et orientée utilisateur.",
        "antibiograms": "🧫 Antibiogrammes",
        "bacteria": "🦠 Bactéries",
        "antibiotics": "💊 Antibiotiques",
        "countries": "🌍 Pays ECOWAS",
        "problem_title": "🎯 Problème ciblé",
        "problem_text": "La résistance aux antibiotiques complique la prise en charge des infections bactériennes, en particulier dans les régions où l’accès aux spécialistes, aux données de surveillance et aux outils d’aide à la décision reste limité.<br><br>ResistIA vise à transformer des données microbiologiques en recommandations lisibles, exploitables et prudentes pour appuyer la décision clinique.",
        "ai_title": "🧠 Architecture IA",
        "ai_text": "<strong>1. Moteur ResistIA :</strong> classe les antibiotiques selon les taux historiques de résistance bactérie × antibiotique.<br><br><strong>2. Modèle machine learning :</strong> modèle Scikit-learn sauvegardé pour l’analyse probabiliste des profils de résistance.<br><br><strong>3. Gemma via Ollama :</strong> utilisé comme assistant d’explication, en local, afin d’améliorer la lisibilité des résultats sans remplacer le moteur médical.<br><br><strong>Principe de sécurité :</strong> ResistIA décide, Gemma explique.",
        "method_title": "🔬 Méthodologie",
        "method_text": "<strong>A1 — Collecte des données :</strong> CARD v4.0.1 + dataset ECOWAS calibré à partir de sources GLASS/OMS et références régionales.<br><br><strong>A2 — Prétraitement :</strong> nettoyage, encodage, feature engineering, construction du dataset final.<br><br><strong>A3 — Modèle IA :</strong> modèle probabiliste et moteur de recommandation fondé sur les profils de résistance.<br><br><strong>A4 — Plateforme :</strong> interface Streamlit avec modules Recommandation, Assistant Gemma, Heatmap, Statistiques et À propos.",
        "hackathon_title": "🏆 Positionnement hackathon",
        "hackathon_text": "ResistIA s’inscrit principalement dans les catégories :<br><br>✅ <strong>Health & Sciences</strong> — aide à l’interprétation des données AMR<br>✅ <strong>Safety & Trust</strong> — recommandations contrôlées, explicables et prudentes<br>✅ <strong>Ollama Track</strong> — utilisation locale de Gemma via Ollama<br>✅ <strong>Main Track</strong> — impact réel, démo fonctionnelle et potentiel terrain",
        "author_title": "👨‍💻 Porteur du projet",
        "author_text": "<strong>TEKO Koffi Ephrem Diano</strong><br>Biomedical Analyst<br>Bioinformatique & Data Analytics<br><br>📧 ephremteko@gmail.com<br>📱 +228 99 30 15 77",
        "structure_title": "🏢 Structure",
        "structure_text": "<strong>Global Biotek</strong><br>Projet de Bioinformatique<br>Lomé, Togo — 2026",
        "stack_title": "⚙️ Stack technique",
        "sources_title": "📚 Sources",
        "sources_text": "• CARD v4.0.1<br>• GLASS / OMS<br>• RESAOLAB<br>• Dataset ECOWAS calibré<br>• Profils synthétiques validés pour prototype",
        "limits_title": "⚠️ Limites et sécurité médicale",
        "limits_text": "<strong>Avertissement légal :</strong><br>ResistIA est un outil d'aide à la décision clinique fondé sur des données épidémiologiques régionales. Les recommandations générées <strong>ne constituent pas un acte médical</strong> et ne remplacent en aucun cas l'avis d'un professionnel de santé qualifié.<br><br>Le système doit être utilisé comme support d’analyse, de priorisation et d’explication. Toute prescription antibiotique doit être validée et supervisée par un médecin.",
        "footer": "ResistIA Hackathon Edition — Global Biotek © 2026<br>Powered by Streamlit, Scikit-learn, Ollama and Gemma"
    },

    "English": {
        "sidebar_desc": "AI-Powered Therapeutic<br>Recommendation Platform — West Africa",
        "title": "ℹ️ About ResistIA",
        "subtitle": "*AI-powered clinical decision-support platform against antimicrobial resistance.*",
        "hero_title": "🧬 ResistIA Hackathon Edition",
        "hero_text": "ResistIA is a clinical decision-support platform designed to help healthcare professionals interpret antibiotic resistance profiles and identify the most relevant therapeutic options in resource-limited settings.<br><br>This version integrates <strong>Gemma via Ollama</strong> as a complementary explanation engine: ResistIA produces the structured recommendation, while Gemma helps generate readable, controlled, and user-oriented clinical summaries.",
        "antibiograms": "🧫 Antibiograms",
        "bacteria": "🦠 Bacteria",
        "antibiotics": "💊 Antibiotics",
        "countries": "🌍 ECOWAS Countries",
        "problem_title": "🎯 Target problem",
        "problem_text": "Antimicrobial resistance complicates the management of bacterial infections, especially in regions where access to specialists, surveillance data, and clinical decision-support tools remains limited.<br><br>ResistIA aims to transform microbiological data into readable, actionable, and cautious recommendations to support clinical decisions.",
        "ai_title": "🧠 AI architecture",
        "ai_text": "<strong>1. ResistIA engine:</strong> ranks antibiotics using historical bacterium × antibiotic resistance profiles.<br><br><strong>2. Machine learning model:</strong> saved Scikit-learn model for probabilistic resistance analysis.<br><br><strong>3. Gemma via Ollama:</strong> used locally as an explanation assistant to improve readability without replacing the medical engine.<br><br><strong>Safety principle:</strong> ResistIA decides, Gemma explains.",
        "method_title": "🔬 Methodology",
        "method_text": "<strong>A1 — Data collection:</strong> CARD v4.0.1 + ECOWAS dataset calibrated using WHO GLASS and regional references.<br><br><strong>A2 — Preprocessing:</strong> cleaning, encoding, feature engineering, and final dataset construction.<br><br><strong>A3 — AI model:</strong> probabilistic model and recommendation engine based on resistance profiles.<br><br><strong>A4 — Platform:</strong> Streamlit interface with Recommendation, Gemma Assistant, Heatmap, Statistics, and About modules.",
        "hackathon_title": "🏆 Hackathon positioning",
        "hackathon_text": "ResistIA mainly fits into the following categories:<br><br>✅ <strong>Health & Sciences</strong> — AMR interpretation support<br>✅ <strong>Safety & Trust</strong> — explainable and controlled recommendations<br>✅ <strong>Ollama Track</strong> — local Gemma integration via Ollama<br>✅ <strong>Main Track</strong> — real-world impact and functional demo",
        "author_title": "👨‍💻 Project lead",
        "author_text": "<strong>TEKO Koffi Ephrem Diano</strong><br>Biomedical Analyst<br>Bioinformatics & Data Analytics<br><br>📧 ephremteko@gmail.com<br>📱 +228 99 30 15 77",
        "structure_title": "🏢 Organization",
        "structure_text": "<strong>Global Biotek</strong><br>Bioinformatics Project<br>Lomé, Togo — 2026",
        "stack_title": "⚙️ Tech stack",
        "sources_title": "📚 Sources",
        "sources_text": "• CARD v4.0.1<br>• WHO GLASS<br>• RESAOLAB<br>• Calibrated ECOWAS dataset<br>• Prototype-validated synthetic profiles",
        "limits_title": "⚠️ Medical limitations & safety",
        "limits_text": "<strong>Legal disclaimer:</strong><br>ResistIA is a clinical decision-support tool based on regional epidemiological data. Generated recommendations <strong>do not constitute medical practice</strong> and never replace the judgment of a qualified healthcare professional.<br><br>The system must be used as an analysis, prioritization, and explanation support tool. Any antibiotic prescription must be validated and supervised by a physician.",
        "footer": "ResistIA Hackathon Edition — Global Biotek © 2026<br>Powered by Streamlit, Scikit-learn, Ollama and Gemma"
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
.hero-card {
    background: linear-gradient(135deg, #EBF5FB 0%, #F8F9FA 100%);
    border-left: 6px solid #1A5276;
    padding: 1.3rem 1.5rem;
    border-radius: 14px;
    margin-bottom: 1rem;
}
.info-card {
    background: #F8F9FA;
    border: 1px solid #DEE2E6;
    border-left: 5px solid #1A5276;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
}
.info-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}
.impact-card {
    background: #D5F5E3;
    border-left: 5px solid #1E8449;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}
.warning-card {
    background: #FADBD8;
    border-left: 5px solid #C0392B;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-top: 1rem;
}
.tech-badge {
    display: inline-block;
    background: #D6EAF8;
    color: #1A5276;
    padding: 0.35rem 0.7rem;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 0.2rem;
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
logo_global = os.path.join(APP_DIR, "logo_globalbiotek.jpg")

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

tx = TEXT[st.session_state["lang"]]

st.title(tx["title"])
st.markdown(tx["subtitle"])

st.markdown(
    f"<div class='hero-card'><h3>{tx['hero_title']}</h3>{tx['hero_text']}</div>",
    unsafe_allow_html=True
)

col_k1, col_k2, col_k3, col_k4 = st.columns(4)
col_k1.metric(tx["antibiograms"], "64 000")
col_k2.metric(tx["bacteria"], "9")
col_k3.metric(tx["antibiotics"], "23")
col_k4.metric(tx["countries"], "8")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### {tx['problem_title']}")
    st.markdown(f"<div class='info-card'>{tx['problem_text']}</div>", unsafe_allow_html=True)

    st.markdown(f"### {tx['ai_title']}")
    st.markdown(f"<div class='info-card'>{tx['ai_text']}</div>", unsafe_allow_html=True)

    st.markdown(f"### {tx['method_title']}")
    st.markdown(f"<div class='info-card'>{tx['method_text']}</div>", unsafe_allow_html=True)

    st.markdown(f"### {tx['hackathon_title']}")
    st.markdown(f"<div class='impact-card'>{tx['hackathon_text']}</div>", unsafe_allow_html=True)

with col2:
    if os.path.exists(logo_global):
        st.image(logo_global, width=220)

    st.markdown(f"### {tx['author_title']}")
    st.markdown(f"<div class='info-card'>{tx['author_text']}</div>", unsafe_allow_html=True)

    st.markdown(f"### {tx['structure_title']}")
    st.markdown(f"<div class='info-card'>{tx['structure_text']}</div>", unsafe_allow_html=True)

    st.markdown(f"### {tx['stack_title']}")
    st.markdown("""
    <span class="tech-badge">Python</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">Scikit-learn</span>
    <span class="tech-badge">Pandas</span>
    <span class="tech-badge">Plotly</span>
    <span class="tech-badge">Ollama</span>
    <span class="tech-badge">Gemma</span>
    """, unsafe_allow_html=True)

    st.markdown(f"### {tx['sources_title']}")
    st.markdown(f"<div class='info-card'>{tx['sources_text']}</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(f"### {tx['limits_title']}")
st.markdown(f"<div class='warning-card'>{tx['limits_text']}</div>", unsafe_allow_html=True)

st.markdown(
    f"<div style='text-align:center; color:#555; font-size:0.85rem; margin-top:1.5rem;'>{tx['footer']}</div>",
    unsafe_allow_html=True
)