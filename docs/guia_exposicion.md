# Guía de Exposición — Qué Decir en Cada Slide
## Predicción de Lluvia en Australia con PCA
### Tiempo total: 12 minutos · ~45 segundos por slide

> **Cómo usar esta guía:** no memorices palabra por palabra. Lee cada bloque varias veces hasta que entiendas la *idea*, luego dilo con tus propias palabras. Las frases en cursiva son transiciones para pasar a la siguiente slide.

---

## SLIDE 1 — Portada
**Tiempo estimado: 30 segundos**

> "Buenas, somos el Grupo 3 de Inteligencia Artificial. Hoy les presentamos nuestro proyecto: un sistema de predicción de lluvia para Australia usando Análisis de Componentes Principales — PCA. La idea es simple: dado el clima de hoy, ¿va a llover mañana?"

*[pasar slide]*

---

## SLIDE 2 — Introducción / Contexto
**Tiempo estimado: 45 segundos**

> "Australia es uno de los países con clima más variable del mundo — desde sequías extremas hasta inundaciones. Predecir lluvia con anticipación tiene un impacto real en agricultura, transporte y gestión de recursos hídricos.

> El problema es complejo porque el clima involucra muchas variables que interactúan entre sí, y muchas están correlacionadas. Ahí es donde entra PCA."

*[pasar slide]*

---

## SLIDE 3 — Objetivo
**Tiempo estimado: 30 segundos**

> "Nuestro objetivo es entrenar un modelo que clasifique si lloverá o no al día siguiente, usando variables meteorológicas del día actual. Y antes de entrenar, aplicamos PCA para simplificar y limpiar los datos."

*[pasar slide]*

---

## SLIDE 4 — Dataset
**Tiempo estimado: 45 segundos**

> "Trabajamos con el dataset 'Rain in Australia' de Kaggle — aproximadamente 145 mil registros de estaciones meteorológicas de todo el país. Después de limpiar los datos, quedamos con 17 variables de entrada: temperatura, humedad, presión, viento, nubosidad y si llovió ese día. La variable que queremos predecir es 'RainTomorrow' — lluvia o no lluvia."

*[pasar slide]*

---

## SLIDE 5 — Resultados del modelo
**Tiempo estimado: 60 segundos**

> "Antes de explicar cómo funciona PCA, les muestro los resultados para que tengan contexto.

> Nuestro modelo alcanzó un Accuracy del 76.97% — supera el umbral mínimo del 70% que exige la actividad. El ROC-AUC es de 0.85, lo que significa que el modelo distingue bien entre días lluviosos y secos.

> El Precision es más bajo — 49% — porque el dataset está desbalanceado: solo el 22% de los días tiene lluvia. Pero el Recall es del 76%, lo que significa que el modelo detecta 3 de cada 4 días lluviosos reales. En meteorología, eso es lo más importante: no queremos que el modelo deje pasar un día de lluvia sin detectarlo."

*[pasar slide]*

---

## SLIDE 6 — PCA: Varianza Explicada
**Tiempo estimado: 60 segundos**

> "Ahora les explico cómo funciona PCA en este proyecto. Teníamos 17 variables originales con alta correlación entre sí — por ejemplo, la temperatura máxima y mínima siempre se mueven juntas.

> PCA detecta esas correlaciones y crea componentes nuevos, independientes entre sí, ordenados de mayor a menor importancia. Como ven en el gráfico, con solo 11 componentes capturamos el 95.18% de toda la información. Los 6 componentes restantes solo aportan el 4.82% — básicamente ruido estadístico que descartamos."

*[pasar slide]*

---

## SLIDE 7 — PCA: Loadings
**Tiempo estimado: 60 segundos**

> "¿Qué significa cada componente? El heatmap muestra el peso de cada variable original dentro de cada componente.

> PC1, que captura el 29.8% de la varianza, está dominado por las variables de temperatura — Temp9am, Temp3pm, MaxTemp, MinTemp. Podemos interpretarlo como el 'factor térmico' del día.

> PC2, con el 16.4%, concentra humedad y nubosidad — Humidity9am, Humidity3pm, Cloud. Es el 'factor de humedad'.

> PC3, con el 10.1%, refleja velocidad del viento. Así el modelo no trabaja con 17 columnas redundantes, sino con 11 factores limpios e interpretables."

*[pasar slide]*

---

## SLIDE 8 — Demo / App
**Tiempo estimado: 45 segundos**

> "La aplicación está desplegada en Streamlit Cloud y es accesible desde cualquier navegador, sin instalación. El usuario ingresa los datos meteorológicos del día — distribuidos en tres pestañas — y la app aplica automáticamente el pipeline completo: escala los datos, les aplica PCA y lanza la predicción.

> El resultado muestra si lloverá o no, con la probabilidad de cada clase."

*[si hay demo en vivo, agregar:]*
> "Vamos a abrirla ahora mismo."

*[pasar slide]*

---

## SLIDE 9 — Arquitectura / Pipeline
**Tiempo estimado: 45 segundos**

> "El pipeline tiene cuatro pasos en orden. Primero, StandardScaler normaliza las variables para que estén todas en la misma escala — PCA es sensible a esto. Segundo, PCA transforma las 17 variables en 11 componentes. Tercero, el clasificador — Regresión Logística — hace la predicción sobre esos 11 componentes. Todo el pipeline está serializado en archivos .pkl para que la app lo cargue sin reentrenar."

*[pasar slide]*

---

## SLIDE 10 — Despliegue
**Tiempo estimado: 45 segundos**

> "El código está en GitHub, el repositorio es público. El despliegue se hizo en Streamlit Cloud conectando directamente el repositorio — cualquier cambio que se suba al main se despliega automáticamente. La URL es pública, accesible 24/7, sin costo."

*[pasar slide]*

---

## SLIDE 11 — Repositorio / Estructura
**Tiempo estimado: 30 segundos**

> "La estructura del proyecto separa claramente los datos, el notebook de entrenamiento, los modelos serializados y el código de la app. El README documenta todo el proceso — instalación, uso, estructura del proyecto, dataset y referencias."

*[pasar slide]*

---

## SLIDE 12 — Demo en vivo (si aplica)
**Tiempo estimado: 60 segundos**

> "Vamos a hacer la demo. Voy a ingresar valores de un día típico en Sydney — temperatura máxima de 28 grados, humedad del 70%, sin viento fuerte... y la app nos dice que la probabilidad de lluvia mañana es del X%."

> *(Ajustar con los valores reales que muestres en la demo. Practica antes con un par de escenarios: uno donde prediga lluvia y uno donde no.)*

*[pasar slide]*

---

## SLIDE 13 — Conclusiones
**Tiempo estimado: 30 segundos**

> "En resumen: PCA nos permitió reducir 17 variables ruidosas a 11 componentes limpios, y sobre esos componentes entrenamos un clasificador que alcanza un 77% de accuracy y un ROC-AUC de 0.85. La aplicación está desplegada y funcional."

*[pasar slide]*

---

## SLIDE 14 — Trabajo Futuro
**Tiempo estimado: 30 segundos**

> "Como trabajo futuro, identificamos tres líneas: mejorar el modelo con Kernel PCA o Random Forest sobre los componentes; conectar con datos en tiempo real de la API del Bureau of Meteorology de Australia; y evolucionar la app con historial de predicciones y selector de ciudad."

*[pasar slide]*

---

## SLIDE 15 — Referencias
**Tiempo estimado: 15 segundos**

> "El dataset es público en Kaggle, las librerías usadas son scikit-learn, pandas, matplotlib y Streamlit. Las referencias completas están en esta slide y en el README del repositorio. Muchas gracias."

---

## Cierre — Preguntas del profesor

Si el profesor pregunta algo que no sabes responder en el momento:

> "Esa es una buena pregunta. No tengo el dato exacto de memoria, pero puedo mostrarte en el código / en el notebook donde se puede verificar eso."

Nunca inventes un número o resultado. Si no sabes, reconócelo y ofrece dónde buscarlo.

---

## Distribución del tiempo por bloque

| Bloque | Slides | Minutos |
|---|---|---|
| Introducción y contexto | 1–4 | ~2 min |
| Resultados | 5 | ~1 min |
| PCA (núcleo técnico) | 6–7 | ~2 min |
| App y demo | 8, 12 | ~2 min |
| Arquitectura y despliegue | 9–11 | ~2 min |
| Conclusiones y cierre | 13–15 | ~1 min |
| **Total** | | **~12 min** |

---

## Tres frases para recordar si te ponen a prueba

1. **"¿Por qué PCA?"** → *"Para eliminar la correlación entre variables antes de entrenar — el modelo aprende mejor sobre componentes independientes."*

2. **"¿Por qué el Precision es bajo?"** → *"El dataset está desbalanceado: solo el 22% de los días llueve. Priorizamos el Recall porque en clima, es más costoso no detectar lluvia que generar una falsa alarma."*

3. **"¿Cómo eligieron 11 componentes?"** → *"Usamos el criterio del 95% de varianza explicada acumulada, visible en el scree plot."*
