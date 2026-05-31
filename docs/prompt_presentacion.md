# Prompt para Claude Design — Presentación Actividad 3 IA I

---

## OBJETIVO

Crear una presentación de **15 diapositivas** en PowerPoint (.pptx) para la
Actividad 3 de Inteligencia Artificial I. El tema es el proyecto
"Predicción de Lluvia en Australia con PCA".

La presentación debe combinar el sistema de diseño del archivo de referencia
(azul y blanco, estilo moderno limpio) con contenido técnico real del proyecto.

---

## SISTEMA DE DISEÑO (extraído del PDF de referencia)

### Tipografías
| Uso | Fuente | Peso | Tamaño aprox. |
|---|---|---|---|
| Títulos principales de sección | Anton | Regular | 60–80 pt |
| Subtítulos y etiquetas | Helvetica Neue | Bold | 14–18 pt |
| Cuerpo de texto | Helvetica Neue | Regular | 12–16 pt |
| Texto de portada | Anton | Regular | 80–100 pt |

> Si Anton no está disponible en PowerPoint, usar **Oswald Bold** como
> sustituto. Para Helvetica Neue, usar **Arial**.

### Paleta de colores
| Elemento | Color | Hex |
|---|---|---|
| Azul principal (títulos) | Azul medio | `#3B85BC` |
| Fondo blanco | Blanco puro | `#FDFDFD` |
| Texto cuerpo | Negro suave | `#171717` |
| Acento / líneas | Azul claro | `#5BA3D9` |
| Fondo panel oscuro | Azul marino | `#0D2137` |

### Layout general (basado en el PDF de referencia)
- **Diapositivas de contenido**: panel de imagen fotográfica a la izquierda
  (40% del ancho), área de texto a la derecha (60%)
- **Diapositivas de datos/técnicas**: fondo blanco, título en azul `#3B85BC`
  con fuente Anton en la parte superior izquierda, contenido en bloques
- **Línea decorativa**: línea horizontal delgada en `#3B85BC` debajo del título
  en diapositivas de contenido
- Márgenes internos: 2 cm en todos los lados en el área de texto
- Sin sombras, sin efectos 3D — diseño plano y limpio

---

## DATOS DEL PROYECTO (usar exactamente estos valores)

- **Proyecto**: Predicción de Lluvia en Australia
- **Algoritmo**: PCA como preprocesamiento para clasificación
- **Dataset**: Rain in Australia — Kaggle (jsphyg/weather-dataset-rattle-package)
- **Tamaño dataset**: 145,460 registros × 23 columnas | 10 años | 49 estaciones
- **Features usadas**: 17 variables meteorológicas
- **Componentes PCA**: 17 → 11 componentes (95.18% varianza preservada)
- **Pipeline**: StandardScaler → PCA(n_components=0.95) → LogisticRegression(class_weight='balanced')
- **Desbalance de clases**: No lluvia 77.7% / Lluvia 22.3%

### Métricas reales (conjunto de prueba 20% estratificado)
| Métrica | Valor |
|---|---|
| Accuracy | 76.97% |
| Precision | 49.12% |
| Recall | 76.27% |
| F1-Score | 59.75% |
| ROC-AUC | 0.8492 |

### URLs
- **App desplegada**: https://pca-lluvia-australiagit-me6beprsvy7wgcnfkgnbsa.streamlit.app
- **GitHub**: https://github.com/blinaresv/pca-lluvia-australia

### Equipo — Grupo 3
- Integrante 1 — Modelo y notebook
- Integrante 2 — App web y despliegue
- Integrante 3 — Documentación y presentación
- **Institución**: Fundación Universitaria Los Libertadores
- **Materia**: Inteligencia Artificial I — 2024

---

## ESPECIFICACIÓN SLIDE POR SLIDE

---

### SLIDE 1 — PORTADA

**Layout**: Fondo dividido. Panel izquierdo (50%): foto de Australia (cielo
nublado / lluvia / paisaje verde australiano). Panel derecho (50%): fondo
`#0D2137` (azul marino oscuro).

**Contenido panel derecho (sobre fondo azul marino)**:
```
[Línea pequeña en #3B85BC arriba]

PREDICCIÓN DE
LLUVIA EN
AUSTRALIA

[fuente Anton, blanco #FDFDFD, 60 pt, todo mayúsculas]

──────────────────  [línea #3B85BC, 2px]

PCA como preprocesamiento para clasificación
[Helvetica Neue Bold, blanco, 14 pt]

Grupo 3 | Inteligencia Artificial I
Fundación Universitaria Los Libertadores — 2024
[Helvetica Neue Regular, blanco 70% opacidad, 12 pt]

🔗 App: pca-lluvia-australiagit-me6beprsvy7wgcnfkgnbsa.streamlit.app
🔗 GitHub: github.com/blinaresv/pca-lluvia-australia
[Helvetica Neue Regular, #5BA3D9, 10 pt]
```

**Imagen sugerida**: Fotografía de lluvia sobre paisaje australiano u operador
meteorológico / cielo con nubes dramáticas sobre el outback.

---

### SLIDE 2 — PROBLEMA

**Layout**: Título Anton en `#3B85BC` arriba. Fondo blanco. Tres bloques de
contenido en fila horizontal (cada bloque con ícono arriba, título bold,
descripción regular).

**Título**: `EL PROBLEMA`

**Bloque 1 — ¿Qué problema resuelve?**
```
Título bloque: "Predicción meteorológica"
Texto: Predecir si lloverá al día siguiente en Australia
a partir de las condiciones observadas durante el
día actual. Un problema de clasificación binaria
(RainTomorrow: Sí / No).
```

**Bloque 2 — ¿Por qué es importante?**
```
Título bloque: "Impacto real"
Texto: Australia sufre sequías e inundaciones que
afectan agricultura, infraestructura y seguridad.
Predecir lluvia con 24 h de anticipación permite
tomar decisiones preventivas.
```

**Bloque 3 — ¿Por qué PCA?**
```
Título bloque: "Alta redundancia de datos"
Texto: Las 17 variables meteorológicas están
fuertemente correlacionadas entre sí
(Temp9am ↔ Temp3pm: r = 0.97).
PCA elimina esa redundancia antes de clasificar.
```

**Nota de imagen**: Barra lateral derecha (15% ancho) con franja de foto de
Australia o mapa meteorológico — decorativa.

---

### SLIDE 3 — DATASET

**Layout**: Título Anton arriba en `#3B85BC`. Mitad izquierda: tabla de datos.
Mitad derecha: imagen representativa + estadística destacada.

**Título**: `DATASET — RAIN IN AUSTRALIA`

**Contenido izquierdo**:
```
Fuente:  Kaggle — jsphyg/weather-dataset-rattle-package
Período: 10 años de registros diarios
Estaciones: 49 en todo el territorio australiano
Registros: 145,460 observaciones × 23 columnas
Features usadas: 17 variables meteorológicas

Features seleccionadas:
MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine,
WindGustSpeed, WindSpeed9am, WindSpeed3pm,
Humidity9am, Humidity3pm, Pressure9am, Pressure3pm,
Cloud9am, Cloud3pm, Temp9am, Temp3pm, RainToday

Variable objetivo: RainTomorrow (Sí / No)
```

**Contenido derecho — estadísticas visuales** (cajas destacadas):
```
┌─────────────────┐  ┌─────────────────┐
│   145,460       │  │    77.7%        │
│   registros     │  │  No lluvia      │
└─────────────────┘  └─────────────────┘
┌─────────────────┐  ┌─────────────────┐
│   49            │  │    22.3%        │
│   estaciones    │  │   Lluvia        │
└─────────────────┘  └─────────────────┘
```
Cajas con fondo `#3B85BC`, texto blanco, número grande en Anton.

---

### SLIDE 4 — ALGORITMO PCA (Fundamentos)

**Layout**: Fondo blanco. Título Anton en `#3B85BC`. Diagrama de flujo central
del pipeline + explicación en bloques.

**Título**: `ALGORITMO — PCA`

**Diagrama de pipeline** (horizontal, centrado):
```
[Datos crudos]  →  [StandardScaler]  →  [PCA]  →  [LogisticRegression]  →  [Predicción]
  17 features       media=0, std=1     11 comps    class_weight=balanced    Lluvia / No
```
Cada caja con fondo `#3B85BC`, flechas en `#5BA3D9`.

**Tres columnas debajo del diagrama**:
```
Col 1 — StandardScaler
Por qué: PCA es sensible a la escala.
Variables en distintas unidades (hPa vs °C)
dominarían los componentes por magnitud,
no por varianza informativa.

Col 2 — PCA (n_components=0.95)
Encuentra las direcciones de máxima varianza.
Proyecta 17 variables correlacionadas a
11 componentes ortogonales independientes.
Preserva 95.18% de la varianza original.

Col 3 — LogisticRegression
Clasifica en el espacio reducido.
class_weight='balanced' compensa el
desbalance 77.7%/22.3% entre clases.
Frontera de decisión lineal en espacio PCA.
```

---

### SLIDE 5 — ENTRENAMIENTO Y MÉTRICAS

**Layout**: Fondo blanco. Título Anton. Mitad izquierda: tabla de métricas con
color. Mitad derecha: insight sobre PCA + reducción de dimensionalidad.

**Título**: `RESULTADOS DEL MODELO`

**Tabla de métricas izquierda**:
```
┌─────────────┬───────────┬────────────────────────────────┐
│ Métrica     │  Valor    │  Interpretación                │
├─────────────┼───────────┼────────────────────────────────┤
│ Accuracy    │  76.97%   │  Correctos sobre total         │
│ Precision   │  49.12%   │  De los que predice lluvia,    │
│             │           │  cuántos realmente llueven     │
│ Recall      │  76.27%   │  De los días lluviosos reales, │
│             │           │  cuántos detecta el modelo     │
│ F1-Score    │  59.75%   │  Balance precision–recall      │
│ ROC-AUC     │  0.8492   │  Discriminación entre clases   │
└─────────────┴───────────┴────────────────────────────────┘
```

**Bloque derecho**:
```
REDUCCIÓN DE DIMENSIONALIDAD

    17 features  →  11 componentes
         ↓
    35.3% menos dimensiones
    95.18% varianza preservada

Correlación entre componentes: ≈ 0.000000
(ortogonalidad garantizada por PCA)

Validación cruzada 5-fold:
  F1: 0.5954 ± 0.0022
  ROC-AUC: 0.8470 ± 0.0022
```

**Nota**: Resaltar ROC-AUC = 0.849 y Recall = 76.27% como métricas clave
(en meteorología preferimos avisar lluvia aunque sea falsa alarma).

---

### SLIDE 6 — PCA: VARIANZA EXPLICADA

**Layout**: Fondo blanco. Título Anton. Imagen del scree plot (gráfica de
varianza) ocupando 60% central. Texto explicativo a los lados.

**Título**: `PCA — VARIANZA EXPLICADA`

**Imagen central**: Scree plot + varianza acumulada (doble panel) generado por
el notebook. Archivo: `data/processed/pca_variance.png`.
Si no está disponible, describir: "Insertar aquí la imagen
pca_variance.png del proyecto".

**Texto izquierdo** (vertical, pequeño):
```
17 variables
originales con alta
correlación entre sí
↓
PCA detecta las
direcciones de
máxima varianza
```

**Texto derecho**:
```
Con solo 11 componentes
el modelo ya captura
el 95.18% de toda la
información del dataset.

Los 6 componentes
descartados solo
aportan el 4.82% de
varianza — ruido
estadístico.
```

---

### SLIDE 7 — PCA: INTERPRETACIÓN DE LOADINGS

**Layout**: Fondo blanco. Título Anton. Imagen del heatmap de loadings (grande,
centrada). Leyenda explicativa debajo.

**Título**: `PCA — COMPONENTES PRINCIPALES`

**Imagen**: Heatmap de loadings `data/processed/pca_loadings.png`.
"Insertar aquí la imagen pca_loadings.png del proyecto".

**Leyenda debajo** (tres columnas):
```
PC1 (29.8% varianza)        PC2 (16.4% varianza)        PC3 (10.1% varianza)
Dominado por temperatura:   Dominado por humedad:        Dominado por viento:
+ Temp9am, Temp3pm,         + Humidity9am, Humidity3pm   + WindGustSpeed,
  MaxTemp, MinTemp            Cloud9am, Cloud3pm           WindSpeed9am/3pm
→ "Factor de temperatura"   → "Factor de humedad"        → "Factor de viento"
```

**Nota de diseño**: Los tres bloques con fondo `#3B85BC` leve (10% opacidad),
borde izquierdo grueso en `#3B85BC`.

---

### SLIDE 8 — APLICACIÓN WEB

**Layout**: Fondo blanco. Título Anton. Panel izquierdo con captura de pantalla
de la app (mockup o screenshot). Panel derecho con descripción técnica.

**Título**: `APLICACIÓN WEB`

**Panel izquierdo** (55%): Screenshot de la app Streamlit desplegada.
Caption: "App en Streamlit Cloud — interfaz de predicción".

**Panel derecho** (45%):
```
STACK TECNOLÓGICO

  Frontend:   Streamlit 1.x
  Modelo:     scikit-learn (joblib .pkl)
  Lenguaje:   Python 3.11
  Despliegue: Streamlit Cloud

FUNCIONALIDADES
  ✓ 3 pestañas de entrada (Temperatura,
    Viento/Presión, Humedad/Nubosidad)
  ✓ 2 casos de ejemplo precargados
    (Sydney verano / Melbourne invierno)
  ✓ Resultado con probabilidad por clase
  ✓ Visualización en espacio PCA
  ✓ Análisis de loadings PC1

URL:
pca-lluvia-australiagit-
me6beprsvy7wgcnfkgnbsa.streamlit.app
```

---

### SLIDE 9 — FLUJO DE LA APLICACIÓN

**Layout**: Fondo blanco. Título Anton. Diagrama de flujo vertical o horizontal
con 5 pasos numerados.

**Título**: `FLUJO DE USO`

**Diagrama de 5 pasos** (horizontal con flechas):
```
  [1]              [2]              [3]              [4]              [5]
Ingresar      Seleccionar      Hacer clic        Modelo           Ver resultado
condiciones   caso ejemplo     en PREDECIR       procesa:         + probabilidad
del día       o manual        ────────────       Scaler →         + posición PCA
actual                        ▶ Predecir         PCA →            + loadings PC1
                               mañana            LogReg
```

Cada paso en caja con fondo `#3B85BC`, número grande Anton blanco, descripción
en Helvetica Neue Regular debajo en `#171717`.

**Texto abajo**:
```
El modelo no busca en el dataset histórico — aplica lo que
aprendió de 142,193 días para evaluar el patrón actual.
Cada predicción es independiente y se calcula en tiempo real.
```

---

### SLIDE 10 — DESPLIEGUE EN LA NUBE

**Layout**: Mitad izquierda foto de Australia (paisaje, ciudad costera).
Mitad derecha fondo `#0D2137` con contenido en blanco.

**Título** (sobre fondo oscuro): `DESPLIEGUE`
Fuente Anton, color `#3B85BC`.

**Contenido derecho**:
```
SERVICIO: Streamlit Cloud
─────────────────────────

Gratuito — integración directa con GitHub
URL pública accesible 24/7
Despliega automáticamente con cada push

PROCESO DE DESPLIEGUE:
  1. Código subido a GitHub (rama main)
  2. runtime.txt: python-3.11
  3. requirements.txt con versiones fijas
  4. Conectar repo en streamlit.io/cloud
  5. Deploy con un clic → URL pública

ACCESO:
  🔗 pca-lluvia-australiagit-
     me6beprsvy7wgcnfkgnbsa.streamlit.app
```

---

### SLIDE 11 — REPOSITORIO GITHUB

**Layout**: Fondo blanco. Título Anton. Árbol de directorios a la izquierda.
Buenas prácticas a la derecha.

**Título**: `REPOSITORIO GITHUB`

**Izquierda — estructura del proyecto**:
```
pca-lluvia-australia/
│
├── README.md               ← Documentación principal
├── requirements.txt        ← Dependencias fijas
├── runtime.txt             ← Python 3.11 (Streamlit Cloud)
├── .gitignore
│
├── data/
│   ├── raw/                ← weatherAUS.csv
│   └── processed/          ← Gráficas generadas
│
├── notebooks/
│   └── 01_training.ipynb   ← Entrenamiento completo
│
├── models/
│   ├── scaler.pkl   pca.pkl   classifier.pkl
│   ├── feature_ranges.pkl  feature_names.pkl
│
├── src/
│   ├── preprocessing.py
│   └── predict.py
│
├── app/
│   └── app.py              ← App Streamlit
└── docs/
    └── presentacion.pdf
```

**Derecha — buenas prácticas MLOps**:
```
✓ random_state=42 en todos los pasos
  → Resultados reproducibles

✓ Scaler y PCA ajustados SOLO en train
  → Sin data leakage

✓ class_weight='balanced'
  → Manejo del desbalance 77/23

✓ Artefactos serializados por separado
  → Actualizaciones independientes

✓ requirements.txt con versiones fijas
  → Entorno reproducible

✓ Validación cruzada 5-fold además
  de split train/test estratificado
```

---

### SLIDE 12 — DEMOSTRACIÓN EN VIVO

**Layout**: Fondo `#0D2137`. Contenido centrado. Estilo "call to action".

**Título** (Anton, blanco, grande): `DEMO EN VIVO`

**Contenido centrado**:
```
[ícono de laptop o browser grande, en #3B85BC]

Vamos a la aplicación:

pca-lluvia-australiagit-me6beprsvy7wgcnfkgnbsa.streamlit.app

─────────────────────────────────────────────

CASOS QUE DEMOSTRAREMOS:

  Caso 1 — Día seco (Sydney, verano)
  Humedad 30%, Presión 1020 hPa, Sin lluvia hoy
  → Predicción esperada: No lloverá

  Caso 2 — Día lluvioso (Melbourne, invierno)
  Humedad 88%, Presión 1005 hPa, Llovió hoy
  → Predicción esperada: Lloverá

  Caso 3 — Valores intermedios (ingresados en vivo)
```

**Nota de diseño**: Texto en blanco sobre `#0D2137`. URL en `#5BA3D9`
destacada. Cajas de casos con borde `#3B85BC`.

---

### SLIDE 13 — DESAFÍOS Y APRENDIZAJES

**Layout**: Fondo blanco. Título Anton en `#3B85BC`. Dos columnas: desafíos a
la izquierda, aprendizajes a la derecha.

**Título**: `DESAFÍOS Y APRENDIZAJES`

**Columna izquierda — Desafíos**:
```
1. Despliegue en Python 3.14
   Streamlit Cloud usaba Python 3.14
   por defecto (sin wheels para numpy).
   Solución: runtime.txt con python-3.11.

2. Desbalance de clases 77/23
   El modelo tendía a predecir siempre
   "No lluvia". Solución: class_weight
   ='balanced' en LogisticRegression.

3. Datos faltantes masivos
   Sunshine (48%) y Evaporation (43%)
   con más del 40% de nulos.
   Solución: imputación por mediana.

4. Alta correlación entre variables
   Temp9am↔Temp3pm r=0.97 — redundancia
   estructural. Solución: ese fue
   exactamente el caso de uso de PCA.
```

**Columna derecha — Aprendizajes**:
```
✓ PCA no solo reduce dimensiones —
  explica la estructura de los datos

✓ El ROC-AUC (0.849) es más informativo
  que el Accuracy (76.97%) cuando hay
  desbalance de clases

✓ El Recall alto (76.27%) es la métrica
  más relevante en meteorología: mejor
  avisar de más que no avisar

✓ El pipeline completo (Scaler+PCA+CLF)
  debe fit solo en train para evitar
  data leakage

✓ Streamlit Cloud simplifica el ciclo
  de despliegue a menos de 5 minutos
```

---

### SLIDE 14 — TRABAJO FUTURO

**Layout**: Fondo blanco. Título Anton. Tres bloques en fila con ícono + título
+ descripción.

**Título**: `TRABAJO FUTURO`

**Bloque 1 — Modelo**:
```
Kernel PCA
Explorar PCA no lineal (kernel RBF)
para capturar relaciones no lineales
entre variables meteorológicas.

Clasificador no lineal
Random Forest o XGBoost en el espacio
PCA para capturar interacciones
entre componentes.
```

**Bloque 2 — Datos**:
```
Datos en tiempo real
Conectar con la API del Bureau of
Meteorology de Australia para
predicciones con datos actuales.

Variables adicionales
Incluir dirección del viento (categórica)
y variables de presión de olas para
mejorar el Recall.
```

**Bloque 3 — Aplicación**:
```
Historial de predicciones
Guardar predicciones anteriores para
que el usuario compare condiciones
vs resultados reales.

Selector de ciudad
Permitir elegir la estación meteorológica
australiana y ajustar umbrales según
el clima local de cada región.
```

---

### SLIDE 15 — REFERENCIAS

**Layout**: Fondo blanco. Título Anton. Lista de referencias en formato IEEE,
bien espaciadas. Logo de la institución abajo a la derecha.

**Título**: `REFERENCIAS`

**Contenido** (formato IEEE, Helvetica Neue Regular 11 pt):
```
[1] J. Young, "Rain in Australia," Kaggle, 2017. [Online].
    Available: https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package

[2] Bureau of Meteorology, Australia, "Climate Data Online." [Online].
    Available: http://www.bom.gov.au/climate/data/

[3] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python,"
    J. Mach. Learn. Res., vol. 12, pp. 2825–2830, 2011.

[4] Scikit-learn Developers, "sklearn.decomposition.PCA,"
    Scikit-learn Documentation, v1.4, 2024.
    Available: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

[5] A. Hannachi, I. T. Jolliffe, and D. B. Stephenson, "Empirical orthogonal
    functions and related techniques in atmospheric science: A review,"
    Int. J. Climatol., vol. 27, no. 9, pp. 1119–1152, Jul. 2007.

[6] I. T. Jolliffe and J. Cadima, "Principal component analysis: a review
    and recent developments," Philos. Trans. R. Soc. A, vol. 374,
    Art. 20150202, Apr. 2016.

[7] Streamlit Inc., "Streamlit Documentation," 2024.
    Available: https://docs.streamlit.io
```

**Pie de slide** (centrado, pequeño):
```
Grupo 3 — Inteligencia Artificial I | Fundación Universitaria Los Libertadores — 2024
🔗 github.com/blinaresv/pca-lluvia-australia
```

---

## INSTRUCCIONES PARA CLAUDE DESIGN

1. Crear el archivo `.pptx` con exactamente 15 diapositivas en el orden indicado.
2. Usar el sistema de diseño especificado: Anton (o Oswald) para títulos,
   Helvetica Neue (o Arial) para cuerpo, colores exactos `#3B85BC`, `#0D2137`,
   `#FDFDFD`, `#171717`.
3. En slides con imagen, usar fotos de Australia relacionadas con lluvia,
   meteorología o paisajes (puedes generarlas o usar placeholders descriptivos).
4. En slides 6 y 7 (pca_variance.png y pca_loadings.png), insertar un
   placeholder con el nombre exacto del archivo — el usuario los tiene en
   `data/processed/`.
5. Cada slide debe verse balanceada — no sobrecargar de texto. Priorizar
   legibilidad sobre completitud.
6. El pie de cada slide (excepto portada y demo) debe llevar en pequeño:
   "Grupo 3 | IA I — Fundación Universitaria Los Libertadores"
7. Guardar como: `docs/presentacion_grupo3_IA1.pptx`
