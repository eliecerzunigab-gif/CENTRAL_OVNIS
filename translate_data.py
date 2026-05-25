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
    'Department of Energy': 'Departamento de Energía (DOE)',
    'Department of the Air Force': 'Departamento de la Fuerza Aérea',
    'Department of the Army': 'Departamento del Ejército',
    'United States Central Command': 'Comando Central de EE.UU. (CENTCOM)',
    'United States Indo-Pacific Command': 'Comando del Indo-Pacífico de EE.UU. (INDOPACOM)',
    'United States Northern Command': 'Comando del Norte de EE.UU. (NORTHCOM)',
    'United States Africa Command': 'Comando de África de EE.UU. (AFRICOM)',
    'United States European Command': 'Comando Europeo de EE.UU. (EUCOM)',
    'United States Southern Command': 'Comando del Sur de EE.UU. (SOUTHCOM)',
    'United States Space Command': 'Comando Espacial de EE.UU. (SPACECOM)',
    'United States Transportation Command': 'Comando de Transporte de EE.UU. (TRANSCOM)',
    'United States Strategic Command': 'Comando Estratégico de EE.UU. (STRATCOM)',
    'United States Cyber Command': 'Comando Cibernético de EE.UU. (CYBERCOM)',
    'United States Special Operations Command': 'Comando de Operaciones Especiales de EE.UU. (SOCOM)',
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
    'N/A': 'N/D',
    'CENTCOM': 'CENTCOM',
    'INDOPACOM': 'INDOPACOM',
    'Kuwait': 'Kuwait',
    'Iran': 'Irán',
    'Afghanistan': 'Afganistán',
    'Africa': 'África',
    'Vandenberg AFB': 'Base Vandenberg AFB',
    'Pacific Time Zone': 'Zona Horaria del Pacífico',
    'Department of the Army': 'Departamento del Ejército',
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

# Translation mappings for descriptions
description_translations = {
    "As part of the review of historical UAP materials under PURSUE, DOW has opened a case to investigate the accompanying NASA photograph from the Apollo 17 mission, taken December 1972. The image contains three": 
        "Como parte de la revisión de materiales históricos UAP bajo PURSUE, el Departamento de Guerra abrió un caso para investigar la fotografía de la NASA de la misión Apolo 17, tomada en diciembre de 1972. La imagen contiene tres",
    "This is an FBI 302 interview conducted with a senior US intelligence official regarding his first-hand account of a UAP encounter at a US military facility. USPER relayed to FBI agents that he and oth":
        "Esta es una entrevista FBI 302 realizada a un alto oficial de inteligencia de EE.UU. sobre su testimonio de primera mano de un encuentro UAP en una instalación militar estadounidense. El testigo relató a agentes del FBI que él y otro",
    "This archival photograph depicts the lunar surface as viewed from the landing site of Apollo 12. This image features a highlighted area of interest slightly to the right of the vertical axis of the fr":
        "Esta fotografía de archivo muestra la superficie lunar vista desde el lugar de alunizaje del Apolo 12. La imagen presenta un área de interés resaltada ligeramente a la derecha del eje vertical del",
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
    # FBI reports
    "The Federal Bureau of Investigation (FBI) submitted a report":
        "La Oficina Federal de Investigación (FBI) presentó un informe",
    # Mission Reports
    "This document is a Mission Report (MISREP), a standardized r":
        "Este documento es un Informe de Misión (MISREP), un formato estandarizado",
    # House of Representatives
    "On March 6, 2026, eight members of the U.S. House of Represe":
        "El 6 de marzo de 2026, ocho miembros de la Cámara de Representantes de EE.UU.",
    # CENTCOM reports
    "The United States Central Command submitted a report of an u":
        "El Comando Central de EE.UU. presentó un informe de un",
    # FBI 62-HQ-83894
    "The FBI's 62-HQ-83894 case file includes investigative recor":
        "El archivo del caso 62-HQ-83894 del FBI incluye registros de investigación",
    # Apollo 11
    "Apollo 11 was the third crewed mission to the Moon and the f":
        "El Apolo 11 fue la tercera misión tripulada a la Luna y la primera",
    # Mexican Congress
    "On September 12, 20023 the Mexican Congress heard testimony ":
        "El 12 de septiembre de 2023, el Congreso Mexicano escuchó el testimonio",
    # Audio recordings
    "This audio recording contains air to ground communications a":
        "Esta grabación de audio contiene comunicaciones aire-tierra",
    # Gemini 7
    "Gemini 7 was the tenth crewed American spaceflight. This doc":
        "El Gemini 7 fue el décimo vuelo espacial tripulado estadounidense. Este documento",
    # Georgia incident
    "On October 28-29, there was an incident alleged by the Georg":
        "El 28-29 de octubre, hubo un incidente alegado por el gobierno de Georgia",
    # Turkmenistan
    "UFOlogists of Turkmenistan has gained a positive reputation ":
        "Los ufólogos de Turkmenistán han ganado una reputación positiva",
    # Skylab
    "Launched on May 14, 1973, Skylab was the United States' firs":
        "Lanzado el 14 de mayo de 1973, Skylab fue la primera estación espacial de EE.UU.",
    # Mission briefing
    "This document is a mission briefing summarizing an observati":
        "Este documento es un informe de misión que resume una observación",
    # Modeling report
    "This report describes the Modeling of Unlikely Space-Booster":
        "Este informe describe el Modelado de Fragmentos Espaciales Improbables",
    # Launch summary
    "This report summarizes the historical record of launches occ":
        "Este informe resume el registro histórico de lanzamientos ocurridos",
    # INDOPACOM
    "The United States Indo-Pacific Command submitted a report of":
        "El Comando del Indo-Pacífico de EE.UU. presentó un informe de",
    # Email correspondence
    "This document is email correspondence describing the content":
        "Este documento es una correspondencia por correo electrónico que describe el contenido",
    # State Department cables
    "This document is a U.S. Department of State diplomatic cable":
        "Este documento es un cable diplomático del Departamento de Estado de EE.UU.",
    # Range Fouler Debrief
    "This document is a Range Fouler Debrief, a standardized repo":
        "Este documento es un Informe de Incidente (Range Fouler Debrief), un formato estandarizado",
    "This document is a Range Fouler Debrief Form, a standardized":
        "Este documento es un Formulario de Informe de Incidente (Range Fouler Debrief), un formato estandarizado",
    "This document is a Range Fouler Reporting Form, a standardiz":
        "Este documento es un Formulario de Reporte de Incidente (Range Fouler), un formato estandarizado",
    # Incident summaries
    "Each of these incident summaries includes a \"Check-List - Un":
        "Cada uno de estos resúmenes de incidentes incluye una \"Lista de Verificación",
    # FBI 302 interview
    "This is an FBI 302 interview conducted with a US citizen reg":
        "Esta es una entrevista FBI 302 realizada a un ciudadano estadounidense sobre",
    # NORTHCOM
    "The United States Northern Command submitted a report of an ":
        "El Comando del Norte de EE.UU. presentó un informe de un",
    # AFRICOM
    "The United States Africa Command submitted a report of an un":
        "El Comando de África de EE.UU. presentó un informe de un",
    # Air Force
    "The Department of the Air Force submitted a report of an uni":
        "El Departamento de la Fuerza Aérea presentó un informe de un",
    # Army
    "The Department of the Army submitted a report of an unidenti":
        "El Departamento del Ejército presentó un informe de un",
    # Armed Forces documentation
    "This file contains 116 pages of documentation from the Armed":
        "Este archivo contiene 116 páginas de documentación de las Fuerzas Armadas",
    # Apollo 12 medical debriefing
    "During a medical debriefing of the crew of the Apollo 12 mis":
        "Durante una sesión informativa médica de la tripulación de la misión Apolo 12",
    # Apollo 11 final mission
    "During the eleventh and final crewed mission in the Apollo p":
        "Durante la undécima y última misión tripulada del programa Apolo",
    # Air Force intelligence 1948
    "An Air Force intelligence report from November 1948 relating":
        "Un informe de inteligencia de la Fuerza Aérea de noviembre de 1948 relacionado con",
    # PR094
    "46. DOW-UAP-PR094, \"[CALLSIGN] (Mission) - HD 2020-02-13\"On ":
        "46. DOW-UAP-PR094, \"[CALLSIGN] (Misión) - HD 2020-02-13\"El",
    # Apollo 17 final
    "Approximately one hour and 41 minutes into the final and lon":
        "Aproximadamente una hora y 41 minutos del último y más largo",
    # Mercury Atlas 9
    "During the final and longest flight of Project Mercury, Merc":
        "Durante el vuelo final y más largo del Proyecto Mercury, la Mercury",
    # Mercury Atlas 8
    "During the Mercury Atlas 8 mission, Sigma 7 pilot Walter M. ":
        "Durante la misión Mercury Atlas 8, el piloto del Sigma 7, Walter M.",
    # Mercury Atlas 7
    "During the fourth crewed spaceflight and second orbital flig":
        "Durante el cuarto vuelo espacial tripulado y segundo vuelo orbital",
    # Mercury recovery
    "During the recovery of the fourth launch and second crewed s":
        "Durante la recuperación del cuarto lanzamiento y segundo vuelo espacial tripulado",
    # Pajarito Astronomers
    "A letter to the members of the Pajarito Astronomers club reg":
        "Una carta a los miembros del club Pajarito Astronomers sobre",
    # US PERSON statements
    "This document is a summary of statements by seven US PERSONs":
        "Este documento es un resumen de declaraciones de siete PERSONAS de EE.UU.",
    # Pantex incident
    "A Pantex Unidentified Object Incident Report that includes a":
        "Un Informe de Incidente de Objeto No Identificado de Pantex que incluye un",
    # FBI 1957
    "An FBI report from 1957 detailing the interview with Wladysl":
        "Un informe del FBI de 1957 que detalla la entrevista con Wladyslaw",
    # Air Intelligence 1955
    "Air Intelligence Information Report, 14 October 1955, Report":
        "Informe de Inteligencia Aérea, 14 de octubre de 1955, Reporte",
    # FBI 1958
    "An FBI memo from 1958 reporting a UFO sighting by a Detroit ":
        "Un memorando del FBI de 1958 que reporta un avistamiento OVNI por un",
    # James Tuck correspondence
    "Personal correspondence to and from James Tuck, a Los Alamos":
        "Correspondencia personal hacia y desde James Tuck, un científico de Los Álamos",
    # SHAEF messages
    "This file contains SHAEF messages and memorandums related to":
        "Este archivo contiene mensajes y memorandos del SHAEF relacionados con",
    # Incident reports
    "This file primarily contains incident reports on Unidentifie":
        "Este archivo contiene principalmente informes de incidentes sobre Objetos Voladores No Identificados",
    # Executive Office memo
    "This memorandum, dated July 18, 1963, from the Executive Off":
        "Este memorando, fechado el 18 de julio de 1963, de la Oficina Ejecutiva",
    # Memorandums and correspondence
    "This file contains memorandums, correspondence, and forms re":
        "Este archivo contiene memorandos, correspondencia y formularios relacionados con",
    # Independent report on UFOs
    "This file contains an independent report on UFOs written by ":
        "Este archivo contiene un informe independiente sobre OVNIs escrito por",
    # July 28, 1952 memo
    "This two page memorandum, dated July 28, 1952, relates to in":
        "Este memorando de dos páginas, fechado el 28 de julio de 1952, se relaciona con",
    # Memorandums related to
    "This file contains memorandums and correspondence related to":
        "Este archivo contiene memorandos y correspondencia relacionados con",
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
