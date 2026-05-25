import json

d = json.load(open('ufo_records.json', encoding='utf-8'))
print(f'Total registros en ufo_records.json: {len(d)}')

types = {}
agencies = {}
for r in d:
    t = r.get('type', 'N/A')
    types[t] = types.get(t, 0) + 1
    a = r.get('agency', 'N/A')
    agencies[a] = agencies.get(a, 0) + 1

print('\nTipos:')
for k, v in sorted(types.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

print('\nAgencias:')
for k, v in sorted(agencies.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

# Check records with dvid_video_id
vids = [r for r in d if r.get('dvid_video_id')]
print(f'\nRegistros con dvid_video_id: {len(vids)}')

# Check records with modal_image
imgs = [r for r in d if r.get('modal_image')]
print(f'Registros con modal_image: {len(imgs)}')

# Check unique dvid_video_id
unique_vids = set(r.get('dvid_video_id') for r in d if r.get('dvid_video_id'))
print(f'Videos unicos (dvid_video_id): {len(unique_vids)}')

# Check unique modal_image
unique_imgs = set(r.get('modal_image') for r in d if r.get('modal_image'))
print(f'Imagenes unicas (modal_image): {len(unique_imgs)}')

# Latest release dates
dates = sorted([r.get('release_date', '') for r in d if r.get('release_date')])
print(f'\nRango de fechas: {dates[0] if dates else "N/A"} -> {dates[-1] if dates else "N/A"}')
print(f'Ultimas 5 fechas: {dates[-5:]}')
