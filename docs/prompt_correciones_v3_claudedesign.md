# Prompt para Claude Design — Correcciones v3 de la Presentación
## Predicción de Lluvia en Australia — PCA

---

## CONTEXTO

Tengo la presentación "Predicción de Lluvia en Australia — PCA (v3 corregida)"
en Canva con 15 diapositivas. El diseño está aprobado — **NO cambiar colores,
tipografías ni estructura general**. Solo aplicar las correcciones puntuales
que se describen abajo.

---

## CORRECCIÓN 1 — AÑO: unificar todo a 2024

Hay inconsistencia de año entre slides:
- Slide 1 (portada) dice **2024** ← este es el correcto
- Slides 5, 6, 7, 8 tienen citas de imagen que dicen **2026** ← incorrecto

En todas las citas de imagen que digan "Python 3.11, 2026" cambiar a
"Python 3.11, 2024". Resultado final: todas las slides deben mostrar 2024.

---

## CORRECCIÓN 2 — ELIMINAR TEXTO DUPLICADO

En varias slides hay cajas de texto superpuestas que hacen que el mismo
texto aparezca dos veces (se ve borroso al proyectar). Revisar y eliminar
duplicados en:

- **Slide 1**: Los tres nombres del equipo aparecen duplicados.
  Dejar una sola instancia:
  ```
  Brandon Felipe Linares Viasus · Adriana Lucia Carreño Medina · Sariath Eyleen Xiomara Ariza Vargas
  ```
  También "Grupo 3 | Inteligencia Artificial I" aparece duplicado — dejar solo una vez.
  También "Fundación Universitaria Los Libertadores — 2024" aparece duplicado — dejar solo una vez.
  También "Fuente: Unsplash. Licencia: Unsplash License." aparece duplicado — dejar solo una vez.

- **Slide 10**: Los pasos del proceso de despliegue aparecen duplicados
  (1·Código en GitHub, 2·runtime.txt, etc.). Dejar cada paso una sola vez.

Revisar el resto de slides y eliminar cualquier otra caja de texto duplicada
que encuentres.

---

## CORRECCIÓN 3 — AGREGAR CITAS A FOTOS DE FONDO

Toda imagen debe tener su fuente citada. Las slides que tienen fotografía
de fondo de Australia y NO tienen cita todavía son: 2, 3, 4, 9, 13 y 14.

En cada una de esas slides agregar al pie de la fotografía (o en esquina
inferior derecha sobre la foto), en texto pequeño (8 pt, blanco o gris
claro, Helvetica Neue Regular, itálica):

```
Fuente: Unsplash. Licencia: Unsplash License.
```

Si alguna de esas slides no tiene fotografía (fondo liso), ignorarla.

---

## CORRECCIÓN 4 — SLIDE 6: HACER LA GRÁFICA MÁS GRANDE

La imagen `pca_variance.png` que se insertará en la Slide 6 queda muy
pequeña con el layout actual. Rediseñar el espacio así:

**Layout nuevo para Slide 6:**
- Panel izquierdo (30% del ancho): texto explicativo en columna angosta
  con los 4 bullets actuales, fuente 10–11 pt
- Panel derecho (68% del ancho): imagen `pca_variance.png`
  ocupando todo ese espacio, con la cita debajo

El texto de los bullets queda así (en la columna izquierda):
```
17 variables originales con alta
correlación entre sí.
↓
PCA detecta las direcciones de
máxima varianza.

Con solo 11 componentes el modelo
captura el 95.18% de la información.

Los 6 componentes descartados
aportan solo 4.82% — ruido
estadístico.
```

El placeholder de imagen (panel derecho, grande):
```
┌──────────────────────────────────────────┐
│                                          │
│   [Insertar: pca_variance.png]           │
│   Scree plot + varianza acumulada        │
│   — imagen provista por el equipo        │
│                                          │
└──────────────────────────────────────────┘
Elaboración propia. Generado con scikit-learn
y matplotlib sobre Rain in Australia [1]. 2024.
```

---

## CORRECCIÓN 5 — SLIDE 7: HACER LA GRÁFICA MÁS GRANDE

Mismo problema que Slide 6. Rediseñar:

**Layout nuevo para Slide 7:**
- Panel izquierdo (30%): los tres bloques PC1/PC2/PC3 resumidos, fuente 10 pt
- Panel derecho (68%): imagen `pca_loadings.png` grande, cita debajo

Texto de los bloques en columna izquierda (reducido para dar espacio):
```
PC1 — 29.8% varianza
Factor de temperatura
Temp9am, Temp3pm,
MaxTemp, MinTemp

PC2 — 16.4% varianza
Factor de humedad
Humidity9am/3pm,
Cloud9am/3pm

PC3 — 10.1% varianza
Factor de viento
WindGustSpeed,
WindSpeed9am/3pm
```

Placeholder de imagen (panel derecho, grande):
```
┌──────────────────────────────────────────┐
│                                          │
│   [Insertar: pca_loadings.png]           │
│   Heatmap de loadings —                  │
│   primeros 6 componentes                 │
│   — imagen provista por el equipo        │
│                                          │
└──────────────────────────────────────────┘
Elaboración propia. Generado con scikit-learn
y matplotlib sobre Rain in Australia [1]. 2024.
```

---

## CORRECCIÓN 6 — SLIDE 8: PLACEHOLDER DE SCREENSHOT

La Slide 8 muestra el texto `SCREENSHOT · app Streamlit desplegada`
como placeholder. Convertirlo en un espacio visual claro para que
el equipo inserte la captura real:

Dejar un rectángulo con borde punteado azul (`#3B85BC`), fondo
azul muy claro (`#EBF4FB`), y dentro el texto centrado:

```
[Insertar captura de pantalla de la app]
pca-lluvia-australiagit-me6beprsvy7wgcnfkgnbsa.streamlit.app
— imagen provista por el equipo
```

La cita debajo del placeholder ya existe y es correcta:
```
Captura propia de la aplicación desplegada en Streamlit Cloud.
github.com/blinaresv/pca-lluvia-australia, 2024.
```
Solo cambiar el año de 2026 a 2024 en esa cita.

---

## RESUMEN DE LOS 6 CAMBIOS

| # | Cambio | Slides afectadas |
|---|---|---|
| 1 | Cambiar año 2026 → 2024 en citas de imagen | 5, 6, 7, 8 |
| 2 | Eliminar texto duplicado | 1, 10 (y resto si aplica) |
| 3 | Agregar cita de foto `Fuente: Unsplash` | 2, 3, 4, 9, 13, 14 |
| 4 | Ampliar imagen a 68% del ancho | Slide 6 |
| 5 | Ampliar imagen a 68% del ancho | Slide 7 |
| 6 | Mejorar placeholder de screenshot + corregir año | Slide 8 |

---

## LO QUE NO SE DEBE TOCAR

- Diseño, colores, tipografías
- Contenido de texto en slides no mencionadas
- Slides 1 (portada), 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15
  (solo se corrigen los problemas específicos listados arriba)
