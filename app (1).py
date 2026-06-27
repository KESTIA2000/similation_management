!pip install streamlit matplotlib numpy
!streamlit run app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Gécamines - Simulateur de Performance", layout="wide")

st.title("📊 Simulateur de Performance Prédictive — Gécamines")
st.markdown("""
Cette application permet de simuler l'impact des choix managériaux sur le Résultat Net de la Gécamines à l'horizon 2028, 
en se basant sur les modèles de la chaîne de valeur.
""")

# --- BARRE LATÉRALE : PARAMÈTRES INTERACTIFS ---
st.sidebar.header("⚙️ Paramètres du Scénario de Réforme")
st.sidebar.markdown("Modifiez les leviers managériaux pour simuler la trajectoire :")

croissance_ca = st.sidebar.slider("Hausse annuelle du CA (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.5) / 100
baisse_cons = st.sidebar.slider("Réduction annuelle des consommations (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5) / 100

# --- SIMULATION DES DONNÉES ---
annees = ['2024 (Réel)', '2025 (Prév.)', '2026 (Prév.)', '2027 (Prév.)', '2028 (Prév.)']
x = np.arange(len(annees))

rn_statu_quo = [-18.1, -22.3, -25.9, -29.2, -32.1]

ca_init = 395.8
cons_init = 290.2
cf_init = 123.7

rn_reforme = [-18.1]
ca_temp, cons_temp, cf_temp = ca_init, cons_init, cf_init

for i in range(1, 5):
    ca_temp *= (1 + croissance_ca)
    cons_temp *= (1 - baisse_cons)
    cf_temp *= 1.01  
    va_temp = ca_temp - cons_temp
    rn_reforme.append(va_temp - cf_temp)

# --- AFFICHAGE DES RÉSULTATS ---
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Résultat Net Prévu en 2028 (Statu Quo)", value="-32.1 M$", delta="-14.0 M$ (Dégradation)")
with col2:
    gain_final = rn_reforme[-1]
    st.metric(label="Résultat Net Prévu en 2028 (Réforme)", value=f"{gain_final:.1f} M$", delta=f"+{gain_final+18.1:.1f} M$ (Amélioration)")

# --- TRACÉ DU GRAPHIQUE ---
fig, ax = plt.subplots(figsize=(11, 5.5), facecolor='#f8f9fa')
ax.set_facecolor('#ffffff')

plt.plot(annees, rn_statu_quo, marker='o', linewidth=3, color='#dc3545', label='Scénario A : Statu Quo (Management Directif)')
plt.plot(annees, rn_reforme, marker='s', linewidth=3, color='#28a745', label='Scénario B : Réforme Managériale (MPO & Participatif)')

plt.axhline(0, color='gray', linestyle='--', linewidth=1)

for i in range(len(annees)):
    plt.annotate(f"{rn_statu_quo[i]:.1f} M$", (x[i], rn_statu_quo[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='#8b0000', weight='bold')
    plt.annotate(f"{rn_reforme[i]:.1f} M$", (x[i], rn_reforme[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1e5631', weight='bold')

plt.title("Évolution Comparée et Prédictive du Résultat Net (Millions USD)", fontsize=12, weight='bold', pad=15)
plt.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')
plt.ylim(-40, max(max(rn_reforme)+10, 25))
plt.legend(loc='upper left', frameon=True)

st.pyplot(fig)
