# Predictor de Lluvia en Australia con PCA

Predice si lloverá mañana en Australia a partir de mediciones meteorológicas del día actual. Usa PCA para reducir las 17 variables climáticas correlacionadas a un espacio de componentes independientes, y Regresión Logística para clasificar.

---

## Demo en vivo

**[Abrir aplicación](https://pca-lluvia-australia.streamlit.app)** ← actualiza con tu URL tras el despliegue

**Repositorio:** [github.com/blinaresv/pca-lluvia-australia](https://github.com/blinaresv/pca-lluvia-australia)

---

## Descripción

El dataset Rain in Australia (Kaggle) tiene 145,000 observaciones diarias de 49 estaciones meteorológicas australianas durante 10 años. El problema es clasificar si lloverá al día siguiente (`RainTomorrow`) usando las condiciones del día actual.

Lo que hace al problema interesante para PCA es que muchas variables están muy correlacionadas entre sí: la temperatura de las 9am y las 3pm tienen correlación > 0.97, la presión de ambos horarios también ronda 0.96, y todas las mediciones de temperatura están correlacionadas entre sí. Sin hacer nada al respecto, el clasificador recibe información redundante. PCA colapsa esas correlaciones en componentes ortogonales independientes, pasando de 17 variables a 7-9 componentes que explican el 95% de la varianza.

---

## Algoritmo utilizado

**PCA como preprocesamiento para clasificación**

PCA busca las direcciones del espacio de características donde los datos varían más (componentes principales), proyecta todos los puntos sobre esos ejes y descarta los de menor varianza. El resultado son variables nuevas, ortogonales entre sí (sin correlación).

El pipeline completo:

1. `StandardScaler` — estandariza a media 0 y desviación estándar 1. Sin esto, variables en escalas distintas (p. ej. `Area` en mm² vs `Humidity` en %) dominarían los componentes.
2. `PCA(n_components=0.95)` — reduce las 17 features a los N componentes que explican el 95% de la varianza.
3. `LogisticRegression(class_weight='balanced')` — clasifica en el espacio reducido. El parámetro `balanced` compensa que hay más días sin lluvia que con lluvia.

Por qué tiene sentido aquí: `Temp9am` y `Temp3pm` miden prácticamente lo mismo (r = 0.97). Igual `Pressure9am` y `Pressure3pm` (r = 0.96). PCA detecta esa redundancia y la colapsa en un solo componente principal, dejando los demás libres para capturar variación independiente.

**Métricas (conjunto de prueba 20%, estratificado):**

| Métrica | Valor |
|---|---|
| Accuracy | ejecutar notebook para ver |
| Precision | ejecutar notebook para ver |
| Recall | ejecutar notebook para ver |
| F1-Score | ejecutar notebook para ver |
| ROC-AUC | ejecutar notebook para ver |

---

## Dataset

**Nombre:** Rain in Australia  
**Fuente:** [Kaggle — jsphyg/weather-dataset-rattle-package](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package)  
**Tamaño:** 145,460 registros × 23 columnas  
**Clases:** No llueve (77.7%) / Llueve (22.3%)  
**Período:** 10 años, 49 estaciones meteorológicas australianas

Features utilizadas (17):

| Feature | Qué mide |
|---|---|
| MinTemp | temperatura mínima del día (°C) |
| MaxTemp | temperatura máxima del día (°C) |
| Rainfall | precipitación acumulada (mm) |
| Evaporation | evaporación diaria (mm) |
| Sunshine | horas de sol |
| WindGustSpeed | velocidad máxima de ráfaga (km/h) |
| WindSpeed9am | velocidad del viento a las 9am |
| WindSpeed3pm | velocidad del viento a las 3pm |
| Humidity9am | humedad relativa 9am (%) |
| Humidity3pm | humedad relativa 3pm (%) |
| Pressure9am | presión atmosférica 9am (hPa) |
| Pressure3pm | presión atmosférica 3pm (hPa) |
| Cloud9am | nubosidad 9am (0-8 oktas) |
| Cloud3pm | nubosidad 3pm (0-8 oktas) |
| Temp9am | temperatura a las 9am (°C) |
| Temp3pm | temperatura a las 3pm (°C) |
| RainToday | ¿llovió hoy? (binaria) |

---

## Descarga del dataset

El dataset requiere una cuenta gratuita de Kaggle.

**Opción 1 — Manual:**
1. Entra a https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package
2. Haz clic en **Download**
3. Descomprime y coloca `weatherAUS.csv` en `data/raw/`

**Opción 2 — API de Kaggle:**
```bash
pip install kaggle
kaggle datasets download -d jsphyg/weather-dataset-rattle-package -p data/raw/ --unzip
```

---

## Instalación local

Requiere Python 3.11+ y pip.

```bash
git clone https://github.com/blinaresv/pca-lluvia-australia.git
cd pca-lluvia-australia

python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

pip install -r requirements.txt

# Coloca weatherAUS.csv en data/raw/ (ver sección anterior)

# Entrenar el modelo
jupyter notebook notebooks/01_training.ipynb
# Ejecuta todas las celdas en orden

# Lanzar la app
streamlit run app/app.py
```

La app queda en `http://localhost:8501`.

---

## Despliegue en Streamlit Cloud

1. Sube el repositorio a GitHub con visibilidad **pública**.
2. Asegúrate de incluir los archivos `.pkl` generados en `models/` (pesan menos de 5 MB).
3. Entra a [streamlit.io/cloud](https://streamlit.io/cloud), conecta tu GitHub y haz clic en **New app**.
4. Selecciona repo, rama `main`, archivo `app/app.py`.
5. Haz clic en **Deploy**.

---

## Estructura del proyecto

```
rain-australia-pca/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/                # weatherAUS.csv (descargar de Kaggle)
│   └── processed/          # gráficos generados por el notebook
│
├── notebooks/
│   └── 01_training.ipynb   # entrenamiento completo paso a paso
│
├── models/
│   ├── scaler.pkl
│   ├── pca.pkl
│   ├── classifier.pkl
│   ├── feature_ranges.pkl
│   └── feature_names.pkl
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   └── predict.py
│
├── app/
│   └── app.py
│
└── docs/
    └── presentacion.pdf
```

---

## Uso de la aplicación

La app tiene tres pestañas de entrada (Temperatura y Lluvia, Viento y Presión, Humedad y Nubosidad). Puedes ingresar los valores manualmente o cargar uno de los casos de ejemplo (día seco típico en Sydney o día lluvioso en Melbourne). Después de hacer clic en **Predecir**, el sistema muestra si lloverá mañana, la probabilidad de cada clase, los componentes PCA más influyentes y la posición de la observación en el espacio de componentes principales.

---

## Buenas prácticas MLOps

- `random_state=42` en todos los pasos para reproducibilidad.
- El scaler y el PCA se ajustan solo sobre el conjunto de entrenamiento, nunca sobre test.
- `class_weight='balanced'` para manejar el desbalance de clases (77% / 23%).
- Artefactos del pipeline serializados por separado para facilitar actualizaciones individuales.
- `requirements.txt` con versiones fijas.
- Validación cruzada 5-fold en adición al split train/test.

---

## Autores

- **Integrante 1** — modelo y notebook
- **Integrante 2** — app web y despliegue
- **Integrante 3** — documentación y presentación

*Fundación Universitaria Los Libertadores — Inteligencia Artificial I, 2024*

---

## Licencia

MIT

---

## Referencias

- Young, J. (2017). *Rain in Australia* [Dataset]. Kaggle. https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package
- Bureau of Meteorology, Australia. http://www.bom.gov.au/climate/data/
- Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825-2830.
- Streamlit Inc. (2023). *Streamlit documentation*. https://docs.streamlit.io
