import csv
import json
import re
import requests
from collections import Counter, defaultdict

# ============================================================
# ACTUALIZADO: Lee desde gov/war/ufo (nueva ruta)
# ============================================================
print("=" * 60)
print("EXTRAYENDO DATOS DESDE gov/war/ufo")
print("=" * 60)

# Descargar el nuevo CSV desde web.archive
csv_url = 'https://web.archive.org/web/20260523142755/https://www.war.gov/Portals/1/Interactive/2026/UFO/uap-data.csv'
print(f"\n📥 Descargando CSV desde: {csv_url}")
r = requests.get(csv_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
print(f"   Status: {r.status_code}, Size: {len(r.text)} bytes")

# Guardar como nuevo CSV
with open('uap-data-new.csv', 'w', encoding='utf-8') as f:
    f.write(r.text)
print("   Guardado como uap-data-new.csv")

# También cargar el CSV local anterior para combinar
print("\n📂 Cargando CSV local anterior (uap-csv.csv)...")
with open('uap-csv.csv', 'r', encoding='utf-8') as f:
    old_content = f.read()

# Parsear ambos
content = r.text  # Nuevo CSV

# Parse CSV properly
lines = content.split('\n')
reader = csv.reader(lines)
headers = next(reader)
print(f"Headers: {headers}")
print(f"Total columns: {len(headers)}")

# Parse all rows
rows = []
for row in reader:
    if len(row) >= 14:
        rows.append(row)

print(f"Total records: {len(rows)}")

# Extract key fields
records = []
for row in rows:
    record = {
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
    }
    records.append(record)

# Analyze data
print("\n=== DATA ANALYSIS ===")

# Types
type_counts = Counter(r['type'] for r in records)
print(f"\nTypes: {dict(type_counts)}")

# Agencies
agency_counts = Counter(r['agency'] for r in records)
print(f"\nAgencies: {dict(agency_counts.most_common(20))}")

# Locations
location_counts = Counter(r['incident_location'] for r in records if r['incident_location'] and r['incident_location'] != 'N/A')
print(f"\nTop Locations: {dict(location_counts.most_common(20))}")

# Incident dates
dates = [r['incident_date'] for r in records if r['incident_date'] and r['incident_date'] != 'N/A']
print(f"\nSample dates (first 20): {dates[:20]}")

# Records with images
with_images = [r for r in records if r['modal_image']]
print(f"\nRecords with modal images: {len(with_images)}")

# Records with PDF links
with_pdf = [r for r in records if r['pdf_image_link']]
print(f"\nRecords with PDF links: {len(with_pdf)}")

# Records with descriptions
with_desc = [r for r in records if len(r['description']) > 50]
print(f"\nRecords with substantial descriptions: {len(with_desc)}")

# Find records with specific interesting keywords
keywords = ['UAP', 'UFO', 'unidentified', 'anomalous', 'encounter', 'sighting', 'incident', 'report', 'video', 'photograph', 'image']
for kw in keywords:
    matching = [r for r in records if kw.lower() in r['title'].lower() or kw.lower() in r['description'].lower()]
    print(f"Records mentioning '{kw}': {len(matching)}")

# Print all records with their key info
print("\n\n=== ALL RECORDS ===")
for i, r in enumerate(records):
    print(f"\n--- Record {i+1} ---")
    print(f"  Title: {r['title'][:100]}")
    print(f"  Type: {r['type']}")
    print(f"  Agency: {r['agency']}")
    print(f"  Incident Date: {r['incident_date']}")
    print(f"  Incident Location: {r['incident_location']}")
    print(f"  Release Date: {r['release_date']}")
    print(f"  Description: {r['description'][:200]}")
    print(f"  Modal Image: {r['modal_image'][:100]}")
    print(f"  PDF Link: {r['pdf_image_link'][:100]}")

# Save as JSON
with open('ufo_records.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2, ensure_ascii=False)
print(f"\n\nSaved {len(records)} records to ufo_records.json")
