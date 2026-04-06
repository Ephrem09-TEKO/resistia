# ═══════════════════════════════════════════════════
# utils/recommender.py
# Moteur de recommandation ResistIA
# ═══════════════════════════════════════════════════
import pandas as pd
import numpy as np
import joblib
import json
import os

# ── Chemins des fichiers ──
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR  = os.path.join(BASE_DIR, "..", "models")
DATA_DIR   = os.path.join(BASE_DIR, "..", "data", "processed")

def charger_ressources():
    """Charge tous les fichiers nécessaires au moteur de recommandation"""
    
    # Taux de résistance par paire bactérie × antibiotique
    resist_pair = pd.read_csv(
        os.path.join(MODEL_DIR, "resist_rate_pair.csv")
    )
    
    # Mappings d'encodage
    with open(os.path.join(MODEL_DIR, "label_mappings.json"), encoding="utf-8") as f:
        mappings = json.load(f)
    
    # Dataset complet pour les statistiques
    df_complet = pd.read_csv(
        os.path.join(DATA_DIR, "antibiograms_clean.csv")
    )
    
    return resist_pair, mappings, df_complet


def recommander(bacteria_name, pays="Togo", site="Sang"):
    """
    Retourne les recommandations thérapeutiques pour une bactérie donnée.
    
    Returns:
        dict avec clés :
        - 'antibiotiques' : DataFrame classé par efficacité
        - 'recommandes'   : liste des antibiotiques efficaces (≥80%)
        - 'cocktail'      : tuple (ab1, ab2) ou None
        - 'bactérie'      : nom de la bactérie
        - 'pays'          : pays sélectionné
        - 'site'          : site de prélèvement
    """
    resist_pair, mappings, _ = charger_ressources()
    
    # Filtrer pour la bactérie choisie
    df_bacterie = resist_pair[
        resist_pair["bacteria_name"] == bacteria_name
    ].copy()
    
    if df_bacterie.empty:
        return None
    
    # Calculer l'efficacité et classer
    df_bacterie["efficacite_pct"] = ((1 - df_bacterie["resist_rate_pair"]) * 100).round(1)
    df_bacterie = df_bacterie.sort_values("efficacite_pct", ascending=False)
    
    # Zones de confiance
    def zone(eff):
        if eff >= 80:  return ("✅ RECOMMANDÉ",  "#1E8449", "Très efficace")
        elif eff >= 60: return ("🟡 POSSIBLE",    "#D35400", "Modérément efficace")
        elif eff >= 40: return ("⚠️ PRUDENCE",    "#E67E22", "Efficacité incertaine")
        else:           return ("🔴 ÉVITER",       "#C0392B", "Résistance élevée")
    
    df_bacterie[["label", "couleur", "description"]] = pd.DataFrame(
        df_bacterie["efficacite_pct"].apply(zone).tolist(),
        index=df_bacterie.index
    )
    
    # Molécules recommandées
    recommandes = df_bacterie[df_bacterie["efficacite_pct"] >= 80]["antibiotic"].tolist()
    possibles   = df_bacterie[df_bacterie["efficacite_pct"] >= 60]["antibiotic"].tolist()
    
    # Cocktail thérapeutique
    if len(possibles) >= 2:
        cocktail = (possibles[0], possibles[1])
    elif len(df_bacterie) >= 2:
        cocktail = (df_bacterie.iloc[0]["antibiotic"], df_bacterie.iloc[1]["antibiotic"])
    else:
        cocktail = None
    
    return {
        "antibiotiques": df_bacterie,
        "recommandes"  : recommandes if recommandes else possibles[:2],
        "cocktail"     : cocktail,
        "bacterie"     : bacteria_name,
        "pays"         : pays,
        "site"         : site,
    }


def get_statistiques():
    """Retourne les statistiques globales pour le module M4"""
    _, _, df = charger_ressources()
    resist_pair, _, _ = charger_ressources()
    
    stats = {
        "nb_antibiogrammes" : len(df),
        "nb_bacteries"      : df["bacteria_name"].nunique(),
        "nb_antibiotiques"  : df["antibiotic"].nunique(),
        "nb_pays"           : df["country"].nunique(),
        "dist_resistance"   : df["resistance"].value_counts().to_dict(),
        "resist_par_bact"   : df.groupby("bacteria_name")["is_resistant"].mean().sort_values(ascending=False).to_dict(),
        "resist_par_atb"    : df.groupby("antibiotic")["is_resistant"].mean().sort_values(ascending=False).to_dict(),
        "resist_par_pays"   : df.groupby("country")["is_resistant"].mean().sort_values(ascending=False).to_dict(),
        "resist_pair"       : resist_pair,
    }
    return stats


# Liste des bactéries et pays disponibles
BACTERIES = [
    "Escherichia coli",
    "Klebsiella pneumoniae",
    "Staphylococcus aureus",
    "Acinetobacter baumannii",
    "Pseudomonas aeruginosa",
    "Streptococcus pneumoniae",
    "Salmonella typhi",
    "Enterococcus faecalis",
    "Neisseria gonorrhoeae",
]

PAYS = [
    "Togo", "Benin", "Ghana", "Senegal",
    "Cote d'Ivoire", "Burkina Faso", "Mali", "Nigeria"
]

SITES = ["Sang", "Urine", "LCR", "Plaie", "Selles", "Expectoration"]