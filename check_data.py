import json

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check all records with modal_image
print("=== Records with modal_image (first 20) ===")
count = 0
for r in data['all_records']:
    if r.get('modal_image') and r['modal_image'].strip():
        print(f"  [{r.get('type','?')}] {r.get('title','')[:60]}")
        print(f"    modal_image: {r['modal_image'][:120]}")
        print(f"    pdf_image_link: {r.get('pdf_image_link','')[:120]}")
        print(f"    pdf_link: {r.get('pdf_link','')[:120]}")
        print()
        count += 1
        if count >= 20:
            break

# Check slideshow_images
print("\n=== slideshow_images ===")
if 'slideshow_images' in data:
    for i, img in enumerate(data['slideshow_images'][:10]):
        print(f"  [{i}] {img[:120]}")
else:
    print("  NOT FOUND")

# Check top10 images
print("\n=== top10 records with modal_image ===")
if 'top10' in data:
    count = 0
    for r in data['top10']:
        if r.get('modal_image') and r['modal_image'].strip():
            print(f"  [{r.get('type','?')}] {r.get('title','')[:60]}")
            print(f"    modal_image: {r['modal_image'][:120]}")
            count += 1
            if count >= 10:
                break

# Check what video URLs exist
print("\n=== Records with dvid_video_id ===")
count = 0
for r in data['all_records']:
    if r.get('dvid_video_id'):
        print(f"  {r.get('title','')[:60]} -> dvid: {r['dvid_video_id']}")
        count += 1
print(f"  Total: {count}")

# Check war.gov video URLs - look for any URL patterns
print("\n=== Checking for any URL fields in all records ===")
url_fields = set()
for r in data['all_records']:
    for k, v in r.items():
        if isinstance(v, str) and ('http' in v or 'www' in v or '.gov' in v or '.mil' in v):
            url_fields.add(k)
print(f"Fields containing URLs: {sorted(url_fields)}")

# Check ufo_records.json for any additional video URLs
print("\n=== Checking ufo_records.json ===")
with open('ufo_records.json', 'r', encoding='utf-8') as f:
    ufo = json.load(f)
    
# Check for any URL fields in ufo_records
ufo_url_fields = set()
for r in ufo:
    for k, v in r.items():
        if isinstance(v, str) and ('http' in v or 'www' in v or '.gov' in v or '.mil' in v):
            ufo_url_fields.add(k)
print(f"Fields containing URLs in ufo_records: {sorted(ufo_url_fields)}")

# Check for any records with video URLs
print("\n=== Records with video URLs in any field ===")
for r in data['all_records']:
    for k, v in r.items():
        if isinstance(v, str) and ('video' in v.lower() or 'mp4' in v.lower() or 'webm' in v.lower()):
            print(f"  [{k}] {v[:120]}")
            print(f"    Title: {r.get('title','')[:60]}")
