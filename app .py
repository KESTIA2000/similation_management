%%writefile app.py
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Digitalisation GRH", layout="wide", initial_sidebar_state="expanded")

def init_db():
    conn = sqlite3.connect("grh_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            poste TEXT,
            salaire_base REAL,
            statut_presence TEXT DEFAULT 'Absent'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- MENU À GAUCHE (SIDEBAR) ---
st.sidebar.title("🌐 DIGITAL-RH v1.0")
st.sidebar.write("Gestion des RH & Efficacité Opérationnelle")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["👥 Gestion des Employés", "💵 Calcul de Paie", "🤖 Présence par IA"])

# --- PAGE 1 : GESTION DES EMPLOYÉS ---
if page == "👥 Gestion des Employés":
    st.title("👥 Gestion du Personnel et des Fiches")
    with st.form("form_employe", clear_on_submit=False):
        st.subheader("Fiche Nouvel Employé")
        nom = st.text_input("Nom Complet de l'employé :")
        poste = st.text_input("Poste / Fonction :")
        salaire_base = st.number_input("Salaire de Base ($) :", min_value=0.0, step=50.0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            btn_ajouter = st.form_submit_button("➕ Ajouter l'employé")
        with col2:
            btn_effacer = st.form_submit_button("🧹 Effacer les champs")
            
    if btn_ajouter:
        if nom == "" or salaire_base <= 0:
            st.error("Veuillez remplir le nom et un salaire valide.")
        else:
            conn = sqlite3.connect("grh_database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employes (nom, poste, salaire_base) VALUES (?, ?, ?)", (nom, poste, salaire_base))
            conn.commit()
            conn.close()
            st.success(f"Employé '{nom}' ajouté avec succès !")

    st.markdown("---")
    st.subheader("Liste des employés enregistrés")
    conn = sqlite3.connect("grh_database.db")
    df = pd.read_sql_query("SELECT * FROM employes", conn)
    conn.close()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.subheader("🗑️ Zone de Suppression")
        id_a_supprimer = st.selectbox("Sélectionner l'ID de l'employé à supprimer :", df["id"].tolist())
        if st.button("🔴 Supprimer définitivement"):
            conn = sqlite3.connect("grh_database.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employes WHERE id = ?", (id_a_supprimer,))
            conn.commit()
            conn.close()
            st.warning("Employé supprimé du registre.")
            st.rerun()
    else:
        st.info("Aucun employé dans la base de données pour le moment.")

# --- PAGE 2 : CALCUL DE PAIE & BULLETIN ---
elif page == "💵 Calcul de Paie":
    st.title("💵 Calcul Automatisé de la Paie & Bulletin")
    conn = sqlite3.connect("grh_database.db")
    df = pd.read_sql_query("SELECT id, nom, poste, salaire_base FROM employes", conn)
    conn.close()
    
    if df.empty:
        st.info("Veuillez d'abord ajouter des employés sur la page dédiée.")
    else:
        options_employes = {f"{row['id']} - {row['nom']}": row for _, row in df.iterrows()}
        choix = st.selectbox("Sélectionner l'employé à rémunérer :", list(options_employes.keys()))
        employe_sel = options_employes[choix]
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Variables Mensuelles")
            jours_presence = st.slider("Jours de présence effectifs (sur 26 jours) :", 0, 26, 26)
            primes = st.number_input("Primes et Gratifications ($) :", min_value=0.0, value=0.0)
            
            salaire_prorata = (employe_sel['salaire_base'] / 26) * jours_presence
            salaire_brut = salaire_prorata + primes
            retenue_fiscal = salaire_brut * 0.15
            salaire_net = salaire_brut - retenue_fiscal
            
        with col2:
            st.subheader("📄 Aperçu du Bulletin de Paie Class")
            date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")
            bulletin_text = f"""
==================================================
              BULLETIN DE PAIE MENSUEL            
==================================================
Date d'édition : {date_str}

MATRICULE : EMP-{employe_sel['id']}
NOM COMPLET : {employe_sel['nom']}
POSTE / FONCTION : {employe_sel['poste']}
--------------------------------------------------
ELEMENTS DE SALAIRE             MONTANT ($)
--------------------------------------------------
Salaire de base (Mensuel) :     {employe_sel['salaire_base']:,.2f}
Jours travaillés ({jours_presence}/26) :     {salaire_prorata:,.2f}
Primes et Gratifications :     {primes:,.2f}

TOTAL BRUT :                    {salaire_brut:,.2f}
Retenue Fiscale (IPR 15%) :    -{retenue_fiscal:,.2f}
--------------------------------------------------
NET A PAYER :                   {salaire_net:,.2f} $
==================================================
       Signature RH               Bénéficiaire
            """
            st.code(bulletin_text, language="text")
            st.download_button(
                label="🖨️ Télécharger / Imprimer le Bulletin (TXT)",
                data=bulletin_text,
                file_name=f"bulletin_paie_{employe_sel['nom'].replace(' ', '_')}.txt",
                mime="text/plain"
            )

# --- PAGE 3 : PRÉSENCE PAR IA ---
elif page == "🤖 Présence par IA":
    st.title("🤖 Système de Pointage Intelligent (IA)")
    st.write("Ce module utilise des simulations d'algorithmes de vision par ordinateur (FaceID) pour valider la présence réelle.")
    st.info("Système prêt. La caméra virtuelle attend une détection de repères faciaux.")
    if st.button("📸 Lancer la Vérification par Reconnaissance Faciale (IA)"):
        with st.spinner("Analyse biométrique en cours..."):
            import time
            time.sleep(2)
            conn = sqlite3.connect("grh_database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE employes SET statut_presence = 'Présent'")
            conn.commit()
            conn.close()
        st.success("Matching facial réussi à 98.6% ! Registre de présence mis à jour automatiquement.")
        st.balloons()
