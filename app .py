import streamlit as st
import pandas as pd
import numpy as np

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

# --- SÉCURITÉ ET INITIALISATION DU SESSION_STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

donnees_initiales = [
    {"ID": "EMP001", "Nom": "Joel Mulumba Kapuku", "Poste": "Administrateur Budget / Finances", "Salaire_Base": 4500.0, "Presences": 22, "Login": "joel kapuku"},
    {"ID": "EMP002", "Nom": "Kestia Kusuba", "Poste": "Directeur RH", "Salaire_Base": 3800.0, "Presences": 22, "Login": "kestia"},
    {"ID": "EMP003", "Nom": "Jean Mukendi", "Poste": "Ingénieur Mine", "Salaire_Base": 2600.0, "Presences": 19, "Login": "jean"}
]

if 'employes' not in st.session_state or not isinstance(st.session_state.employes, pd.DataFrame) or "Login" not in st.session_state.employes.columns:
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
                # ÉLÉVATION DES DROITS POUR JOEL KAPUKU EN TANT QU'ADMINISTRATEUR PRINCIPAL
                if (identifiant == "joel kapuku" or identifiant == "admin") and (mot_de_passe == "gcm2026" or mot_de_passe == "2000" or mot_de_passe == "admin123"):
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Administrateur"
                    st.session_state.current_user = "Joel Mulumba Kapuku"
                    st.rerun()
                
                # Accès pour le reste du personnel (consultation seule)
                elif identifiant in st.session_state.employes["Login"].str.lower().tolist():
                    if mot_de_passe == "gcm2026":
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Employé"
                        st.session_state.current_user = identifiant
                        st.rerun()
                    else:
                        st.error("Mot de passe incorrect.")
                else:
                    st.error("Identifiant utilisateur non reconnu.")

# ==========================================
# LOGIQUE DE L'APPLICATION
# ==========================================
if not st.session_state.authenticated:
    ecran_connexion()
else:
    # Barre de navigation latérale
    st.sidebar.markdown(f"**Utilisateur :** {st.session_state.current_user}")
    st.sidebar.markdown(f"**Rôle :** {st.session_state.user_role}")
    if st.sidebar.button("🔒 Se déconnecter", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.rerun()
    st.sidebar.markdown("---")

    # --- INTERFACE DE GESTION COMPLETE (ADMINISTRATEUR) ---
    if st.session_state.user_role == "Administrateur":
        menu = [
            "💵 Calcul & Édition de la Paie",
            "👥 Gestion du Personnel (Ajout/Modif/Suppr)", 
            "📉 Simulateur de Performance"
        ]
        choix = st.sidebar.selectbox("Menu Principal", menu)
        
        # PAGE 1 : TRAITEMENT DE LA PAIE ET CALCULS
        if choix == "💵 Calcul & Édition de la Paie":
            st.title("💵 Traitement Fiscal de la Paie & Bulletins RDC")
            
            agent = st.selectbox("Sélectionner l'agent à traiter :", st.session_state.employes["Nom"].tolist())
            data = st.session_state.employes[st.session_state.employes["Nom"] == agent].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                sb = st.number_input("Salaire de base ($)", value=float(data["Salaire_Base"]))
                primes = st.number_input("Primes et Avantages ($)", value=0.0)
            with col2:
                retenue_abs = (sb / 22) * (22 - int(data["Presences"]))
                base_imposable = sb + primes - retenue_abs
                cnss = base_imposable * 0.05
                ipr = base_imposable * 0.15
                st.metric("Retenue Absence calculée", f"{retenue_abs:.2f} $")
            
            net = base_imposable - cnss - ipr
            
            # Affichage du bulletin
            bulletin_html = f"""
            <div class="bulletin-box">
                <h3 class="bulletin-header">GÉCAMINES SA</h3>
                <p style="text-align:center; font-size:11px;">Lubumbashi, RDC</p>
                <hr>
                <p><b>Matricule :</b> {data['ID']} | <b>Nom :</b> {data['Nom']}</p>
                <p><b>Poste :</b> {data['Poste']} | <b>Présence constatée :</b> {data['Presences']}/22j</p>
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
            
            txt_content = f"GÉCAMINES SA\nBULLETIN\nAgent: {data['Nom']}\nNet à Payer: {net:,.2f} $"
            st.download_button("📥 Télécharger / Imprimer le Bulletin", data=txt_content, file_name=f"bulletin_{data['ID']}.txt")

        # PAGE 2 : AJOUT, MODIFICATION ET SUPPRESSION
        elif choix == "👥 Gestion du Personnel (Ajout/Modif/Suppr)":
            st.title("👥 Registre Matriculaire Personnel")
            t1, t2, t3 = st.tabs(["➕ Enregistrer un Agent", "✏️ Modifier Salaire & Présences", "❌ Radier un Agent"])
            
            with t1:
                with st.form("form_ajout"):
                    nv_nom = st.text_input("Nom complet de l'agent :")
                    nv_poste = st.text_input("Poste :")
                    nv_sal = st.number_input("Salaire initial ($) :", value=1200.0)
                    nv_login = st.text_input("Identifiant (login) :")
                    if st.form_submit_button("Valider l'enregistrement"):
                        if nv_nom and nv_login:
                            nv_id = f"EMP{len(st.session_state.employes)+1:03d}"
                            new_row = {"ID": nv_id, "Nom": nv_nom, "Poste": nv_poste, "Salaire_Base": nv_sal, "Presences": 22, "Login": nv_login.lower().strip()}
                            st.session_state.employes = pd.concat([st.session_state.employes, pd.DataFrame([new_row])], ignore_index=True)
                            st.success(f"{nv_nom} a bien été ajouté aux effectifs !")
                            st.rerun()
            
            with t2:
                emp_sel = st.selectbox("Sélectionner l'agent à modifier :", st.session_state.employes["Nom"].tolist())
                idx = st.session_state.employes[st.session_state.employes["Nom"] == emp_sel].index[0]
                with st.form("form_modif"):
                    ch_poste = st.text_input("Poste actuel :", value=st.session_state.employes.at[idx, "Poste"])
                    ch_sal = st.number_input("Ajuster le Salaire de base ($) :", value=float(st.session_state.employes.at[idx, "Salaire_Base"]))
                    ch_pres = st.slider("Jours de présence ce mois-ci :", 0, 22, int(st.session_state.employes.at[idx, "Presences"]))
                    if st.form_submit_button("Enregistrer les modifications"):
                        st.session_state.employes.at[idx, "Poste"] = ch_poste
                        st.session_state.employes.at[idx, "Salaire_Base"] = ch_sal
                        st.session_state.employes.at[idx, "Presences"] = ch_pres
                        st.success("Données de l'agent mises à jour.")
                        st.rerun()
                        
            with t3:
                emp_sup = st.selectbox("Sélectionner l'agent à supprimer :", st.session_state.employes["Nom"].tolist(), key="suppr")
                if st.button("Confirmer la radiation définitive", type="primary"):
                    st.session_state.employes = st.session_state.employes[st.session_state.employes["Nom"] != emp_sup].reset_index(drop=True)
                    st.warning(f"L'agent {emp_sup} a été retiré des registres.")
                    st.rerun()

            st.write("### Liste actuelle du personnel")
            st.dataframe(st.session_state.employes, use_container_width=True)

        # PAGE 3 : LE SIMULATEUR FINANCIER D'ORIGINE
        elif choix == "📉 Simulateur de Performance":
            st.title("📊 Simulateur de Performance Prédictive")
            st.sidebar.header("⚙️ Paramètres du Scénario")
            croissance_ca = st.sidebar.slider("Hausse annuelle du CA (%)", 0.0, 15.0, 5.0, 0.5) / 100
            reduction_couts = st.sidebar.slider("Réduction des coûts (%)", 0.0, 10.0, 3.0, 0.5) / 100
            
            ca_actuel = 120000000
            charges_actuelles = 95000000
            ca_2028 = ca_actuel * ((1 + croissance_ca) ** 2)
            charges_2028 = charges_actuelles * ((1 - reduction_couts) ** 2)
            resultat_net = ca_2028 - charges_2028
            
            st.metric("Chiffre d'Affaires Projeté (2028)", f"{ca_2028:,.2f} $")
            st.metric("Résultat Net Estimé (2028)", f"{resultat_net:,.2f} $")

    # --- PORTAIL EXCLUSIF EMPLOYÉ STANDARD ---
    elif st.session_state.user_role == "Employé":
        st.title("🔒 Mon Espace Personnel")
        info_perso = st.session_state.employes[st.session_state.employes["Login"].str.lower() == st.session_state.current_user].iloc[0]
        st.info(f"Bienvenue, **{info_perso['Nom']}**.")
        st.metric("Votre Poste", info_perso["Poste"])
        st.metric("Présences enregistrées", f"{info_perso['Presences']} / 22j")
