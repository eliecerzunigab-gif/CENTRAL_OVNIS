# 🛸 CENTRAL OVNIS - Dashboard UAP

Dashboard interactivo con los datos más recientes del **All-domain Anomaly Resolution Office (AARO)** del Departamento de Guerra de EE.UU.

## 🌐 Link Público

[https://eliecerzunigab-gif.github.io/central-ovnis-dashboard/dashboard_ufo.html](https://eliecerzunigab-gif.github.io/central-ovnis-dashboard/dashboard_ufo.html)

## 📊 Datos

- **348 registros** combinados desde `gov/war/ufo` + datos locales
- **7 agencias**: FBI, CIA, NASA, ODNI, Depto. de Guerra, Depto. de Estado, DOE
- **10 imágenes** del Slideshow-2
- **Top 10** con los casos más relevantes

## 🔄 Actualización

Para regenerar los datos más recientes:

```powershell
python generate_dashboard_v3.py
python translate_data.py
python rebuild_dashboard.py
```

## 📁 Archivos principales

| Archivo | Descripción |
|---------|-------------|
| `dashboard_ufo.html` | Dashboard completo (standalone, no necesita servidor) |
| `generate_dashboard_v3.py` | Genera datos desde `gov/war/ufo` |
| `translate_data.py` | Traduce al español |
| `rebuild_dashboard.py` | Incrusta datos en el HTML |
| `deploy_github.ps1` | Script para subir a GitHub Pages |
