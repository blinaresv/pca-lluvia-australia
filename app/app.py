"""
app.py — RainCast Australia
PCA + Regresión Logística | Fundación Universitaria Los Libertadores 2024
v3.0: diseño limpio, sin emojis, imagenes via Unsplash, Open-Meteo API
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import joblib, requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Pagina ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RainCast Australia",
    page_icon="https://www.bom.gov.au/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F8FAFC; }

[data-testid="stSidebar"] {
    background: #1E293B;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #F1F5F9 !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: .08em; }

.hero-banner {
    position: relative; border-radius: 14px; overflow: hidden;
    height: 160px; margin-bottom: 1.4rem;
    background: linear-gradient(120deg, #0F2B5B 0%, #1565C0 100%);
    display: flex; flex-direction: column; justify-content: center; padding: 0 2rem;
}
.hero-banner::before {
    content: ''; position: absolute; inset: 0;
    background: url('https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=1200&q=60') center/cover no-repeat;
    opacity: .18;
}
.hero-banner * { position: relative; }
.hero-title { font-size: 22px; font-weight: 700; color: #F1F5F9; margin: 0 0 4px; }
.hero-sub   { font-size: 12px; color: #94A3B8; margin: 0; }

.card {
    background: #fff; border: 1px solid #E2E8F0;
    border-radius: 12px; padding: 14px 16px;
}
.metric-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px; }
.metric-box  {
    background: #F1F5F9; border-radius: 8px;
    padding: 8px 10px; text-align: center;
}
.metric-val { font-size: 15px; font-weight: 700; color: #1565C0; }
.metric-lbl { font-size: 9px; color: #64748B; text-transform: uppercase; letter-spacing: .07em; margin-top: 2px; }
.metric-box:hover .tooltip { display: block; }
.tooltip {
    display: none; position: absolute; bottom: 100%; left: 50%;
    transform: translateX(-50%); background: #1E293B; color: #F1F5F9;
    font-size: 10px; padding: 6px 10px; border-radius: 6px; width: 160px;
    text-align: left; z-index: 10; white-space: normal;
}

.sel-pill {
    display: inline-block; font-size: 11px; padding: 3px 10px;
    border-radius: 20px; background: #DBEAFE; color: #1565C0;
    border: 1px solid #BFDBFE; margin-right: 4px;
}

.w-card {
    background: #fff; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px 14px;
}
.w-val { font-size: 20px; font-weight: 700; color: #1E293B; }
.w-lbl { font-size: 10px; color: #64748B; margin-top: 3px; }

.result-rain {
    background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
    border: 1px solid #93C5FD; border-radius: 14px; padding: 1.2rem; text-align: center;
}
.result-dry  {
    background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
    border: 1px solid #86EFAC; border-radius: 14px; padding: 1.2rem; text-align: center;
}
.result-label { font-size: 15px; font-weight: 700; color: #1E293B; margin-top: 6px; }
.result-prob  { font-size: 30px; font-weight: 800; color: #1565C0; margin: 4px 0 2px; }
.result-sub   { font-size: 10px; color: #64748B; }

.algo-tag {
    display: inline-block; background: #1E293B; color: #94A3B8;
    font-size: 10px; padding: 2px 9px; border-radius: 4px; margin-right: 4px;
    font-family: monospace;
}

.pca-stat-row { display: flex; gap: 6px; margin-top: 8px; }
.pca-stat {
    background: #F1F5F9; border-radius: 8px; padding: 7px; text-align: center; flex: 1;
}
.pca-stat-v { font-size: 15px; font-weight: 700; color: #1565C0; }
.pca-stat-l { font-size: 9px; color: #64748B; text-transform: uppercase; letter-spacing: .06em; }

[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Ciudades ──────────────────────────────────────────────────────────────────
CITIES = {
    "Sydney":     {"lat":-33.87,"lon":151.21,"region":"NSW · Costa este",  "season":"Mar–Jun"},
    "Melbourne":  {"lat":-37.81,"lon":144.96,"region":"VIC · Sur",         "season":"May–Ago"},
    "Brisbane":   {"lat":-27.47,"lon":153.02,"region":"QLD · Subtropical", "season":"Feb–May"},
    "Perth":      {"lat":-31.95,"lon":115.86,"region":"WA · Suroeste",     "season":"May–Sep"},
    "Darwin":     {"lat":-12.46,"lon":130.84,"region":"NT · Tropical",     "season":"Nov–Abr"},
    "Adelaide":   {"lat":-34.93,"lon":138.60,"region":"SA · Mediterráneo", "season":"May–Ago"},
    "Canberra":   {"lat":-35.28,"lon":149.13,"region":"ACT · Interior",    "season":"Oct–Mar"},
    "Hobart":     {"lat":-42.88,"lon":147.33,"region":"TAS · Sur",         "season":"May–Sep"},
    "Cairns":     {"lat":-16.92,"lon":145.77,"region":"QLD · Tropical",    "season":"Dic–Mar"},
    "Gold Coast": {"lat":-28.00,"lon":153.43,"region":"QLD · Costa",       "season":"Feb–May"},
    "Newcastle":  {"lat":-32.93,"lon":151.78,"region":"NSW · Costa norte", "season":"Mar–Jun"},
    "Wollongong": {"lat":-34.42,"lon":150.89,"region":"NSW · Costa sur",   "season":"Abr–Jun"},
}

# ── Open-Meteo API ────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_weather(city: str):
    c = CITIES[city]
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={c['lat']}&longitude={c['lon']}"
        "&daily=precipitation_sum,sunshine_duration,et0_fao_evapotranspiration"
        "&hourly=temperature_2m,relativehumidity_2m,surface_pressure,windspeed_10m,windgusts_10m,cloudcover"
        "&timezone=auto&forecast_days=2&wind_speed_unit=kmh"
    )
    try:
        r = requests.get(url, timeout=8); r.raise_for_status()
        d = r.json()
        t = d["hourly"]["time"]
        daily = d["daily"]
        H_ = lambda h: next((i for i,x in enumerate(t) if x.endswith(f"T{h:02d}:00")), 0)
        T  = d["hourly"]["temperature_2m"]
        Hm = d["hourly"]["relativehumidity_2m"]
        P  = d["hourly"]["surface_pressure"]
        W  = d["hourly"]["windspeed_10m"]
        WG = d["hourly"]["windgusts_10m"]
        CC = d["hourly"]["cloudcover"]
        today_idx = [i for i,x in enumerate(t) if x.startswith(daily["time"][0])]
        avg = lambda arr: float(np.mean([arr[i] for i in today_idx]))
        rain_today = float(daily["precipitation_sum"][0] or 0)
        return {
            "MinTemp":       float(min(T[i] for i in today_idx)),
            "MaxTemp":       float(max(T[i] for i in today_idx)),
            "Rainfall":      rain_today,
            "Evaporation":   float(daily["et0_fao_evapotranspiration"][0] or 4.0),
            "Sunshine":      float((daily["sunshine_duration"][0] or 0)/3600),
            "WindGustSpeed": avg(WG),
            "WindSpeed9am":  float(W[H_(9)]),
            "WindSpeed3pm":  float(W[H_(15)]),
            "Humidity9am":   float(Hm[H_(9)]),
            "Humidity3pm":   float(Hm[H_(15)]),
            "Pressure9am":   float(P[H_(9)]),
            "Pressure3pm":   float(P[H_(15)]),
            "Cloud9am":      round(float(CC[H_(9)])/12.5),
            "Cloud3pm":      round(float(CC[H_(15)])/12.5),
            "Temp9am":       float(T[H_(9)]),
            "Temp3pm":       float(T[H_(15)]),
            "RainToday":     1 if rain_today > 1.0 else 0,
            "_temp9":  float(T[H_(9)]),
            "_hum3":   float(Hm[H_(15)]),
            "_wind":   avg(WG),
            "_rain":   rain_today,
        }
    except Exception:
        return None

# ── Modelos ───────────────────────────────────────────────────────────────────
MODELS_PATH = os.path.join(os.path.dirname(__file__), "..", "models")

@st.cache_resource(show_spinner="Cargando modelos…")
def load_models():
    s = joblib.load(os.path.join(MODELS_PATH, "scaler.pkl"))
    p = joblib.load(os.path.join(MODELS_PATH, "pca.pkl"))
    c = joblib.load(os.path.join(MODELS_PATH, "classifier.pkl"))
    fr = joblib.load(os.path.join(MODELS_PATH, "feature_ranges.pkl"))
    fn = joblib.load(os.path.join(MODELS_PATH, "feature_names.pkl"))
    return s, p, c, fr, fn

try:
    scaler, pca, classifier, feature_ranges, feature_names = load_models()
    models_ok = True
except Exception as e:
    models_ok = False
    st.error(f"Error cargando modelos: {e}")

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style='text-align:center;padding:1rem 0 .5rem'>
  <img src='https://images.unsplash.com/photo-1561484930-998b6a7b22e8?w=240&q=70'
       style='width:100%;border-radius:10px;opacity:.7'/>
  <div style='font-size:16px;font-weight:700;color:#F1F5F9;margin-top:.8rem'>RainCast</div>
  <div style='font-size:10px;color:#64748B'>Predictor de lluvia · Australia</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### Modelo")
    st.markdown("""
<span class='algo-tag'>PCA</span>
<span class='algo-tag'>LogisticRegression</span>
<span class='algo-tag'>scikit-learn</span>
""", unsafe_allow_html=True)

    if models_ok:
        st.divider()
        st.markdown("### Métricas del modelo")
        metrics = [("76.97%","Accuracy","De cada 100 dias, el modelo acierta en 77"),
                   ("0.849","ROC-AUC","Discriminacion entre lluvia y no lluvia. 1=perfecto"),
                   ("76.27%","Recall","De los dias que llovio, el modelo detecto el 76%"),
                   ("59.75%","F1-Score","Balance entre precision y recall")]
        cols = st.columns(2)
        for i,(v,l,tip) in enumerate(metrics):
            with cols[i%2]:
                st.markdown(f"""
<div class='metric-box' style='position:relative'>
  <div class='metric-val'>{v}</div>
  <div class='metric-lbl'>{l}</div>
</div>
""", unsafe_allow_html=True)
                st.caption(tip)

        st.divider()
        st.markdown("### Reducción de variables")
        st.markdown(f"""
<div style='background:#0F172A;border-radius:8px;padding:10px 12px;margin-top:4px'>
  <span style='font-size:16px;font-weight:700;color:#7DD3FC'>17 → {pca.n_components_}</span>
  <span style='font-size:10px;color:#475569;margin-left:6px'>componentes</span>
  <div style='font-size:10px;color:#475569;margin-top:3px'>{sum(pca.explained_variance_ratio_)*100:.1f}% de informacion preservada</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='font-size:10px;color:#475569;line-height:1.6'>
Dataset: Rain in Australia<br>
145 000+ observaciones · 49 estaciones<br>
2007–2017<br>
Fuente: <a href='https://www.bom.gov.au/climate/data/' style='color:#60A5FA'>Bureau of Meteorology</a>
</div>
""", unsafe_allow_html=True)
    st.markdown("""
<div style='background:#1E2D1E;border:1px solid #166534;border-radius:8px;padding:8px 10px;font-size:10px;color:#86EFAC;margin-top:.8rem'>
  Herramienta académica. No reemplaza sistemas meteorológicos profesionales.
</div>
""", unsafe_allow_html=True)

# ── MAIN ──────────────────────────────────────────────────────────────────────
# Hero banner
st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>Predicción de lluvia en Australia</div>
  <div class='hero-sub'>PCA + Regresión Logística &nbsp;·&nbsp; Datos en tiempo real vía Open-Meteo &nbsp;·&nbsp; Fuente: Bureau of Meteorology</div>
</div>
""", unsafe_allow_html=True)

if not models_ok:
    st.stop()

# Modo de entrada
mode = st.radio(
    "Modo de entrada",
    ["Datos reales de una ciudad", "Ingresar manualmente", "Caso de ejemplo"],
    horizontal=True, label_visibility="collapsed"
)

inputs = {}; api_data = None

# ── MODO API ──────────────────────────────────────────────────────────────────
if "ciudad" in mode or "reales" in mode:
    st.markdown("#### Seleccionar ciudad australiana")
    selected = st.selectbox(
        "Ciudad",
        list(CITIES.keys()),
        format_func=lambda c: f"{c}  —  {CITIES[c]['region']}  ·  Lluvia: {CITIES[c]['season']}",
        label_visibility="collapsed"
    )
    st.markdown(f"<span class='sel-pill'>{selected}</span><span class='sel-pill'>{CITIES[selected]['region']}</span><span class='sel-pill'>Temporada: {CITIES[selected]['season']}</span>", unsafe_allow_html=True)
    st.write("")

    with st.spinner(f"Consultando Open-Meteo para {selected}…"):
        api_data = fetch_weather(selected)

    if api_data:
        st.success(f"Datos obtenidos correctamente para **{selected}**")
        c1,c2,c3,c4 = st.columns(4)
        for col, val, lbl in [
            (c1, f"{api_data['Temp9am']:.1f} °C","Temperatura 9am"),
            (c2, f"{api_data['Humidity3pm']:.0f} %","Humedad 3pm"),
            (c3, f"{api_data['WindGustSpeed']:.0f} km/h","Rafaga viento"),
            (c4, f"{api_data['Rainfall']:.1f} mm","Lluvia hoy"),
        ]:
            with col:
                st.markdown(f"<div class='w-card'><div class='w-val'>{val}</div><div class='w-lbl'>{lbl}</div></div>", unsafe_allow_html=True)
        st.write("")
        inputs = {k:v for k,v in api_data.items() if not k.startswith("_")}
    else:
        st.warning("No se pudo conectar con la API. Cambia a modo manual.")

# ── MODO MANUAL ───────────────────────────────────────────────────────────────
elif "manual" in mode:
    def med(f): return float(feature_ranges[f]["median"])
    with st.expander("Temperatura y precipitacion", expanded=True):
        c1,c2 = st.columns(2)
        with c1:
            inputs["MinTemp"]   = st.number_input("Temp. minima (°C)", -10.0, 50.0, med("MinTemp"), .5)
            inputs["MaxTemp"]   = st.number_input("Temp. maxima (°C)", -5.0, 55.0, med("MaxTemp"), .5)
            inputs["Temp9am"]   = st.number_input("Temp. 9am (°C)", -10.0, 50.0, med("Temp9am"), .5)
            inputs["Temp3pm"]   = st.number_input("Temp. 3pm (°C)", -10.0, 50.0, med("Temp3pm"), .5)
        with c2:
            inputs["Rainfall"]    = st.number_input("Lluvia hoy (mm)", 0.0, 400.0, med("Rainfall"), .5)
            inputs["Evaporation"] = st.number_input("Evaporacion (mm)", 0.0, 150.0, med("Evaporation"), .5)
            inputs["Sunshine"]    = st.number_input("Horas de sol", 0.0, 14.5, med("Sunshine"), .5)
            inputs["RainToday"]   = st.selectbox("Llovio hoy", [0,1], format_func=lambda x:"Si" if x else "No")
    with st.expander("Viento y presion"):
        c1,c2 = st.columns(2)
        with c1:
            inputs["WindGustSpeed"] = st.number_input("Rafaga (km/h)", 0.0, 200.0, med("WindGustSpeed"), 1.0)
            inputs["WindSpeed9am"]  = st.number_input("Viento 9am (km/h)", 0.0, 150.0, med("WindSpeed9am"), 1.0)
            inputs["WindSpeed3pm"]  = st.number_input("Viento 3pm (km/h)", 0.0, 150.0, med("WindSpeed3pm"), 1.0)
        with c2:
            inputs["Pressure9am"] = st.number_input("Presion 9am (hPa)", 970.0, 1050.0, med("Pressure9am"), .5)
            inputs["Pressure3pm"] = st.number_input("Presion 3pm (hPa)", 970.0, 1050.0, med("Pressure3pm"), .5)
    with st.expander("Humedad y nubosidad"):
        c1,c2 = st.columns(2)
        with c1:
            inputs["Humidity9am"] = st.number_input("Humedad 9am (%)", 0.0, 100.0, med("Humidity9am"), 1.0)
            inputs["Humidity3pm"] = st.number_input("Humedad 3pm (%)", 0.0, 100.0, med("Humidity3pm"), 1.0)
        with c2:
            inputs["Cloud9am"] = st.number_input("Nubosidad 9am (oktas)", 0.0, 9.0, med("Cloud9am"), 1.0)
            inputs["Cloud3pm"] = st.number_input("Nubosidad 3pm (oktas)", 0.0, 9.0, med("Cloud3pm"), 1.0)

# ── MODO EJEMPLO ──────────────────────────────────────────────────────────────
else:
    EXAMPLES = {
        "Dia seco — Sydney (verano)": {
            "MinTemp":18.0,"MaxTemp":29.5,"Rainfall":0.0,"Evaporation":6.4,
            "Sunshine":9.5,"WindGustSpeed":35.0,"WindSpeed9am":15.0,"WindSpeed3pm":24.0,
            "Humidity9am":55.0,"Humidity3pm":30.0,"Pressure9am":1020.0,"Pressure3pm":1015.0,
            "Cloud9am":2.0,"Cloud3pm":3.0,"Temp9am":22.0,"Temp3pm":27.5,"RainToday":0},
        "Dia lluvioso — Melbourne (invierno)": {
            "MinTemp":9.0,"MaxTemp":14.5,"Rainfall":8.2,"Evaporation":1.6,
            "Sunshine":1.0,"WindGustSpeed":56.0,"WindSpeed9am":28.0,"WindSpeed3pm":35.0,
            "Humidity9am":88.0,"Humidity3pm":80.0,"Pressure9am":1005.0,"Pressure3pm":1000.0,
            "Cloud9am":7.0,"Cloud3pm":8.0,"Temp9am":11.0,"Temp3pm":13.5,"RainToday":1},
        "Monzon — Darwin (noviembre)": {
            "MinTemp":24.0,"MaxTemp":33.0,"Rainfall":12.4,"Evaporation":7.1,
            "Sunshine":3.0,"WindGustSpeed":63.0,"WindSpeed9am":22.0,"WindSpeed3pm":30.0,
            "Humidity9am":90.0,"Humidity3pm":82.0,"Pressure9am":1007.0,"Pressure3pm":1003.0,
            "Cloud9am":7.0,"Cloud3pm":8.0,"Temp9am":27.5,"Temp3pm":31.0,"RainToday":1},
    }
    choice = st.selectbox("Escenario", list(EXAMPLES.keys()))
    inputs = EXAMPLES[choice]
    st.info(f"Escenario: **{choice}**")

# ── PREDICCION ────────────────────────────────────────────────────────────────
st.divider()
predict_btn = st.button("Predecir si lloverá mañana", type="primary", use_container_width=True)

if predict_btn and inputs:
    row = pd.DataFrame([inputs], columns=feature_names)
    Xs  = scaler.transform(row)
    Xp  = pca.transform(Xs)
    pred = int(classifier.predict(Xp)[0])
    probs = classifier.predict_proba(Xp)[0]
    p_rain, p_dry = float(probs[1]), float(probs[0])

    st.divider()
    st.markdown("## Resultado")
    col_res, col_chart = st.columns([1,1], gap="large")

    with col_res:
        if pred == 1:
            st.markdown(f"""
<div class='result-rain'>
  <div style='font-size:28px;font-weight:800;color:#1565C0;margin-bottom:6px'>Lluvia esperada</div>
  <div class='result-prob'>{p_rain*100:.1f}%</div>
  <div class='result-sub'>probabilidad de lluvia mañana</div>
  <div style='font-size:10px;color:#64748B;margin-top:12px'>
    El modelo detecta condiciones propicias para precipitaciones.<br>
    Recall: 76.27% — captura la mayoría de días lluviosos.
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class='result-dry'>
  <div style='font-size:28px;font-weight:800;color:#166534;margin-bottom:6px'>Dia seco esperado</div>
  <div class='result-prob' style='color:#166534'>{p_dry*100:.1f}%</div>
  <div class='result-sub'>probabilidad de dia sin lluvia</div>
  <div style='font-size:10px;color:#64748B;margin-top:12px'>
    Las condiciones actuales sugieren un dia sin precipitaciones.<br>
    Accuracy general: 76.97%.
  </div>
</div>""", unsafe_allow_html=True)

    with col_chart:
        fig, ax = plt.subplots(figsize=(5.5, 4), facecolor="white")
        ax.set_facecolor("white")
        bars = ax.bar(["Sin lluvia","Con lluvia"], [p_dry*100, p_rain*100],
                      color=["#2E7D32","#1565C0"], width=0.45, edgecolor="white")
        for bar, v in zip(bars, [p_dry*100, p_rain*100]):
            ax.text(bar.get_x()+bar.get_width()/2, v+1.5,
                    f"{v:.1f}%", ha="center", va="bottom", fontsize=13, fontweight="bold")
        ax.set_ylim(0, 110)
        ax.set_ylabel("Probabilidad (%)")
        ax.set_title("Probabilidad por clase", fontsize=12, fontweight="bold")
        ax.yaxis.grid(True, color="#E0E0E0", linewidth=0.6)
        ax.set_axisbelow(True)
        for sp in ["top","right"]:
            ax.spines[sp].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # Tabs de análisis
    st.markdown("### Análisis de componentes")
    tab_dim, tab_pesos = st.tabs(["Reducción dimensional", "Peso de variables"])

    with tab_dim:
        st.markdown("""
Variables con alta correlacion como **Temp9am / Temp3pm** (r = 0.97) y **Presion 9am / 3pm** (r = 0.96)
aportan informacion redundante. El modelo las agrupa internamente para evitar que repitan su peso.
""")
        st.markdown(f"""
<div class='pca-stat-row'>
  <div class='pca-stat'><div class='pca-stat-v'>17</div><div class='pca-stat-l'>Variables leidas</div></div>
  <div class='pca-stat'><div class='pca-stat-v'>{pca.n_components_}</div><div class='pca-stat-l'>Componentes</div></div>
  <div class='pca-stat'><div class='pca-stat-v'>{sum(pca.explained_variance_ratio_)*100:.1f}%</div><div class='pca-stat-l'>Informacion preservada</div></div>
</div>
""", unsafe_allow_html=True)

    with tab_pesos:
        loadings = pd.DataFrame(pca.components_.T,
                                index=[f.replace("_"," ") for f in feature_names],
                                columns=[f"PC{i+1}" for i in range(pca.n_components_)])
        top5 = loadings["PC1"].abs().nlargest(5)
        fig2, ax2 = plt.subplots(figsize=(7, 3), facecolor="white")
        ax2.set_facecolor("white")
        colors = ["#1565C0" if loadings.loc[f,"PC1"]>0 else "#E65100" for f in top5.index]
        ax2.barh(list(top5.index), [loadings.loc[f,"PC1"] for f in top5.index],
                 color=colors, edgecolor="white")
        ax2.set_xlabel("Peso en PC1")
        ax2.set_title("Variables con mayor influencia en PC1", fontweight="bold", fontsize=11)
        ax2.axvline(0, color="#94A3B8", lw=0.8)
        for sp in ["top","right"]:
            ax2.spines[sp].set_visible(False)
        ax2.xaxis.grid(True, color="#E0E0E0", lw=0.6)
        ax2.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close()
        st.caption("Azul = relacion positiva con PC1 | Naranja = relacion negativa")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center;color:#94A3B8;font-size:10px;padding:6px 0'>
  Inteligencia Artificial I &nbsp;|&nbsp; Fundación Universitaria Los Libertadores 2024 &nbsp;|&nbsp;
  Dataset: <a href='https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package' style='color:#60A5FA'>Rain in Australia — Kaggle</a> &nbsp;|&nbsp;
  Fuente primaria: <a href='https://www.bom.gov.au/climate/data/' style='color:#60A5FA'>Bureau of Meteorology</a> &nbsp;|&nbsp;
  Datos en tiempo real: <a href='https://open-meteo.com' style='color:#60A5FA'>Open-Meteo API</a>
</div>
""", unsafe_allow_html=True)
