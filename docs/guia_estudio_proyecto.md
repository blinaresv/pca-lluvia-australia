# Guía de Estudio — Predicción de Lluvia en Australia con PCA
## Para entender y defender el proyecto en la exposición

---

## 1. El problema que resolvemos

**Pregunta central:** ¿Va a llover mañana en Australia?

Esto es un problema de **clasificación binaria** — la respuesta es Sí o No. Le damos al modelo datos meteorológicos del día de hoy (temperatura, humedad, viento, presión, etc.) y el modelo predice si mañana lloverá.

**¿Por qué es difícil?**
- El clima tiene muchas variables (17 en nuestro caso)
- Muchas de esas variables están correlacionadas entre sí (si sube la temperatura máxima, la temperatura mínima también tiende a subir)
- Esa redundancia dificulta el entrenamiento del modelo

**La solución:** aplicar PCA para limpiar esa redundancia antes de entrenar.

---

## 2. El dataset

**Nombre:** Rain in Australia (Kaggle)
**Filas:** ~145,000 registros de estaciones meteorológicas de toda Australia
**Variables originales:** 23 columnas en crudo → usamos 17 tras la limpieza

Las 17 variables que usamos son:

| Variable | Qué mide |
|---|---|
| MinTemp | Temperatura mínima del día |
| MaxTemp | Temperatura máxima del día |
| Rainfall | Milímetros de lluvia ese día |
| Evaporation | Evaporación |
| Sunshine | Horas de sol |
| WindGustSpeed | Velocidad del golpe de viento más fuerte |
| WindSpeed9am | Velocidad del viento a las 9am |
| WindSpeed3pm | Velocidad del viento a las 3pm |
| Humidity9am | Humedad a las 9am |
| Humidity3pm | Humedad a las 3pm |
| Pressure9am | Presión atmosférica a las 9am |
| Pressure3pm | Presión atmosférica a las 3pm |
| Cloud9am | Nubosidad a las 9am |
| Cloud3pm | Nubosidad a las 3pm |
| Temp9am | Temperatura a las 9am |
| Temp3pm | Temperatura a las 3pm |
| RainToday | ¿Llovió hoy? (Sí/No) |

**Variable objetivo:** `RainTomorrow` — ¿Lloverá mañana?

---

## 3. El algoritmo PCA — qué hace en este proyecto

### Idea simple
PCA toma las 17 variables originales (que están correlacionadas) y las convierte en **componentes nuevas, independientes entre sí**, ordenadas de mayor a menor importancia.

### Lo que encontró PCA en nuestros datos
Con 11 componentes se captura el **95.18%** de toda la información. Los 6 restantes solo aportan el 4.82% — básicamente ruido.

### Los tres componentes más importantes

**PC1 — Factor de Temperatura (29.8% de la varianza)**
- Las variables que más pesan: Temp9am, Temp3pm, MaxTemp, MinTemp
- Interpret.: cuando PC1 es alto → día caluroso; cuando es bajo → día frío

**PC2 — Factor de Humedad (16.4% de la varianza)**
- Las variables que más pesan: Humidity9am, Humidity3pm, Cloud9am, Cloud3pm
- Interpret.: cuando PC2 es alto → día húmedo y nublado

**PC3 — Factor de Viento (10.1% de la varianza)**
- Las variables que más pesan: WindGustSpeed, WindSpeed9am, WindSpeed3pm
- Interpret.: cuando PC3 es alto → día ventoso

### ¿Por qué aplicar PCA antes de entrenar?
1. Elimina la correlación entre variables (el modelo aprende mejor)
2. Reduce ruido estadístico (el 4.82% descartado)
3. Reduce dimensiones de 17 a 11 sin perder información importante

---

## 4. El modelo de clasificación

Después de aplicar PCA, entrenamos un **clasificador** (Regresión Logística) con los 11 componentes.

### Preprocesamiento aplicado antes de PCA
1. **Imputación** — rellenar valores faltantes (mediana para numéricas)
2. **Escalado** — StandardScaler para que todas las variables estén en la misma escala (PCA es sensible a la escala)
3. **PCA** — reducir de 17 a 11 componentes
4. **Clasificador** — Regresión Logística sobre los 11 componentes

### Validación
- **Split train/test:** 80% entrenamiento, 20% prueba, estratificado (mantiene la proporción de clases)
- **Validación cruzada:** 5-fold CV para asegurar que los resultados son estables

---

## 5. Las métricas — qué significan y cómo defenderlas

### Accuracy: 76.97%
- **Definición:** de todos los días, ¿en qué porcentaje predijo bien?
- **Cómo defenderlo:** supera el umbral mínimo del curso (70%). Para clima, 77% es un resultado sólido dado el ruido inherente del fenómeno.

### Precision: 49.12%
- **Definición:** de todos los días que el modelo dijo "va a llover", ¿en qué porcentaje realmente llovió?
- **Por qué es baja:** el dataset está desbalanceado — llueve mucho menos de lo que no llueve. El modelo a veces "alerta" lluvia cuando no la hay.
- **Cómo defenderlo:** en meteorología, un falso positivo (predecir lluvia cuando no llueve) es menos peligroso que un falso negativo. El recall es la métrica más crítica aquí.

### Recall: 76.27%
- **Definición:** de todos los días que realmente llovió, ¿qué porcentaje detectó el modelo?
- **Cómo defenderlo:** el modelo detecta 3 de cada 4 días lluviosos reales. Para una aplicación práctica de alertas, esto es lo más valioso.

### F1-Score: 59.75%
- **Definición:** media armónica entre Precision y Recall. Balance entre los dos.
- **Cómo defenderlo:** refleja la dificultad del dataset desbalanceado, pero el recall alto (lo importante) compensa.

### ROC-AUC: 0.8492
- **Definición:** qué tan bien distingue el modelo entre "lluvia" y "no lluvia" en general, independientemente del umbral de decisión.
- **Cómo defenderlo:** 0.85 es considerado "bueno" (0.5 = aleatorio, 1.0 = perfecto). Es la métrica más robusta para datasets desbalanceados.

---

## 6. Los archivos serializados (.pkl)

El modelo se guarda en 5 archivos para poder usarlo en la app sin reentrenar:

| Archivo | Qué contiene |
|---|---|
| `scaler.pkl` | El StandardScaler ajustado al train |
| `pca.pkl` | El modelo PCA ajustado al train |
| `classifier.pkl` | El clasificador (Regresión Logística) entrenado |
| `feature_names.pkl` | Los nombres de las 17 variables en orden correcto |
| `feature_ranges.pkl` | Los rangos válidos de cada variable (para validar inputs) |

**Proceso de predicción en la app:**
```
Input del usuario
    → Escalado con scaler.pkl
    → Transformación PCA con pca.pkl
    → Predicción con classifier.pkl
    → Resultado + probabilidades
```

---

## 7. La aplicación Streamlit

### Qué hace la app
1. El usuario ingresa 17 valores meteorológicos (distribuidos en 3 pestañas)
2. La app valida que los valores estén en rangos razonables
3. Aplica el pipeline completo (scaler → pca → classifier)
4. Muestra: predicción (Sí/No), probabilidades por clase, posición en espacio PCA, loadings del PC1

### Los 3 tabs de la app
- **Tab 1:** Temperatura y lluvia (MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine)
- **Tab 2:** Viento (WindGustSpeed, WindSpeed9am/3pm)
- **Tab 3:** Humedad, presión y nubosidad (Humidity, Pressure, Cloud, Temp9am/3pm, RainToday)

### Dónde está desplegada
```
pca-lluvia-australiagit-me6beprsvy7wgcnfkgnbsa.streamlit.app
```

### Repositorio
```
github.com/blinaresv/pca-lluvia-australia
```

---

## 8. Preguntas que puede hacer el profesor — y cómo responderlas

**"¿Por qué usaron PCA y no directamente Regresión Logística sobre las 17 variables?"**
> PCA elimina la multicolinealidad entre variables. La Regresión Logística asume que los predictores son independientes; si están correlacionados, las estimaciones son inestables. PCA garantiza componentes ortogonales (independientes) y además reduce ruido.

**"¿Por qué el Precision es bajo?"**
> El dataset está desbalanceado — aproximadamente 78% de los días no llueve y 22% sí. El modelo aprende a ser conservador y solo predice lluvia cuando hay señales claras, lo que baja el Precision. Priorizamos el Recall porque en contexto meteorológico es más costoso no detectar lluvia que generar una falsa alarma.

**"¿Cómo eligieron 11 componentes?"**
> Usamos el criterio del 95% de varianza explicada acumulada. Con el scree plot vimos que en 11 componentes se alcanza el 95.18%. Los 6 restantes solo aportan 4.82% y añaden ruido sin información útil.

**"¿Qué significa PC1 en términos reales?"**
> PC1 es una combinación lineal de las variables originales que captura el 29.8% de la variación total. Las variables con mayor peso son las de temperatura (Temp9am, Temp3pm, MaxTemp, MinTemp), así que PC1 representa principalmente el "nivel térmico" del día.

**"¿Podría mejorar el modelo?"**
> Sí. Como trabajo futuro identificamos: usar Kernel PCA para capturar relaciones no lineales, probar Random Forest o XGBoost en el espacio PCA, y conectar con datos en tiempo real de la API del Bureau of Meteorology de Australia.

**"¿Por qué Streamlit y no Flask?"**
> Para el alcance del proyecto Streamlit es la herramienta más adecuada: despliegue gratuito, sin configuración de servidor, y permite construir una interfaz funcional en pocas líneas de código. Flask añadiría complejidad de HTML/CSS/rutas sin beneficio para este caso de uso.

---

## 9. Conceptos clave para memorizar

| Concepto | Definición de 1 frase |
|---|---|
| PCA | Técnica que convierte variables correlacionadas en componentes independientes ordenados por varianza |
| Varianza explicada | Porcentaje de información que captura cada componente |
| Scree plot | Gráfico que muestra cuánta varianza acumula cada componente |
| Loadings | El peso de cada variable original dentro de cada componente |
| StandardScaler | Normaliza las variables para que tengan media 0 y desviación 1 |
| Clasificación binaria | Predecir una de dos clases (en este caso: llueve / no llueve) |
| ROC-AUC | Métrica que mide la capacidad discriminatoria del modelo (0.5 = aleatorio, 1 = perfecto) |
| Recall | De todos los positivos reales, ¿cuántos detecta el modelo? |
| Overfitting | Cuando el modelo aprende de memoria el train y falla en datos nuevos |
| Validación cruzada | Técnica para estimar el desempeño real del modelo con múltiples splits |
