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

# Score records by importance - refined
def score_record(r):
    s = 0
    t = r['title'].lower()
    d = r['description'].lower()
    
    # Penalize FBI bulk files (they are sections of the same case)
    if '62-hq-83894' in t:
        s -= 5
    
    # Bonus for specific incident locations
    if r['incident_location'] and r['incident_location'] not in ['N/A', '']:
        s += 5
    
    # Bonus for specific dates
    if r['incident_date'] and r['incident_date'] not in ['N/A', '']:
        s += 3
    
    # High-profile keywords in title
    high_impact_title = ['moon', 'apollo', 'nasa', 'composite sketch', 'sighting', 
                         'encounter', 'photograph', 'video', 'unresolved uap report',
                         'incident', 'western us event', 'statement', 'interview',
                         'uap cable', 'uap report']
    for kw in high_impact_title:
        if kw in t:
            s += 8
    
    # High-profile keywords in description
    high_impact_desc = ['composite sketch', 'eyewitness', 'first-hand account',
                        'photographic evidence', 'video evidence', 'declassified',
                        'testimony', 'interview', 'investigation']
    for kw in high_impact_desc:
        if kw in d:
            s += 4
    
    # Type bonus
    if r['type'] == 'IMG': s += 5
    if r['type'] == 'VID': s += 3
    
    # Has image
    if r['modal_image'] and r['modal_image'].endswith(('.jpg', '.png')):
        s += 2
    
    # Agency bonus
    if r['agency'] == 'NASA': s += 3
    if r['agency'] == 'FBI': s += 2
    
    # Description length (more detailed = more important)
    if len(r['description']) > 200:
        s += 2
    
    return s

# Score and sort
for r in records:
    r['score'] = score_record(r)

records.sort(key=lambda x: -x['score'])

# Top 10 most important (skip FBI bulk files)
top10 = [r for r in records if '62-hq-83894' not in r['title'].lower()][:10]

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
    } for r in records]
}

with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

print(f"Dashboard data generated: {len(records)} records")
print(f"\nTop 10 Most Important UAP Cases:")
print("=" * 80)
for i, r in enumerate(top10):
    print(f"\n{i+1}. {r['title']}")
    print(f"   Agency: {r['agency']} | Date: {r['incident_date']} | Location: {r['incident_location']}")
    print(f"   Type: {r['type']} | Score: {r['score']}")
    print(f"   Description: {r['description'][:200]}")
    print(f"   Image: {r['modal_image']}")
