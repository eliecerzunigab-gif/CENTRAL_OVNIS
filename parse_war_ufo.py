import requests
import re
import json

# Actualizado para leer desde gov/war/ufo (nueva ruta)
r = requests.get('https://web.archive.org/web/20260523142755/https://www.war.gov/ufo/', 
                 headers={'User-Agent': 'Mozilla/5.0'})
text = r.text

# Save full HTML for analysis
with open('war_ufo_full.html', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Total HTML size: {len(text)} bytes")

# Find all script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)
print(f"\nTotal scripts: {len(scripts)}")

# Look for interesting data in scripts
for i, s in enumerate(scripts):
    s_lower = s.lower()
    if any(kw in s_lower for kw in ['data', 'case', 'ufo', 'uap', 'report', 'incident', 'sighting', 'encounter', 'json', 'records', 'slideshow', 'slides']):
        print(f"\n=== Script {i} (len={len(s)}) ===")
        print(s[:500])
        print("...")

# Look for specific divs with content
content_divs = re.findall(r'<div[^>]*class="[^"]*"[^>]*>', text)
print(f"\nTotal divs: {len(content_divs)}")

# Find sections with specific class names
for cls in ['content', 'main', 'data', 'records', 'slideshow', 'slide', 'gallery', 'card', 'item', 'entry', 'incident']:
    matches = re.findall(rf'<div[^>]*class="[^"]*{cls}[^"]*"[^>]*>', text, re.IGNORECASE)
    if matches:
        print(f"\nDivs with class containing '{cls}': {len(matches)}")
        for m in matches[:3]:
            print(f"  {m[:200]}")

# Look for image references
images = re.findall(r'<img[^>]*src="([^"]*)"[^>]*>', text)
print(f"\nTotal images: {len(images)}")
for img in images[:20]:
    if 'ufo' in img.lower() or 'uap' in img.lower() or 'slide' in img.lower():
        print(f"  {img}")

# Look for links to case details
links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', text, re.DOTALL)
print(f"\nTotal links: {len(links)}")
for href, link_text in links[:30]:
    if any(kw in href.lower() for kw in ['case', 'report', 'incident', 'uap', 'ufo', 'record', 'document']):
        print(f"  {href} -> {link_text.strip()[:100]}")

# Look for any JSON-like data structures
json_patterns = re.findall(r'\[{.*?}\]', text, re.DOTALL)
print(f"\nJSON array patterns found: {len(json_patterns)}")
for j in json_patterns[:5]:
    if len(j) < 500:
        print(f"  {j[:300]}")
