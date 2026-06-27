import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Gécamines - Simulateur & ERP RH", layout="wide", page_icon="📊")

# --- STYLE CSS DU BULLETIN DE PAIE ---
st.markdown("""
    <style>
    .bulletin-box {
        border: 2px solid #0F172A;
        padding: 25px;
        border-radius: 8px;
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Courier New', Courier, monospace;
    }
    .bulletin-header {
        text-align: center;
        color: #1E3A8A;
        font-weight: bold;
    }
    .bulletin-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    .bulletin-table th {
        background-color: #0F172A;
        color: white;
        padding: 5px;
        text-align: left;
    }
    .bulletin-table td {
        padding: 5px;
        border-bottom: 1px dashed #CBD5E1;
    }
    .total-net {
        text-align: right;
        color: #1E3A8A;
        font-size: 1.3em;
        margin-top: 20px;
        font-weight: bold;
        border-top: 2px solid #0F172A;
        padding-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SÉCURITÉ ANTI-BUG : CORRECTION ET INITIALISATION DU SESSION_STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Définition de la base de données brute de secours
donnees_initiales = [
    {"ID": "EMP001", "Nom": "Joel Mulumba Kapuku", "Poste": "Administrateur Budget / Finances", "Salaire_Base": 4500.0, "Presences": 22, "Login": "joel kapuku"},
    {"ID": "EMP002", "Nom": "Kestia Kusuba", "Poste": "Directeur RH", "Salaire_Base": 3800.0, "Presences": 22, "Login": "kestia"},
    {"ID": "EMP003", "Nom": "Jean Mukendi", "Poste": "Ingénieur Mine", "Salaire_Base": 2600.0, "Presences": 19, "Login": "jean"}
]

# Force la recréation ou la réparation immédiate si la variable est corrompue ou s'il manque "Login"
if 'employes' not in st.session_state or not isinstance(st.session_state.employes, pd.DataFrame):
    st.session_state.employes = pd.DataFrame(donnees_initiales)
elif "Login" not in st.session_state.employes.columns:
    # Si le tableau existe mais a été mémorisé sans la colonne Login, on force sa reconstruction
    st.session_state.employes = pd.DataFrame(donnees_initiales)

# ==========================================
# ÉCRAN DE CONNEXION (SÉCURITÉ)
# ==========================================
def ecran_connexion():
    st.markdown("<h2 style='text-align: center;'>🛡️ Authentification Portail RH & Performance - Gécamines</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        with st.form("login_form"):
            identifiant = st.text_input("Identifiant utilisateur :").strip().lower()
            mot_de_passe = st.text_input("Mot de passe :", type="password")
            soumettre = st.form_submit_button("Se connecter", use_container_width=True)
            
            if soumettre:
                # 1. Option d'accès Super-Administrateur
                if identifiant == "admin" and mot_de_passe == "admin123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Administrateur"
                    st.session_state.current_user = "Direction Générale"
                    st.rerun()
                
                # 2. Option d'accès Employé dynamique (Vérification blindée sur la colonne existante)
                elif identifiant in st.session_state.employes["Login"].str.lower().tolist():
                    # Extraction sécurisée du mot de passe associé pour l'exercice (ou par défaut général)
                    if mot_de_passe == "gcm2026" or mot_de_passe == "2000":
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Employé"
                        st.session_state.current_user = identifiant
                        st.rerun()
                    else:
                        st.error("Mot de passe incorrect pour cet utilisateur.")
                else:
                    st.error("Identifiant utilisateur non répertorié dans les effectifs.")

# ==========================================
# GESTION DES PAGES ET DU MENU
# ==========================================
if not st.session_state.authenticated:
    ecran_connexion()
else:
    # Barre de navigation latérale
    st.sidebar.markdown(f"**Utilisateur :** {st.session_state.current_user.title()}")
    st.sidebar.markdown(f"**Rôle :** {st.session_state.user_role}")
    if st.sidebar.button("🔒 Se déconnecter", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.rerun()
    st.sidebar.markdown("---")

    # --- PORTAIL ADMINISTRATEUR (DIRECTION INTERNE) ---
    if st.session_state.user_role == "Administrateur":
        menu = [
            "📉 Simulateur de Performance", 
            "👥 Gestion du Personnel (Ajout/Modif/Suppr)", 
            "💵 Calcul & Édition de la Paie"
        ]
        choix = st.sidebar.selectbox("Menu Principal", menu)
        
        if choix == "📉 Simulateur de Performance":
            st.title("📊 Simulateur de Performance Prédictive – Gécamines")
            st.markdown("Cette application permet de simuler l'impact des choix managériaux sur le Résultat Net de la Gécamines à l'horizon 2028.")
            
            st.sidebar.header("⚙️ Paramètres du Scénario")
            croissance_ca = st.sidebar.slider("Hausse annuelle du CA (%)", 0.0, 15.0, 5.0, 0.5) / 100
            reduction_couts = st.sidebar.slider("Réduction des coûts opératoires (%)", 0.0, 10.0, 3.0, 0.5) / 100
            
            ca_actuel = 120000000
            charges_actuelles = 95000000
            ca_2028 = ca_actuel * ((1 + croissance_ca) ** 2)
            charges_2028 = charges_actuelles * ((1 - reduction_couts) ** 2)
            resultat_net = ca_2028 - charges_2028
            
            c1, c2 = st.columns(2)
            c1.metric("Chiffre d'Affaires Projeté (2028)", f"{ca_2028:,.2f} $")
            c2.metric("Résultat Net Estimé (2028)", f"{resultat_net:,.2f} $")

        elif choix == "👥 Gestion du Personnel (Ajout/Modif/Suppr)":
            st.subheader("👥 Registre Matriculaire Professionnel")
            t1, t2, t3 = st.tabs(["➕ Ajouter un Agent", "✏️ Modifier Profil", "❌ Radier un Agent"])
            
            with t1:
                with st.form("form_ajout"):
                    nv_nom = st.text_input("Nom complet :")
                    nv_poste = st.text_input("Intitulé du Poste :")
                    nv_sal = st.number_input("Salaire de base ($) :", min_value=0.0, value=1500.0)
                    nv_login = st.text_input("Identifiant de connexion :")
                    if st.form_submit_button("Enregistrer"):
                        if nv_nom and nv_login:
                            nv_id = f"EMP{len(st.session_state.employes)+1:03d}"
                            new_row = {"ID": nv_id, "Nom": nv_nom, "Poste": nv_poste, "Salaire_Base": nv_sal, "Presences": 22, "Login": nv_login.lower().strip()}
                            st.session_state.employes = pd.concat([st.session_state.employes, pd.DataFrame([new_row])], ignore_index=True)
                            st.success("Collaborateur enregistré.")
                            st.rerun()
            
            with t2:
                emp_sel = st.selectbox("Collaborateur à modifier :", st.session_state.employes["Nom"].tolist())
                idx = st.session_state.employes[st.session_state.employes["Nom"] == emp_sel].index[0]
                with st.form("form_modif"):
                    ch_poste = st.text_input("Poste :", value=st.session_state.employes.at[idx, "Poste"])
                    ch_sal = st.number_input("Salaire ($) :", value=float(st.session_state.employes.at[idx, "Salaire_Base"]))
                    ch_pres = st.slider("Jours de présence :", 0, 22, int(st.session_state.employes.at[idx, "Presences"]))
                    if st.form_submit_button("Mettre à jour"):
                        st.session_state.employes.at[idx, "Poste"] = ch_poste
                        st.session_state.employes.at[idx, "Salaire_Base"] = ch_sal
                        st.session_state.employes.at[idx, "Presences"] = ch_pres
                        st.success("Profil modifié.")
                        st.rerun()
                        
            with t3:
                emp_sup = st.selectbox("Collaborateur à supprimer :", st.session_state.employes["Nom"].tolist(), key="suppr")
                if st.button("Confirmer la suppression", type="primary"):
                    st.session_state.employes = st.session_state.employes[st.session_state.employes["Nom"] != emp_sup].reset_index(drop=True)
                    st.warning(f"L'agent {emp_sup} supprimé.")
                    st.rerun()

            st.dataframe(st.session_state.employes, use_container_width=True)

        elif choix == "💵 Calcul & Édition de la Paie":
            st.subheader("💵 Émission Fiscale du Bulletin de Paie RDC")
            agent = st.selectbox("Sélectionner l'agent :", st.session_state.employes["Nom"].tolist())
            data = st.session_state.employes[st.session_state.employes["Nom"] == agent].iloc[0]
            
            sb = float(data["Salaire_Base"])
            retenue_abs = (sb / 22) * (22 - int(data["Presences"]))
            cnss = (sb - retenue_abs) * 0.05
            ipr = (sb - retenue_abs) * 0.15
            net = (sb - retenue_abs) - cnss - ipr
            
            bulletin_html = f"""
            <div class="bulletin-box">
                <h3 class="bulletin-header">GÉCAMINES SA</h3>
                <p style="text-align:center; font-size:11px;">Lubumbashi, RDC</p>
                <hr>
                <p><b>Matricule :</b> {data['ID']} | <b>Nom :</b> {data['Nom']}</p>
                <p><b>Poste :</b> {data['Poste']} | <b>Présence :</b> {data['Presences']}/22j</p>
                <table class="bulletin-table">
                    <tr><th>Rubrique</th><th style="text-align:right;color:white;">Gains</th><th style="text-align:right;color:white;">Retenues</th></tr>
                    <tr><td>Salaire de base</td><td style="text-align:right;">{sb:.2f}</td><td></td></tr>
                    <tr><td>Retenue Absences</td><td></td><td style="text-align:right;">{retenue_abs:.2f}</td></tr>
                    <tr><td>CNSS (5%)</td><td></td><td style="text-align:right;">{cnss:.2f}</td></tr>
                    <tr><td>IPR (15%)</td><td></td><td style="text-align:right;">{ipr:.2f}</td></tr>
                </table>
                <div class="total-net">NET À PAYER : {net:,.2f} $</div>
            </div>
            """
            st.markdown(bulletin_html, unsafe_allow_html=True)
            txt_content = f"GÉCAMINES SA\nBULLETIN\nAgent: {data['Nom']}\nNet: {net:,.2f} $"
            st.download_button("📥 Télécharger / Imprimer le Bulletin", data=txt_content, file_name=f"bulletin_{data['ID']}.txt")

    # --- PORTAIL SÉCURISÉ COLLABORATEUR ---
    elif st.session_state.user_role == "Employé":
        st.title("🔒 Espace Personnel Collaborateur")
        user_login = st.session_state.current_user
        info_perso = st.session_state.employes[st.session_state.employes["Login"].str.lower() == user_login].iloc[0]
        
        st.info(f"Bienvenue, connecté en tant que : **{info_perso['Nom']}**.")
        
        sb = float(info_perso["Salaire_Base"])
        retenue_abs = (sb / 22) * (22 - int(info_perso["Presences"]))
        cnss = (sb - retenue_abs) * 0.05
        ipr = (sb - retenue_abs) * 0.15
        net_emp = (sb - retenue_abs) - cnss - ipr
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Votre Poste Actuel", info_perso["Poste"])
        c2.metric("Jours Présents", f"{info_perso['Presences']} / 22j")
        c3.metric("Salaire Net Estimé", f"{net_emp:,.2f} $")
        
        st.markdown("---")
        txt_attestation = f"Attestation de Rémunération\nNom: {info_perso['Nom']}\nPoste: {info_perso['Poste']}\nSalaire Contractuel Bruter: {sb} $"
        st.download_button("📥 Télécharger mon attestation de paie brute", data=txt_attestation, file_name=f"attestation_{info_perso['ID']}.txt")
