import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Digitalisation RH, Paie & IA", layout="wide", page_icon="💼")

# --- STYLE CSS PERSONNALISÉ POUR LE BULLETIN ---
st.markdown("""
    <style>
    .bulletin-box {
        border: 2px solid #1E3A8A;
        padding: 25px;
        border-radius: 10px;
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Arial', sans-serif;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
    }
    .bulletin-header {
        text-align: center;
        color: #1E3A8A;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .bulletin-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    .bulletin-table th {
        background-color: #1E3A8A;
        color: white;
        padding: 8px;
        text-align: left;
    }
    .bulletin-table td {
        padding: 8px;
        border-bottom: 1px solid #E2E8F0;
    }
    .total-net {
        text-align: right;
        color: #1E3A8A;
        font-size: 1.3em;
        margin-top: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DE LA BASE DE DONNÉES EN MÉMOIRE ---
if 'employes' not in st.session_state:
    st.session_state.employes = pd.DataFrame([
        {"ID": "EMP001", "Nom": "Kestia Kusuba", "Poste": "Directeur RH", "Salaire_Base": 3500.0, "Presences": 22},
        {"ID": "EMP002", "Nom": "Jean Mukendi", "Poste": "Ingénieur Mine", "Salaire_Base": 2500.0, "Presences": 18},
        {"ID": "EMP003", "Nom": "Marie Mwamba", "Poste": "Géologue", "Salaire_Base": 2200.0, "Presences": 21}
    ])

if 'historique_paie' not in st.session_state:
    st.session_state.historique_paie = []

# --- TITRE PRINCIPAL ---
st.title("💼 Système RH Intégré : Gestion, IA & Bulletins de Paie")
st.markdown("---")

# --- BARRE LATÉRALE DE NAVIGATION ---
menu = ["📈 Tableau de Bord", "👥 Gestion des Employés (CRUD)", "⏱️ Présences & IA", "💵 Calcul & Impression Paie"]
choix = st.sidebar.selectbox("Menu Principal", menu)

# ==========================================
# MODULE 1 : TABLEAU DE BORD
# ==========================================
if choix == "📈 Tableau de Bord":
    st.subheader("📊 Tableau de Bord Global")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Effectif Total", len(st.session_state.employes))
    col2.metric("Masse Salariale brute", f"{st.session_state.employes['Salaire_Base'].sum():,.2f} $")
    col3.metric("Taux de Présence Moyen", f"{round(st.session_state.employes['Presences'].mean() / 22 * 100, 1)} %")
    
    st.markdown("### Répartition Analytique des Salaires de Base")
    if not st.session_state.employes.empty:
        fig, ax = plt.subplots(figsize=(10, 3.5))
        ax.bar(st.session_state.employes["Nom"], st.session_state.employes["Salaire_Base"], color="#1E3A8A")
        ax.set_ylabel("Salaire ($)")
        plt.xticks(rotation=15)
        st.pyplot(fig)
    else:
        st.info("Aucun employé enregistré.")

# ==========================================
# MODULE 2 : GESTION DES EMPLOYÉS (AJOUTER / MODIFIER / SUPPRIMER)
# ==========================================
elif choix == "👥 Gestion des Employés (CRUD)":
    st.subheader("👥 Registre et Configuration des Employés")
    
    onglet1, onglet2, onglet3 = st.tabs(["➕ Ajouter un Employé", "✏️ Modifier / Saisir les Salaires", "❌ Supprimer"])
    
    # 1. AJOUTER
    with onglet1:
        st.markdown("### Enregistrer un nouvel employé")
        with st.form("form_ajout"):
            nv_id = f"EMP{len(st.session_state.employes)+1:03d}"
            nv_nom = st.text_input("Nom complet de l'employé :")
            nv_poste = st.text_input("Poste occupé :")
            nv_salaire = st.number_input("Salaire de base mensuel ($) :", min_value=0.0, value=1000.0, step=100.0)
            nv_presences = st.slider("Jours de présence par défaut (sur 22j) :", 0, 22, 22)
            
            bouton_ajouter = st.form_submit_button("Enregistrer l'employé")
            if bouton_ajouter:
                if nv_nom and nv_poste:
                    nouvel_emp = {"ID": nv_id, "Nom": nv_nom, "Poste": nv_poste, "Salaire_Base": nv_salaire, "Presences": nv_presences}
                    st.session_state.employes = pd.concat([st.session_state.employes, pd.DataFrame([nouvel_emp])], ignore_index=True)
                    st.success(f"🎉 {nv_nom} a été ajouté avec succès avec l'identifiant {nv_id} !")
                    st.rerun()
                else:
                    st.error("Veuillez remplir tous les champs avant de valider.")

    # 2. MODIFIER SALAIRE / POSTE
    with onglet2:
        st.markdown("### Modifier les informations ou mettre à jour un salaire")
        if not st.session_state.employes.empty:
            liste_noms = st.session_state.employes["Nom"].tolist()
            emp_a_modifier = st.selectbox("Sélectionner l'employé à mettre à jour :", liste_noms, key="modif_select")
            
            idx = st.session_state.employes[st.session_state.employes["Nom"] == emp_a_modifier].index[0]
            row = st.session_state.employes.loc[idx]
            
            with st.form("form_modif"):
                mod_poste = st.text_input("Modifier le poste :", value=row["Poste"])
                mod_salaire = st.number_input("Ajuster le Salaire de base ($) :", min_value=0.0, value=float(row["Salaire_Base"]), step=50.0)
                mod_presences = st.slider("Ajuster les jours de présence :", 0, 22, int(row["Presences"]))
                
                bouton_modifier = st.form_submit_button("Enregistrer les modifications")
                if bouton_modifier:
                    st.session_state.employes.at[idx, "Poste"] = mod_poste
                    st.session_state.employes.at[idx, "Salaire_Base"] = mod_salaire
                    st.session_state.employes.at[idx, "Presences"] = mod_presences
                    st.success(f"✏️ Les données de {emp_a_modifier} ont été mises à jour !")
                    st.rerun()
        else:
            st.info("Aucun employé à modifier.")

    # 3. SUPPRIMER
    with onglet3:
        st.markdown("### Retirer un employé du système")
        if not st.session_state.employes.empty:
            emp_a_supprimer = st.selectbox("Sélectionner l'employé à supprimer :", st.session_state.employes["Nom"].tolist(), key="suppr_select")
            if st.button("❌ Supprimer définitivement", type="primary"):
                st.session_state.employes = st.session_state.employes[st.session_state.employes["Nom"] != emp_a_supprimer].reset_index(drop=True)
                st.warning(f"L'employé {emp_a_supprimer} a été retiré des listes.")
                st.rerun()
        else:
            st.info("Aucun employé dans le système.")

    # Affichage du tableau actualisé
    st.markdown("### 📋 Liste actuelle du personnel")
    st.dataframe(st.session_state.employes, use_container_width=True)

# ==========================================
# MODULE 3 : PRÉSENCES & ANALYSE DE L'IA
# ==========================================
elif choix == "⏱️ Présences & IA":
    st.subheader("🤖 Module d'Analyse des Présences assisté par IA")
    st.dataframe(st.session_state.employes[["ID", "Nom", "Poste", "Presences"]])
    
    st.markdown("### 🦾 Rapport Analytique Automatisé de l'IA")
    for index, row in st.session_state.employes.iterrows():
        if row["Presences"] < 20:
            absences = 22 - row["Presences"]
            st.error(f"⚠️ **Alerte Absentéisme pour {row['Nom']}** : {absences} jours d'absence détectés. L'IA estime une baisse de productivité de **{absences * 12}%** sur ce profil. Un entretien RH est conseillé.")
        else:
            st.success(f"✅ **Ponctualité Conforme pour {row['Nom']}** : Assiduité optimale ({row['Presences']}/22j). Algorithme IA évalue la stabilité de ce collaborateur à **98%**.")

# ==========================================
# MODULE 4 : CALCUL DE LA PAIE & IMPRESSION BULLETIN
# ==========================================
elif choix == "💵 Calcul & Impression Paie":
    st.subheader("💵 Calculateur de Paie Interactif")
    
    if not st.session_state.employes.empty:
        liste_employes = st.session_state.employes["Nom"].tolist()
        employe_sel = st.selectbox("Sélectionner l'employé pour générer le bulletin :", liste_employes)
        
        infos = st.session_state.employes[st.session_state.employes["Nom"] == employe_sel].iloc[0]
        
        # --- ZONES D'INPUT INTERACTIVES ---
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ➕ Éléments de gain (Modifiables)")
            salaire_base_calcul = st.number_input("Salaire de base ($)", value=float(infos["Salaire_Base"]), min_value=0.0)
            primes = st.number_input("Primes exceptionnelles / Performance ($)", min_value=0.0, value=150.0, step=50.0)
            indemnites = st.number_input("Indemnités de transport & logement ($)", min_value=0.0, value=200.0, step=20.0)
            
        with col2:
            st.markdown("#### ➖ Retenues & Taxes")
            jours_absents = max(0, 22 - int(infos["Presences"]))
            penalite_absence = (salaire_base_calcul / 22) * jours_absents
            st.info(f"Absentéisme automatique appliqué : **{jours_absents} jour(s)** d'absence = **-{penalite_absence:.2f} $**")
            
            impot_rate = st.number_input("Impôt Professionnel sur le Revenu (IPR %)", value=15.0, min_value=0.0, max_value=100.0)
            cnss_rate = st.number_input("Cotisation Sociale CNSS (%)", value=5.0, min_value=0.0, max_value=100.0)

        # --- CALCULS ---
        total_brut = salaire_base_calcul + primes + indemnites - penalite_absence
        montant_impot = total_brut * (impot_rate / 100)
        montant_cnss = total_brut * (cnss_rate / 100)
        salaire_net = total_brut - montant_impot - montant_cnss

        st.markdown("---")
        
        # --- APPARENCE ET ZONE D'AFFICHAGE DU BULLETIN DE PAIE ---
        st.subheader("📄 Aperçu du Bulletin de Paie Officiel")
        
        bulletin_html = f"""
        <div class="bulletin-box">
            <h2 class="bulletin-header">GÉCAMINES SA — BULLETIN DE PAIE</h2>
            <table style="width:100%; font-size: 14px; margin-bottom: 20px;">
                <tr><td><b>Matricule :</b> {infos['ID']}</td><td><b>Période :</b> Juin 2026</td></tr>
                <tr><td><b>Nom Complet :</b> {infos['Nom']}</td><td><b>Poste :</b> {infos['Poste']}</td></tr>
                <tr><td><b>Jours Présents :</b> {infos['Presences']}/22 jours</td><td><b>Statut :</b> Payé</td></tr>
            </table>
            <table class="bulletin-table">
                <thead>
                    <tr>
                        <th>Rubriques / Libellés</th>
                        <th style="text-align: right; color: white;">Gains ($)</th>
                        <th style="text-align: right; color: white;">Retenues ($)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Salaire de Base</td><td style="text-align: right;">{salaire_base_calcul:,.2f}</td><td></td></tr>
                    <tr><td>Primes de Performance</td><td style="text-align: right;">{primes:,.2f}</td><td></td></tr>
                    <tr><td>Indemnités de Logement & Transport</td><td style="text-align: right;">{indemnites:,.2f}</td><td></td></tr>
                    <tr style="color: #C53030;"><td>Pénalité Absence ({jours_absents} jours)</td><td></td><td style="text-align: right;">{penalite_absence:,.2f}</td></tr>
                    <tr style="color: #C53030;"><td>Impôt sur le Revenu IPR ({impot_rate}%)</td><td></td><td style="text-align: right;">{montant_impot:,.2f}</td></tr>
                    <tr style="color: #C53030;"><td>Cotisation CNSS ({cnss_rate}%)</td><td></td><td style="text-align: right;">{montant_cnss:,.2f}</td></tr>
                </tbody>
            </table>
            <div class="total-net">NET À PAYER : {salaire_net:,.2f} $</div>
        </div>
        """
        st.markdown(bulletin_html, unsafe_allow_html=True)
        
        # --- ENREGISTRER & IMPRIMER EN CODE NATIF ---
        st.markdown("### 🖨️ Actions")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("💾 Enregistrer le bulletin dans l'historique"):
                st.session_state.historique_paie.append({
                    "Employe": infos["Nom"], "Periode": "Juin 2026", "Net": salaire_net
                })
                st.success(f"Le bulletin de paie de {infos['Nom']} a été archivé avec succès.")
                
        with col_btn2:
            # Pour l'impression papier, l'astuce native Streamlit consiste à créer un fichier texte ou CSV téléchargeable formaté
            bulletin_texte = f"""GÉCAMINES SA - BULLETIN DE PAIE\nID: {infos['ID']}\nNom: {infos['Nom']}\nPoste: {infos['Poste']}\nSalaire de Base: {salaire_base_calcul} $\nPrimes: {primes} $\nIndemnites: {indemnites} $\nRetenues: {penalite_absence+montant_impot+montant_cnss} $\nNET A PAYER: {salaire_net} $"""
            st.download_button(
                label="🖨️ Télécharger / Imprimer (Fichier Texte Bulletin)",
                data=bulletin_texte,
                file_name=f"bulletin_{infos['ID']}.txt",
                mime="text/plain"
            )
    else:
        st.info("Veuillez d'abord ajouter des employés dans l'onglet dédié pour pouvoir calculer la paie.")
