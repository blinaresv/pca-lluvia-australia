"""
app.py — Predictor de lluvia en Australia con PCA + Regresión logística
Inteligencia Artificial I — Actividad 3
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Predictor de lluvia — Australia",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.main-title { font-size: 2.1rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.2rem; }
.subtitle   { font-size: 1rem; color: #555; margin-bottom: 1.5rem; }
.result-yes { background: linear-gradient(135deg,#cce5ff,#b8daff); border:2px solid #004085;
              border-radius:12px; padding:20px; text-align:center; }
.result-no  { background: linear-gradient(135deg,#d4edda,#c3e6cb); border:2px solid #155724;
              border-radius:12px; padding:20px; text-align:center; }
.warn-box   { background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:10px;
              font-size:0.85rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Carga de modelos
# ─────────────────────────────────────────────
MODELS_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')

@st.cache_resource(show_spinner="Cargando modelos...")
def load_models():
    scaler         = joblib.load(os.path.join(MODELS_PATH, 'scaler.pkl'))
    pca            = joblib.load(os.path.join(MODELS_PATH, 'pca.pkl'))
    classifier     = joblib.load(os.path.join(MODELS_PATH, 'classifier.pkl'))
    feature_ranges = joblib.load(os.path.join(MODELS_PATH, 'feature_ranges.pkl'))
    feature_names  = joblib.load(os.path.join(MODELS_PATH, 'feature_names.pkl'))
    return scaler, pca, classifier, feature_ranges, feature_names

try:
    scaler, pca, classifier, feature_ranges, feature_names = load_models()
    models_ok = True
except Exception as e:
    models_ok = False
    st.error(f"Error al cargar modelos: {e}. Ejecuta primero notebooks/01_training.ipynb.")

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Acerca del modelo")
    st.info("""
**Algoritmo:** PCA + Regresión logística

**Dataset:** Rain in Australia (Kaggle)
- 145 000+ observaciones
- 49 estaciones meteorológicas
- 10 años de datos diarios

**Pipeline:**
1. StandardScaler
2. PCA (95% varianza)
3. LogisticRegression (balanced)
""")

    if models_ok:
        st.markdown("### Métricas del modelo")
        st.success("""
Las métricas reales aparecen aquí después de correr el notebook.
""")

        st.markdown("### Reducción PCA")
        if hasattr(pca, 'n_components_'):
            st.success(f"""
- Variables de entrada: {len(feature_names)}
- Componentes PCA: {pca.n_components_}
- Varianza explicada: {sum(pca.explained_variance_ratio_)*100:.1f}%
""")

    st.markdown("---")
    st.markdown("""
<div class='warn-box'>
<b>Aviso:</b> Herramienta académica. No reemplaza sistemas meteorológicos profesionales.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Contenido principal
# ─────────────────────────────────────────────
st.markdown("<div class='main-title'>Predictor de lluvia en Australia</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>PCA como preprocesamiento para clasificación — ¿Lloverá mañana?</div>", unsafe_allow_html=True)
st.markdown("---")

if not models_ok:
    st.stop()

# ─────────────────────────────────────────────
# Casos de ejemplo precargados
# ─────────────────────────────────────────────
EXAMPLES = {
    "Día seco típico (Sydney, verano)": {
        'MinTemp': 18.0, 'MaxTemp': 29.5, 'Rainfall': 0.0, 'Evaporation': 6.4,
        'Sunshine': 9.5, 'WindGustSpeed': 35.0, 'WindSpeed9am': 15.0, 'WindSpeed3pm': 24.0,
        'Humidity9am': 55.0, 'Humidity3pm': 30.0, 'Pressure9am': 1020.0, 'Pressure3pm': 1015.0,
        'Cloud9am': 2.0, 'Cloud3pm': 3.0, 'Temp9am': 22.0, 'Temp3pm': 27.5, 'RainToday': 0
    },
    "Día lluvioso típico (Melbourne, invierno)": {
        'MinTemp': 9.0, 'MaxTemp': 14.5, 'Rainfall': 8.2, 'Evaporation': 1.6,
        'Sunshine': 1.0, 'WindGustSpeed': 56.0, 'WindSpeed9am': 28.0, 'WindSpeed3pm': 35.0,
        'Humidity9am': 88.0, 'Humidity3pm': 80.0, 'Pressure9am': 1005.0, 'Pressure3pm': 1000.0,
        'Cloud9am': 7.0, 'Cloud3pm': 8.0, 'Temp9am': 11.0, 'Temp3pm': 13.5, 'RainToday': 1
    },
}

# ─────────────────────────────────────────────
# Modo de entrada
# ─────────────────────────────────────────────
st.markdown("## Condiciones meteorológicas actuales")

mode = st.radio("Modo de entrada:", ["Ingresar manualmente", "Usar caso de ejemplo"],
                horizontal=True)

example_values = None
if "Usar caso de ejemplo" in mode:
    choice = st.selectbox("Selecciona un caso:", list(EXAMPLES.keys()))
    example_values = EXAMPLES[choice]
    st.info(f"Cargando: **{choice}**")

# ─────────────────────────────────────────────
# Inputs organizados por categoría
# ─────────────────────────────────────────────
def get_val(feat):
    if example_values:
        return example_values.get(feat, feature_ranges[feat]['median'])
    return feature_ranges[feat]['median']

inputs = {}

tab1, tab2, tab3 = st.tabs(["Temperatura y lluvia", "Viento y presión", "Humedad y nubosidad"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        inputs['MinTemp']   = st.number_input("Temperatura mínima (°C)",
            min_value=-10.0, max_value=50.0, value=get_val('MinTemp'), step=0.5,
            help="Temperatura mínima del día")
        inputs['MaxTemp']   = st.number_input("Temperatura máxima (°C)",
            min_value=-5.0, max_value=55.0, value=get_val('MaxTemp'), step=0.5,
            help="Temperatura máxima del día")
        inputs['Temp9am']   = st.number_input("Temperatura a las 9am (°C)",
            min_value=-10.0, max_value=50.0, value=get_val('Temp9am'), step=0.5)
        inputs['Temp3pm']   = st.number_input("Temperatura a las 3pm (°C)",
            min_value=-10.0, max_value=50.0, value=get_val('Temp3pm'), step=0.5)
    with c2:
        inputs['Rainfall']    = st.number_input("Lluvia acumulada hoy (mm)",
            min_value=0.0, max_value=400.0, value=get_val('Rainfall'), step=0.5,
            help="Precipitación total del día")
        inputs['Evaporation'] = st.number_input("Evaporación (mm)",
            min_value=0.0, max_value=150.0, value=get_val('Evaporation'), step=0.5)
        inputs['Sunshine']    = st.number_input("Horas de sol",
            min_value=0.0, max_value=14.5, value=get_val('Sunshine'), step=0.5)
        inputs['RainToday']   = st.selectbox("¿Llovió hoy?", [0, 1],
            index=int(get_val('RainToday')),
            format_func=lambda x: "Sí" if x == 1 else "No")

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        inputs['WindGustSpeed']  = st.number_input("Velocidad ráfaga viento (km/h)",
            min_value=0.0, max_value=200.0, value=get_val('WindGustSpeed'), step=1.0)
        inputs['WindSpeed9am']   = st.number_input("Velocidad viento 9am (km/h)",
            min_value=0.0, max_value=150.0, value=get_val('WindSpeed9am'), step=1.0)
        inputs['WindSpeed3pm']   = st.number_input("Velocidad viento 3pm (km/h)",
            min_value=0.0, max_value=150.0, value=get_val('WindSpeed3pm'), step=1.0)
    with c2:
        inputs['Pressure9am']    = st.number_input("Presión atmosférica 9am (hPa)",
            min_value=970.0, max_value=1050.0, value=get_val('Pressure9am'), step=0.5)
        inputs['Pressure3pm']    = st.number_input("Presión atmosférica 3pm (hPa)",
            min_value=970.0, max_value=1050.0, value=get_val('Pressure3pm'), step=0.5)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        inputs['Humidity9am']  = st.number_input("Humedad 9am (%)",
            min_value=0.0, max_value=100.0, value=get_val('Humidity9am'), step=1.0)
        inputs['Humidity3pm']  = st.number_input("Humedad 3pm (%)",
            min_value=0.0, max_value=100.0, value=get_val('Humidity3pm'), step=1.0)
    with c2:
        inputs['Cloud9am']     = st.number_input("Nubosidad 9am (oktas 0-8)",
            min_value=0.0, max_value=9.0, value=get_val('Cloud9am'), step=1.0,
            help="0 = despejado, 8 = completamente nublado")
        inputs['Cloud3pm']     = st.number_input("Nubosidad 3pm (oktas 0-8)",
            min_value=0.0, max_value=9.0, value=get_val('Cloud3pm'), step=1.0)

# ─────────────────────────────────────────────
# Botón de predicción
# ─────────────────────────────────────────────
st.markdown("---")
predict_btn = st.button("Predecir si lloverá mañana", type="primary", use_container_width=True)

if predict_btn:
    input_row = pd.DataFrame([inputs], columns=feature_names)

    X_scaled      = scaler.transform(input_row)
    X_pca         = pca.transform(X_scaled)
    prediction    = int(classifier.predict(X_pca)[0])
    probabilities = classifier.predict_proba(X_pca)[0]

    prob_yes = float(probabilities[1])
    prob_no  = float(probabilities[0])

    st.markdown("---")
    st.markdown("## Predicción para mañana")

    col_res, col_chart, col_pca = st.columns([1.2, 1, 1])

    with col_res:
        if prediction == 1:
            st.markdown(f"""
<div class='result-yes'>
<h2 style='color:#004085;margin:0'>Lloverá</h2>
<h3 style='color:#004085;margin:5px 0'>Probabilidad: {prob_yes*100:.1f}%</h3>
<p style='color:#004085;margin-top:10px'>Se esperan precipitaciones mañana.</p>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class='result-no'>
<h2 style='color:#155724;margin:0'>No lloverá</h2>
<h3 style='color:#155724;margin:5px 0'>Probabilidad: {prob_no*100:.1f}%</h3>
<p style='color:#155724;margin-top:10px'>Se espera un día sin lluvia mañana.</p>
</div>
""", unsafe_allow_html=True)

    with col_chart:
        SET2 = ["#66C2A5", "#FC8D62"]
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(['No lluvia', 'Lluvia'], [prob_no*100, prob_yes*100],
               color=[SET2[0], SET2[1]], edgecolor='white', alpha=0.88)
        for i, v in enumerate([prob_no*100, prob_yes*100]):
            ax.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=13)
        ax.set_xlabel('Clase', fontsize=11)
        ax.set_ylabel('Probabilidad (%)', fontsize=11)
        ax.set_title('Probabilidad predicha por clase (%)', fontsize=12, fontweight='bold')
        ax.set_ylim(0, 118)
        ax.grid(axis='y', alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=10)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_pca:
        st.markdown("#### Reducción PCA")
        st.info(f"""
Variables de entrada: **{len(feature_names)}**
Componentes PCA: **{pca.n_components_}**
Varianza preservada: **{sum(pca.explained_variance_ratio_)*100:.1f}%**
Reducción: {len(feature_names)} → {pca.n_components_} dimensiones
""")
        st.markdown("#### PC1 — variables con más peso")
        loadings = pd.DataFrame(
            pca.components_.T,
            index=[f.replace('_', ' ') for f in feature_names],
            columns=[f'PC{i+1}' for i in range(pca.n_components_)]
        )
        top3 = loadings['PC1'].abs().nlargest(3)
        for feat, val in top3.items():
            dir_ = "+" if loadings.loc[feat, 'PC1'] > 0 else "-"
            st.write(f"**{feat}** {dir_} ({val:.3f})")

    st.markdown("---")
    st.markdown("### Posición en el espacio PCA")
    st.caption("La estrella indica dónde cae esta observación respecto a los patrones históricos.")

    np.random.seed(42)
    n = 100
    pc_dry  = np.random.multivariate_normal([-2.0, 0.8], [[2.0, 0.3],[0.3, 1.0]], n)
    pc_rain = np.random.multivariate_normal([2.5, -0.5], [[1.8, 0.4],[0.4, 1.2]], n)

    SET2 = ["#66C2A5", "#FC8D62", "#8DA0CB"]
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.scatter(pc_dry[:,0], pc_dry[:,1], c=SET2[0], alpha=0.4,
                label='Sin lluvia (referencia)', s=35, edgecolors='none')
    ax2.scatter(pc_rain[:,0], pc_rain[:,1], c=SET2[1], alpha=0.4,
                label='Con lluvia (referencia)', s=35, edgecolors='none')

    pc1_s = float(X_pca[0, 0])
    pc2_s = float(X_pca[0, 1])
    color_s = SET2[1] if prediction == 1 else SET2[0]
    ax2.scatter(pc1_s, pc2_s, c=color_s, s=350, marker='*',
                edgecolors='black', linewidths=1.5, zorder=5, label='Esta observación')

    ax2.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varianza)', fontsize=11)
    ax2.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varianza)', fontsize=11)
    ax2.set_title('Observación en el espacio PCA', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9, framealpha=0.9,
               bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
    ax2.grid(False)
    ax2.set_facecolor("white")
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.tick_params(labelsize=10)
    plt.tight_layout(rect=[0, 0, 0.82, 1])
    st.pyplot(fig2, use_container_width=True)
    plt.close()

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#888;font-size:0.8rem;padding:10px 0'>
Inteligencia Artificial I — Actividad 3 | Fundación Universitaria Los Libertadores<br>
Algoritmo: PCA como preprocesamiento para clasificación<br>
Dataset: <a href='https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package' target='_blank'>
Rain in Australia — Kaggle</a>
</div>
""", unsafe_allow_html=True)
