#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the esc function in generate_new_dashboard.py using chr() to avoid auto-formatting issues"""

with open('generate_new_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Build the correct esc function using chr() to avoid auto-formatting
amp = chr(38)  # &
amp_esc = chr(38) + 'amp;'  # &
lt_esc = chr(38) + 'lt;'    # <
gt_esc = chr(38) + 'gt;'    # >
quot_esc = chr(38) + 'quot;' # "
apos_esc = chr(38) + '#39;'  # &#39;

old_func = "def esc(s):\n    if not isinstance(s, str): s = str(s)\n    return s.replace('" + chr(38) + "', '" + chr(38) + "').replace('<', '<').replace('>', '>').replace('\"', '\"').replace(\"'\", '&#39;')"

new_func = f"def esc(s):\n    if not isinstance(s, str): s = str(s)\n    return s.replace('{amp}', '{amp_esc}').replace('<', '{lt_esc}').replace('>', '{gt_esc}').replace('\"', '{quot_esc}').replace(\"'\", '{apos_esc}')"

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('generate_new_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed esc function successfully!")
else:
    print("Could not find old esc function pattern")
    print("Looking for:", repr(old_func[:50]))
