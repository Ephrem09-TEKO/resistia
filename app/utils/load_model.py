# ═══════════════════════════════════════════════════
# utils/load_model.py
# Génère le modèle si absent (pour Streamlit Cloud)
# ═══════════════════════════════════════════════════
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import joblib
import json

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR  = os.path.join(BASE_DIR, "data", "processed")

def generer_et_sauvegarder():
    """Génère le dataset synthétique et entraîne le modèle si absent"""
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(DATA_DIR,  exist_ok=True)

    print("⏳ Génération du dataset ECOWAS...")

    np.random.seed(42)
    N = 8000

    BACTERIES_W = {
        'Escherichia coli':0.25,'Klebsiella pneumoniae':0.20,
        'Staphylococcus aureus':0.18,'Streptococcus pneumoniae':0.10,
        'Salmonella typhi':0.08,'Pseudomonas aeruginosa':0.07,
        'Acinetobacter baumannii':0.06,'Enterococcus faecalis':0.04,
        'Neisseria gonorrhoeae':0.02,
    }
    PAYS_W = {
        'Togo':0.15,'Benin':0.10,'Ghana':0.15,'Senegal':0.15,
        "Cote d'Ivoire":0.13,'Burkina Faso':0.10,'Mali':0.07,'Nigeria':0.15,
    }
    SITES = ['Urine','Sang','LCR','Plaie','Selles','Expectoration']
    RESISTANCE_RATES = {
        'Escherichia coli':{'Ampicillin':0.85,'Ciprofloxacin':0.55,
            'Ceftriaxone':0.45,'Trimethoprim':0.70,'Gentamicin':0.35,
            'Imipenem':0.08,'Amikacin':0.12,'Nitrofurantoin':0.20},
        'Klebsiella pneumoniae':{'Ampicillin':0.98,'Ciprofloxacin':0.50,
            'Ceftriaxone':0.60,'Trimethoprim':0.65,'Gentamicin':0.40,
            'Imipenem':0.15,'Amikacin':0.18,'Colistin':0.05},
        'Staphylococcus aureus':{'Oxacillin':0.40,'Ciprofloxacin':0.45,
            'Erythromycin':0.55,'Trimethoprim':0.40,'Gentamicin':0.30,
            'Vancomycin':0.02,'Clindamycin':0.35,'Tetracycline':0.50},
        'Streptococcus pneumoniae':{'Penicillin':0.30,'Erythromycin':0.25,
            'Trimethoprim':0.55,'Ciprofloxacin':0.10,'Ceftriaxone':0.15,
            'Vancomycin':0.01,'Tetracycline':0.45,'Clindamycin':0.20},
        'Salmonella typhi':{'Ampicillin':0.60,'Ciprofloxacin':0.30,
            'Chloramphenicol':0.45,'Trimethoprim':0.55,'Ceftriaxone':0.10,
            'Azithromycin':0.08,'Tetracycline':0.60,'Amikacin':0.05},
        'Pseudomonas aeruginosa':{'Ciprofloxacin':0.40,'Imipenem':0.35,
            'Gentamicin':0.45,'Ceftazidime':0.40,'Amikacin':0.25,
            'Piperacillin':0.45,'Colistin':0.05,'Meropenem':0.30},
        'Acinetobacter baumannii':{'Ciprofloxacin':0.75,'Imipenem':0.60,
            'Gentamicin':0.70,'Ceftriaxone':0.80,'Amikacin':0.55,
            'Colistin':0.08,'Meropenem':0.60,'Trimethoprim':0.75},
        'Enterococcus faecalis':{'Ampicillin':0.20,'Vancomycin':0.10,
            'Erythromycin':0.60,'Tetracycline':0.65,'Ciprofloxacin':0.50,
            'Gentamicin':0.40,'Linezolid':0.03,'Nitrofurantoin':0.15},
        'Neisseria gonorrhoeae':{'Penicillin':0.70,'Ciprofloxacin':0.65,
            'Tetracycline':0.75,'Ceftriaxone':0.10,'Azithromycin':0.20,
            'Spectinomycin':0.05,'Cefixime':0.15,'Gentamicin':0.08},
    }

    records = []
    bact_list = list(BACTERIES_W.keys())
    bact_w    = list(BACTERIES_W.values())
    pays_list = list(PAYS_W.keys())
    pays_w    = list(PAYS_W.values())

    for _ in range(N):
        bacterie = np.random.choice(bact_list, p=bact_w)
        pays     = np.random.choice(pays_list, p=pays_w)
        site     = np.random.choice(SITES)
        annee    = np.random.randint(2019, 2025)
        for atb, p_r in RESISTANCE_RATES[bacterie].items():
            rand = np.random.random()
            ph   = 'R' if rand < p_r else ('I' if rand < p_r+0.08 else 'S')
            records.append({
                'bacteria_name':bacterie,'antibiotic':atb,
                'resistance':ph,'country':pays,
                'specimen_site':site,'year':annee,
                'source':'Synthetic_ECOWAS',
                'is_resistant':1 if ph in ['R','I'] else 0
            })

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, "antibiograms_clean.csv"), index=False)

    # Taux par paire
    rp = df.groupby(['bacteria_name','antibiotic'])['is_resistant'].mean().reset_index()
    rp.columns = ['bacteria_name','antibiotic','resist_rate_pair']
    rp.to_csv(os.path.join(MODEL_DIR, "resist_rate_pair.csv"), index=False)

    # Features pour le modèle
    df2 = df.merge(
        df.groupby('bacteria_name')['is_resistant'].mean().rename('resist_rate_bacteria'),
        on='bacteria_name')
    df2 = df2.merge(
        df.groupby('antibiotic')['is_resistant'].mean().rename('resist_rate_antibiotic'),
        on='antibiotic')
    df2 = df2.merge(
        df.groupby('country')['is_resistant'].mean().rename('resist_rate_country'),
        on='country')
    df2 = df2.merge(rp, on=['bacteria_name','antibiotic'])

    from sklearn.preprocessing import LabelEncoder
    mappings = {}
    for col in ['bacteria_name','antibiotic','country','specimen_site']:
        le = LabelEncoder()
        df2[col+'_encoded'] = le.fit_transform(df2[col])
        mappings[col] = {str(k):int(v) for k,v in
                         zip(le.classes_, le.transform(le.classes_))}

    with open(os.path.join(MODEL_DIR,"label_mappings.json"),'w',encoding='utf-8') as f:
        json.dump(mappings, f, ensure_ascii=False, indent=2)

    FEATURES = ['bacteria_name_encoded','antibiotic_encoded',
                'country_encoded','specimen_site_encoded','year',
                'resist_rate_bacteria','resist_rate_antibiotic',
                'resist_rate_country','resist_rate_pair']

    with open(os.path.join(MODEL_DIR,"features.json"),'w') as f:
        json.dump(FEATURES, f)

    X = df2[FEATURES]
    y = df2['is_resistant']
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                               random_state=42, stratify=y)

    print("⏳ Entraînement du modèle...")
    modele = GradientBoostingClassifier(n_estimators=100, random_state=42)
    modele.fit(X_tr, y_tr)
    joblib.dump(modele, os.path.join(MODEL_DIR,"resistia_model.pkl"))

    # dataset_complet
    df2.to_csv(os.path.join(DATA_DIR,"dataset_complet.csv"), index=False)

    print("✅ Modèle et données générés avec succès !")


def verifier_ou_generer():
    """Vérifie si les fichiers existent, sinon les génère"""
    model_path = os.path.join(MODEL_DIR, "resistia_model.pkl")
    data_path  = os.path.join(DATA_DIR,  "antibiograms_clean.csv")
    if not os.path.exists(model_path) or not os.path.exists(data_path):
        generer_et_sauvegarder()