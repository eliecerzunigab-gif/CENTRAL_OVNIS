import json, re

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build a map of PR numbers to slideshow images
pr_to_slideshow = {}
if 'slideshow_images' in data:
    for img_url in data['slideshow_images']:
        # Extract PR number from filename
        match = re.search(r'(DOW-UAP-PR\d+)', img_url, re.IGNORECASE)
        if match:
            pr = match.group(1).upper()
            pr_to_slideshow[pr] = img_url

print(f"Found {len(pr_to_slideshow)} slideshow images with PR numbers:")
for pr, url in sorted(pr_to_slideshow.items()):
    print(f"  {pr}: {url}")

# Now check which VID records have no dvid_video_id and no modal_image
print("\n=== VID records without dvid_video_id ===")
no_dvid = []
for r in data['all_records']:
    if r.get('type') == 'VID' and not r.get('dvid_video_id'):
        no_dvid.append(r)
        pr_match = re.search(r'(DOW-UAP-PR\d+)', r.get('title', ''), re.IGNORECASE)
        pr = pr_match.group(1).upper() if pr_match else 'NO_PR'
        slideshow = pr_to_slideshow.get(pr, 'NONE')
        print(f"  {pr}: {r.get('title','')[:60]}")
        print(f"    modal_image: {r.get('modal_image','')[:80]}")
        print(f"    slideshow: {slideshow[:80]}")
        print()

print(f"\nTotal VID without DVIDS: {len(no_dvid)}")

# Check if war.gov/medialink has thumbnail images for these PRs
# Pattern: https://www.war.gov/medialink/ufo/release_1/thumbnail/DOW-UAP-PR050.jpg
print("\n=== Building thumbnail URLs for VID without DVIDS ===")
for r in no_dvid:
    pr_match = re.search(r'(DOW-UAP-PR\d+)', r.get('title', ''), re.IGNORECASE)
    if pr_match:
        pr = pr_match.group(1).upper()
        thumbnail_url = f"https://www.war.gov/medialink/ufo/release_1/thumbnail/{pr.lower()}.jpg"
        print(f"  {pr}: {thumbnail_url}")
