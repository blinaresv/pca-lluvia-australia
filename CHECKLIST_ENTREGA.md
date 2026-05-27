# Checklist de Entrega — Actividad 3 IA1
**Proyecto:** Predictor de Lluvia en Australia con PCA  
**Grupo:** 3 — Algoritmo: PCA como preprocesamiento para clasificación  
**Institución:** Fundación Universitaria Los Libertadores — IA I, 2024

---

## Entrega 1 — Asesoría (30% = 15 pts)

| Criterio | Estado | Notas |
|---|---|---|
| Tema asignado identificado | ✅ | PCA como preprocesamiento |
| Fuente de datos real seleccionada | ✅ | Rain in Australia (Kaggle) |
| URL del dataset documentada | ✅ | https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package |
| Justificación del dataset | ✅ | Variables meteorológicas altamente correlacionadas → PCA ideal |
| Algoritmo explicado conceptualmente | ✅ | README sección "Algoritmo utilizado" |
| Pipeline definido | ✅ | StandardScaler → PCA(95%) → LogisticRegression(balanced) |

---

## Entrega 2 — Repositorio + Documentación (40% = 20 pts)

### Repositorio GitHub
| Criterio | Estado | Notas |
|---|---|---|
| Repositorio público creado | ✅ | https://github.com/blinaresv/pca-lluvia-australia |
| Estructura de carpetas correcta | ✅ | data/, notebooks/, models/, src/, app/, docs/ |
| `.gitignore` configurado | ✅ | Excluye venv, __pycache__, data/raw/*.csv, .DS_Store |
| `requirements.txt` con versiones fijas | ✅ | numpy, pandas, sklearn, streamlit, matplotlib, seaborn, joblib, jupyter |
| `README.md` completo | ✅ | Descripción, algoritmo, dataset, instalación, despliegue, estructura |

### Notebook de entrenamiento (`notebooks/01_training.ipynb`)
| Criterio | Estado | Notas |
|---|---|---|
| Carga del dataset | ✅ | Lee weatherAUS.csv desde data/raw/ |
| EDA — valores nulos | ✅ | Celda "Información general" |
| EDA — distribución de clases | ✅ | Gráficos barras + pie, guardados en data/processed/ |
| EDA — distribuciones por variable | ✅ | Histogramas por clase para 10 variables clave |
| EDA — outliers (IQR) | ✅ | Sección 2.4 — boxplots y tabla de porcentajes |
| EDA — correlaciones | ✅ | Heatmap completo 16×16, evidencia para PCA |
| Preprocesamiento | ✅ | Codificación binaria, imputación mediana, split estratificado |
| Estandarización (solo en train) | ✅ | StandardScaler.fit solo sobre X_train |
| Aplicación de PCA | ✅ | PCA(n_components=0.95), gráficas de varianza explicada |
| Visualización PCA | ✅ | Scatter PC1 vs PC2, varianza acumulada |
| Entrenamiento | ✅ | LogisticRegression(class_weight='balanced') |
| Validación cruzada | ✅ | cross_val_score 5-fold con F1 |
| Métricas de evaluación | ✅ | Accuracy, Precision, Recall, F1, ROC-AUC |
| Matriz de confusión | ✅ | Heatmap seaborn |
| Curva ROC | ✅ | Con área bajo la curva |
| Serialización de artefactos | ✅ | scaler.pkl, pca.pkl, classifier.pkl, feature_ranges.pkl, feature_names.pkl |
| random_state=42 en todo | ✅ | Reproducibilidad garantizada |

### Módulos de código (`src/`)
| Criterio | Estado | Notas |
|---|---|---|
| `preprocessing.py` | ✅ | load_dataset, preprocess, prepare_single_input |
| `predict.py` | ✅ | load_pipeline, predict — terminología lluvia/sin lluvia |
| `__init__.py` | ✅ | Exporta ALL_FEATURES, load_pipeline, predict |

### Aplicación web (`app/app.py`)
| Criterio | Estado | Notas |
|---|---|---|
| Interfaz Streamlit funcional | ✅ | 3 pestañas de entrada, sidebar con info del modelo |
| Casos de ejemplo precargados | ✅ | Sydney verano (seco) + Melbourne invierno (lluvioso) |
| Predicción con resultado visual | ✅ | Caja coloreada Llueve/No llueve + probabilidad |
| Gráfico de probabilidades | ✅ | Barras con porcentajes |
| Panel PCA | ✅ | Componentes usados, varianza preservada, top loadings PC1 |
| Scatter en espacio PCA | ✅ | Posición de la observación respecto a patrones históricos |
| Manejo de error si no hay modelos | ✅ | Mensaje claro con instrucciones para correr el notebook |

### Buenas prácticas MLOps
| Criterio | Estado | Notas |
|---|---|---|
| Sin data leakage | ✅ | Scaler y PCA fitean solo en X_train |
| Desbalance de clases manejado | ✅ | class_weight='balanced' (77% No / 23% Sí) |
| Artefactos serializados por separado | ✅ | Facilita actualización individual de componentes |
| Versiones fijas en requirements.txt | ✅ | Reproducibilidad de entorno |

---

## Entrega 3 — Demo + Exposición (30% = 15 pts)

| Criterio | Estado | Notas |
|---|---|---|
| App desplegada en Streamlit Cloud | ⏳ | Pendiente — ver guía de despliegue en README |
| URL pública compartida | ⏳ | Actualizar README con URL real tras deploy |
| Presentación preparada | ⏳ | Crear docs/presentacion.pdf |
| Demo en vivo funcional | ⏳ | Requiere modelos reales (correr notebook con weatherAUS.csv) |

---

## Pasos pendientes antes de la entrega final

1. **Descargar el dataset** de Kaggle y colocarlo en `data/raw/weatherAUS.csv`
2. **Correr el notebook** completo — genera los modelos .pkl reales en `models/`
3. **Desplegar en Streamlit Cloud** — conectar GitHub y seleccionar `app/app.py`
4. **Actualizar README** con la URL real de la app desplegada
5. **Crear presentación** en `docs/presentacion.pdf` (ver estructura sugerida abajo)
6. **Hacer push final** con modelos y URL actualizada

---

## Estructura sugerida para la presentación (15 slides)

1. Portada — título, integrantes, institución
2. Problema — predecir lluvia en Australia, dataset Kaggle
3. Dataset — 145k registros, 17 features, desbalance de clases
4. EDA — visualizaciones clave (distribución de clases, correlaciones)
5. Análisis de outliers — boxplots, decisión de conservarlos
6. ¿Por qué PCA? — matriz de correlación, redundancia evidenciada
7. Fundamento matemático de PCA — covarianza, eigenvalores, eigenvectores
8. Pipeline completo — StandardScaler → PCA → LogisticRegression
9. Varianza explicada — gráficas de codo, 17 → N componentes
10. Resultados del modelo — métricas, matriz de confusión, ROC-AUC
11. Validación cruzada — 5-fold F1
12. Aplicación web — capturas de pantalla de la app Streamlit
13. Demo en vivo — predecir con casos de ejemplo
14. Conclusiones — PCA redujo dimensionalidad X%, accuracy Y%
15. Referencias

---

*Documento generado automáticamente — actualizar métricas reales tras correr el notebook*
