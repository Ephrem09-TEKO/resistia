import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma:2b"


def interroger_gemma(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 180
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return "Gemma indisponible : Ollama n'est pas lancé."

    except requests.exceptions.ReadTimeout:
        return "Gemma a mis trop de temps à répondre. La synthèse contrôlée ResistIA reste disponible."

    except Exception as e:
        return f"Erreur Gemma : {e}"


def generer_explication_clinique(bacterie, pays, site, recommandations):
    prompt = f"""
Explique brièvement en français les résultats ResistIA ci-dessous.
Ne reclasse pas les antibiotiques.
Ne donne pas de nouvelle recommandation.
Maximum 6 phrases.

Contexte :
Bactérie : {bacterie}
Pays : {pays}
Site : {site}

Résultats :
{recommandations}
"""
    return interroger_gemma(prompt)