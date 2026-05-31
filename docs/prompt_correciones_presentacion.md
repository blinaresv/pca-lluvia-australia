# Prompt para Claude Design — Correcciones a la Presentación
## Predicción de Lluvia en Australia — PCA (v2)

---

## CONTEXTO

Tengo una presentación en Canva de 14 diapositivas ya diseñada.
Necesito que apliques las siguientes correcciones. **NO cambies el diseño,
tipografía ni paleta de colores — solo aplica los cambios descritos aquí.**
El estilo (azul marino, blanco, Anton para títulos, Helvetica para cuerpo)
debe mantenerse exactamente igual.

---

## CORRECCIONES OBLIGATORIAS

---

### CORRECCIÓN 1 — ELIMINAR PIE DE PÁGINA DE TODAS LAS SLIDES

En la versión actual cada diapositiva lleva en la parte inferior el texto:
```
Grupo 3 · IA I — Fundación Universitaria Los Libertadores
```
**Eliminar ese pie de página de absolutamente todas las diapositivas.**
No debe aparecer en ninguna slide. La información institucional solo va
en la portada (Slide 1).

---

### CORRECCIÓN 2 — SLIDE 1 (PORTADA): CORREGIR URL Y NOMBRES

**URL incorrecta:** la portada muestra:
```
pca-lluvia-australia.streamlit.app    ← INCORRECTA, no funciona
```
Reemplazar con la URL real:
```
pca-lluvia-australiagit-me6beprsvy7wgcnfkgnbsa.streamlit.app
```
Esta misma URL correcta debe aparecer también en la **Slide 12 (Demo)**.

**Nombres del equipo** — verificar que los tres integrantes aparezcan
correctamente en la portada (sin duplicados):
```
Brandon Felipe Linares Viasus
Adriana Lucia Carreño Medina
Sariath Eyleen Xiomara Ariza Vargas
```
Si algún nombre aparece duplicado, conservar solo una vez cada uno.

---

### CORRECCIÓN 3 — SLIDE 5 (MÉTRICAS): TABLA DESORDENADA

La tabla de resultados del modelo migró a Canva con tamaños inconsistentes
(algunas celdas muy pequeñas, otras muy grandes). Reconstruir la tabla con
tamaño uniforme:

| Métrica | Valor | Interpretación |
|---|---|---|
| Accuracy | 76.97% | Correctos sobre el total |
| Precision | 49.12% | De lo predicho como lluvia, cuánto acierta |
| Recall | 76.27% | De los días lluviosos reales, cuántos detecta |
| F1-Score | 59.75% | Balance precision–recall |
| ROC-AUC | 0.8492 | Discriminación entre clases |

Reglas de formato para la tabla:
- Todas las filas deben tener la misma altura
- Encabezado con fondo `#3B85BC`, texto blanco, Helvetica Neue Bold 12 pt
- Filas alternas: fondo blanco / fondo `#EBF4FB` (azul muy claro)
- Texto cuerpo: Helvetica Neue Regular 11 pt, color `#171717`
- Ancho de columnas proporcional: Métrica 20% | Valor 15% | Interpretación 65%

---

### CORRECCIÓN 4 — AGREGAR SLIDE "TRABAJO FUTURO" (OBLIGATORIA)

El profesor exige explícitamente esta diapositiva en la guía de la actividad.
**Insertarla como Slide 14, justo antes de Referencias (que pasa a ser Slide 15).**

**Título**: `TRABAJO FUTURO`
**Subtítulo de sección** (letras espaciadas, azul): `P R Ó X I M O S  P A S O S`

**Layout**: Tres bloques en fila con el mismo diseño visual de las otras slides
de contenido. Cada bloque: ícono arriba + título en bold + texto regular.

```
BLOQUE 1 — MODELO
Título: "Mejorar el clasificador"
• Kernel PCA: explorar PCA no lineal
  (kernel RBF) para capturar relaciones
  no lineales entre variables.
• Random Forest o XGBoost en el espacio
  PCA para capturar interacciones entre
  componentes principales.

BLOQUE 2 — DATOS
Título: "Datos en tiempo real"
• Conectar con la API del Bureau of
  Meteorology de Australia para
  predicciones con datos actuales
  (no históricos).
• Incluir dirección del viento como
  variable categórica codificada.

BLOQUE 3 — APLICACIÓN
Título: "Evolución de la app"
• Historial de predicciones: comparar
  predicciones anteriores con lo que
  realmente ocurrió.
• Selector de ciudad/estación para
  ajustar umbrales según el clima
  local de cada región australiana.
```

---

### CORRECCIÓN 5 — CITACIÓN OBLIGATORIA DE TODAS LAS IMÁGENES

**Regla del curso:** toda imagen debe llevar su fuente citada, incluso las
generadas por el propio equipo.

En cada slide que contenga una imagen, agregar debajo de ella un caption
pequeño (Helvetica Neue Regular, 8 pt, color `#888888`, itálica) con la
fuente correspondiente:

**Para fotos de Australia (imágenes decorativas / paisajes):**
```
Fuente: [nombre del banco de imágenes, p. ej. Unsplash / Pexels / Freepik].
Licencia: [CC0 / licencia del sitio].
```

**Para todas las gráficas generadas por el proyecto**
(pca_variance.png, pca_loadings.png, model_evaluation.png, class_distribution.png,
cualquier otra del notebook):
```
Elaboración propia. Generado con scikit-learn y matplotlib sobre el dataset
Rain in Australia [1]. Python 3.11, 2026.
```
donde [1] refiere a la referencia del dataset en la slide de bibliografía.

**Para capturas de pantalla de la aplicación web:**
```
Captura propia de la aplicación desplegada en Streamlit Cloud.
github.com/blinaresv/pca-lluvia-australia, 2026.
```

---

### CORRECCIÓN 6 — PLACEHOLDERS PARA IMÁGENES DEL PROYECTO

En las siguientes slides dejar un placeholder visible (caja con borde
punteado `#3B85BC`, fondo `#EBF4FB`, texto centrado en gris):

**Slide 6 — PCA Varianza Explicada:**
```
┌─────────────────────────────────────┐
│  [Insertar: pca_variance.png]       │
│  Scree plot + varianza acumulada    │
│  — archivo provisto por el equipo   │
└─────────────────────────────────────┘
```
Caption bajo el placeholder:
```
Elaboración propia. Generado con scikit-learn y matplotlib
sobre el dataset Rain in Australia [1]. Python 3.11, 2026.
```

**Slide 7 — PCA Loadings:**
```
┌─────────────────────────────────────┐
│  [Insertar: pca_loadings.png]       │
│  Heatmap de loadings primeros       │
│  6 componentes principales          │
│  — archivo provisto por el equipo   │
└─────────────────────────────────────┘
```
Caption:
```
Elaboración propia. Generado con scikit-learn y matplotlib
sobre el dataset Rain in Australia [1]. Python 3.11, 2026.
```

**Slide 5 — Resultados del modelo** (opcional pero recomendado):
```
┌─────────────────────────────────────┐
│  [Insertar: model_evaluation.png]   │
│  Matriz de confusión + curva ROC    │
│  — archivo provisto por el equipo   │
└─────────────────────────────────────┘
```
Caption:
```
Elaboración propia. Generado con scikit-learn y matplotlib
sobre el dataset Rain in Australia [1]. Python 3.11, 2026.
```

---

## RESUMEN DE CAMBIOS EN ORDEN

| # | Qué cambiar | Slide afectada |
|---|---|---|
| 1 | Eliminar pie "Grupo 3 · IA I…" | Todas |
| 2 | Corregir URL de la app | Slide 1 y Slide 12 |
| 3 | Verificar nombres sin duplicados | Slide 1 |
| 4 | Reconstruir tabla de métricas uniforme | Slide 5 |
| 5 | Agregar placeholders con caption de fuente | Slides 5, 6, 7 |
| 6 | Agregar captions de fuente a fotos decorativas | Todas las que tengan foto |
| 7 | Agregar caption a capturas de app | Slide 8 |
| 8 | Insertar slide nueva "Trabajo Futuro" | Nueva Slide 14 |
| 9 | Referencias pasa a Slide 15 | Reordenar numeración |

---

## LO QUE NO DEBES CAMBIAR

- Diseño general, colores (`#3B85BC`, `#0D2137`, `#FDFDFD`, `#171717`)
- Tipografías (Anton para títulos, Helvetica Neue para cuerpo)
- Contenido de texto en slides que no se mencionen arriba
- Estructura de layout de cada slide
- Diapositiva de demostración en vivo (Slide 12) — solo corregir la URL

---

## NOTA FINAL

El equipo entregará las imágenes del proyecto
(pca_variance.png, pca_loadings.png, model_evaluation.png)
para insertarlas en los placeholders. Los espacios deben quedar
listos para recibir esas imágenes sin alterar el layout.
