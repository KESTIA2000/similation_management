import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="ERP RH & Paie Sécurisé - Gécamines", layout="wide", page_icon="🛡️")

# --- STYLE CSS POUR LE BULLETIN DE PAIE ---
st.markdown("""
    <style>
    .bulletin-box {
        border: 2px solid #0F172A;
        padding: 30px;
        border-radius: 8px;
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .bulletin-header {
        text-align: center;
        color: #1E3A8A;
        margin-bottom: 5px;
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
        padding: 6px;
        text-align: left;
    }
    .bulletin-table td {
        padding: 6px;
        border-bottom: 1px dashed #CBD5E1;
    }
    .total-net {
        text-align: right;
        color: #1E3A8A;
        font-size: 1.4em;
        margin-top: 25px;
        font-weight: bold;
        border-top: 2px solid #0F172A;
        padding-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DES VARIABLES DE SESSION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

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
    st.markdown("<h2 style='text-align: center;'>🛡️ Authentification Portail RH - Gécamines</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        with st.form("login_form"):
            identifiant = st.text_input("Identifiant utilisateur :").strip()
            mot_de_passe = st.text_input("Mot de passe :", type="password")
            soumettre = st.form_submit_button("Se connecter", use_container_width=True)
            
            if soumettre:
                if identifiant == "admin" and mot_de_passe == "admin123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Administrateur"
                    st.session_state.current_user = "Direction RH"
                    st.success("Connexion réussie en tant qu'Administrateur.")
                    st.rerun()
                elif identifiant in st.session_state.employes["Login"].tolist() and mot_de_passe == "gcm2026":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Employé"
                    st.session_state.current_user = identifiant
                    st.success("Connexion réussie au portail employé.")
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")

# ==========================================
# APPLICATION PRINCIPALE (APRÈS CONNEXION)
# ==========================================
if not st.session_state.authenticated:
    ecran_connexion()
else:
    st.sidebar.markdown(f"**Utilisateur :** {st.session_state.current_user}")
    st.sidebar.markdown(f"**Rôle :** {st.session_state.user_role}")
    if st.sidebar.button("🔒 Se déconnecter", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.rerun()
        
    st.sidebar.markdown("---")

    # --- INTERFACE DIRECTION / RH ---
    if st.session_state.user_role == "Administrateur":
        menu = ["📈 Tableau de Bord", "👥 Gestion du Personnel", "🤖 Analyse IA des Présences", "💵 Calcul & Édition de la Paie"]
        choix = st.sidebar.selectbox("Menu Direction", menu)
        
        if choix == "📈 Tableau de Bord":
            st.subheader("📊 Pilotage Stratégique des Ressources Humaines")
            col1, col2, col3 = st.columns(3)
            col1.metric("Effectif Actif", len(st.session_state.employes))
            col2.metric("Masse Salariale Contractuelle", f"{st.session_state.employes['Salaire_Base'].sum():,.2f} $")
            col3.metric("Taux d'Assiduité Global", f"{round(st.session_state.employes['Presences'].mean() / 22 * 100, 1)} %")
            
            st.markdown("### Évolution et Répartition des Rémunérations")
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.bar(st.session_state.employes["Nom"], st.session_state.employes["Salaire_Base"], color="#0F172A")
            ax.set_ylabel("Salaire de Base ($)")
            st.pyplot(fig)

        elif choix == "👥 Gestion du Personnel":
            st.subheader("👥 Registre Matriculaire des Agents")
            t1, t2, t3 = st.tabs(["Ajouter un Agent", "Modifier Salaire / Poste", "Radiation"])
            
            with t1:
                with st.form("add_agent"):
                    nv_nom = st.text_input("Nom et Prénom :")
                    nv_poste = st.text_input("Intitulé du Poste :")
                    nv_sal = st.number_input("Salaire de base contractuel ($) :", min_value=0.0, value=1500.0)
                    nv_login = st.text_input("Nom d'utilisateur unique (login) :")
                    if st.form_submit_button("Inscrire l'employé"):
                        if nv_nom and nv_poste and nv_login:
                            nv_id = f"EMP{len(st.session_state.employes)+1:03d}"
                            new_row = {"ID": nv_id, "Nom": nv_nom, "Poste": nv_poste, "Salaire_Base": nv_sal, "Presences": 22, "Login": nv_login.lower().strip()}
                            st.session_state.employes = pd.concat([st.session_state.employes, pd.DataFrame([new_row])], ignore_index=True)
                            st.success("Nouvel agent enregistré dans la base de données.")
                            st.rerun()
            
            with t2:
                emp_sel = st.selectbox("Sélectionner l'agent à modifier :", st.session_state.employes["Nom"].tolist())
                idx = st.session_state.employes[st.session_state.employes["Nom"] == emp_sel].index[0]
                with st.form("edit_agent"):
                    ch_poste = st.text_input("Poste :", value=st.session_state.employes.at[idx, "Poste"])
                    ch_sal = st.number_input("Salaire de Base ($) :", value=float(st.session_state.employes.at[idx, "Salaire_Base"]))
                    ch_pres = st.slider("Présences mensuelles (sur 22j) :", 0, 22, int(st.session_state.employes.at[idx, "Presences"]))
                    if st.form_submit_button("Sauvegarder les modifications"):
                        st.session_state.employes.at[idx, "Poste"] = ch_poste
                        st.session_state.employes.at[idx, "Salaire_Base"] = ch_sal
                        st.session_state.employes.at[idx, "Presences"] = ch_pres
                        st.success("Mise à jour effectuée.")
                        st.rerun()
                        
            with t3:
                emp_sup = st.selectbox("Sélectionner l'agent à radier :", st.session_state.employes["Nom"].tolist(), key="del")
                if st.button("Confirmer la suppression définitive", type="primary"):
                    st.session_state.employes = st.session_state.employes[st.session_state.employes["Nom"] != emp_sup].reset_index(drop=True)
                    st.warning(f"Agent {emp_sup} retiré du système.")
                    st.rerun()

            st.dataframe(st.session_state.employes[["ID", "Nom", "Poste", "Salaire_Base", "Presences", "Login"]], use_container_width=True)

        elif choix == "🤖 Analyse IA des Présences":
            st.subheader("⏱️ Contrôle Analytique de l'Assiduité par l'IA")
            for _, row in st.session_state.employes.iterrows():
                if row["Presences"] < 21:
                    st.error(f"⚠️ **Alerte Risque d'Absentéisme ({row['Nom']})** : {22 - row['Presences']} jours manqués.")
                else:
                    st.success(f"✅ **Stabilité Assurée ({row['Nom']})** : Taux d'assiduité optimal.")

        elif choix == "💵 Calcul & Édition de la Paie":
            st.subheader("💵 Traitement de la Paie Légale & Génération du Bulletin")
            agent = st.selectbox("Sélectionner un collaborateur :", st.session_state.employes["Nom"].tolist())
            data = st.session_state.employes[st.session_state.employes["Nom"] == agent].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### ➕ Gains variables")
                sb = st.number_input("Salaire de base de calcul ($)", value=float(data["Salaire_Base"]))
                primes = st.number_input("Primes de rendement / fonction ($)", value=250.0)
                logement = st.number_input("Indemnités de logement & transport ($)", value=300.0)
            with col2:
                st.markdown("##### ➖ Calcul Fiscal & Social")
                jours_abs = max(0, 22 - int(data["Presences"]))
                retenue_abs = (sb / 22) * jours_abs
                st.warning(f"Retenue sur absence calculée ({jours_abs} jours) : -{retenue_abs:.2f} $")
                cnss_tx = st.number_input("Taux Cotisation Sociale CNSS (%)", value=5.0)
                ipr_tx = st.number_input("Taux Impôt sur le Revenu IPR (%)", value=15.0)
            
            brut_imposable = sb + primes + logement - retenue_abs
            retenue_cnss = brut_imposable * (cnss_tx / 100)
            retenue_ipr = brut_imposable * (ipr_tx / 100)
            salaire_net = brut_imposable - retenue_cnss - retenue_ipr
            
            st.markdown("---")
            
            bulletin_html = f"""
            <div class="bulletin-box">
                <h3 class="bulletin-header">GÉCAMINES SA</h3>
                <p style="text-align:center; font-size:11px; margin-top:0;">Siège Social - Lubumbashi, RDC</p>
                <hr style="border-top: 1px solid #000;">
                <table style="width:100%; font-size:13px;">
                    <tr><td><b>Matricule :</b> {data['ID']}</td><td><b>Période :</b> Juin 2026</td></tr>
                    <tr><td><b>Nom & Prénom :</b> {data['Nom']}</td><td><b>Poste :</b> {data['Poste']}</td></tr>
                    <tr><td><b>Jours de Présence :</b> {data['Presences']}/22j</td><td><b>Devise :</b> USD ($)</td></tr>
                </table>
                <table class="bulletin-table">
                    <thead>
                        <tr><th>Libellés des Rubriques</th><th style="text-align:right; color:white;">Gains</th><th style="text-align:right; color:white;">Retenues</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Salaire de base contractuel</td><td style="text-align:right;">{sb:,.2f}</td><td></td></tr>
                        <tr><td>Primes exceptionnelles</td><td style="text-align:right;">{primes:,.2f}</td><td></td></tr>
                        <tr><td>Indemnités Logement / Transport</td><td style="text-align:right;">{logement:,.2f}</td><td></td></tr>
                        <tr style="color:#C53030;"><td>Retenue pour absences non justifiées</td><td></td><td style="text-align: right;">{retenue_abs:,.2f}</td></tr>
                        <tr style="color:#C53030;"><td>Cotisation Sociale Ouvrière (CNSS)</td><td></td><td style="text-align: right;">{retenue_cnss:,.2f}</td></tr>
                        <tr style="color:#C53030;"><td>Impôt Professionnel sur le Revenu (IPR)</td><td></td><td style="text-align: right;">{retenue_ipr:,.2f}</td></tr>
                    </tbody>
                </table>
                <div class="total-net">NET À PAYER : {salaire_net:,.2f} $</div>
            </div>
            """
            st.markdown(bulletin_html, unsafe_allow_html=True)
            
            txt_bulletin = f"GÉCAMINES SA\nBulletin de paie - {data['Nom']}\nID: {data['ID']}\nPoste: {data['Poste']}\nNet à Payer : {salaire_net:,.2f} $"
            st.download_button("🖨️ Imprimer / Télécharger le bulletin", data=txt_bulletin, file_name=f"bulletin_{data['ID']}.txt", mime="text/plain")

    # --- INTERFACE PORTAIL EMPLOYÉ ---
    elif st.session_state.user_role == "Employé":
        st.subheader("🔒 Votre Espace Collaborateur Sécurisé")
        user_login = st.session_state.current_user
        info_perso = st.session_state.employes[st.session_state.employes["Login"] == user_login].iloc[0]
        
        st.info(f"Bienvenue **{info_perso['Nom']}**.")
        tab_infos, tab_bulletin = st.tabs(["📊 Mon Profil", "📄 Mon Bulletin de Paie"])
        
        with tab_infos:
            st.metric("Votre Poste", info_perso["Poste"])
            st.metric("Jours de présence enregistrés", f"{info_perso['Presences']} / 22 jours")
            
        with tab_bulletin:
            base_sal = float(info_perso["Salaire_Base"])
            p_abs = (base_sal / 22) * max(0, 22 - int(info_perso["Presences"]))
            brut = base_sal + 250.0 + 300.0 - p_abs
            cns = brut * 0.05
            ipr = brut * 0.15
            net_payer = brut - cns - ipr
            
            bulletin_emp_html = f"""
            <div class="bulletin-box">
                <h3 class="bulletin-header">GÉCAMINES SA</h3>
                <table style="width:100%; font-size:13px;">
                    <tr><td><b>Matricule :</b> {info_perso['ID']}</td><td><b>Période :</b> Juin 2026</td></tr>
                    <tr><td><b>Nom Complet :</b> {info_perso['Nom']}</td></tr>
                </table>
                <div class="total-net">NET À ENCAISSER : {net_payer:,.2f} $</div>
            </div>
            """
            st.markdown(bulletin_emp_html, unsafe_allow_html=True)
            
            txt_bulletin_emp = f"GÉCAMINES SA\nBulletin Perso - {info_perso['Nom']}\nNet à Encaisser : {net_payer:,.2f} $"
            st.download_button("🖨️ Télécharger mon bulletin", data=txt_bulletin_emp, file_name=f"mon_bulletin.txt", mime="text/plain")
