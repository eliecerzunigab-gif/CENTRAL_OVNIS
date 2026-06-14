import json, re

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check what video links exist in the data
vid_records = [r for r in data['all_records'] if r.get('type') == 'VID']

# Check for any URL fields
print("=== Checking all fields in VID records ===")
all_fields = set()
for r in vid_records:
    all_fields.update(r.keys())
print(f"All fields in VID records: {sorted(all_fields)}")

# Check for any records with pdf_image_link or modal_image that might be video URLs
print("\n=== Checking pdf_image_link and modal_image in VID records ===")
for r in vid_records[:10]:
    print(f"  Title: {r['title'][:60]}")
    print(f"  pdf_image_link: {r.get('pdf_image_link', '')[:80]}")
    print(f"  modal_image: {r.get('modal_image', '')[:80]}")
    print(f"  dvid_video_id: {r.get('dvid_video_id', '')}")
    print()

# Check if war.gov has direct video URLs
# Pattern: https://www.war.gov/medialink/ufo/.../video/... or similar
print("=== Searching for video URLs in all records ===")
for r in data['all_records']:
    for field in ['pdf_image_link', 'modal_image', 'pdf_link']:
        val = r.get(field, '')
        if val and ('video' in val.lower() or 'mp4' in val.lower() or 'webm' in val.lower()):
            print(f"  Found video URL in {field}: {val[:120]}")
            print(f"  Title: {r['title'][:60]}")
            print()

# Check the war.gov/ufo page structure
# The videos are likely embedded as MP4 files
# Let's check if there's a pattern for direct video URLs
print("=== Building potential direct video URLs ===")
for r in vid_records[:5]:
    title = r['title']
    # Extract PR number
    match = re.match(r'(DOW-UAP-PR\d+)', title)
    if match:
        pr_id = match.group(1)
        # Possible direct video URL patterns
        print(f"  {pr_id}: {title[:60]}")
        print(f"    Possible URL 1: https://www.war.gov/medialink/ufo/video/{pr_id.lower()}.mp4")
        print(f"    Possible URL 2: https://www.war.gov/medialink/ufo/release_1/video/{pr_id.lower()}.mp4")
        print()
