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

# --- INITIALISATION DE LA SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Initialisation de la liste des employés avec la colonne Login requise
if 'employes' not in st.session_state:
    st.session_state.employes = pd.DataFrame([
        {"ID": "EMP001", "Nom": "Kestia Kusuba", "Poste": "Directeur RH", "Salaire_Base": 3800.0, "Presences": 22, "Login": "kestia"},
        {"ID": "EMP002", "Nom": "Jean Mukendi", "Poste": "Ingénieur Mine", "Salaire_Base": 2600.0, "Presences": 19, "Login": "jean"},
        {"ID": "EMP003", "Nom": "Marie Mwamba", "Poste": "Géologue Principal", "Salaire_Base": 2300.0, "Presences": 22, "Login": "marie"}
    ])

# ==========================================
# ÉCRAN DE CONNEXION (SÉCURITÉ)
# ==========================================
def ecran_connexion():
    st.markdown("<h2 style='text-align: center;'>🛡️ Authentification Portail Portail RH & Performance - Gécamines</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        with st.form("login_form"):
            identifiant = st.text_input("Identifiant utilisateur :").strip().lower()
            mot_de_passe = st.text_input("Mot de passe :", type="password")
            soumettre = st.form_submit_button("Se connecter", use_container_width=True)
            
            if soumettre:
                if identifiant == "admin" and mot_de_passe == "admin123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Administrateur"
                    st.session_state.current_user = "Direction RH"
                    st.rerun()
                elif identifiant in st.session_state.employes["Login"].tolist() and mot_de_passe == "gcm2026":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Employé"
                    st.session_state.current_user = identifiant
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")

# ==========================================
# APPLICATION PRINCIPALE
# ==========================================
if not st.session_state.authenticated:
    ecran_connexion()
else:
    # Barre latérale commune
    st.sidebar.markdown(f"**Utilisateur :** {st.session_state.current_user}")
    st.sidebar.markdown(f"**Rôle :** {st.session_state.user_role}")
    if st.sidebar.button("🔒 Se déconnecter", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.rerun()
    st.sidebar.markdown("---")

    # --- INTERFACE DIRECTION / ADMINISTRATEUR ---
    if st.session_state.user_role == "Administrateur":
        menu = [
            "📉 Simulateur de Performance", 
            "👥 Gestion du Personnel (Ajout/Modif/Suppr)", 
            "💵 Calcul & Édition de la Paie"
        ]
        choix = st.sidebar.selectbox("Menu Principal", menu)
        
        # 1. VOTRE SIMULATEUR D'ORIGINE
        if choix == "📉 Simulateur de Performance":
            st.title("📊 Simulateur de Performance Prédictive – Gécamines")
            st.markdown("""
            Cette application permet de simuler l'impact des choix managériaux sur le Résultat Net de la Gécamines à l'horizon 2028,
            en se basant sur les modèles de chaîne de valeur.
            """)
            
            st.sidebar.header("⚙️ Paramètres du Scénario de Réforme")
            croissance_ca = st.sidebar.slider("Hausse annuelle du CA (%)", 0.0, 15.0, 5.0, 0.5) / 100
            reduction_couts = st.sidebar.slider("Réduction des coûts opératoires (%)", 0.0, 10.0, 3.0, 0.5) / 100
            
            # Calculs fictifs du simulateur
            ca_actuel = 120000000
            charges_actuelles = 95000000
            
            ca_2028 = ca_actuel * ((1 + croissance_ca) ** 2)
            charges_2028 = charges_actuelles * ((1 - reduction_couts) ** 2)
            resultat_net = ca_2028 - charges_2028
            
            c1, c2 = st.columns(2)
            c1.metric("Chiffre d'Affaires Projeté (2028)", f"{ca_2028:,.2f} $")
            c2.metric("Résultat Net Estimé (2028)", f"{resultat_net:,.2f} $", delta=f"{(resultat_net - (ca_actuel - charges_actuelles)):,.2f} $")

        # 2. GESTION COMPLETE (AJOUT, MODIFICATION, SUPPRESSION)
        elif choix == "👥 Gestion du Personnel (Ajout/Modif/Suppr)":
            st.subheader("👥 Registre Matriculaire Professionnel des Agents")
            t1, t2, t3 = st.tabs(["➕ Ajouter un Agent", "✏️ Modifier Profil / Présences", "❌ Radier un Agent"])
            
            with t1:
                with st.form("form_ajout"):
                    nv_nom = st.text_input("Nom complet :")
                    nv_poste = st.text_input("Intitulé du Poste :")
                    nv_sal = st.number_input("Salaire de base ($) :", min_value=0.0, value=1500.0)
                    nv_login = st.text_input("Identifiant de connexion (ex: jean) :")
                    if st.form_submit_button("Enregistrer le collaborateur"):
                        if nv_nom and nv_login:
                            nv_id = f"EMP{len(st.session_state.employes)+1:03d}"
                            new_row = {"ID": nv_id, "Nom": nv_nom, "Poste": nv_poste, "Salaire_Base": nv_sal, "Presences": 22, "Login": nv_login.lower().strip()}
                            st.session_state.employes = pd.concat([st.session_state.employes, pd.DataFrame([new_row])], ignore_index=True)
                            st.success("Collaborateur ajouté avec succès !")
                            st.rerun()
            
            with t2:
                emp_sel = st.selectbox("Collaborateur à modifier :", st.session_state.employes["Nom"].tolist())
                idx = st.session_state.employes[st.session_state.employes["Nom"] == emp_sel].index[0]
                with st.form("form_modif"):
                    ch_poste = st.text_input("Poste :", value=st.session_state.employes.at[idx, "Poste"])
                    ch_sal = st.number_input("Salaire ($) :", value=float(st.session_state.employes.at[idx, "Salaire_Base"]))
                    ch_pres = st.slider("Jours de présence (Max 22) :", 0, 22, int(st.session_state.employes.at[idx, "Presences"]))
                    if st.form_submit_button("Mettre à jour"):
                        st.session_state.employes.at[idx, "Poste"] = ch_poste
                        st.session_state.employes.at[idx, "Salaire_Base"] = ch_sal
                        st.session_state.employes.at[idx, "Presences"] = ch_pres
                        st.success("Profil modifié.")
                        st.rerun()
                        
            with t3:
                emp_sup = st.selectbox("Collaborateur à supprimer :", st.session_state.employes["Nom"].tolist(), key="suppr")
                if st.button("Confirmer la suppression définitive", type="primary"):
                    st.session_state.employes = st.session_state.employes[st.session_state.employes["Nom"] != emp_sup].reset_index(drop=True)
                    st.warning(f"L'agent {emp_sup} a été retiré du personnel.")
                    st.rerun()

            st.dataframe(st.session_state.employes, use_container_width=True)

        # 3. PAIE FISCALE RDC ET IMPRESSION
        elif choix == "💵 Calcul & Édition de la Paie":
            st.subheader("💵 Traitement Fiscale de la Paie & Bulletin")
            agent = st.selectbox("Sélectionner l'agent :", st.session_state.employes["Nom"].tolist())
            data = st.session_state.employes[st.session_state.employes["Nom"] == agent].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                sb = st.number_input("Salaire de base ($)", value=float(data["Salaire_Base"]))
                primes = st.number_input("Primes ($)", value=200.0)
            with col2:
                retenue_abs = (sb / 22) * (22 - int(data["Presences"]))
                cnss = (sb + primes - retenue_abs) * 0.05
                ipr = (sb + primes - retenue_abs) * 0.15
                st.metric("Retenue Absence", f"{retenue_abs:.2f} $")
            
            net = (sb + primes - retenue_abs) - cnss - ipr
            
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
                    <tr><td>Primes</td><td style="text-align:right;">{primes:.2f}</td><td></td></tr>
                    <tr><td>Retenue Absences</td><td></td><td style="text-align:right;">{retenue_abs:.2f}</td></tr>
                    <tr><td>CNSS (5%)</td><td></td><td style="text-align:right;">{cnss:.2f}</td></tr>
                    <tr><td>IPR (15%)</td><td></td><td style="text-align:right;">{ipr:.2f}</td></tr>
                </table>
                <div class="total-net">NET À PAYER : {net:,.2f} $</div>
            </div>
            """
            st.markdown(bulletin_html, unsafe_allow_html=True)
            
            # Téléchargement / Impression du fichier texte officiel
            txt_content = f"GÉCAMINES SA\nBULLETIN DE PAIE\nAgent: {data['Nom']}\nNet à Payer: {net:,.2f} $"
            st.download_button("📥 Télécharger / Imprimer le Bulletin", data=txt_content, file_name=f"bulletin_{data['ID']}.txt")

    # --- INTERFACE RESTREINTE POUR L'EMPLOYÉ ---
    elif st.session_state.user_role == "Employé":
        st.title("🔒 Portail Salarié Confienditiel")
        user_login = st.session_state.current_user
        info_perso = st.session_state.employes[st.session_state.employes["Login"] == user_login].iloc[0]
        
        st.info(f"Bienvenue dans votre espace sécurisé, **{info_perso['Nom']}**.")
        
        sb = float(info_perso["Salaire_Base"])
        net_emp = sb - (sb * 0.05) - (sb * 0.15)
        
        st.metric("Votre Poste", info_perso["Poste"])
        st.metric("Présence Enregistrée", f"{info_perso['Presences']} / 22 jours")
        
        if st.download_button("📥 Télécharger mon attestation de paie brute", data=f"Attestation: {info_perso['Nom']}\nSalaire de Base: {sb} $", file_name="mon_profil.txt"):
            st.success("Téléchargement lancé !")
