"""
embed_data.py
Incrusta los datos del dashboard directamente en el HTML.
Lee desde dashboard_data.json (generado por generate_dashboard_v3.py)
"""

import json

# Read the dashboard HTML
with open('dashboard_ufo.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read the JSON data
with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    content = f.read()
    data = json.loads(content)

# Convert data to a compact JSON string for embedding
data_json = json.dumps(data, ensure_ascii=False)

# Find and replace the EMBEDDED_DATA section
start_marker = 'const EMBEDDED_DATA = '
end_marker = ';\n\n// Use embedded data directly'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx >= 0 and end_idx >= 0:
    old_section = html[start_idx:end_idx + len(end_marker)]
    new_section = f'const EMBEDDED_DATA = {data_json};\n\n// Use embedded data directly'
    html = html.replace(old_section, new_section)
    print("✅ Datos EMBEDDED_DATA actualizados correctamente")
else:
    print("⚠️ No se encontró EMBEDDED_DATA, buscando fetch()...")
    old_fetch = """fetch('dashboard_data.json')
  .then(r => r.json())
  .then(data => {
    allRecordsData = data.all_records;
    renderDashboard(data);
  })
  .catch(err => {
    console.error('Error loading data:', err);
    document.body.innerHTML = '<div style="text-align:center;padding:100px 20px;color:var(--text-secondary)"><h2>Error cargando datos</h2><p>' + err.message + '</p></div>';
  });"""
    
    new_script = f"""const EMBEDDED_DATA = {data_json};

// Use embedded data directly
allRecordsData = EMBEDDED_DATA.all_records;
renderDashboard(EMBEDDED_DATA);"""
    
    if old_fetch in html:
        html = html.replace(old_fetch, new_script)
        print("✅ Fetch reemplazado con datos incrustados")
    else:
        print("❌ No se pudo encontrar ninguna sección para reemplazar")

# Save the standalone HTML
with open('dashboard_ufo.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Dashboard actualizado. Tamaño: {len(html):,} bytes")
