# ═══════════════════════════════════════════════════
# pages/06_🎥_Demo_Clinique.py
# Module — Clinical Demo / Démo clinique hackathon
# ═══════════════════════════════════════════════════

import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.recommender import recommander

st.set_page_config(
    page_title="Clinical Demo — ResistIA",
    page_icon="🎥",
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
        "page_title": "🎥 Démo Clinique Hackathon",
        "page_subtitle": "*Un scénario guidé pour démontrer l’impact terrain de ResistIA.*",
        "scenario_title": "🏥 Scénario : Hôpital de Lomé, Togo",
        "scenario_text": """
        Un patient arrive aux urgences avec suspicion d’infection bactérienne sévère.
        Le laboratoire identifie <strong>Escherichia coli</strong> dans un prélèvement sanguin.
        Le médecin doit choisir rapidement une option antibiotique adaptée, dans un contexte où
        la résistance aux antibiotiques est fréquente.
        """,
        "patient_profile": "👤 Profil patient",
        "age": "Âge",
        "context": "Contexte",
        "context_value": "fièvre élevée, suspicion de septicémie",
        "site": "Site",
        "country": "Pays",
        "bacteria": "Bactérie",
        "constraint": "Contrainte",
        "constraint_value": "décision rapide nécessaire",
        "clinical_challenge": "⚠️ Défi clinique",
        "challenge_text": """
        Les antibiotiques courants peuvent être inefficaces si la bactérie est résistante.
        Une mauvaise décision peut entraîner un échec thérapeutique, une aggravation clinique
        et une augmentation du risque de complications.
        """,
        "button": "🚀 Lancer la démo ResistIA",
        "spinner": "Analyse du cas clinique en cours...",
        "no_data": "Aucune donnée disponible pour ce scénario.",
        "result_title": "🧬 Résultat de l’analyse ResistIA",
        "recommended": "✅ Recommandé",
        "possible": "🟡 Options possibles",
        "avoid": "🚫 À éviter",
        "full_table": "### 📋 Tableau complet",
        "clinical_interpretation": "### 🧠 Interprétation clinique",
        "interpretation": """
        Pour ce cas, ResistIA recommande prioritairement <strong>{rec_list}</strong>,
        car cette option présente le meilleur niveau d’efficacité estimée dans les données disponibles.
        Les options <strong>{pos_list}</strong> peuvent être considérées selon le contexte clinique,
        tandis que <strong>{evit_list}</strong> doivent être évitées en raison d’une résistance élevée.
        <br><br>
        <strong>Message clé pour le hackathon :</strong>
        ResistIA transforme des données microbiologiques complexes en recommandations claires,
        explicables et utilisables en quelques secondes.
        """,
        "warning": "⚠️ Cette démonstration est une aide à la décision. La prescription finale doit toujours être validée par un professionnel de santé.",
        "none": "Aucun",
        "table_cols": {
            "antibiotic": "Antibiotique",
            "efficacite_pct": "Efficacité (%)",
            "label": "Zone",
            "description": "Évaluation"
        }
    },

    "English": {
        "sidebar_desc": "AI-Powered Therapeutic<br>Recommendation Platform — West Africa",
        "page_title": "🎥 Clinical Hackathon Demo",
        "page_subtitle": "*A guided clinical scenario showing ResistIA’s field impact.*",
        "scenario_title": "🏥 Scenario: Hospital in Lomé, Togo",
        "scenario_text": """
        A patient arrives in the emergency department with suspected severe bacterial infection.
        The laboratory identifies <strong>Escherichia coli</strong> from a blood sample.
        The clinician must rapidly choose an appropriate antibiotic option in a setting where
        antimicrobial resistance is common.
        """,
        "patient_profile": "👤 Patient profile",
        "age": "Age",
        "context": "Clinical context",
        "context_value": "high fever, suspected sepsis",
        "site": "Specimen site",
        "country": "Country",
        "bacteria": "Bacterium",
        "constraint": "Constraint",
        "constraint_value": "rapid decision required",
        "clinical_challenge": "⚠️ Clinical challenge",
        "challenge_text": """
        Common antibiotics may fail if the bacterium is resistant.
        A poor antibiotic choice can lead to treatment failure, clinical deterioration,
        and increased risk of complications.
        """,
        "button": "🚀 Launch ResistIA demo",
        "spinner": "Analyzing clinical case...",
        "no_data": "No data available for this scenario.",
        "result_title": "🧬 ResistIA analysis result",
        "recommended": "✅ Recommended",
        "possible": "🟡 Possible options",
        "avoid": "🚫 Avoid",
        "full_table": "### 📋 Full table",
        "clinical_interpretation": "### 🧠 Clinical interpretation",
        "interpretation": """
        For this case, ResistIA prioritizes <strong>{rec_list}</strong>,
        because it shows the highest estimated effectiveness in the available data.
        <strong>{pos_list}</strong> may be considered depending on the clinical context,
        while <strong>{evit_list}</strong> should be avoided due to high resistance.
        <br><br>
        <strong>Key hackathon message:</strong>
        ResistIA turns complex microbiology data into clear, explainable, and usable
        recommendations within seconds.
        """,
        "warning": "⚠️ This demonstration is for decision-support only. Final prescription must always be validated by a qualified healthcare professional.",
        "none": "None",
        "table_cols": {
            "antibiotic": "Antibiotic",
            "efficacite_pct": "Effectiveness (%)",
            "label": "Zone",
            "description": "Assessment"
        }
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
.scenario-card {
    background: linear-gradient(135deg, #EBF5FB 0%, #F8F9FA 100%);
    border-left: 6px solid #1A5276;
    padding: 1.3rem 1.5rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    animation: fadeIn 0.8s ease-in-out;
}
.case-card {
    background: #F8F9FA;
    border: 1px solid #DEE2E6;
    border-left: 5px solid #1E8449;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}
.warning-card {
    background: #FDEBD0;
    border-left: 5px solid #D35400;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}
.result-card {
    background: #D5F5E3;
    border-left: 5px solid #1E8449;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}
.danger-card {
    background: #FADBD8;
    border-left: 5px solid #C0392B;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}
.stButton > button {
    background-color: #1E8449;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.7rem 2rem;
    font-weight: bold;
    font-size: 1rem;
    transition: all 0.25s ease;
}
.stButton > button:hover {
    background-color: #27AE60;
    transform: scale(1.02);
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
# PAGE
# ═══════════════════════════════════════════════════

tx = TEXT[st.session_state["lang"]]

st.title(tx["page_title"])
st.markdown(tx["page_subtitle"])

st.markdown(f"""
<div class="scenario-card">
<h3>{tx["scenario_title"]}</h3>
{tx["scenario_text"]}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"### {tx['patient_profile']}")
    st.markdown(f"""
    <div class="case-card">
    <strong>{tx["age"]}:</strong> 42<br>
    <strong>{tx["context"]}:</strong> {tx["context_value"]}<br>
    <strong>{tx["site"]}:</strong> Sang / Blood<br>
    <strong>{tx["country"]}:</strong> Togo<br>
    <strong>{tx["bacteria"]}:</strong> Escherichia coli<br>
    <strong>{tx["constraint"]}:</strong> {tx["constraint_value"]}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"### {tx['clinical_challenge']}")
    st.markdown(f"""
    <div class="warning-card">
    {tx["challenge_text"]}
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
with col_b2:
    lancer = st.button(tx["button"], use_container_width=True)

if lancer:
    with st.spinner(tx["spinner"]):
        resultat = recommander(
            bacteria_name="Escherichia coli",
            pays="Togo",
            site="Sang"
        )

    if resultat is None:
        st.error(tx["no_data"])
    else:
        df = resultat["antibiotiques"]

        recommandes = df[df["label"].str.contains("RECOMMANDÉ", case=False, na=False)]
        possibles = df[df["label"].str.contains("POSSIBLE", case=False, na=False)]
        eviter = df[df["label"].str.contains("ÉVITER|EVITER", case=False, na=False)]

        rec_list = ", ".join(recommandes["antibiotic"].tolist()) if not recommandes.empty else tx["none"]
        pos_list = ", ".join(possibles["antibiotic"].tolist()) if not possibles.empty else tx["none"]
        evit_list = ", ".join(eviter["antibiotic"].tolist()) if not eviter.empty else tx["none"]

        st.markdown("---")
        st.subheader(tx["result_title"])

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            st.markdown(f"""
            <div class="result-card">
            <h4>{tx["recommended"]}</h4>
            <strong>{rec_list}</strong>
            </div>
            """, unsafe_allow_html=True)

        with col_r2:
            st.markdown(f"""
            <div class="case-card">
            <h4>{tx["possible"]}</h4>
            <strong>{pos_list}</strong>
            </div>
            """, unsafe_allow_html=True)

        with col_r3:
            st.markdown(f"""
            <div class="danger-card">
            <h4>{tx["avoid"]}</h4>
            <strong>{evit_list}</strong>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(tx["full_table"])

        table_df = df[["antibiotic", "efficacite_pct", "label", "description"]].copy()
        table_df = table_df.rename(columns=tx["table_cols"])

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown(tx["clinical_interpretation"])
        st.markdown(f"""
        <div class="scenario-card">
        {tx["interpretation"].format(
            rec_list=rec_list,
            pos_list=pos_list,
            evit_list=evit_list
        )}
        </div>
        """, unsafe_allow_html=True)

        st.warning(tx["warning"])