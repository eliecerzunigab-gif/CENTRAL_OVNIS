import json
import csv
from collections import Counter

# Read CSV
with open('uap-csv.csv', 'r', encoding='utf-8') as f:
    content = f.read()

reader = csv.reader(content.split('\n'))
headers = next(reader)

records = []
for row in reader:
    if len(row) >= 14:
        records.append({
            'redaction': row[0].strip(),
            'release_date': row[1].strip(),
            'title': row[2].strip(),
            'type': row[3].strip(),
            'video_pairing': row[4].strip(),
            'pdf_pairing': row[5].strip(),
            'description': row[6].strip(),
            'dvid_video_id': row[7].strip(),
            'video_title': row[8].strip(),
            'agency': row[9].strip(),
            'incident_date': row[10].strip(),
            'incident_location': row[11].strip(),
            'pdf_image_link': row[12].strip(),
            'modal_image': row[13].strip(),
        })

# Score records by importance
def score_record(r):
    s = 0
    t = r['title'].lower()
    d = r['description'].lower()
    
    # High-profile keywords
    high_impact = ['moon', 'apollo', 'nasa', 'fbi', 'composite sketch', 'sighting', 
                   'encounter', 'photograph', 'video', 'unresolved', 'incident',
                   'uap report', 'declassified', 'eyewitness', 'testimony',
                   'interview', 'statement', 'investigation']
    for kw in high_impact:
        if kw in t or kw in d:
            s += 3
    
    # Medium impact
    med_impact = ['ufo', 'unidentified', 'anomalous', 'phenomena', 'object',
                  'military', 'air force', 'navy', 'army', 'intelligence',
                  'document', 'record', 'report', 'evidence', 'proof']
    for kw in med_impact:
        if kw in t or kw in d:
            s += 2
    
    # Type bonus
    if r['type'] == 'IMG': s += 3
    if r['type'] == 'VID': s += 2
    
    # Has image
    if r['modal_image'] and r['modal_image'].endswith(('.jpg', '.png')):
        s += 1
    
    # Has specific location
    if r['incident_location'] and r['incident_location'] not in ['N/A', '']:
        s += 1
    
    # Has specific date
    if r['incident_date'] and r['incident_date'] not in ['N/A', '']:
        s += 1
    
    return s

# Score and sort
for r in records:
    r['score'] = score_record(r)

records.sort(key=lambda x: -x['score'])

# Top 10 most important
top10 = records[:10]

# Statistics
type_counts = dict(Counter(r['type'] for r in records))
agency_counts = dict(Counter(r['agency'] for r in records))
location_counts = dict(Counter(r['incident_location'] for r in records if r['incident_location'] not in ['N/A', '']))

# Prepare data for dashboard
dashboard_data = {
    'total_records': len(records),
    'types': type_counts,
    'agencies': agency_counts,
    'top_locations': dict(sorted(location_counts.items(), key=lambda x: -x[1])[:15]),
    'top10': [{
        'title': r['title'],
        'agency': r['agency'],
        'incident_date': r['incident_date'],
        'incident_location': r['incident_location'],
        'type': r['type'],
        'description': r['description'][:300],
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
    } for r in records]
}

with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

print(f"Dashboard data generated: {len(records)} records")
print(f"Top 10:")
for i, r in enumerate(top10):
    print(f"  {i+1}. [{r['score']}] {r['title'][:70]} - {r['agency']} - {r['incident_location']}")
