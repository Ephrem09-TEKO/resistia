# ═══════════════════════════════════════════════════
# pages/01_🔬_Recommandation.py
# Module M2 — Recommandation Thérapeutique
# ═══════════════════════════════════════════════════
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os

from utils.load_model import verifier_ou_generer
verifier_ou_generer()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.recommender import recommander, BACTERIES, PAYS, SITES

st.set_page_config(page_title="Recommandation — ResistIA", page_icon="🔬", layout="wide")

# ── CSS ──
st.markdown("""
<style>
[data-testid="stSidebar"] { background: linear-gradient(180deg,#1A5276 0%,#154360 100%); }
[data-testid="stSidebar"] * { color: white !important; }
h1,h2 { color: #1A5276 !important; }
h3    { color: #1E8449 !important; }
.stButton > button {
    background-color: #1E8449; color: white;
    border-radius: 8px; border: none;
    padding: 0.6rem 2rem; font-weight: bold; font-size: 1rem; width: 100%;
}
.stButton > button:hover { background-color: #196F3D; }
.card-recommande {
    background: #D5F5E3; border-left: 5px solid #1E8449;
    padding: 1rem 1.2rem; border-radius: 8px; margin-bottom: 0.5rem;
}
.card-cocktail {
    background: #D6EAF8; border-left: 5px solid #1A5276;
    padding: 1rem 1.2rem; border-radius: 8px; margin-bottom: 1rem;
}
.avertissement {
    background: #FDEBD0; border-left: 5px solid #D35400;
    padding: 0.8rem 1.2rem; border-radius: 6px; margin-bottom: 1rem;
}
[data-testid="stSidebarNav"] a { color: white !important; }
[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 6px !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(30,132,73,0.4) !important;
    border-radius: 6px !important;
}
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
        "v1.0 — VivaTech Paris 2026</p>", unsafe_allow_html=True
    )

# ── EN-TÊTE ──
st.title("🔬 Recommandation Thérapeutique")
st.markdown("*Saisissez le profil microbiologique pour obtenir les recommandations IA en temps réel*")

st.markdown("""
<div class="avertissement">
⚠️ <strong>Avertissement :</strong> Les recommandations de ResistIA sont des aides à la décision
fondées sur des données épidémiologiques régionales. Elles ne remplacent pas l'avis médical.
Tout traitement doit être prescrit et supervisé par un professionnel de santé qualifié.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════
# FORMULAIRE DE SAISIE
# ══════════════════════════════════════════════════
st.subheader("📋 Profil Microbiologique")

col1, col2, col3 = st.columns(3)

with col1:
    bacterie = st.selectbox(
        "🦠 Bactérie identifiée",
        options=BACTERIES,
        help="Sélectionnez la bactérie isolée en laboratoire"
    )

with col2:
    pays = st.selectbox(
        "🌍 Pays d'isolement",
        options=PAYS,
        help="Pays où le prélèvement a été réalisé"
    )

with col3:
    site = st.selectbox(
        "🧪 Site de prélèvement",
        options=SITES,
        help="Site anatomique du prélèvement microbiologique"
    )

st.markdown("")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    analyser = st.button("🔍 Analyser et Recommander", use_container_width=True)

# ══════════════════════════════════════════════════
# RÉSULTATS
# ══════════════════════════════════════════════════
if analyser:
    with st.spinner("⚙️ Analyse en cours..."):
        resultat = recommander(bacterie, pays, site)

    if resultat is None:
        st.error("❌ Données insuffisantes pour cette bactérie.")
    else:
        st.markdown("---")
        st.subheader(f"📊 Résultats — *{bacterie}* | {pays} | {site}")

        df = resultat["antibiotiques"]

        # ── SECTION 1 : Molécules recommandées ──
        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown("### 💊 Classement des Antibiotiques")

            # Graphique barres horizontales
            couleurs = []
            for eff in df["efficacite_pct"]:
                if eff >= 80:   couleurs.append("#1E8449")
                elif eff >= 60: couleurs.append("#D35400")
                elif eff >= 40: couleurs.append("#E67E22")
                else:           couleurs.append("#C0392B")

            fig = go.Figure(go.Bar(
                x=df["efficacite_pct"],
                y=df["antibiotic"],
                orientation="h",
                marker_color=couleurs,
                text=[f"{v:.1f}%" for v in df["efficacite_pct"]],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Efficacité : %{x:.1f}%<extra></extra>",
            ))
            fig.add_vline(x=80, line_dash="dash", line_color="#1E8449",
                          annotation_text="Seuil recommandé (80%)",
                          annotation_position="top right")
            fig.add_vline(x=60, line_dash="dot",  line_color="#D35400",
                          annotation_text="Seuil possible (60%)",
                          annotation_position="bottom right")
            fig.update_layout(
                xaxis_title="% Efficacité estimée",
                yaxis=dict(autorange="reversed"),
                height=400,
                margin=dict(l=10, r=80, t=20, b=40),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                showlegend=False,
            )
            fig.update_xaxes(range=[0, 110], showgrid=True, gridcolor="#EEEEEE")
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.markdown("### 🎯 Recommandations Prioritaires")

            # Molécules de 1ère intention
            recommandes = resultat["recommandes"]
            if recommandes:
                st.markdown("**✅ Première intention (efficacité ≥ 80%) :**")
                for ab in recommandes:
                    eff = df[df["antibiotic"] == ab]["efficacite_pct"].values[0]
                    st.markdown(f"""
                    <div class="card-recommande">
                        💊 <strong>{ab}</strong> — 
                        <span style='color:#1E8449; font-size:1.1rem;'><strong>{eff:.1f}% d'efficacité estimée</strong></span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Aucun antibiotique avec efficacité ≥ 80% — voir meilleures options disponibles.")

            # Cocktail
            cocktail = resultat["cocktail"]
            if cocktail:
                eff1 = df[df["antibiotic"] == cocktail[0]]["efficacite_pct"].values
                eff2 = df[df["antibiotic"] == cocktail[1]]["efficacite_pct"].values
                e1 = f"{eff1[0]:.1f}%" if len(eff1) > 0 else "N/A"
                e2 = f"{eff2[0]:.1f}%" if len(eff2) > 0 else "N/A"
                st.markdown("**🧪 Cocktail thérapeutique suggéré :**")
                st.markdown(f"""
                <div class="card-cocktail">
                    🧪 <strong>{cocktail[0]}</strong> ({e1})
                    &nbsp;+&nbsp;
                    <strong>{cocktail[1]}</strong> ({e2})<br>
                    <small style='color:#555;'>
                    Synergie sur mécanismes différents — à confirmer avec un clinicien
                    </small>
                </div>
                """, unsafe_allow_html=True)

        # ── SECTION 2 : Tableau détaillé ──
        st.markdown("---")
        st.markdown("### 📋 Tableau Détaillé des Antibiotiques")

        df_display = df[["antibiotic", "efficacite_pct", "resist_rate_pair", "label", "description"]].copy()
        df_display["efficacite_pct"] = df_display["efficacite_pct"].round(1)
        df_display.columns = ["Antibiotique", "Efficacité (%)", "Taux Résistance", "Zone", "Évaluation"]
        df_display["Taux Résistance"] = (df_display["Taux Résistance"] * 100).round(1).astype(str) + "%"

        # Coloration des lignes
        def colorize(val):
            if "RECOMMANDÉ" in str(val): return "background-color: #D5F5E3"
            elif "POSSIBLE"  in str(val): return "background-color: #FDEBD0"
            elif "PRUDENCE"  in str(val): return "background-color: #FEF9E7"
            elif "ÉVITER"    in str(val): return "background-color: #FADBD8"
            return ""

        st.dataframe(
            df_display.style.map(colorize, subset=["Zone"]),
            use_container_width=True,
            hide_index=True,
            height=300
        )

        # ── SECTION 3 : Résumé clinique ──
        st.markdown("---")
        st.markdown("### 📝 Résumé Clinique")

        nb_rec  = len(df[df["efficacite_pct"] >= 80])
        nb_evit = len(df[df["efficacite_pct"] < 40])
        nb_tot  = len(df)

        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("🦠 Bactérie", bacterie.split()[0])
        col_s2.metric("✅ Antibiotiques recommandés", f"{nb_rec} / {nb_tot}")
        col_s3.metric("🔴 À éviter", f"{nb_evit} / {nb_tot}")
        col_s4.metric("🌍 Contexte", pays)

        # Sauvegarde en session pour export
        st.session_state["dernier_resultat"] = resultat
        st.session_state["derniere_bact"]    = bacterie
        st.session_state["dernier_pays"]     = pays
        st.session_state["dernier_site"]     = site

        st.success("✅ Analyse terminée. Utilisez le bouton ci-dessous pour exporter le rapport PDF.")

        # Bouton nouvelle analyse
        st.markdown("")
        col_r1, col_r2, col_r3 = st.columns([1, 1, 1])
        with col_r2:
            if st.button("🔄 Nouvelle Analyse", use_container_width=True):
                st.rerun()