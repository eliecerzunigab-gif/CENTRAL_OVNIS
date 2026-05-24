import json

with open('ufo_records.json','r',encoding='utf-8') as f:
    data = json.load(f)

print(f'Total records: {len(data)}')
print(f'Records with dvid_video_id: {len([r for r in data if r.get("dvid_video_id","") != ""])}')
print()

# Show all records with dvid IDs
count = 0
for r in data:
    if r.get('dvid_video_id','') != '':
        count += 1
        print(f'{count}. Title: {r["title"][:70]}')
        print(f'   DVID: {r["dvid_video_id"]} | Type: {r["type"]} | Agency: {r.get("agency","")}')
        print(f'   Date: {r.get("incident_date","")} | Location: {r.get("incident_location","")}')
        print(f'   Score: {r.get("score","?")}')
        print()

# Check release dates
print("=== Release dates ===")
dates = {}
for r in data:
    rd = r.get('release_date','')
    if rd:
        dates[rd] = dates.get(rd,0) + 1
for d in sorted(dates.keys()):
    print(f'  {d}: {dates[d]} records')

# Check types
print("\n=== Types ===")
types = {}
for r in data:
    t = r.get('type','')
    types[t] = types.get(t,0) + 1
for t in sorted(types.keys()):
    print(f'  {t}: {types[t]} records')
