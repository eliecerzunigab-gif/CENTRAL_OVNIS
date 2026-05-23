"""
generate_dashboard_final.py
Genera el dashboard combinando datos de:
  - URL nueva:   https://www.war.gov/ufo/  (uap-data.csv) - vía web.archive
  - CSV local:   uap-csv.csv (datos anteriores)
  
Lee desde gov/war/ufo (web.archive) y combina con datos locales previos.
"""

import requests, csv, json, re
from collections import Counter

# ============================================================
# CONFIGURACIÓN
# ============================================================
# URL nueva: /ufo/ con uap-data.csv (vía web.archive)
NEW_CSV_URL = 'https://web.archive.org/web/20260523142755/https://www.war.gov/Portals/1/Interactive/2026/UFO/uap-data.csv'
NEW_PAGE_URL = 'https://web.archive.org/web/20260523142755/https://www.war.gov/ufo/'

# ============================================================
# 1. DESCARGAR NUEVO CSV
# ============================================================
print("=" * 70)
print("GENERATE DASHBOARD FINAL - LEYENDO DESDE gov/war/ufo")
print("=" * 70)

print(f"\n📥 Descargando nuevo CSV desde gov/war/ufo...")
print(f"   URL: {NEW_CSV_URL}")
r = requests.get(NEW_CSV_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
print(f"   Status: {r.status_code}, Size: {len(r.text)} bytes")

lines = r.text.split('\n')
reader = csv.reader(lines)
headers = next(reader)

new_records = []
for row in reader:
    if len(row) >= 14:
        new_records.append({
            'redaction': row[0].strip() if len(row) > 0 else '',
            'release_date': row[1].strip() if len(row) > 1 else '',
            'title': row[2].strip() if len(row) > 2 else '',
            'type': row[3].strip() if len(row) > 3 else '',
            'video_pairing': row[4].strip() if len(row) > 4 else '',
            'pdf_pairing': row[5].strip() if len(row) > 5 else '',
            'description': row[6].strip() if len(row) > 6 else '',
            'dvid_video_id': row[7].strip() if len(row) > 7 else '',
            'video_title': row[8].strip() if len(row) > 8 else '',
            'agency': row[9].strip() if len(row) > 9 else '',
            'incident_date': row[10].strip() if len(row) > 10 else '',
            'incident_location': row[11].strip() if len(row) > 11 else '',
            'pdf_image_link': row[12].strip() if len(row) > 12 else '',
            'modal_image': row[13].strip() if len(row) > 13 else '',
        })

print(f"   Registros nuevos: {len(new_records)}")

# ============================================================
# 2. CARGAR CSV LOCAL ANTERIOR
# ============================================================
print(f"\n📂 Cargando CSV local anterior (uap-csv.csv)...")
old_records = []
try:
    with open('uap-csv.csv', 'r', encoding='utf-8') as f:
        old_content = f.read()
    old_reader = csv.reader(old_content.split('\n'))
    next(old_reader)
    for row in old_reader:
        if len(row) >= 14:
            old_records.append({
                'redaction': row[0].strip() if len(row) > 0 else '',
                'release_date': row[1].strip() if len(row) > 1 else '',
                'title': row[2].strip() if len(row) > 2 else '',
                'type': row[3].strip() if len(row) > 3 else '',
                'video_pairing': row[4].strip() if len(row) > 4 else '',
                'pdf_pairing': row[5].strip() if len(row) > 5 else '',
                'description': row[6].strip() if len(row) > 6 else '',
                'dvid_video_id': row[7].strip() if len(row) > 7 else '',
                'video_title': row[8].strip() if len(row) > 8 else '',
                'agency': row[9].strip() if len(row) > 9 else '',
                'incident_date': row[10].strip() if len(row) > 10 else '',
                'incident_location': row[11].strip() if len(row) > 11 else '',
                'pdf_image_link': row[12].strip() if len(row) > 12 else '',
                'modal_image': row[13].strip() if len(row) > 13 else '',
            })
    print(f"   Registros locales: {len(old_records)}")
except FileNotFoundError:
    print("   ⚠️ No se encontró uap-csv.csv")
    old_records = []

# ============================================================
# 3. COMBINAR REGISTROS
# ============================================================
print("\n🔄 Combinando registros...")

def normalize_title(title):
    t = title.lower().strip()
    t = re.sub(r'section_(\d+)$', lambda m: f'section_{int(m.group(1)):03d}', t)
    return t

new_by_title = {}
for r in new_records:
    key = normalize_title(r['title'])
    if key not in new_by_title:
        new_by_title[key] = r

combined = list(new_records)
old_added = 0
for r in old_records:
    key = normalize_title(r['title'])
    if key not in new_by_title:
        combined.append(r)
        old_added += 1

print(f"   Registros nuevos (de gov/war/ufo): {len(new_records)}")
print(f"   Registros adicionales (locales):   {old_added}")
print(f"   Total combinado:                  {len(combined)}")

# ============================================================
# 4. SLIDESHOW IMAGES
# ============================================================
print("\n🖼️ Descargando slideshow images desde gov/war/ufo...")
r_page = requests.get(NEW_PAGE_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
text = r_page.text

images1 = re.findall(
    r'https://www\.war\.gov/portals/1/Interactive/2026/UFO/Slideshow/[^"\'\\]+\.(?:jpg|png)',
    text, re.IGNORECASE
)
images2 = re.findall(
    r'https://www\.war\.gov/portals/1/Interactive/2026/UFO/Slideshow-2/[^"\'\\]+\.(?:jpg|png)',
    text, re.IGNORECASE
)

all_slideshow = sorted(set(images1 + images2))
print(f"   Slideshow: {len(images1)} imágenes")
print(f"   Slideshow-2: {len(images2)} imágenes")
print(f"   Total: {len(all_slideshow)}")

# ============================================================
# 5. SCORE Y TOP 10
# ============================================================
print("\n🏆 Calculando scores...")

def score_record(r):
    s = 0
    t = r['title'].lower()
    d = r['description'].lower()
    
    if '62-hq-83894' in t:
        s -= 5
    
    if r['incident_location'] and r['incident_location'] not in ['N/A', '']:
        s += 5
    if r['incident_date'] and r['incident_date'] not in ['N/A', '']:
        s += 3
    
    high_impact_title = ['moon', 'apollo', 'nasa', 'composite sketch', 'sighting', 
                         'encounter', 'photograph', 'video', 'unresolved uap report',
                         'incident', 'western us event', 'statement', 'interview',
                         'uap cable', 'uap report', 'cia', 'odni', 'doe', 'pantex',
                         'intelligence', 'ussr', 'sandia']
    for kw in high_impact_title:
        if kw in t:
            s += 8
    
    high_impact_desc = ['composite sketch', 'eyewitness', 'first-hand account',
                        'photographic evidence', 'video evidence', 'declassified',
                        'testimony', 'interview', 'investigation', 'intelligence',
                        'classified']
    for kw in high_impact_desc:
        if kw in d:
            s += 4
    
    if r['type'] == 'IMG': s += 5
    if r['type'] == 'VID': s += 3
    
    if r['modal_image'] and r['modal_image'].endswith(('.jpg', '.png')):
        s += 2
    
    if r['agency'] == 'NASA': s += 3
    if r['agency'] == 'FBI': s += 2
    if 'CIA' in r['agency'].upper(): s += 4
    if 'ODNI' in r['agency'].upper(): s += 4
    if 'DOE' in r['agency'].upper(): s += 3
    
    if len(r['description']) > 200:
        s += 2
    
    return s

for r in combined:
    r['score'] = score_record(r)

combined.sort(key=lambda x: -x['score'])
top10 = [r for r in combined if '62-hq-83894' not in r['title'].lower()][:10]

# ============================================================
# 6. ESTADÍSTICAS
# ============================================================
type_counts = dict(Counter(r['type'] for r in combined))
agency_counts = dict(Counter(r['agency'] for r in combined))
location_counts = dict(Counter(r['incident_location'] for r in combined if r['incident_location'] not in ['N/A', '']))

# ============================================================
# 7. PREPARAR DATOS
# ============================================================
print("\n📊 Preparando datos del dashboard...")

dashboard_data = {
    'total_records': len(combined),
    'types': type_counts,
    'agencies': agency_counts,
    'top_locations': dict(sorted(location_counts.items(), key=lambda x: -x[1])[:15]),
    'slideshow_images': all_slideshow,
    'top10': [{
        'title': r['title'],
        'agency': r['agency'],
        'incident_date': r['incident_date'],
        'incident_location': r['incident_location'],
        'type': r['type'],
        'description': r['description'][:400],
        'modal_image': r['modal_image'],
        'pdf_link': r['pdf_image_link'],
        'score': r['score']
    } for r in top10],
    'all_records': [{
        'title': r['title'],
        'agency': r['agency'],
        'incident_date': r['incident_date'],
        'incident_location': r['incident_location'],
        'type': r['type'],
        'description': r['description'][:200],
        'modal_image': r['modal_image'],
        'score': r['score']
    } for r in combined]
}

with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Dashboard data generado: {len(combined)} registros totales")
print(f"   Slideshow images: {len(all_slideshow)}")
print(f"   Tipos: {type_counts}")
print(f"   Agencias ({len(agency_counts)}): {agency_counts}")

print(f"\n{'='*70}")
print(f"🏆 TOP 10 (combinando gov/war/ufo + datos locales)")
print(f"{'='*70}")
for i, r in enumerate(top10):
    print(f"\n{i+1}. [{r['score']}] {r['title']}")
    print(f"   Agencia: {r['agency']} | Fecha: {r['incident_date']} | Ubicación: {r['incident_location']}")
    print(f"   Tipo: {r['type']}")
    print(f"   Descripción: {r['description'][:150]}...")
