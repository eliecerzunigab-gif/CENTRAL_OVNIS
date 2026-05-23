import requests, re, json

# Actualizado para leer desde gov/war/ufo (nueva ruta)
r = requests.get('https://web.archive.org/web/20260523142755/https://www.war.gov/ufo/', 
                 headers={'User-Agent': 'Mozilla/5.0'})
text = r.text

# Find all slideshow images (both Slideshow and Slideshow-2)
images1 = re.findall(
    r'https://www\.war\.gov/portals/1/Interactive/2026/UFO/Slideshow/[^"\'\\]+\.(?:jpg|png)',
    text, re.IGNORECASE
)
images2 = re.findall(
    r'https://www\.war\.gov/portals/1/Interactive/2026/UFO/Slideshow-2/[^"\'\\]+\.(?:jpg|png)',
    text, re.IGNORECASE
)

all_images = sorted(set(images1 + images2))
print(f"Found {len(all_images)} slideshow images:")
print(f"  Slideshow: {len(images1)}")
print(f"  Slideshow-2: {len(images2)}")
for img in all_images:
    fname = img.split('/')[-1]
    print(f"  {fname}")

# Save to JSON
with open('slideshow_images.json', 'w', encoding='utf-8') as f:
    json.dump(all_images, f, indent=2)

print("\nSaved to slideshow_images.json")
