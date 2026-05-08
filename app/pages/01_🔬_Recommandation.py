# ═══════════════════════════════════════════════════
# pages/01_🔬_Recommandation.py
# Module — Therapeutic Recommendation / Recommandation Thérapeutique
# ═══════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.load_model import verifier_ou_generer
from utils.recommender import recommander, BACTERIES, PAYS, SITES

verifier_ou_generer()

st.set_page_config(
    page_title="Recommendation — ResistIA",
    page_icon="🔬",
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
        "title": "🔬 Recommandation Thérapeutique",
        "subtitle": "*Analyse microbiologique intelligente pour classer les antibiotiques selon leur efficacité estimée.*",
        "warning": "⚠️ <strong>Avertissement médical :</strong> Les recommandations de ResistIA sont des aides à la décision fondées sur des données épidémiologiques régionales. Elles ne remplacent pas l'avis d'un professionnel de santé. Tout traitement doit être prescrit et supervisé par un médecin.",
        "profile": "📋 Profil microbiologique",
        "bacteria": "🦠 Bactérie identifiée",
        "bacteria_help": "Sélectionnez la bactérie isolée en laboratoire.",
        "country": "🌍 Pays d'isolement",
        "country_help": "Pays où le prélèvement a été réalisé.",
        "site": "🧪 Site de prélèvement",
        "site_help": "Site anatomique du prélèvement microbiologique.",
        "button": "🔍 Analyser et recommander",
        "spinner": "⚙️ Analyse ResistIA en cours...",
        "no_data": "❌ Données insuffisantes pour cette bactérie.",
        "results": "📊 Résultats",
        "ranking": "### 💊 Classement des antibiotiques",
        "xaxis": "% d’efficacité estimée",
        "threshold_rec": "Recommandé",
        "threshold_possible": "Possible",
        "priorities": "### 🎯 Recommandations prioritaires",
        "first_line": "**✅ Première intention :**",
        "eff_text": "d’efficacité estimée",
        "no_high_eff": "⚠️ Aucun antibiotique avec efficacité ≥ 80%.",
        "cocktail_title": "**🧪 Cocktail thérapeutique suggéré :**",
        "cocktail_note": "Suggestion basée sur les profils de résistance — à valider par un clinicien.",
        "table_title": "### 📋 Tableau détaillé des antibiotiques",
        "table_cols": ["Antibiotique", "Efficacité (%)", "Taux de résistance", "Zone", "Évaluation"],
        "summary_title": "### 📝 Résumé clinique",
        "metric_bacteria": "🦠 Bactérie",
        "metric_rec": "✅ Recommandés",
        "metric_possible": "🟡 Possibles",
        "metric_avoid": "🔴 À éviter",
        "interpretation_label": "Interprétation",
        "interpretation": "Pour <strong>{bacterie}</strong> isolée au niveau <strong>{site}</strong> au <strong>{pays}</strong>, ResistIA identifie <strong>{nb_rec}</strong> antibiotique(s) recommandé(s), <strong>{nb_possible}</strong> option(s) possible(s), et <strong>{nb_evit}</strong> molécule(s) à éviter en raison d’un niveau de résistance élevé.",
        "success": "✅ Analyse terminée avec succès.",
        "new_analysis": "🔄 Nouvelle analyse",
        "hover_eff": "Efficacité",
    },

    "English": {
        "sidebar_desc": "AI-Powered Therapeutic<br>Recommendation Platform — West Africa",
        "title": "🔬 Therapeutic Recommendation",
        "subtitle": "*Smart microbiological analysis to rank antibiotics by estimated effectiveness.*",
        "warning": "⚠️ <strong>Medical disclaimer:</strong> ResistIA provides decision-support recommendations based on regional epidemiological data. It does not replace the advice of a qualified healthcare professional. Any treatment must be prescribed and supervised by a physician.",
        "profile": "📋 Microbiological profile",
        "bacteria": "🦠 Identified bacterium",
        "bacteria_help": "Select the bacterium isolated in the laboratory.",
        "country": "🌍 Country of isolation",
        "country_help": "Country where the sample was collected.",
        "site": "🧪 Specimen site",
        "site_help": "Anatomical site of the microbiological sample.",
        "button": "🔍 Analyze and recommend",
        "spinner": "⚙️ Running ResistIA analysis...",
        "no_data": "❌ Insufficient data for this bacterium.",
        "results": "📊 Results",
        "ranking": "### 💊 Antibiotic ranking",
        "xaxis": "% estimated effectiveness",
        "threshold_rec": "Recommended",
        "threshold_possible": "Possible",
        "priorities": "### 🎯 Priority recommendations",
        "first_line": "**✅ First-line option:**",
        "eff_text": "estimated effectiveness",
        "no_high_eff": "⚠️ No antibiotic with effectiveness ≥ 80%.",
        "cocktail_title": "**🧪 Suggested therapeutic combination:**",
        "cocktail_note": "Suggestion based on resistance profiles — to be validated by a clinician.",
        "table_title": "### 📋 Detailed antibiotic table",
        "table_cols": ["Antibiotic", "Effectiveness (%)", "Resistance rate", "Zone", "Assessment"],
        "summary_title": "### 📝 Clinical summary",
        "metric_bacteria": "🦠 Bacterium",
        "metric_rec": "✅ Recommended",
        "metric_possible": "🟡 Possible",
        "metric_avoid": "🔴 Avoid",
        "interpretation_label": "Interpretation",
        "interpretation": "For <strong>{bacterie}</strong> isolated from <strong>{site}</strong> in <strong>{pays}</strong>, ResistIA identifies <strong>{nb_rec}</strong> recommended antibiotic(s), <strong>{nb_possible}</strong> possible option(s), and <strong>{nb_evit}</strong> molecule(s) to avoid due to high resistance.",
        "success": "✅ Analysis completed successfully.",
        "new_analysis": "🔄 New analysis",
        "hover_eff": "Effectiveness",
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

.avertissement {
    background: #FDEBD0;
    border-left: 5px solid #D35400;
    padding: 0.9rem 1.2rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.stButton > button {
    background-color: #1E8449;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.65rem 2rem;
    font-weight: bold;
    font-size: 1rem;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background-color: #27AE60;
    transform: scale(1.02);
}

.card-recommande {
    background: #D5F5E3;
    border-left: 5px solid #1E8449;
    padding: 1rem 1.2rem;
    border-radius: 10px;
    margin-bottom: 0.7rem;
    transition: all 0.25s ease;
}

.card-recommande:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}

.card-cocktail {
    background: #D6EAF8;
    border-left: 5px solid #1A5276;
    padding: 1rem 1.2rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
}

.card-cocktail:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}

.result-card {
    background: #F8F9FA;
    border: 1px solid #DEE2E6;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    border-left: 4px solid #1A5276;
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

st.title(tx["title"])
st.markdown(tx["subtitle"])

st.markdown(f"""
<div class="avertissement">
{tx["warning"]}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── FORMULAIRE ───────────────────────────────────
st.subheader(tx["profile"])

col1, col2, col3 = st.columns(3)

with col1:
    bacterie = st.selectbox(
        tx["bacteria"],
        options=BACTERIES,
        help=tx["bacteria_help"]
    )

with col2:
    pays = st.selectbox(
        tx["country"],
        options=PAYS,
        help=tx["country_help"]
    )

with col3:
    site = st.selectbox(
        tx["site"],
        options=SITES,
        help=tx["site_help"]
    )

st.markdown("")

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    analyser = st.button(tx["button"], use_container_width=True)

# ── RÉSULTATS ────────────────────────────────────
if analyser:
    with st.spinner(tx["spinner"]):
        resultat = recommander(bacterie, pays, site)

    if resultat is None:
        st.error(tx["no_data"])
    else:
        df = resultat["antibiotiques"]

        st.markdown("---")
        st.subheader(f"{tx['results']} — *{bacterie}* | {pays} | {site}")

        col_left, col_right = st.columns([1.25, 1])

        with col_left:
            st.markdown(tx["ranking"])

            couleurs = []
            for eff in df["efficacite_pct"]:
                if eff >= 80:
                    couleurs.append("#1E8449")
                elif eff >= 60:
                    couleurs.append("#D4AC0D")
                elif eff >= 40:
                    couleurs.append("#E67E22")
                else:
                    couleurs.append("#C0392B")

            fig = go.Figure(go.Bar(
                x=df["efficacite_pct"],
                y=df["antibiotic"],
                orientation="h",
                marker_color=couleurs,
                text=[f"{v:.1f}%" for v in df["efficacite_pct"]],
                textposition="outside",
                hovertemplate=f"<b>%{{y}}</b><br>{tx['hover_eff']} : %{{x:.1f}}%<extra></extra>",
            ))

            fig.add_vline(
                x=80,
                line_dash="dash",
                line_color="#1E8449",
                annotation_text=tx["threshold_rec"],
                annotation_position="top right"
            )

            fig.add_vline(
                x=60,
                line_dash="dot",
                line_color="#D4AC0D",
                annotation_text=tx["threshold_possible"],
                annotation_position="bottom right"
            )

            fig.update_layout(
                xaxis_title=tx["xaxis"],
                yaxis=dict(autorange="reversed"),
                height=430,
                margin=dict(l=10, r=90, t=20, b=40),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                showlegend=False,
            )

            fig.update_xaxes(range=[0, 110], showgrid=True, gridcolor="#EEEEEE")

            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.markdown(tx["priorities"])

            recommandes = resultat["recommandes"]

            if recommandes:
                st.markdown(tx["first_line"])

                for ab in recommandes:
                    eff = df[df["antibiotic"] == ab]["efficacite_pct"].values[0]
                    st.markdown(f"""
                    <div class="card-recommande">
                        💊 <strong>{ab}</strong><br>
                        <span style='color:#1E8449; font-size:1.05rem;'>
                        <strong>{eff:.1f}% {tx["eff_text"]}</strong>
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(tx["no_high_eff"])

            cocktail = resultat["cocktail"]

            if cocktail:
                eff1 = df[df["antibiotic"] == cocktail[0]]["efficacite_pct"].values
                eff2 = df[df["antibiotic"] == cocktail[1]]["efficacite_pct"].values

                e1 = f"{eff1[0]:.1f}%" if len(eff1) > 0 else "N/A"
                e2 = f"{eff2[0]:.1f}%" if len(eff2) > 0 else "N/A"

                st.markdown(tx["cocktail_title"])
                st.markdown(f"""
                <div class="card-cocktail">
                    🧪 <strong>{cocktail[0]}</strong> ({e1})
                    &nbsp;+&nbsp;
                    <strong>{cocktail[1]}</strong> ({e2})<br>
                    <small style='color:#555;'>
                    {tx["cocktail_note"]}
                    </small>
                </div>
                """, unsafe_allow_html=True)

        # ── TABLEAU DÉTAILLÉ ─────────────────────
        st.markdown("---")
        st.markdown(tx["table_title"])

        df_display = df[
            ["antibiotic", "efficacite_pct", "resist_rate_pair", "label", "description"]
        ].copy()

        df_display["efficacite_pct"] = df_display["efficacite_pct"].round(1)
        df_display["resist_rate_pair"] = (df_display["resist_rate_pair"] * 100).round(1).astype(str) + "%"

        df_display.columns = tx["table_cols"]

        def colorize(val):
            val = str(val)
            if "RECOMMANDÉ" in val:
                return "background-color: #D5F5E3"
            elif "POSSIBLE" in val:
                return "background-color: #FCF3CF"
            elif "PRUDENCE" in val:
                return "background-color: #FDEBD0"
            elif "ÉVITER" in val or "EVITER" in val:
                return "background-color: #FADBD8"
            return ""

        zone_col = tx["table_cols"][3]

        st.dataframe(
            df_display.style.map(colorize, subset=[zone_col]),
            use_container_width=True,
            hide_index=True,
            height=300
        )

        # ── RÉSUMÉ CLINIQUE ──────────────────────
        st.markdown("---")
        st.markdown(tx["summary_title"])

        nb_rec = len(df[df["efficacite_pct"] >= 80])
        nb_possible = len(df[(df["efficacite_pct"] >= 60) & (df["efficacite_pct"] < 80)])
        nb_evit = len(df[df["efficacite_pct"] < 40])
        nb_tot = len(df)

        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric(tx["metric_bacteria"], bacterie.split()[0])
        col_s2.metric(tx["metric_rec"], f"{nb_rec} / {nb_tot}")
        col_s3.metric(tx["metric_possible"], f"{nb_possible} / {nb_tot}")
        col_s4.metric(tx["metric_avoid"], f"{nb_evit} / {nb_tot}")

        st.markdown(f"""
        <div class="result-card">
            <strong>{tx["interpretation_label"]}:</strong><br>
            {tx["interpretation"].format(
                bacterie=bacterie,
                site=site,
                pays=pays,
                nb_rec=nb_rec,
                nb_possible=nb_possible,
                nb_evit=nb_evit
            )}
        </div>
        """, unsafe_allow_html=True)

        st.session_state["dernier_resultat"] = resultat
        st.session_state["derniere_bact"] = bacterie
        st.session_state["dernier_pays"] = pays
        st.session_state["dernier_site"] = site

        st.success(tx["success"])

        col_r1, col_r2, col_r3 = st.columns([1, 1, 1])
        with col_r2:
            if st.button(tx["new_analysis"], use_container_width=True):
                st.rerun()