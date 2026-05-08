import streamlit as st


LANGUAGES = {
    "Français": "fr",
    "English": "en"
}


TEXT = {
    "fr": {
        "sidebar_desc": "Plateforme IA de Recommandation<br>Thérapeutique — Afrique de l'Ouest",
        "language_label": "🌍 Langue / Language",
        "medical_warning": (
            "⚠️ Ces résultats sont une aide à la décision. "
            "La prescription finale doit être validée par un professionnel de santé qualifié."
        ),
    },

    "en": {
        "sidebar_desc": "AI-Powered Therapeutic<br>Recommendation Platform — West Africa",
        "language_label": "🌍 Language / Langue",
        "medical_warning": (
            "⚠️ These results are intended as decision-support only. "
            "Final prescription must be validated by a qualified healthcare professional."
        ),
    }
}


def get_language():
    """
    Returns current selected language code.
    Default language is English for hackathon judges.
    """
    if "language" not in st.session_state:
        st.session_state["language"] = "English"

    selected = st.sidebar.selectbox(
        TEXT[LANGUAGES[st.session_state["language"]]]["language_label"],
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state["language"])
    )

    st.session_state["language"] = selected
    return LANGUAGES[selected]


def t(key):
    """
    Shortcut to get translated text.
    """
    lang = LANGUAGES.get(st.session_state.get("language", "English"), "en")
    return TEXT[lang].get(key, key)