# Guía de commits — Sariaht y Adriana
## Windows PowerShell — ejecutar comandos uno a uno

> IMPORTANTE: Ejecutar primero todos los de Sariaht, luego Adriana hace `git pull` y ejecuta los suyos.

---

## SARIAHT — 2 commits pendientes

> El Commit 1 (notebook) ya fue ejecutado exitosamente. Solo faltan estos dos.

### Antes de empezar — ir al repo

```powershell
cd C:\Users\sarya\OneDrive\Documentos\PCA-LLUVIAS\pca-lluvia-australia
```

---

### Commit 2 — Mejorar documentación de predict.py

Abrir el archivo `src/predict.py` en Notepad o cualquier editor y reemplazar la línea:

```
# Ruta base de los modelos (relativa a la raíz del proyecto)
```

por estas dos líneas:

```
# Ruta base de los modelos (relativa a la raíz del proyecto)
# Pipeline: StandardScaler -> PCA(95% varianza) -> LogisticRegression(balanced)
```

Guardar el archivo. Luego ejecutar:

```powershell
git add src/predict.py
```
```powershell
git commit --author="Sariaht Eyleen Xiomara Ariza Vargas <Sariaht@users.noreply.github.com>" -m "docs(src): documentar pipeline completo en modulo de prediccion"
```
```powershell
git push origin main
```

---

### Commit 3 — Mejorar documentación de preprocessing.py

Abrir `src/preprocessing.py` en Notepad y reemplazar la línea:

```
    data = data.dropna(subset=[TARGET])
```

por estas dos líneas (respetar los 4 espacios de sangría):

```
    data = data.dropna(subset=[TARGET])
    # Se usa mediana en lugar de media por robustez ante outliers climaticos
```

Guardar el archivo. Luego ejecutar:

```powershell
git add src/preprocessing.py
```
```powershell
git commit --author="Sariaht Eyleen Xiomara Ariza Vargas <Sariaht@users.noreply.github.com>" -m "docs(src): agregar comentario sobre estrategia de imputacion por mediana"
```
```powershell
git push origin main
```

---
---

## ADRIANA — 3 commits

### Antes de empezar — ir al repo y actualizar

```powershell
cd C:\Users\sarya\OneDrive\Documentos\PCA-LLUVIAS\pca-lluvia-australia
```

> Cambiar la ruta si tu carpeta está en otro lugar.

```powershell
git pull origin main
```

---

### Commit 1 — Dependencias

```powershell
git add requirements.txt
```
```powershell
git commit --author="Adriana Lucia Carreno Medina <Adrilu22@users.noreply.github.com>" -m "feat(deps): agregar requests para integracion con Open-Meteo API"
```
```powershell
git push origin main
```

---

### Commit 2 — App rediseñada

```powershell
git add app/app.py
```
```powershell
git commit --author="Adriana Lucia Carreno Medina <Adrilu22@users.noreply.github.com>" -m "feat(app): redisenar interfaz con tema claro, Open-Meteo API y selector de ciudades"
```
```powershell
git push origin main
```

---

### Commit 3 — README y gitignore

```powershell
git add README.md .gitignore
```
```powershell
git commit --author="Adriana Lucia Carreno Medina <Adrilu22@users.noreply.github.com>" -m "docs: ampliar README con ejemplos PCA en meteorologia, tabla PCA vs LDA y limitaciones"
```
```powershell
git push origin main
```

---

## Verificar el resultado final

Después de que ambas hayan subido, cualquiera puede ejecutar:

```powershell
git log --oneline -10
```

Deben aparecer 5 commits nuevos encima de los 20 anteriores (19 de Brandon + 1 de Sariaht ya subido).  
En GitHub, la pestaña **Contributors** mostrará los tres integrantes del grupo.

---

## Si sale error "rejected" al hacer push

Significa que alguien subió antes. Ejecutar primero:

```powershell
git pull origin main
```

Y luego repetir el push:

```powershell
git push origin main
```
