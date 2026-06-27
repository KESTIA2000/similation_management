import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Digitalisation RH & Paie IA", layout="wide", page_icon="💼")

# --- TITRE PRINCIPAL ---
st.title("💼 Système RH Digitalisé & Paie Intelligent (IA)")
st.markdown("---")

# --- NAVIGATION ---
menu = ["Tableau de bord", "Gestion des Présences & IA", "Calcul de la Paie & Bulletin"]
choix = st.sidebar.selectbox("Navigation", menu)

# --- BASE DE DONNÉES SIMULÉE ---
if 'employes' not in st.session_state:
    st.session_state.employes = pd.DataFrame([
        {"ID": "EMP001", "Nom": "Kestia Kusuba", "Poste": "Analyste RH", "Salaire_Base": 1500, "Presences": 22},
        {"ID": "EMP002", "Nom": "Jean Mukendi", "Poste": "Ingénieur Mine", "Salaire_Base": 2500, "Presences": 18},
        {"ID": "EMP003", "Nom": "Marie Mwamba", "Poste": "Géologue", "Salaire_Base": 2200, "Presences": 21}
    ])

# ==========================================
# MODULE 1 : TABLEAU DE BORD
# ==========================================
if choix == "Tableau de bord":
    st.subheader("📊 Vue d'ensemble de l'entreprise")
    
    # Métriques globales
    col1, col2, col3 = st.columns(3)
    col1.metric("Effectif Total", len(st.session_state.employes))
    col2.metric("Masse Salariale Base", f"{st.session_state.employes['Salaire_Base'].sum()} $")
    col3.metric("Taux de Présence Moyen", f"{round(st.session_state.employes['Presences'].mean() / 22 * 100, 1)} %")
    
    # Graphique
    st.markdown("### Répartition des Salaires par Employé")
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.bar(st.session_state.employes["Nom"], st.session_state.employes["Salaire_Base"], color="#1E3A8A")
    ax.set_ylabel("Salaire de base ($)")
    st.pyplot(fig)

# ==========================================
# MODULE 2 : GESTION DES PRÉSENCES & IA
# ==========================================
elif choix == "Gestion des Présences & IA":
    st.subheader("⏱️ Suivi des Présences et Analyse des Anomalies par l'IA")
    
    df = st.session_state.employes.copy()
    
    # Simulation des heures d'arrivée pour simuler une IA de détection
    st.markdown("### Registre des entrées (Exemple d'une journée)")
    df["Heure_Arrivee"] = ["08:02", "09:15", "08:10"] # 08:00 étant l'heure normale
    st.dataframe(df[["ID", "Nom", "Poste", "Presences", "Heure_Arrivee"]])
    
    st.markdown("---")
    st.markdown("### 🤖 Analyse Prédictive & Détection d'Anomalies (IA)")
    
    # Simulation d'un algorithme IA de détection des profils à risque (Anomalies de présence)
    for index, row in df.iterrows():
        heure_arr = int(row["Heure_Arrivee"].split(":")[0]) * 60 + int(row["Heure_Arrivee"].split(":")[1])
        heure_normale = 8 * 60 # 08h00 en minutes
        
        if heure_arr > heure_normale + 30: # Plus de 30 min de retard
            st.error(f"⚠️ **Anomalie détectée pour {row['Nom']}** : Retard critique répété ({row['Heure_Arrivee']}). Risque de baisse de productivité évalué par l'IA à **78%**.")
        elif row["Presences"] < 20:
            st.warning(f"📉 **Alerte Absentéisme pour {row['Nom']}** : Seulement {row['Presences']} jours de présence. L'IA suggère un entretien managérial.")
        else:
            st.success(f"✅ **Profil Stable pour {row['Nom']}** : Présences et ponctualité conformes aux standards de l'entreprise.")

# ==========================================
# MODULE 3 : CALCUL DE LA PAIE & BULLETIN
# ==========================================
elif choix == "Calcul de la Paie & Bulletin":
    st.subheader("💵 Calculateur de Paie et Générateur de Bulletin")
    
    # Sélection de l'employé
    liste_employes = st.session_state.employes["Nom"].tolist()
    employe_sel = st.selectbox("Sélectionner un employé pour la paie :", liste_employes)
    
    # Récupération des données de l'employé
    infos = st.session_state.employes[st.session_state.employes["Nom"] == employe_sel].iloc[0]
    
    # Formulaire de paie interactif
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ➕ Gains")
        salaire_base = st.number_input("Salaire de base ($)", value=float(infos["Salaire_Base"]))
        primes = st.number_input("Primes de performance ($)", value=100.0, step=50.0)
        indemnites = st.number_input("Indemnités de transport / Logement ($)", value=150.0, step=10.0)
        
    with col2:
        st.markdown("### ➖ Retenues")
        # Calcul automatique basé sur les présences (pénalité si jours < 22)
        jours_absents = max(0, 22 - infos["Presences"])
        penalite_absence = (salaire_base / 22) * jours_absents
        
        st.info(f"Absentéisme : {jours_absents} jour(s) détecté(s). Pénalité automatique : {round(penalite_absence, 2)} $")
        
        impot = st.number_input("Impôt sur le revenu (IPR %) ", value=15.0, min_value=0.0, max_value=100.0)
        cnss = st.number_input("Cotisation Sociale (CNSS %)", value=5.0, min_value=0.0, max_value=100.0)

    # Calculs finaux
    total_brut = salaire_base + primes + indemnites - penalite_absence
    montant_impot = total_brut * (impot / 100)
    montant_cnss = total_brut * (cnss / 100)
    salaire_net = total_brut - montant_impot - montant_cnss

    st.markdown("---")
    
    # --- VISUEL DU BULLETIN DE PAIE ---
    st.subheader(f"📄 BULLETIN DE PAIE - {employe_sel.upper()}")
    
    bulletin_html = f"""
    <div style="border: 2px solid #1E3A8A; padding: 20px; border-radius: 10px; background-color: #F8FAFC; color: black;">
        <h2 style="text-align: center; color: #1E3A8A;">BULLETIN DE PAIE - CADRE RH</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td><b>ID Employé :</b> {infos['ID']}</td><td><b>Poste :</b> {infos['Poste']}</td></tr>
            <tr><td><b>Nom :</b> {infos['Nom']}</td><td><b>Période :</b> Juin 2026</td></tr>
        </table>
        <hr style="border-top: 1px dashed #1E3A8A;">
        <table style="width: 100%;">
            <tr style="background-color: #E2E8F0;"><th>Libellé</th><th style="text-align: right;">À charger ($)</th><th style="text-align: right;">À déduire ($)</th></tr>
            <tr><td>Salaire de base</td><td style="text-align: right;">{salaire_base:.2f}</td><td></td></tr>
            <tr><td>Primes</td><td style="text-align: right;">{primes:.2f}</td><td></td></tr>
            <tr><td>Indemnités</td><td style="text-align: right;">{indemnites:.2f}</td><td></td></tr>
            <tr style="color: red;"><td>Retenue Absence ({jours_absents} j)</td><td></td><td style="text-align: right;">{penalite_absence:.2f}</td></tr>
            <tr style="color: red;"><td>Impôt IPR ({impot}%)</td><td></td><td style="text-align: right;">{montant_impot:.2f}</td></tr>
            <tr style="color: red;"><td>Cotisation CNSS ({cnss}%)</td><td></td><td style="text-align: right;">{montant_cnss:.2f}</td></tr>
        </table>
        <hr style="border-top: 2px solid #1E3A8A;">
        <h3 style="text-align: right; color: #1E3A8A;">NET À PAYER : {salaire_net:.2f} $</h3>
    </div>
    """
    
    st.markdown(bulletin_html, unsafe_allow_html=True)
    
    # Petit bouton bonus pour simuler l'envoi
    if st.button("📧 Envoyer le bulletin par courriel à l'employé"):
        st.success(f"Le bulletin a été généré de manière numérique et envoyé à {infos['Nom']} !") 
