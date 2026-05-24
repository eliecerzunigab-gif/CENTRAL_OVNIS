#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de TOP DASHBOARD - Central Ovnis
Combina registros R1 (dashboard_ufo.html) y R2 (ufo_records.json)
"""

import json

# ============================================================
# CARGAR DATOS R2
# ============================================================
with open('ufo_records.json', 'r', encoding='utf-8') as f:
    r2_data = json.load(f)

# ============================================================
# SCORE R2 RECORDS
# ============================================================
r2_records_js = []
for r in r2_data:
    title = r.get('title', 'N/A')
    agency = r.get('agency', 'N/A')
    loc = r.get('incident_location', 'N/A')
    date = r.get('incident_date', 'N/A')
    rtype = r.get('type', 'PDF')
    desc = r.get('description', '')[:200]
    modal = r.get('modal_image', '')
    pdf = r.get('pdf_image_link', '')
    vid = r.get('dvid_video_id', '')
    
    score = 10
    kw = desc.lower()
    if 'triangular' in kw or 'metallic' in kw: score += 3
    if '90-degree' in kw or 'erratic' in kw: score += 3
    if 'orb' in kw or 'sphere' in kw: score += 2
    if 'diamond' in kw: score += 3
    if 'materialized' in kw or 'disappeared' in kw: score += 4
    if 'fast-moving' in kw or 'high-speed' in kw: score += 2
    if 'multiple' in kw or 'formation' in kw: score += 2
    if 'Apollo' in title or 'Moon' in loc: score += 3
    if 'Western US Event' in title: score += 5
    if 'Composite Sketch' in title: score += 4
    if 'USPER' in title: score += 4
    
    r2_records_js.append({
        'title': title, 'agency': agency, 'incident_date': date,
        'incident_location': loc, 'type': rtype, 'description': desc,
        'modal_image': modal, 'pdf_link': pdf, 'dvid_video_id': vid, 'score': score
    })

r2_records_js.sort(key=lambda x: -x['score'])

# ============================================================
# R1 TOP RECORDS (curated from dashboard_ufo.html)
# ============================================================
r1_top = [
    {'title':'FBI - Western US Event (2023)','agency':'FBI','date':'2023','loc':'Western United States','type':'PDF','desc':'Siete testigos federales reportan orbes lanzando otros orbes, objetos translucidos tipo cometa, y fenomenos de gran tamano cerca del suelo. Considerado uno de los casos mas convincentes de AARO.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/western_us_event_slides_5.08.2026.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/western_us_event_slides_5.08.2026.pdf','score':25},
    {'title':'FBI - Composite Sketch Sept 2023','agency':'FBI','date':'9/1/23','loc':'United States','type':'PDF','desc':'Dibujo compuesto del FBI: objeto metalico bronce elipsoide de 40-60m materializandose de una luz brillante y desapareciendo instantaneamente.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/2024-04-30-composite-sketch.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/2024-04-30-composite-sketch.pdf','score':24},
    {'title':'FBI - USPER Statement UAP Sighting','agency':'FBI','date':'Late 2025','loc':'United States','type':'PDF','desc':'Declaracion jurada de alto oficial de inteligencia: orbe super-caliente perseguido por helicoptero a velocidad imposible, enjambre de luces en todas direcciones.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/usper-statement-redacted.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/usper-statement-redacted.pdf','score':24},
    {'title':'NASA-UAP-VM6 - Apollo 17 (1972)','agency':'NASA','date':'1972','loc':'Moon','type':'IMG','desc':'Fotografia Apollo 17 con tres puntos en formacion triangular en el cielo lunar. Nuevo analisis gubernamental sugiere objeto fisico real en la escena.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/nasa-uap-vm6-apollo-17-1972.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/nasa-uap-vm6-apollo-17-1972.jpg','score':23},
    {'title':'DoD - DOW-UAP-PR34 Greece Oct 2023','agency':'Department of War','date':'10/2023','loc':'Greece','type':'VID','desc':'Video de 3 min: UAP realizando multiples giros de 90 grados a 80 mph sobre el mar. Maniobras imposibles para aeronaves convencionales.','img':'','pdf':'','score':22},
    {'title':'State Dept - Cable 2 Kazakhstan 1994','agency':'Department of State','date':'1/27/94','loc':'Kazakhstan','type':'PDF','desc':'Piloto tayiko + 3 ciudadanos EEUU encuentran UAP a 41,000 pies. Luz brillante haciendo giros de 90 grados, tirabuzones a velocidad extrema.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/dos-uap-d2-cable-2-kazakhstan-january-1994.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/dos-uap-d2-cable-2-kazakhstan-january-1994.pdf','score':22},
    {'title':'DoD - DOW-UAP-PR28 Greece Jan 2024','agency':'Department of War','date':'1/2024','loc':'Greece','type':'VID','desc':'UAP con forma de diamante, detectable solo en SWIR. Velocidad ~434 nudos. Forma de lagrima invertida con masa suspendida.','img':'','pdf':'','score':22},
    {'title':'NASA-UAP-D1 Apollo 12 Transcript 1969','agency':'NASA','date':'1969','loc':'Moon','type':'PDF','desc':'Transcripcion Apollo 12: Astronauta Alan Bean describe particulas y destellos escapando de la Luna vistos desde el AOT.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/nasa-uap-d1-apollo-12-transcript-1969.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/nasa-uap-d1-apollo-12-transcript-1969.pdf','score':21},
    {'title':'NASA-UAP-D2 Apollo 17 Transcript 1972','agency':'NASA','date':'1972','loc':'Moon','type':'PDF','desc':'Astronauta Cernan reporta destellos intensos como tren, objetos girando. Schmitt ve flash en superficie lunar.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/nasa-uap-d2-apollo-17-transcript-1972.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/nasa-uap-d2-apollo-17-transcript-1972.pdf','score':21},
    {'title':'DoD - DOW-UAP-D74 Syria Nov 2023','agency':'Department of War','date':'11/9/23','loc':'Syria','type':'PDF','desc':'UAP con forma de pelota saltarina viajando a 424 nudos (483 mph) consistentemente por 7+ minutos.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/dow-uap-d74-mission-report-syria-november-2023.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/dow-uap-d74-mission-report-syria-november-2023.pdf','score':21},
    {'title':'State Dept - Cable 1 Papua New Guinea 1985','agency':'Department of State','date':'1/24/85','loc':'Papua New Guinea','type':'PDF','desc':'Cable diplomatico: objetos voladores de alta altitud/velocidad. Piloto de Air Niugini confirmo deteccion radar.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/dos-uap-d1-cable-1-papua-new-guinea-january-1985.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/dos-uap-d1-cable-1-papua-new-guinea-january-1985.pdf','score':20},
    {'title':'DoD - DOW-UAP-D54 Mediterranean','agency':'Department of War','date':'N/A','loc':'Mediterranean Sea','type':'PDF','desc':'UAP triangular y metalico. Altitud estimada 24,989 pies, velocidad 168 nudos (193 mph).','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/dow-uap-d54-mission-report-mediterranean-sea-na.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/dow-uap-d54-mission-report-mediterranean-sea-na.pdf','score':20},
    {'title':'DoD - DOW-UAP-D58 Range Fouler Oct 2020','agency':'Department of War','date':'10/27/20','loc':'N/A','type':'PDF','desc':'Dos UAP: forma de globo, metalicos y reflectantes con luces rojas intermitentes. Uno orbitando al otro.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/dow-uap-d58-range-fouler-debrief-na-october-2020.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/dow-uap-d58-range-fouler-debrief-na-october-2020.pdf','score':19},
    {'title':'DoD - DOW-UAP-D57 Gulf of Aden Sep 2020','agency':'Department of War','date':'9/4/20','loc':'Gulf of Aden','type':'PDF','desc':'Objeto redondo y frio tracking por 8 min. Multiples cambios abruptos de direccion. Velocidad 277 mph.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/dow-uap-d57-mission-report-gulf-of-aden-september-2020.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/dow-uap-d57-mission-report-gulf-of-aden-september-2020.pdf','score':19},
    {'title':'DoD - DOW-UAP-PR46 East China Sea 2024','agency':'Department of War','date':'2024','loc':'East China Sea','type':'VID','desc':'UAP forma de balon de futbol con 3 proyecciones radiales. Detectado por INDOPACOM.','img':'','pdf':'','score':18},
    {'title':'DoD - DOW-UAP-PR47 Japan 2023','agency':'Department of War','date':'2023','loc':'Japan','type':'VID','desc':'Tres areas de contraste manteniendo posicion y orientacion fijas entre si. Formacion coordinada.','img':'','pdf':'','score':18},
    {'title':'DoD - DOW-UAP-D75 Gulf of Aden Jul 2024','agency':'Department of War','date':'7/14/24','loc':'Gulf of Aden','type':'PDF','desc':'UAP trayectoria recta misma altitud. Velocidad mayor que la de vuelo. Seguido hasta perderlo por distancia.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/dow-uap-d75-mission-report-gulf-of-aden-july-2024.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/dow-uap-d75-mission-report-gulf-of-aden-july-2024.pdf','score':18},
    {'title':'DoD - DOW-UAP-D56 Arabian Sea Aug 2020','agency':'Department of War','date':'8/24/20','loc':'Arabian Sea','type':'PDF','desc':'Grupo 3 contactos aereos no identificados con estructura de alas. Mantuvieron rumbo, velocidad y altitud relativos.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf','score':18},
    {'title':'FBI Photo B6 - Western US','agency':'FBI','date':'Late 2025','loc':'Western United States','type':'PDF','desc':'Objeto oscuro estructurado con apendice. Segundo objeto circular. Imagen sistema militar con redacciones.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/fbi-photo-b6.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/fbi-photo-b6.pdf','score':18},
    {'title':'FBI Photo A1 - Reticle','agency':'FBI','date':'Late 2025','loc':'N/A','type':'IMG','desc':'Imagen monocroma con reticula central. Objeto pequeno, oscuro e irregular. Alterada con redacciones.','img':'https://www.war.gov/medialink/ufo/release_1/thumbnail/fbi-photo-a1.jpg','pdf':'https://www.war.gov/medialink/ufo/release_1/fbi-photo-a1.png','score':17},
]

# ============================================================
# R1 TABLE RECORDS (all R1 records for the full table)
# ============================================================
r1_table = [
    {'title':'FBI - Western US Event Slides','agency':'FBI','date':'2023','loc':'Western United States','type':'PDF'},
    {'title':'FBI - Composite Sketch September 2023','agency':'FBI','date':'9/1/23','loc':'United States','type':'PDF'},
    {'title':'FBI - USPER Statement UAP Sighting','agency':'FBI','date':'Late 2025','loc':'United States','type':'PDF'},
    {'title':'FBI - Serial 3 September 2023','agency':'FBI','date':'9/1/23','loc':'United States','type':'PDF'},
    {'title':'FBI - Serial 4 September 2023','agency':'FBI','date':'9/1/23','loc':'United States','type':'PDF'},
    {'title':'FBI - Serial 5 September 2023','agency':'FBI','date':'9/1/23','loc':'United States','type':'PDF'},
    {'title':'FBI Photo A1-A8','agency':'FBI','date':'Late 2025','loc':'N/A','type':'IMG'},
    {'title':'FBI Photo B1-B24 (Western US)','agency':'FBI','date':'Late 2025','loc':'Western United States','type':'PDF'},
    {'title':'NASA-UAP-VM1 to VM5 Apollo 12','agency':'NASA','date':'1969','loc':'Moon','type':'IMG'},
    {'title':'NASA-UAP-VM6 Apollo 17','agency':'NASA','date':'1972','loc':'Moon','type':'IMG'},
    {'title':'NASA-UAP-D1 Apollo 12 Transcript','agency':'NASA','date':'1969','loc':'Moon','type':'PDF'},
    {'title':'NASA-UAP-D2 Apollo 17 Transcript','agency':'NASA','date':'1972','loc':'Moon','type':'PDF'},
    {'title':'NASA-UAP-D4 Apollo 11 Debriefing','agency':'NASA','date':'1969','loc':'Moon','type':'PDF'},
    {'title':'NASA-UAP-D5 Apollo 17 Science Debrief','agency':'NASA','date':'1973','loc':'N/A','type':'PDF'},
    {'title':'NASA-UAP-D6 Apollo 17 Tech Debrief','agency':'NASA','date':'1973','loc':'N/A','type':'PDF'},
    {'title':'NASA-UAP-D7 Skylab Debriefing','agency':'NASA','date':'1973','loc':'Low Earth Orbit','type':'PDF'},
    {'title':'State Dept Cable 1 - Papua New Guinea','agency':'Department of State','date':'1/24/85','loc':'Papua New Guinea','type':'PDF'},
    {'title':'State Dept Cable 2 - Kazakhstan','agency':'Department of State','date':'1/27/94','loc':'Kazakhstan','type':'PDF'},
    {'title':'State Dept Cable 3 - Georgia','agency':'Department of State','date':'10/28/01','loc':'Georgia','type':'PDF'},
    {'title':'State Dept Cable 4 - Turkmenistan','agency':'Department of State','date':'11/5/04','loc':'Turkmenistan','type':'PDF'},
    {'title':'State Dept Cable 5 - Mexico','agency':'Department of State','date':'9/12/03','loc':'Mexico','type':'PDF'},
    {'title':'DoD - DOW-UAP-D54 Mediterranean','agency':'Department of War','date':'N/A','loc':'Mediterranean Sea','type':'PDF'},
    {'title':'DoD - DOW-UAP-D55 Syria Nov 2016','agency':'Department of War','date':'11/18/16','loc':'Syria','type':'PDF'},
    {'title':'DoD - DOW-UAP-D56 Arabian Sea Aug 2020','agency':'Department of War','date':'8/24/20','loc':'Arabian Sea','type':'PDF'},
    {'title':'DoD - DOW-UAP-D57 Gulf of Aden Sep 2020','agency':'Department of War','date':'9/4/20','loc':'Gulf of Aden','type':'PDF'},
    {'title':'DoD - DOW-UAP-D58 Range Fouler Oct 2020','agency':'Department of War','date':'10/27/20','loc':'N/A','type':'PDF'},
    {'title':'DoD - DOW-UAP-D60 Persian Gulf Aug 2020','agency':'Department of War','date':'8/8/20','loc':'Persian Gulf','type':'PDF'},
    {'title':'DoD - DOW-UAP-D61 Persian Gulf Aug 2020','agency':'Department of War','date':'8/27/20','loc':'Persian Gulf','type':'PDF'},
    {'title':'DoD - DOW-UAP-D62 Strait of Hormuz Sep 2020','agency':'Department of War','date':'9/16/20','loc':'Strait of Hormuz','type':'PDF'},
    {'title':'DoD - DOW-UAP-D63 Strait of Hormuz Oct 2020','agency':'Department of War','date':'10/1/20','loc':'Strait of Hormuz','type':'PDF'},
    {'title':'DoD - DOW-UAP-D64 Iran Nov 2020','agency':'Department of War','date':'11/2/20','loc':'Iran','type':'PDF'},
    {'title':'DoD - DOW-UAP-D65 Persian Gulf Jul 2020','agency':'Department of War','date':'7/16/20','loc':'Persian Gulf','type':'PDF'},
    {'title':'DoD - DOW-UAP-D74 Syria Nov 2023','agency':'Department of War','date':'11/9/23','loc':'Syria','type':'PDF'},
    {'title':'DoD - DOW-UAP-D75 Gulf of Aden Jul 2024','agency':'Department of War','date':'7/14/24','loc':'Gulf of Aden','type':'PDF'},
    {'title':'DoD - DOW-UAP-PR19 Middle East May 2022','agency':'Department of War','date':'2022','loc':'Middle East','type':'VID'},
    {'title':'DoD - DOW-UAP-PR20 Kuwait May 2022','agency':'Department of War','date':'2022','loc':'Iraq','type':'PDF'},
    {'title':'DoD - DOW-UAP-PR21 Iraq May 2022','agency':'Department of War','date':'2022','loc':'Iraq','type':'VID'},
    {'title':'DoD - DOW-UAP-PR22 Syria Jul 2022','agency':'Department of War','date':'2022','loc':'Syria','type':'VID'},
    {'title':'DoD - DOW-UAP-PR23 Iraq Dec 2022','agency':'Department of War','date':'2022','loc':'Iraq','type':'VID'},
    {'title':'DoD - DOW-UAP-PR26 UAE Oct 2023','agency':'Department of War','date':'2023','loc':'United Arab Emirates','type':'VID'},
    {'title':'DoD - DOW-UAP-PR27 UAE Oct 2023','agency':'Department of War','date':'2023','loc':'United Arab Emirates','type':'VID'},
    {'title':'DoD - DOW-UAP-PR28 Greece Jan 2024','agency':'Department of War','date':'2024','loc':'Greece','type':'VID'},
    {'title':'DoD - DOW-UAP-PR29 Gulf of Oman Jun 2024','agency':'Department of War','date':'2024','loc':'Gulf of Oman','type':'VID'},
    {'title':'DoD - DOW-UAP-PR31 Syria Oct 2024','agency':'Department of War','date':'2024','loc':'Syria','type':'VID'},
    {'title':'DoD - DOW-UAP-PR32 Syria Oct 2024','agency':'Department of War','date':'2024','loc':'Syria','type':'VID'},
    {'title':'DoD - DOW-UAP-PR33 Syria Oct 2024','agency':'Department of War','date':'2024','loc':'Syria','type':'VID'},
    {'title':'DoD - DOW-UAP-PR34 Greece Oct 2023','agency':'Department of War','date':'2023','loc':'Greece','type':'VID'},
    {'title':'DoD - DOW-UAP-PR35 Greece Oct 2023','agency':'Department of War','date':'2023','loc':'Greece','type':'VID'},
    {'title':'DoD - DOW-UAP-PR36 Middle East May 2020','agency':'Department of War','date':'2020','loc':'Middle East','type':'VID'},
    {'title':'DoD - DOW-UAP-PR37 Arabian Gulf 2020','agency':'Department of War','date':'2020','loc':'Arabian Gulf','type':'VID'},
    {'title':'DoD - DOW-UAP-PR38 Middle East 2013','agency':'Department of War','date':'2013','loc':'Middle East','type':'VID'},
    {'title':'DoD - DOW-UAP-PR39 Arabian Gulf 2020','agency':'Department of War','date':'2020','loc':'Arabian Gulf','type':'VID'},
    {'title':'DoD - DOW-UAP-PR40 Arabian Gulf 2020','agency':'Department of War','date':'2020','loc':'Arabian Gulf','type':'VID'},
    {'title':'DoD - DOW-UAP-PR41 Arabian Gulf 2020','agency':'Department of War','date':'2020','loc':'Arabian Gulf','type':'VID'},
    {'title':'DoD - DOW-UAP-PR42 Arabian Gulf 2020','agency':'Department of War','date':'2020','loc':'Arabian Gulf','type':'VID'},
    {'title':'DoD - DOW-UAP-PR43 Djibouti 2025','agency':'Department of War','date':'2025','loc':'Djibouti','type':'VID'},
    {'title':'DoD - DOW-UAP-PR44 Arabian Gulf 2020','agency':'Department of War','date':'2020','loc':'Arabian Gulf','type':'VID'},
    {'title':'DoD - DOW-UAP-PR45 Southern US 2020','agency':'Department of War','date':'2020','loc':'Southern United States','type':'VID'},
    {'title':'DoD - DOW-UAP-PR46 East China Sea 2024','agency':'Department of War','date':'2024','loc':'East China Sea','type':'VID'},
    {'title':'DoD - DOW-UAP-PR47 Japan 2023','agency':'Department of War','date':'2023','loc':'Japan','type':'VID'},
    {'title':'DoD - DOW-UAP-PR48 Indo-PACOM 2024','agency':'Department of War','date':'2024','loc':'Indo-PACOM','type':'VID'},
    {'title':'DoD - DOW-UAP-PR49 Dept of Army 2026','agency':'Department of War','date':'2026','loc':'North America','type':'VID'},
]

# ============================================================
# ESCAPE HTML
# ============================================================
def esc(s):
    if not isinstance(s, str):
        s = str(s)
    return s.replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"').replace("'", '&#39;')

# ============================================================
# BUILD TOP 20 CARDS
# ============================================================
combined = []
for r in r1_top:
    combined.append(('r1', r))
for r in r2_records_js[:10]:
    combined.append(('r2', r))
combined.sort(key=lambda x: -x[1]['score'])
combined = combined[:20]

cards = []
for i, (release, r) in enumerate(combined):
    rank = i + 1
    rel_class = 'release-r1' if release == 'r1' else 'release-r2'
    rel_label = 'R1' if release == 'r1' else 'R2'
    
    img_src = r.get('img', '') or r.get('modal_image', '')
    if img_src:
        img_html = '<img class="card-image" src="' + esc(img_src) + '" alt="' + esc(r['title']) + '" onclick="openModal(\'' + esc(img_src) + '\', \'' + esc(r['title']) + '\')">'
    else:
        img_html = '<div class="card-image-placeholder">🛸</div>'
    
    pdf_link = r.get('pdf', '') or r.get('pdf_link', '')
    pdf_btn = '<a href="' + esc(pdf_link) + '" target="_blank" class="btn-pdf">📄 PDF</a>' if pdf_link else ''
    
    date_val = r.get('date', r.get('incident_date', ''))
    loc_val = r.get('loc', r.get('incident_location', ''))
    desc_val = r.get('desc', r.get('description', ''))
    
    card = '<div class="top-card">'
    card += '<div class="rank">' + str(rank) + '</div>'
    card += '<div class="release-badge ' + rel_class + '">' + rel_label + '</div>'
    card += img_html
    card += '<div class="card-body">'
    card += '<div class="card-type type-' + r['type'] + '">' + r['type'] + '</div>'
    card += '<div class="card-title">' + esc(r['title']) + '</div>'
    card += '<div class="card-meta"><span class="agency">' + esc(r['agency']) + '</span><span>' + esc(date_val) + '</span><span>' + esc(loc_val) + '</span></div>'
    card += '<div class="card-desc">' + esc(desc_val) + '</div>'
    card += '<div class="card-links">' + pdf_btn + '</div>'
    card += '</div></div>'
    cards.append(card)

top20_html = '\n'.join(cards)

# ============================================================
# BUILD FULL TABLE
# ============================================================
rows = []
idx = 0
for r in r1_table:
    idx += 1
    row = '<tr class="r1-row"><td>' + str(idx) + '</td><td><span class="rel-badge r1">R1</span></td><td>' + esc(r['title']) + '</td><td>' + esc(r['agency']) + '</td><td>' + esc(r['date']) + '</td><td>' + esc(r['loc']) + '</td><td><span class="table-type ' + r['type'] + '">' + r['type'] + '</span></td></tr>'
    rows.append(row)
for r in r2_data:
    idx += 1
    title = r.get('title', 'N/A')
    agency = r.get('agency', 'N/A')
    date = r.get('incident_date', 'N/A')
    loc = r.get('incident_location', 'N/A')
    rtype = r.get('type', 'PDF')
    row = '<tr class="r2-row"><td>' + str(idx) + '</td><td><span class="rel-badge r2">R2</span></td><td>' + esc(title) + '</td><td>' + esc(agency) + '</td><td>' + esc(date) + '</td><td>' + esc(loc) + '</td><td><span class="table-type ' + rtype + '">' + rtype + '</span></td></tr>'
    rows.append(row)

table_html = '\n'.join(rows)

# ============================================================
# READ TEMPLATE AND GENERATE
# ============================================================
with open('top_dashboard.html', 'r', encoding='utf-8') as f:
    template = f.read()

output = template.replace('<!--TOP20_PLACEHOLDER-->', top20_html)
output = output.replace('<!--TABLE_PLACEHOLDER-->', table_html)

with open('top_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(output)

print("TOP DASHBOARD generado exitosamente!")
print("  - " + str(len(r1_top)) + " registros R1 top")
print("  - " + str(len(r2_data)) + " registros R2")
print("  - Total en tabla: " + str(len(r1_table) + len(r2_data)))
