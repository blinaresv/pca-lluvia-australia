"""
app.py — RainCast Australia
PCA + Regresión Logística | Fundación Universitaria Los Libertadores 2026
v6.0: mapa interactivo Leaflet por ciudad
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import streamlit.components.v1 as components
import joblib, requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

/* Fondo general claro */
.stApp { background: #F0F4F8; }
[data-testid="stAppViewContainer"] { background: #F0F4F8; }
[data-testid="stHeader"] { background: transparent !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0F2B5B;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #B8CCE8 !important; }
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
[data-testid="stSidebar"] hr { border-color: #1E3F6F !important; }

/* Ocultar toolbar */
[data-testid="stToolbar"] { display: none; }

/* Ocultar botón colapso sidebar — CSS amplio */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
button[data-testid="baseButton-headerNoPadding"],
[class*="collapsedControl"],
[class*="sidebarToggle"],
[class*="sidebar-toggle"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* ── Hero con imagen ─────────────────────────────────── */
.hero {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    height: 200px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(10,40,90,0.88) 0%, rgba(10,40,90,0.55) 60%, rgba(10,40,90,0.45) 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 2.5rem;
}
.hero-tag {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7DD3FC;
    margin-bottom: 0.4rem;
}
.hero-title {
    font-size: 1.9rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin: 0 0 0.3rem;
}
.hero-sub {
    font-size: 13px;
    color: #93C5FD;
    margin: 0 0 0.25rem;
}
.hero-source {
    font-size: 10px;
    color: #3B6EA5;
    font-style: italic;
}

/* ── Botones de ciudad ───────────────────────────────── */
.stButton > button {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 10px !important;
    color: #334155 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.15s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
.stButton > button:hover {
    border-color: #1D4ED8 !important;
    color: #1D4ED8 !important;
    background: #EFF6FF !important;
    box-shadow: 0 2px 8px rgba(29,78,216,0.12) !important;
}
.stButton > button:focus {
    box-shadow: none !important;
    outline: none !important;
}

/* Ciudad seleccionada */
.stButton > button[kind="primary"] {
    background: #1D4ED8 !important;
    border: 1.5px solid #1D4ED8 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(29,78,216,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1E40AF !important;
    border-color: #1E40AF !important;
    color: #FFFFFF !important;
}

/* ── Chips de modo ───────────────────────────────────── */
div[data-testid="stRadio"] label {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #64748B !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: #1D4ED8 !important;
    color: #1D4ED8 !important;
}

/* ── Tarjetas clima ──────────────────────────────────── */
.weather-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin: 1rem 0 1.5rem;
}
.w-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.w-val {
    font-size: 22px;
    font-weight: 700;
    color: #0F2B5B;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
}
.w-lbl {
    font-size: 10px;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* ── Ciudad seleccionada tag ─────────────────────────── */
.city-tag {
    font-size: 12px;
    color: #64748B;
    margin: 6px 0 12px;
}
.city-tag strong { color: #1D4ED8; }

/* ── Expanders ───────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
[data-testid="stExpander"] summary {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #334155 !important;
}

/* ── Botón de predicción ─────────────────────────────── */
button[data-testid="baseButton-primary"] {
    background: #1D4ED8 !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    height: 56px !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 14px rgba(29,78,216,0.3) !important;
    transition: all 0.18s !important;
}
button[data-testid="baseButton-primary"]:hover {
    background: #1E40AF !important;
    box-shadow: 0 6px 20px rgba(29,78,216,0.4) !important;
    transform: translateY(-1px);
}
button[data-testid="baseButton-primary"]:active {
    transform: scale(0.98);
}

/* ── Resultado ───────────────────────────────────────── */
.result-wrap {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 1.5rem;
}
.result-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    border: 1.5px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.result-card.rain { border-color: #BAE6FD; background: #F0F9FF; }
.result-card.dry  { border-color: #A7F3D0; background: #F0FDF4; }
.result-pct {
    font-size: 76px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.04em;
    line-height: 1;
    margin: 0.4rem 0;
}
.result-pct.rain { color: #0369A1; }
.result-pct.dry  { color: #065F46; }
.result-verdict {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.result-verdict.rain { color: #0284C7; }
.result-verdict.dry  { color: #059669; }
.result-note {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 0.8rem;
    line-height: 1.6;
}

/* ── Tabs ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #E2E8F0 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #94A3B8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border: none !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #1D4ED8 !important;
    border-bottom: 2px solid #1D4ED8 !important;
}

/* ── PCA pills ───────────────────────────────────────── */
.pca-row { display: flex; gap: 8px; margin: 1rem 0; }
.pca-pill {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 10px 14px;
    text-align: center;
    flex: 1;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.pca-val {
    font-size: 18px;
    font-weight: 700;
    color: #1D4ED8;
    font-family: 'JetBrains Mono', monospace;
}
.pca-lbl {
    font-size: 9px;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 3px;
}

/* ── Sidebar componentes ─────────────────────────────── */
.sb-metric {
    background: #0A1E42;
    border: 1px solid #1E3F6F;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
}
.sb-val { font-size: 17px; font-weight: 700; color: #7DD3FC; font-family: 'JetBrains Mono', monospace; }
.sb-lbl { font-size: 9px; color: #3B6EA5; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }
.sb-tip { font-size: 10px; color: #3B6EA5; margin-top: 3px; line-height: 1.4; }

/* ── Inputs ──────────────────────────────────────────── */
.stNumberInput input {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    color: #1E293B !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
}
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    color: #1E293B !important;
    border-radius: 8px !important;
}

/* ── Sección label ───────────────────────────────────── */
.section-label {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #94A3B8;
    margin: 1.2rem 0 0.4rem;
}

/* ── Footer ──────────────────────────────────────────── */
.footer-bar {
    text-align: center;
    color: #CBD5E1;
    font-size: 11px;
    padding: 12px 0 4px;
    border-top: 1px solid #E2E8F0;
    margin-top: 2rem;
}
.footer-bar a { color: #94A3B8; text-decoration: none; }
.footer-bar a:hover { color: #1D4ED8; }
</style>
""", unsafe_allow_html=True)

# ── Ciudades ──────────────────────────────────────────────────────────────────
CITIES = {
    "Sydney":     {"lat":-33.87,"lon":151.21,"region":"NSW · Costa este",  "season":"Mar-Jun",  "img":"1022692"},
    "Melbourne":  {"lat":-37.81,"lon":144.96,"region":"VIC · Sur",         "season":"May-Ago",  "img":"1321831"},
    "Brisbane":   {"lat":-27.47,"lon":153.02,"region":"QLD · Subtropical", "season":"Feb-May",  "img":"2193300"},
    "Perth":      {"lat":-31.95,"lon":115.86,"region":"WA · Suroeste",     "season":"May-Sep",  "img":"1619317"},
    "Darwin":     {"lat":-12.46,"lon":130.84,"region":"NT · Tropical",     "season":"Nov-Abr",  "img":"1287145"},
    "Adelaide":   {"lat":-34.93,"lon":138.60,"region":"SA · Mediterráneo", "season":"May-Ago",  "img":"1823681"},
    "Canberra":   {"lat":-35.28,"lon":149.13,"region":"ACT · Interior",    "season":"Oct-Mar",  "img":"1603650"},
    "Hobart":     {"lat":-42.88,"lon":147.33,"region":"TAS · Sur",         "season":"May-Sep",  "img":"1566347"},
    "Cairns":     {"lat":-16.92,"lon":145.77,"region":"QLD · Tropical",    "season":"Dic-Mar",  "img":"1018730"},
    "Gold Coast": {"lat":-28.00,"lon":153.43,"region":"QLD · Costa",       "season":"Feb-May",  "img":"1680779"},
    "Newcastle":  {"lat":-32.93,"lon":151.78,"region":"NSW · Costa norte", "season":"Mar-Jun",  "img":"1131546"},
    "Wollongong": {"lat":-34.42,"lon":150.89,"region":"NSW · Costa sur",   "season":"Abr-Jun",  "img":"1591382"},
}

# ── Open-Meteo API ────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_weather(city: str):
    """Consulta wttr.in — sin rate limit, ideal para demos."""
    c = CITIES[city]
    url = f"https://wttr.in/{c['lat']},{c['lon']}?format=j1"
    r = requests.get(url, timeout=10, headers={"User-Agent": "RainCast-Australia/1.0"})
    r.raise_for_status()
    d = r.json()

    cur  = d["current_condition"][0]
    tod  = d["weather"][0]
    hour = {h["time"]: h for h in tod.get("hourly", [])}

    def hval(key, time_str, default=0.0):
        h = hour.get(time_str, {})
        v = h.get(key, [{}])
        return float(v[0].get("value", default)) if isinstance(v, list) else float(v or default)

    temp9am  = hval("tempC",    "900",  float(cur["temp_C"]))
    temp3pm  = hval("tempC",    "1500", float(cur["temp_C"]))
    hum9am   = hval("humidity", "900",  float(cur["humidity"]))
    hum3pm   = hval("humidity", "1500", float(cur["humidity"]))
    pres9am  = hval("pressure", "900",  float(cur["pressure"]))
    pres3pm  = hval("pressure", "1500", float(cur["pressure"]))
    wind9am  = hval("windspeedKmph", "900",  float(cur["windspeedKmph"]))
    wind3pm  = hval("windspeedKmph", "1500", float(cur["windspeedKmph"]))
    cloud9am = hval("cloudcover",    "900",  float(cur["cloudcover"]))
    cloud3pm = hval("cloudcover",    "1500", float(cur["cloudcover"]))

    rain_mm    = float(tod.get("hourly", [{}])[0].get("precipMM", 0) or 0)
    max_temp   = float(tod.get("maxtempC", cur["temp_C"]))
    min_temp   = float(tod.get("mintempC", cur["temp_C"]))
    wind_gust  = float(cur.get("windspeedKmph", 0)) * 1.3
    rain_today = 1 if rain_mm > 1.0 else 0

    return {
        "MinTemp":       min_temp,
        "MaxTemp":       max_temp,
        "Rainfall":      rain_mm,
        "Evaporation":   4.0,
        "Sunshine":      max(0.0, (100 - float(cur["cloudcover"])) / 10),
        "WindGustSpeed": wind_gust,
        "WindSpeed9am":  wind9am,
        "WindSpeed3pm":  wind3pm,
        "Humidity9am":   hum9am,
        "Humidity3pm":   hum3pm,
        "Pressure9am":   pres9am,
        "Pressure3pm":   pres3pm,
        "Cloud9am":      round(cloud9am / 12.5),
        "Cloud3pm":      round(cloud3pm / 12.5),
        "Temp9am":       temp9am,
        "Temp3pm":       temp3pm,
        "RainToday":     rain_today,
        "_temp9":        temp9am,
        "_hum3":         hum3pm,
        "_wind":         wind_gust,
        "_rain":         rain_mm,
    }

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

# ── Mapa Leaflet ──────────────────────────────────────────────────────────────
def render_map(selected_city: str, height: int = 300) -> str:
    """Genera HTML con mapa Leaflet centrado en la ciudad seleccionada."""
    markers_js = ""
    for city, info in CITIES.items():
        lat, lon = info["lat"], info["lon"]
        region   = info["region"]
        season   = info["season"]
        is_sel   = city == selected_city

        if is_sel:
            # Marcador principal — círculo animado con pulso
            markers_js += f"""
var pulseIcon = L.divIcon({{
    className: '',
    html: `<div style="
        width:18px;height:18px;
        background:#1D4ED8;
        border:3px solid #fff;
        border-radius:50%;
        box-shadow:0 0 0 4px rgba(29,78,216,0.25);
        animation: pulse 1.6s ease-in-out infinite;
    "></div>`,
    iconSize:[18,18],
    iconAnchor:[9,9]
}});
L.marker([{lat},{lon}], {{icon: pulseIcon}})
  .addTo(map)
  .bindPopup(`<b style="font-size:13px">{city}</b><br>
    <span style="font-size:11px;color:#64748B">{region}</span><br>
    <span style="font-size:11px;color:#1D4ED8">Lluvia: {season}</span>`)
  .openPopup();
"""
        else:
            # Ciudades no seleccionadas — puntos pequeños
            markers_js += f"""
L.circleMarker([{lat},{lon}], {{
    radius: 5,
    color: '#fff',
    fillColor: '#94A3B8',
    fillOpacity: 0.9,
    weight: 1.5
}}).addTo(map)
  .bindPopup(`<b style="font-size:12px">{city}</b><br>
    <span style="font-size:10px;color:#64748B">{region}</span>`);
"""

    sel = CITIES[selected_city]
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  * {{ margin:0;padding:0;box-sizing:border-box; }}
  html,body,#map {{ width:100%;height:{height}px; }}
  @keyframes pulse {{
    0%   {{ box-shadow:0 0 0 0   rgba(29,78,216,0.5); }}
    70%  {{ box-shadow:0 0 0 10px rgba(29,78,216,0);   }}
    100% {{ box-shadow:0 0 0 0   rgba(29,78,216,0);    }}
  }}
  .leaflet-popup-content-wrapper {{
    border-radius:10px;
    box-shadow:0 4px 16px rgba(0,0,0,0.12);
    font-family:'Outfit',sans-serif;
  }}
  .leaflet-popup-tip {{ background:#fff; }}
</style>
</head>
<body>
<div id="map"></div>
<script>
  var map = L.map('map', {{
    center: [{sel['lat']},{sel['lon']}],
    zoom: 5,
    zoomControl: true,
    attributionControl: false
  }});

  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
    subdomains: 'abcd',
    maxZoom: 19
  }}).addTo(map);

  {markers_js}
</script>
</body>
</html>"""
    return html

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Ocultar botón colapso sidebar via st.html (JS)
    st.html("""
<script>
(function() {
    function hideSidebarBtn() {
        var selectors = [
            '[data-testid="collapsedControl"]',
            '[data-testid="stSidebarCollapsedControl"]',
            'button[data-testid="stBaseButton-headerNoPadding"]',
            'button[data-testid="baseButton-headerNoPadding"]'
        ];
        selectors.forEach(function(sel) {
            parent.document.querySelectorAll(sel).forEach(function(el) {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.width = '0';
                el.style.height = '0';
                el.style.overflow = 'hidden';
                el.style.position = 'absolute';
            });
        });
    }
    hideSidebarBtn();
    new MutationObserver(hideSidebarBtn)
        .observe(parent.document.body, {childList:true, subtree:true});
})();
</script>
""")
    st.markdown("""
<div style='padding:1rem 0 0.2rem'>
  <div style='font-size:20px;font-weight:800;color:#FFFFFF;letter-spacing:-0.02em'>RainCast</div>
  <div style='font-size:10px;color:#3B6EA5;text-transform:uppercase;letter-spacing:0.14em;margin-top:2px'>Australia · PCA</div>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size:10px;color:#3B6EA5;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;font-weight:600'>Métricas del modelo</div>", unsafe_allow_html=True)

    for v, l, tip in [
        ("76.97%","Accuracy","Acierta en 3 de cada 4 días"),
        ("0.849","ROC-AUC","Discriminación lluvia vs seco"),
        ("76.27%","Recall","Días lluviosos detectados"),
        ("59.75%","F1-Score","Balance precisión / recall"),
    ]:
        st.markdown(f"""
<div class='sb-metric'>
  <div class='sb-val'>{v}</div>
  <div class='sb-lbl'>{l}</div>
  <div class='sb-tip'>{tip}</div>
</div>""", unsafe_allow_html=True)

    if models_ok:
        st.divider()
        st.markdown(f"""
<div class='sb-metric'>
  <div class='sb-val'>{len(feature_names)} <span style='color:#1E3F6F'>→</span> {pca.n_components_}</div>
  <div class='sb-lbl'>Variables → Componentes PCA</div>
  <div class='sb-tip'>{sum(pca.explained_variance_ratio_)*100:.1f}% de información preservada</div>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='font-size:10px;color:#3B6EA5;line-height:1.8'>
  145 000+ obs · 49 estaciones · 2007–2017<br>
  <a href='https://www.bom.gov.au' style='color:#7DD3FC'>Bureau of Meteorology</a>
</div>
<div style='background:#071428;border:1px solid #1E3F6F;border-radius:8px;padding:8px 10px;font-size:10px;color:#3B6EA5;margin-top:0.8rem;line-height:1.5'>
  Herramienta académica. No reemplaza sistemas meteorológicos profesionales.
</div>""", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;color:#1E3F6F;margin-top:1rem'>IA I · Los Libertadores · 2026</div>", unsafe_allow_html=True)

# ── MAIN ──────────────────────────────────────────────────────────────────────
if "selected_city" not in st.session_state:
    st.session_state["selected_city"] = "Sydney"

selected = st.session_state["selected_city"]
city_img = CITIES[selected]["img"]

# Hero con imagen de la ciudad seleccionada
st.markdown(f"""
<div class='hero'
     style='background-image: url("https://picsum.photos/seed/{city_img}/1800/400");'>
  <div class='hero-overlay'>
    <div class='hero-tag'>Predicción meteorológica · Machine Learning</div>
    <div class='hero-title'>¿Lloverá mañana en Australia?</div>
    <div class='hero-sub'>PCA + Regresión Logística · Datos en tiempo real vía Open-Meteo</div>
    <div class='hero-source'>Fuente: Bureau of Meteorology / Kaggle · Rain in Australia</div>
  </div>
</div>
""", unsafe_allow_html=True)

if not models_ok:
    st.stop()

# ── MODO ──────────────────────────────────────────────────────────────────────
mode = st.radio(
    "Modo",
    ["Datos reales de una ciudad", "Ingresar manualmente"],
    horizontal=True,
    label_visibility="collapsed"
)

inputs = {}

# ── MODO API ──────────────────────────────────────────────────────────────────
if "reales" in mode:
    with st.expander("Datos reales de una ciudad", expanded=True):
        st.markdown("<div class='section-label'>Seleccionar ciudad</div>", unsafe_allow_html=True)
        city_cols = st.columns(6)
        for i, city in enumerate(CITIES):
            with city_cols[i % 6]:
                is_sel = city == st.session_state["selected_city"]
                if st.button(city, key=f"c_{city}", use_container_width=True,
                             type="primary" if is_sel else "secondary"):
                    st.session_state["selected_city"] = city
                    st.rerun()

        selected = st.session_state["selected_city"]
        st.markdown(f"<div class='city-tag'>Ciudad: <strong>{selected}</strong> · {CITIES[selected]['region']} · Temporada de lluvia: {CITIES[selected]['season']}</div>", unsafe_allow_html=True)

        col_data, col_map = st.columns([1.1, 1], gap="medium")

        with col_map:
            components.html(render_map(selected, height=290), height=290)

        with col_data:
            api_data = None
            with st.spinner(f"Consultando clima actual para {selected}…"):
                try:
                    api_data = fetch_weather(selected)
                except Exception:
                    pass

            if api_data:
                st.markdown(f"""
<div class='weather-row' style='grid-template-columns:1fr 1fr;'>
  <div class='w-card'>
    <div class='w-val'>{api_data['Temp9am']:.1f}°</div>
    <div class='w-lbl'>Temp 9am</div>
  </div>
  <div class='w-card'>
    <div class='w-val'>{api_data['MaxTemp']:.1f}°</div>
    <div class='w-lbl'>Temp máx</div>
  </div>
  <div class='w-card'>
    <div class='w-val'>{api_data['Humidity3pm']:.0f}%</div>
    <div class='w-lbl'>Humedad 3pm</div>
  </div>
  <div class='w-card'>
    <div class='w-val'>{api_data['WindGustSpeed']:.0f}</div>
    <div class='w-lbl'>Ráfaga km/h</div>
  </div>
  <div class='w-card'>
    <div class='w-val'>{api_data['Rainfall']:.1f}</div>
    <div class='w-lbl'>Lluvia hoy mm</div>
  </div>
  <div class='w-card'>
    <div class='w-val'>{api_data['Pressure9am']:.0f}</div>
    <div class='w-lbl'>Presión hPa</div>
  </div>
</div>
""", unsafe_allow_html=True)
                inputs = {k: v for k, v in api_data.items() if not k.startswith("_")}
            else:
                st.info(f"Usando valores climatológicos típicos de {selected}. La predicción sigue disponible.")
                inputs = {f: float(feature_ranges[f]["median"]) for f in feature_names}

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
            inputs["Rainfall"]    = st.number_input("Lluvia hoy (mm)",    0.0, 400.0, med("Rainfall"),    .5)
            inputs["Evaporation"] = st.number_input("Evaporación (mm)",   0.0, 150.0, med("Evaporation"), .5)
            inputs["Sunshine"]    = st.number_input("Horas de sol",        0.0,  14.5, med("Sunshine"),    .5)
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
<div class='result-card rain'>
  <div class='result-verdict rain'>Lluvia esperada mañana</div>
  <div class='result-pct rain'>{p_rain*100:.1f}%</div>
  <div style='font-size:12px;color:#0284C7'>probabilidad de precipitación</div>
  <div class='result-note'>
    El modelo detecta condiciones propicias.<br>
    Recall: 76.27% — captura la mayoría de días lluviosos.
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class='result-card dry'>
  <div class='result-verdict dry'>Día seco esperado</div>
  <div class='result-pct dry'>{p_dry*100:.1f}%</div>
  <div style='font-size:12px;color:#059669'>probabilidad de día sin lluvia</div>
  <div class='result-note'>
    Las condiciones actuales sugieren un día sin precipitaciones.<br>
    Accuracy general: 76.97%.
  </div>
</div>""", unsafe_allow_html=True)

    with col_chart:
        SET2 = ["#66C2A5", "#FC8D62", "#8DA0CB"]
        fig, ax = plt.subplots(figsize=(5.5, 4), facecolor="white")
        ax.set_facecolor("white")
        bars = ax.bar(["Sin lluvia", "Con lluvia"], [p_dry*100, p_rain*100],
                      color=[SET2[0], SET2[1]], width=0.45, edgecolor="white")
        for bar, v in zip(bars, [p_dry*100, p_rain*100]):
            ax.text(bar.get_x()+bar.get_width()/2, v+1.5,
                    f"{v:.1f}%", ha="center", va="bottom",
                    fontsize=13, fontweight="bold", color="#1E293B",
                    fontfamily="monospace")
        ax.set_ylim(0, 115)
        ax.set_ylabel("Probabilidad (%)", fontsize=11)
        ax.set_title("Probabilidad por clase", fontsize=12, fontweight="bold", pad=12)
        ax.tick_params(labelsize=10)
        for sp in ["top","right"]: ax.spines[sp].set_visible(False)
        for sp in ["left","bottom"]: ax.spines[sp].set_color("#E2E8F0")
        ax.yaxis.grid(True, color="#E0E0E0", linewidth=0.6)
        ax.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig, width='stretch')
        plt.close()

    tab_dim, tab_pesos = st.tabs(["Reducción dimensional", "Peso de variables"])

    with tab_dim:
        st.markdown("Variables como **Temp9am / Temp3pm** (r = 0.97) y **Presión 9am / 3pm** (r = 0.96) aportan información redundante. PCA las agrupa en componentes ortogonales, dejando el clasificador libre de multicolinealidad.")

    with tab_pesos:
        loadings = pd.DataFrame(pca.components_.T,
                                index=[f.replace("_"," ") for f in feature_names],
                                columns=[f"PC{i+1}" for i in range(pca.n_components_)])
        top5 = loadings["PC1"].abs().nlargest(5)
        fig2, ax2 = plt.subplots(figsize=(7, 3.2), facecolor="white")
        ax2.set_facecolor("white")
        colors_b = [SET2[0] if loadings.loc[f,"PC1"]>0 else SET2[1] for f in top5.index]
        ax2.barh(list(top5.index), [loadings.loc[f,"PC1"] for f in top5.index],
                 color=colors_b, edgecolor="white", height=0.55)
        ax2.set_xlabel("Peso en PC1", fontsize=11)
        ax2.set_title("Top 5 variables con mayor influencia en PC1",
                      fontsize=12, fontweight="bold")
        ax2.axvline(0, color="#B0BEC5", lw=1)
        ax2.tick_params(labelsize=10)
        for sp in ["top","right"]: ax2.spines[sp].set_visible(False)
        for sp in ["left","bottom"]: ax2.spines[sp].set_color("#E2E8F0")
        ax2.xaxis.grid(True, color="#E0E0E0", lw=0.6)
        ax2.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig2, width='stretch')
        plt.close()
        st.caption("Teal = relación positiva con PC1 · Naranja = relación negativa")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  Inteligencia Artificial I &nbsp;|&nbsp; Fundación Universitaria Los Libertadores 2026 &nbsp;|&nbsp;
  Dataset: <a href='https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package'>Rain in Australia — Kaggle</a> &nbsp;|&nbsp;
  Fuente: <a href='https://www.bom.gov.au/climate/data/'>Bureau of Meteorology</a> &nbsp;|&nbsp;
  API: <a href='https://open-meteo.com'>Open-Meteo</a>
</div>
""", unsafe_allow_html=True)
