import json

with open('ufo_records.json','r',encoding='utf-8') as f:
    data = json.load(f)

# Extract unique video records (VID type or with dvid_video_id)
video_records = []
seen_dvid = set()
for r in data:
    dvid = r.get('dvid_video_id','')
    if dvid and dvid not in seen_dvid:
        seen_dvid.add(dvid)
        video_records.append(r)

# Sort by score if available, otherwise by title
def get_score(r):
    try:
        return int(r.get('score', 0))
    except:
        return 0

video_records.sort(key=get_score, reverse=True)

# Output as JSON for the HTML to use
output = []
for r in video_records:
    output.append({
        'title': r.get('title', 'Sin título'),
        'dvid_video_id': r.get('dvid_video_id', ''),
        'type': r.get('type', ''),
        'agency': r.get('agency', ''),
        'incident_date': r.get('incident_date', ''),
        'incident_location': r.get('incident_location', ''),
        'description': r.get('description', '')[:200],
        'modal_image': r.get('modal_image', ''),
        'score': get_score(r)
    })

print(json.dumps(output, ensure_ascii=False, indent=2))
