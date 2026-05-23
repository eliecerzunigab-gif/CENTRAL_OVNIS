import json

# Read the JSON data
with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Translation mappings for agencies
agency_translations = {
    'Department of War': 'Departamento de Guerra',
    'FBI': 'FBI',
    'NASA': 'NASA',
    'Department of State': 'Departamento de Estado',
    'Central Intelligence Agency': 'Agencia Central de Inteligencia (CIA)',
    'Office of the Director of National Intelligence': 'Oficina del Director de Inteligencia Nacional (ODNI)',
    'Department of Energy': 'Departamento de Energía (DOE)'
}

# Translation mappings for locations
location_translations = {
    'Western United States': 'Oeste de EE.UU.',
    'Syria': 'Siria',
    'Iraq': 'Irak',
    'Moon': 'Luna',
    'Arabian Gulf': 'Golfo Arábigo',
    'Persian Gulf': 'Golfo Pérsico',
    'United States': 'Estados Unidos',
    'Mediterranean Sea': 'Mar Mediterráneo',
    'Middle East': 'Oriente Medio',
    'Greece': 'Grecia',
    'United Arab Emirates': 'Emiratos Árabes Unidos',
    'Gulf of Oman': 'Golfo de Omán',
    'Low Earth Orbit': 'Órbita Terrestre Baja',
    'Germany': 'Alemania',
    'Aegean Sea': 'Mar Egeo',
    'Arabian Sea': 'Mar Arábigo',
    'Gulf of Aden': 'Golfo de Adén',
    'Strait of Hormuz': 'Estrecho de Ormuz',
    'Netherlands': 'Países Bajos',
    'Azerbaijan': 'Azerbaiyán',
    'Papua New Guinea': 'Papúa Nueva Guinea',
    'Kazakhstan': 'Kazajistán',
    'Georgia': 'Georgia',
    'Turkmenistan': 'Turkmenistán',
    'Mexico': 'México',
    'Djibouti': 'Yibuti',
    'Southern United States': 'Sur de EE.UU.',
    'East China Sea': 'Mar de China Oriental',
    'Japan': 'Japón',
    'Indo-PACOM': 'INDOPACOM',
    'North America': 'América del Norte',
    'N/A': 'N/D'
}

# Translate agencies
translated_agencies = {}
for eng, count in data['agencies'].items():
    translated_agencies[agency_translations.get(eng, eng)] = count
data['agencies'] = translated_agencies

# Translate locations
translated_locations = {}
for eng, count in data['top_locations'].items():
    translated_locations[location_translations.get(eng, eng)] = count
data['top_locations'] = translated_locations

# Translate descriptions for top10
description_translations = {
    "As part of the review of historical UAP materials under PURSUE, DOW has opened a case to investigate the accompanying NASA photograph from the Apollo 17 mission, taken December 1972. The image contains three": 
        "Como parte de la revisión de materiales históricos UAP bajo PURSUE, el Departamento de Guerra abrió un caso para investigar la fotografía de la NASA de la misión Apolo 17, tomada en diciembre de 1972. La imagen contiene tres",
    "This is an FBI 302 interview conducted with a senior US intelligence official regarding his first-hand account of a UAP encounter at a US military facility. USPER relayed to FBI agents that he and oth":
        "Esta es una entrevista FBI 302 realizada a un alto oficial de inteligencia de EE.UU. sobre su testimonio de primera mano de un encuentro UAP en una instalación militar estadounidense. El testigo relató a agentes del FBI que él y otro",
    "This archival photograph depicts the lunar surface as viewed from the landing site of Apollo 12. This image features a highlighted area of interest slightly to the right of the vertical axis of the fr":
        "Esta fotografía de archivo muestra la superficie lunar vista desde el lugar de alunizaje del Apolo 12. La imagen presenta un área de interés resaltada ligeramente a la derecha del eje vertical del fr",
    "This archival photograph depicts the lunar surface as viewed from the landing site of Apollo 12. This image features two highlighted areas of interest, labeled":
        "Esta fotografía de archivo muestra la superficie lunar vista desde el lugar de alunizaje del Apolo 12. La imagen presenta dos áreas de interés resaltadas, etiquetadas",
    "This archival photograph depicts the lunar surface as viewed from the landing site of Apollo 12. This image features a highlighted area of interest near the right edge of the frame, above the horizon,":
        "Esta fotografía de archivo muestra la superficie lunar vista desde el lugar de alunizaje del Apolo 12. La imagen presenta un área de interés cerca del borde derecho del encuadre, sobre el horizonte,",
    "This archival photograph depicts the lunar surface as viewed from the landing site of Apollo 12. This image features a highlighted area of interest slightly to the left of the vertical axis of the fra":
        "Esta fotografía de archivo muestra la superficie lunar vista desde el lugar de alunizaje del Apolo 12. La imagen presenta un área de interés resaltada ligeramente a la izquierda del eje vertical del",
    "This archival photograph depicts the lunar surface as viewed from the landing site of Apollo 12. This image features five highlighted areas of interest, labeled":
        "Esta fotografía de archivo muestra la superficie lunar vista desde el lugar de alunizaje del Apolo 12. La imagen presenta cinco áreas de interés resaltadas, etiquetadas",
    "Actual site photo with FBI Lab rendered graphic overlay depicting corroborating eyewitness reports from September 2023 of an apparent ellipsoid bronze metallic object materializing out of a bright lig":
        "Foto real del sitio con superposición gráfica del laboratorio del FBI que representa informes de testigos presenciales de septiembre de 2023 sobre un aparente objeto metálico bronce elipsoide materializándose de una luz brillante",
    "Apollo 12 was the fourth crewed U.S. mission to the Moon and the second to land astronauts on the lunar surface. This document is an excerpt from the Apollo 12 Technical Air-to-Ground Voice Transcript":
        "El Apolo 12 fue la cuarta misión tripulada estadounidense a la Luna y la segunda en aterrizar astronautas en la superficie lunar. Este documento es un extracto de la Transcripción Técnica de Voz Aire-Tierra del Apolo 12",
    "Apollo 17 was the ninth crewed U.S. mission to the Moon, and the sixth to land astronauts on the lunar surface. This document is an excerpt from the Apollo 17 Technical Air-to-Ground Voice Transcription":
        "El Apolo 17 fue la novena misión tripulada estadounidense a la Luna y la sexta en aterrizar astronautas en la superficie lunar. Este documento es un extracto de la Transcripción Técnica de Voz Aire-Tierra del Apolo 17",
    # Nuevas descripciones de registros CIA, ODNI, DOE
    "This document is a Central Intelligence Agency (CIA) intelligence information report (IIR) that describes human intelligence gathering activities in t":
        "Este documento es un informe de información de inteligencia (IIR) de la Agencia Central de Inteligencia (CIA) que describe actividades de recopilación de inteligencia humana en",
    "This document is a first-hand account written by a currently serving (May 2026) senior U.S. intelligence official. The official was part of a team inv":
        "Este documento es un relato de primera mano escrito por un alto oficial de inteligencia de EE.UU. actualmente en servicio (mayo 2026). El oficial formaba parte de un equipo que invest",
    "This document is a Department of Energy (DOE) report containing enhanced imagery of the Pantex Plant in Texas. The imagery was produced by the DOE's":
        "Este documento es un informe del Departamento de Energía (DOE) que contiene imágenes mejoradas de la Planta Pantex en Texas. Las imágenes fueron producidas por el",
    "This document is a Department of Energy (DOE) report containing correspondence from James Tuck, a British physicist who worked at the Los Alamos National Laboratory in the 1970s. The correspondence discusses":
        "Este documento es un informe del Departamento de Energía (DOE) que contiene correspondencia de James Tuck, un físico británico que trabajó en el Laboratorio Nacional de Los Álamos en la década de 1970. La correspondencia discute",
    "This document is a Department of Energy (DOE) report containing an invitation letter from Pajarito Astronomers to a local resident in 1986. The letter invites":
        "Este documento es un informe del Departamento de Energía (DOE) que contiene una carta de invitación de Pajarito Astronomers a un residente local en 1986. La carta invita",
}


# Translate top10 descriptions
for item in data['top10']:
    desc = item['description']
    for eng, esp in description_translations.items():
        if desc.startswith(eng):
            item['description'] = esp + desc[len(eng):]
            break

# Translate all_records descriptions (same logic)
for item in data['all_records']:
    desc = item['description']
    for eng, esp in description_translations.items():
        if desc.startswith(eng):
            item['description'] = esp + desc[len(eng):]
            break

# Translate locations in records
for item in data['top10']:
    if item['incident_location'] in location_translations:
        item['incident_location'] = location_translations[item['incident_location']]
    if item['agency'] in agency_translations:
        item['agency'] = agency_translations[item['agency']]

for item in data['all_records']:
    if item['incident_location'] in location_translations:
        item['incident_location'] = location_translations[item['incident_location']]
    if item['agency'] in agency_translations:
        item['agency'] = agency_translations[item['agency']]

# Save translated data
with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Datos traducidos al español")
print(f"   Agencias: {list(data['agencies'].keys())}")
print(f"   Top ubicaciones: {list(data['top_locations'].keys())[:5]}")
print(f"   Top10 #1: {data['top10'][0]['title']}")
print(f"   Top10 #1 desc: {data['top10'][0]['description'][:80]}...")
