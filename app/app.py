"""
app.py — RainCast Australia
PCA + Regresión Logística | Fundación Universitaria Los Libertadores 2024
v4.0: diseño editorial, paleta slate/copper, layout asimétrico
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

# ── Página ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RainCast Australia",
    page_icon="https://www.bom.gov.au/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp { background: #0C1219; }

[data-testid="stSidebar"] {
    background: #0A0F16;
    border-right: 1px solid #1A2535;
}
[data-testid="stSidebar"] * { color: #94A3B8 !important; }
[data-testid="stSidebar"] strong { color: #E2E8F0 !important; }

/* Ocultar toolbar matplotlib */
[data-testid="stToolbar"] { display: none; }

/* Encabezado principal */
.rh-wrapper {
    display: flex;
    align-items: stretch;
    gap: 0;
    margin-bottom: 2rem;
    border: 1px solid #1A2535;
    border-radius: 14px;
    overflow: hidden;
    background: #0F1923;
}
.rh-accent {
    width: 5px;
    background: linear-gradient(180deg, #EA580C 0%, #C2410C 100%);
    flex-shrink: 0;
}
.rh-content {
    padding: 2rem 2rem 1.6rem;
    flex: 1;
}
.rh-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: #EA580C;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.rh-title {
    font-size: 2rem;
    font-weight: 800;
    color: #F1F5F9;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin: 0 0 0.4rem;
}
.rh-sub {
    font-size: 13px;
    color: #475569;
    margin: 0;
}
.rh-source {
    font-size: 11px;
    color: #334155;
    margin-top: 0.6rem;
    font-style: italic;
}

/* Chips de modo */
div[data-testid="stRadio"] > div {
    gap: 10px;
    flex-direction: row;
    flex-wrap: wrap;
}
div[data-testid="stRadio"] label {
    background: #0F1923;
    border: 1px solid #1A2535;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    color: #94A3B8;
    cursor: pointer;
    transition: all 0.2s;
}
div[data-testid="stRadio"] label:hover {
    border-color: #EA580C;
    color: #F1F5F9;
}

/* Botones de ciudad */
.city-grid { display: flex; flex-wrap: wrap; gap: 8px; margin: 1rem 0; }
.city-btn {
    background: #0F1923;
    border: 1px solid #1A2535;
    border-radius: 8px;
    padding: 8px 14px;
    color: #94A3B8;
    font-size: 12px;
    font-family: 'Outfit', sans-serif;
    cursor: pointer;
    transition: all 0.18s;
    line-height: 1.3;
}
.city-btn:hover { border-color: #EA580C; color: #F1F5F9; }
.city-btn.active {
    background: #1C0F06;
    border-color: #EA580C;
    color: #FB923C;
}
.city-btn .city-name { font-weight: 600; display: block; }
.city-btn .city-region { font-size: 10px; color: #475569; display: block; }
.city-btn.active .city-region { color: #7C2D12; }

/* Tarjetas del clima actual */
.weather-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin: 1rem 0;
}
.weather-card {
    background: #0F1923;
    border: 1px solid #1A2535;
    border-radius: 10px;
    padding: 14px 16px;
}
.weather-val {
    font-size: 20px;
    font-weight: 700;
    color: #F1F5F9;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
}
.weather-lbl {
    font-size: 10px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* Expanders */
[data-testid="stExpander"] {
    background: #0F1923 !important;
    border: 1px solid #1A2535 !important;
    border-radius: 10px !important;
    margin-bottom: 8px;
}
[data-testid="stExpander"] summary {
    font-size: 13px !important;
    color: #94A3B8 !important;
    font-weight: 500 !important;
}

/* Botón de predicción */
.stButton > button[kind="primary"] {
    background: #EA580C !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    color: #fff !important;
    height: 52px !important;
    transition: all 0.18s !important;
}
.stButton > button[kind="primary"]:hover {
    background: #C2410C !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"]:active {
    transform: scale(0.98) translateY(0px);
}

/* Resultado */
.result-block {
    background: #0F1923;
    border: 1px solid #1A2535;
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
}
.result-block.rain {
    border-color: #0369A1;
    background: linear-gradient(135deg, #0C1F30 0%, #0F1923 100%);
}
.result-block.dry {
    border-color: #065F46;
    background: linear-gradient(135deg, #0A1F16 0%, #0F1923 100%);
}
.result-pct {
    font-size: 72px;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.5rem 0;
}
.result-pct.rain { color: #38BDF8; }
.result-pct.dry  { color: #34D399; }
.result-verdict {
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.result-verdict.rain { color: #7DD3FC; }
.result-verdict.dry  { color: #6EE7B7; }
.result-note {
    font-size: 11px;
    color: #334155;
    margin-top: 0.8rem;
    line-height: 1.5;
}

/* Tabs análisis */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1A2535 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border: none !important;
    padding: 10px 18px !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #FB923C !important;
    border-bottom: 2px solid #EA580C !important;
}

/* Stat pills en PCA */
.pca-row { display: flex; gap: 8px; margin: 1rem 0; }
.pca-pill {
    background: #0F1923;
    border: 1px solid #1A2535;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: center;
    flex: 1;
}
.pca-val {
    font-size: 18px;
    font-weight: 700;
    color: #FB923C;
    font-family: 'JetBrains Mono', monospace;
}
.pca-lbl {
    font-size: 9px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 3px;
}

/* Sidebar métricas */
.sb-metric {
    background: #0F1923;
    border: 1px solid #1A2535;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
}
.sb-val { font-size: 17px; font-weight: 700; color: #FB923C; font-family: 'JetBrains Mono', monospace; }
.sb-lbl { font-size: 9px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }
.sb-tip { font-size: 10px; color: #334155; margin-top: 3px; line-height: 1.4; }

/* Divider */
hr { border-color: #1A2535 !important; }

/* Inputs número */
.stNumberInput input {
    background: #0F1923 !important;
    border: 1px solid #1A2535 !important;
    color: #E2E8F0 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
}
.stSelectbox > div > div {
    background: #0F1923 !important;
    border: 1px solid #1A2535 !important;
    color: #E2E8F0 !important;
    border-radius: 8px !important;
}

/* Footer */
.footer-bar {
    text-align: center;
    color: #1E2D3D;
    font-size: 11px;
    padding: 12px 0 4px;
    border-top: 1px solid #1A2535;
    margin-top: 2rem;
}
.footer-bar a { color: #334155; text-decoration: none; }
.footer-bar a:hover { color: #EA580C; }
</style>
""", unsafe_allow_html=True)

# ── Ciudades ──────────────────────────────────────────────────────────────────
CITIES = {
    "Sydney":     {"lat":-33.87,"lon":151.21,"region":"NSW · Costa este",  "season":"Mar-Jun"},
    "Melbourne":  {"lat":-37.81,"lon":144.96,"region":"VIC · Sur",         "season":"May-Ago"},
    "Brisbane":   {"lat":-27.47,"lon":153.02,"region":"QLD · Subtropical", "season":"Feb-May"},
    "Perth":      {"lat":-31.95,"lon":115.86,"region":"WA · Suroeste",     "season":"May-Sep"},
    "Darwin":     {"lat":-12.46,"lon":130.84,"region":"NT · Tropical",     "season":"Nov-Abr"},
    "Adelaide":   {"lat":-34.93,"lon":138.60,"region":"SA · Mediterráneo", "season":"May-Ago"},
    "Canberra":   {"lat":-35.28,"lon":149.13,"region":"ACT · Interior",    "season":"Oct-Mar"},
    "Hobart":     {"lat":-42.88,"lon":147.33,"region":"TAS · Sur",         "season":"May-Sep"},
    "Cairns":     {"lat":-16.92,"lon":145.77,"region":"QLD · Tropical",    "season":"Dic-Mar"},
    "Gold Coast": {"lat":-28.00,"lon":153.43,"region":"QLD · Costa",       "season":"Feb-May"},
    "Newcastle":  {"lat":-32.93,"lon":151.78,"region":"NSW · Costa norte", "season":"Mar-Jun"},
    "Wollongong": {"lat":-34.42,"lon":150.89,"region":"NSW · Costa sur",   "season":"Abr-Jun"},
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
    s  = joblib.load(os.path.join(MODELS_PATH, "scaler.pkl"))
    p  = joblib.load(os.path.join(MODELS_PATH, "pca.pkl"))
    c  = joblib.load(os.path.join(MODELS_PATH, "classifier.pkl"))
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
<div style='padding:1.2rem 0 0.4rem'>
  <div style='font-size:18px;font-weight:800;color:#F1F5F9;letter-spacing:-0.02em'>RainCast</div>
  <div style='font-size:10px;color:#334155;text-transform:uppercase;letter-spacing:0.12em;margin-top:2px'>Australia · PCA</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>Métricas del modelo</div>", unsafe_allow_html=True)

    metrics = [
        ("76.97%", "Accuracy",  "Acierta en 3 de cada 4 días"),
        ("0.849",  "ROC-AUC",   "Discriminación lluvia vs seco"),
        ("76.27%", "Recall",    "Días lluviosos detectados"),
        ("59.75%", "F1-Score",  "Balance precisión / recall"),
    ]
    cols = st.columns(2)
    for i, (v, l, tip) in enumerate(metrics):
        with cols[i % 2]:
            st.markdown(f"""
<div class='sb-metric'>
  <div class='sb-val'>{v}</div>
  <div class='sb-lbl'>{l}</div>
  <div class='sb-tip'>{tip}</div>
</div>
""", unsafe_allow_html=True)

    if models_ok:
        st.divider()
        st.markdown("<div style='font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>Reducción PCA</div>", unsafe_allow_html=True)
        st.markdown(f"""
<div class='sb-metric'>
  <div class='sb-val'>{len(feature_names)} <span style='color:#334155;font-size:14px'>→</span> {pca.n_components_}</div>
  <div class='sb-lbl'>variables → componentes</div>
  <div class='sb-tip'>{sum(pca.explained_variance_ratio_)*100:.1f}% de información preservada</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='font-size:10px;color:#334155;line-height:1.7'>
  Dataset: Rain in Australia<br>
  145 000+ obs · 49 estaciones · 2007–2017<br>
  <a href='https://www.bom.gov.au/climate/data/' style='color:#EA580C'>Bureau of Meteorology</a>
</div>
<div style='background:#1C0F06;border:1px solid #7C2D12;border-radius:8px;padding:8px 10px;font-size:10px;color:#9A3412;margin-top:0.8rem;line-height:1.5'>
  Herramienta académica. No reemplaza sistemas meteorológicos profesionales.
</div>
""", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;color:#1E2D3D;margin-top:1rem'>IA I · Los Libertadores · 2024</div>", unsafe_allow_html=True)

# ── MAIN ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='rh-wrapper'>
  <div class='rh-accent'></div>
  <div class='rh-content'>
    <div class='rh-label'>Predicción meteorológica · Machine Learning</div>
    <div class='rh-title'>¿Lloverá mañana en Australia?</div>
    <div class='rh-sub'>PCA + Regresión Logística · Datos en tiempo real vía Open-Meteo</div>
    <div class='rh-source'>Fuente del dataset: Bureau of Meteorology / Kaggle · Rain in Australia</div>
  </div>
</div>
""", unsafe_allow_html=True)

if not models_ok:
    st.stop()

# ── MODO ──────────────────────────────────────────────────────────────────────
mode = st.radio(
    "Modo",
    ["Datos reales de una ciudad", "Ingresar manualmente", "Caso de ejemplo"],
    horizontal=True,
    label_visibility="collapsed"
)

inputs = {}
api_data = None

# ── MODO API ──────────────────────────────────────────────────────────────────
if "reales" in mode:
    if "selected_city" not in st.session_state:
        st.session_state["selected_city"] = "Sydney"

    city_html = "<div class='city-grid'>"
    for city in CITIES:
        active = "active" if city == st.session_state["selected_city"] else ""
        city_html += f"""
<button class='city-btn {active}' onclick="void(0)">
  <span class='city-name'>{city}</span>
  <span class='city-region'>{CITIES[city]['region']}</span>
</button>"""
    city_html += "</div>"

    city_cols = st.columns(6)
    city_list = list(CITIES.keys())
    for i, city in enumerate(city_list):
        with city_cols[i % 6]:
            is_selected = city == st.session_state["selected_city"]
            btn_type = "primary" if is_selected else "secondary"
            if st.button(city, key=f"c_{city}", use_container_width=True, type=btn_type):
                st.session_state["selected_city"] = city
                st.rerun()

    selected = st.session_state["selected_city"]
    st.markdown(f"<div style='font-size:11px;color:#475569;margin-bottom:0.6rem'>Ciudad seleccionada: <span style='color:#FB923C;font-weight:600'>{selected}</span> · {CITIES[selected]['region']} · Temporada de lluvia: {CITIES[selected]['season']}</div>", unsafe_allow_html=True)

    with st.spinner(f"Consultando Open-Meteo para {selected}…"):
        api_data = fetch_weather(selected)

    if api_data:
        st.markdown(f"""
<div class='weather-row'>
  <div class='weather-card'>
    <div class='weather-val'>{api_data['Temp9am']:.1f}°</div>
    <div class='weather-lbl'>Temp 9am</div>
  </div>
  <div class='weather-card'>
    <div class='weather-val'>{api_data['Humidity3pm']:.0f}%</div>
    <div class='weather-lbl'>Humedad 3pm</div>
  </div>
  <div class='weather-card'>
    <div class='weather-val'>{api_data['WindGustSpeed']:.0f}</div>
    <div class='weather-lbl'>Ráfaga km/h</div>
  </div>
  <div class='weather-card'>
    <div class='weather-val'>{api_data['Rainfall']:.1f}</div>
    <div class='weather-lbl'>Lluvia hoy mm</div>
  </div>
</div>
""", unsafe_allow_html=True)
        inputs = {k: v for k, v in api_data.items() if not k.startswith("_")}
    else:
        st.warning("No se pudo conectar con Open-Meteo. Cambia a modo manual.")

# ── MODO MANUAL ───────────────────────────────────────────────────────────────
elif "manual" in mode:
    def med(f): return float(feature_ranges[f]["median"])
    with st.expander("Temperatura y precipitación", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            inputs["MinTemp"]   = st.number_input("Temp. mínima (°C)",   -10.0, 50.0,  med("MinTemp"),   .5)
            inputs["MaxTemp"]   = st.number_input("Temp. máxima (°C)",    -5.0, 55.0,  med("MaxTemp"),   .5)
            inputs["Temp9am"]   = st.number_input("Temp. 9am (°C)",      -10.0, 50.0,  med("Temp9am"),   .5)
            inputs["Temp3pm"]   = st.number_input("Temp. 3pm (°C)",      -10.0, 50.0,  med("Temp3pm"),   .5)
        with c2:
            inputs["Rainfall"]    = st.number_input("Lluvia hoy (mm)",      0.0, 400.0, med("Rainfall"),    .5)
            inputs["Evaporation"] = st.number_input("Evaporación (mm)",      0.0, 150.0, med("Evaporation"), .5)
            inputs["Sunshine"]    = st.number_input("Horas de sol",          0.0,  14.5, med("Sunshine"),    .5)
            inputs["RainToday"]   = st.selectbox("Llovió hoy", [0,1], format_func=lambda x:"Sí" if x else "No")

    with st.expander("Viento y presión"):
        c1, c2 = st.columns(2)
        with c1:
            inputs["WindGustSpeed"] = st.number_input("Ráfaga (km/h)",     0.0, 200.0, med("WindGustSpeed"), 1.0)
            inputs["WindSpeed9am"]  = st.number_input("Viento 9am (km/h)", 0.0, 150.0, med("WindSpeed9am"),  1.0)
            inputs["WindSpeed3pm"]  = st.number_input("Viento 3pm (km/h)", 0.0, 150.0, med("WindSpeed3pm"),  1.0)
        with c2:
            inputs["Pressure9am"] = st.number_input("Presión 9am (hPa)", 970.0, 1050.0, med("Pressure9am"), .5)
            inputs["Pressure3pm"] = st.number_input("Presión 3pm (hPa)", 970.0, 1050.0, med("Pressure3pm"), .5)

    with st.expander("Humedad y nubosidad"):
        c1, c2 = st.columns(2)
        with c1:
            inputs["Humidity9am"] = st.number_input("Humedad 9am (%)", 0.0, 100.0, med("Humidity9am"), 1.0)
            inputs["Humidity3pm"] = st.number_input("Humedad 3pm (%)", 0.0, 100.0, med("Humidity3pm"), 1.0)
        with c2:
            inputs["Cloud9am"] = st.number_input("Nubosidad 9am (oktas)", 0.0, 9.0, med("Cloud9am"), 1.0)
            inputs["Cloud3pm"] = st.number_input("Nubosidad 3pm (oktas)", 0.0, 9.0, med("Cloud3pm"), 1.0)

# ── MODO EJEMPLO ──────────────────────────────────────────────────────────────
else:
    EXAMPLES = {
        "Día seco — Sydney (verano)": {
            "MinTemp":18.0,"MaxTemp":29.5,"Rainfall":0.0,"Evaporation":6.4,
            "Sunshine":9.5,"WindGustSpeed":35.0,"WindSpeed9am":15.0,"WindSpeed3pm":24.0,
            "Humidity9am":55.0,"Humidity3pm":30.0,"Pressure9am":1020.0,"Pressure3pm":1015.0,
            "Cloud9am":2.0,"Cloud3pm":3.0,"Temp9am":22.0,"Temp3pm":27.5,"RainToday":0},
        "Día lluvioso — Melbourne (invierno)": {
            "MinTemp":9.0,"MaxTemp":14.5,"Rainfall":8.2,"Evaporation":1.6,
            "Sunshine":1.0,"WindGustSpeed":56.0,"WindSpeed9am":28.0,"WindSpeed3pm":35.0,
            "Humidity9am":88.0,"Humidity3pm":80.0,"Pressure9am":1005.0,"Pressure3pm":1000.0,
            "Cloud9am":7.0,"Cloud3pm":8.0,"Temp9am":11.0,"Temp3pm":13.5,"RainToday":1},
        "Monzón — Darwin (noviembre)": {
            "MinTemp":24.0,"MaxTemp":33.0,"Rainfall":12.4,"Evaporation":7.1,
            "Sunshine":3.0,"WindGustSpeed":63.0,"WindSpeed9am":22.0,"WindSpeed3pm":30.0,
            "Humidity9am":90.0,"Humidity3pm":82.0,"Pressure9am":1007.0,"Pressure3pm":1003.0,
            "Cloud9am":7.0,"Cloud3pm":8.0,"Temp9am":27.5,"Temp3pm":31.0,"RainToday":1},
    }
    choice = st.selectbox("Escenario", list(EXAMPLES.keys()))
    inputs = EXAMPLES[choice]
    st.info(f"Escenario cargado: **{choice}**")

# ── PREDICCIÓN ────────────────────────────────────────────────────────────────
st.divider()
predict_btn = st.button("Predecir si lloverá mañana", type="primary", use_container_width=True)

if predict_btn and inputs:
    row   = pd.DataFrame([inputs], columns=feature_names)
    Xs    = scaler.transform(row)
    Xp    = pca.transform(Xs)
    pred  = int(classifier.predict(Xp)[0])
    probs = classifier.predict_proba(Xp)[0]
    p_rain, p_dry = float(probs[1]), float(probs[0])

    st.divider()
    col_res, col_chart = st.columns([1, 1], gap="large")

    with col_res:
        if pred == 1:
            st.markdown(f"""
<div class='result-block rain'>
  <div class='result-verdict rain'>Lluvia esperada mañana</div>
  <div class='result-pct rain'>{p_rain*100:.1f}%</div>
  <div style='font-size:12px;color:#0369A1'>probabilidad de precipitación</div>
  <div class='result-note'>
    El modelo detecta condiciones propicias.<br>
    Recall: 76.27% — captura la mayoría de días lluviosos.
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class='result-block dry'>
  <div class='result-verdict dry'>Día seco esperado</div>
  <div class='result-pct dry'>{p_dry*100:.1f}%</div>
  <div style='font-size:12px;color:#065F46'>probabilidad de día sin lluvia</div>
  <div class='result-note'>
    Las condiciones actuales sugieren un día sin precipitaciones.<br>
    Accuracy general del modelo: 76.97%.
  </div>
</div>""", unsafe_allow_html=True)

    with col_chart:
        BG = "#0C1219"
        fig, ax = plt.subplots(figsize=(5.5, 4), facecolor=BG)
        ax.set_facecolor(BG)
        colors = ["#10B981", "#0EA5E9"]
        bars = ax.bar(["Sin lluvia", "Con lluvia"], [p_dry*100, p_rain*100],
                      color=colors, width=0.45, edgecolor=BG)
        for bar, v in zip(bars, [p_dry*100, p_rain*100]):
            ax.text(bar.get_x()+bar.get_width()/2, v+1.8,
                    f"{v:.1f}%", ha="center", va="bottom",
                    fontsize=13, fontweight="bold", color="#F1F5F9",
                    fontfamily="monospace")
        ax.set_ylim(0, 115)
        ax.set_ylabel("Probabilidad (%)", color="#334155", fontsize=10)
        ax.set_title("Probabilidad por clase", color="#94A3B8", fontsize=11, fontweight="bold", pad=12)
        ax.tick_params(colors="#334155", labelsize=10)
        for sp in ax.spines.values(): sp.set_color("#1A2535")
        ax.yaxis.grid(True, color="#1A2535", linewidth=0.6, linestyle="--")
        ax.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Análisis PCA ──────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem;margin-bottom:0.4rem;font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.1em'>Análisis de componentes principales</div>", unsafe_allow_html=True)

    st.markdown(f"""
<div class='pca-row'>
  <div class='pca-pill'><div class='pca-val'>{len(feature_names)}</div><div class='pca-lbl'>Variables leídas</div></div>
  <div class='pca-pill'><div class='pca-val'>{pca.n_components_}</div><div class='pca-lbl'>Componentes PCA</div></div>
  <div class='pca-pill'><div class='pca-val'>{sum(pca.explained_variance_ratio_)*100:.1f}%</div><div class='pca-lbl'>Información preservada</div></div>
  <div class='pca-pill'><div class='pca-val'>{(1-sum(pca.explained_variance_ratio_))*100:.1f}%</div><div class='pca-lbl'>Ruido descartado</div></div>
</div>
""", unsafe_allow_html=True)

    tab_dim, tab_pesos = st.tabs(["Reducción dimensional", "Peso de variables"])

    with tab_dim:
        st.markdown("""
Variables como **Temp9am / Temp3pm** (r = 0.97) y **Presión 9am / 3pm** (r = 0.96) aportan información redundante.
PCA las agrupa en componentes ortogonales, dejando el clasificador libre de multicolinealidad.
""")

    with tab_pesos:
        loadings = pd.DataFrame(pca.components_.T,
                                index=[f.replace("_"," ") for f in feature_names],
                                columns=[f"PC{i+1}" for i in range(pca.n_components_)])
        top5 = loadings["PC1"].abs().nlargest(5)

        fig2, ax2 = plt.subplots(figsize=(7, 3.2), facecolor=BG)
        ax2.set_facecolor(BG)
        colors_b = ["#EA580C" if loadings.loc[f,"PC1"]>0 else "#0EA5E9" for f in top5.index]
        ax2.barh(list(top5.index), [loadings.loc[f,"PC1"] for f in top5.index],
                 color=colors_b, edgecolor=BG, height=0.55)
        ax2.set_xlabel("Peso en PC1", color="#334155", fontsize=10)
        ax2.set_title("Top 5 variables con mayor influencia en PC1", color="#94A3B8",
                      fontsize=11, fontweight="bold")
        ax2.axvline(0, color="#1A2535", lw=1)
        ax2.tick_params(colors="#475569", labelsize=9)
        for sp in ax2.spines.values(): sp.set_color("#1A2535")
        ax2.xaxis.grid(True, color="#1A2535", lw=0.6, linestyle="--")
        ax2.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close()
        st.caption("Naranja = relación positiva con PC1 · Azul = relación negativa")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  Inteligencia Artificial I &nbsp;|&nbsp; Fundación Universitaria Los Libertadores 2024 &nbsp;|&nbsp;
  Dataset: <a href='https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package'>Rain in Australia — Kaggle</a> &nbsp;|&nbsp;
  Fuente: <a href='https://www.bom.gov.au/climate/data/'>Bureau of Meteorology</a> &nbsp;|&nbsp;
  API: <a href='https://open-meteo.com'>Open-Meteo</a>
</div>
""", unsafe_allow_html=True)
