#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de DASHBOARD COMPARATIVO - Central Ovnis
Release 1 vs Release 2 - Responsive, con videos
"""

import json
from datetime import datetime

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_records = data['all_records']

def clasificar(r):
    modal = r.get('modal_image', '')
    pdf = r.get('pdf_link', '')
    agency = r.get('agency', '')
    if '/052226/release_02/' in modal or '/052226/release_02/' in pdf:
        return 'release2'
    if agency in ['Agencia Central de Inteligencia (CIA)', 'Oficina del Director de Inteligencia Nacional (ODNI)', 'Departamento de Energía (DOE)']:
        return 'release2'
    if r.get('type') == 'VID' and r.get('score', 0) == 13:
        return 'release2'
    return 'release1'

release1 = [r for r in all_records if clasificar(r) == 'release1']
release2 = [r for r in all_records if clasificar(r) == 'release2']

print(f"Release 1: {len(release1)} | Release 2: {len(release2)}")

def esc(s):
    if not isinstance(s, str): s = str(s)
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def calc_stats(records):
    total = len(records)
    types = {}; agencies = {}; locs = {}
    scores = [r.get('score',0) for r in records]
    for r in records:
        t = r.get('type','PDF'); types[t] = types.get(t,0)+1
        a = r.get('agency','?'); agencies[a] = agencies.get(a,0)+1
        l = r.get('incident_location',''); 
        if l: locs[l] = locs.get(l,0)+1
    avg = round(sum(scores)/len(scores),1) if scores else 0
    return {'total':total,'types':types,'agencies':agencies,'locs':locs,'avg_score':avg}

s1 = calc_stats(release1)
s2 = calc_stats(release2)

def build_bars(d, mx, w='100px', cls=''):
    r = []
    for n,c in sorted(d.items(), key=lambda x:-x[1]):
        p = (c/mx)*100 if mx else 0
        r.append(f'<div class="bar-row"><span class="bar-label">{esc(n)}</span><div class="bar-track"><div class="bar-fill {cls}" style="width:{p:.0f}%"></div></div><span class="bar-count">{c}</span></div>')
    return '\n'.join(r)

def build_top10(recs):
    c = []
    for i,r in enumerate(sorted(recs, key=lambda x:-x.get('score',0))[:10]):
        rank=i+1; img=r.get('modal_image',''); rtype=r.get('type','PDF')
        pdf_link = r.get('pdf_link','')
        
        # Si es VIDEO, mostrar reproductor de video
        if rtype == 'VID' and pdf_link:
            media_html = f'''
            <div class="card-media">
              <video class="card-video" controls preload="metadata" onclick="event.stopPropagation()">
                <source src="{esc(pdf_link)}" type="video/mp4">
                Tu navegador no soporta video.
              </video>
              <div class="video-badge">▶ VIDEO</div>
            </div>'''
        elif img:
            media_html = f'<img class="card-img" src="{esc(img)}" alt="{esc(r["title"])}" onclick="openModal(\'{esc(img)}\',\'{esc(r["title"])}\')">'
        else:
            media_html = '<div class="card-img-placeholder">🛸</div>'
        
        pb = f'<a href="{esc(pdf_link)}" target="_blank" class="btn-pdf">📄 PDF</a>' if pdf_link and rtype != 'VID' else ''
        if rtype == 'VID' and pdf_link:
            pb = f'<a href="{esc(pdf_link)}" target="_blank" class="btn-video">🎬 Ver Video</a>'
        
        dv=r.get('incident_date',''); lv=r.get('incident_location',''); dv2=r.get('description','')[:150]; sc=r.get('score',0)
        card=f'''<div class="top-card">
<div class="top-rank">{rank}</div>
<div class="score-badge">{sc}</div>
{media_html}
<div class="card-body">
<div class="card-type type-{rtype}">{rtype}</div>
<div class="card-title">{esc(r["title"])}</div>
<div class="card-meta"><span class="card-agency">{esc(r["agency"])}</span><span>{esc(dv)}</span><span>{esc(lv)}</span></div>
<div class="card-desc">{esc(dv2)}</div>
<div class="card-links">{pb}</div>
</div></div>'''
        c.append(card)
    return '\n'.join(c)

def build_table(recs):
    r = []
    for i,rec in enumerate(recs):
        n=i+1; t=rec.get('title','?'); a=rec.get('agency','?'); d=rec.get('incident_date','?'); l=rec.get('incident_location','?'); tp=rec.get('type','PDF'); sc=rec.get('score',0)
        r.append(f'<tr><td data-label="#">{n}</td><td data-label="Titulo">{esc(t)}</td><td data-label="Agencia">{esc(a)}</td><td data-label="Fecha">{esc(d)}</td><td data-label="Ubicacion">{esc(l)}</td><td data-label="Tipo"><span class="table-type {tp}">{tp}</span></td><td data-label="Score"><span class="score-cell">{sc}</span></td></tr>')
    return '\n'.join(r)

mx_a = max(max(s1['agencies'].values()) if s1['agencies'] else 1, max(s2['agencies'].values()) if s2['agencies'] else 1)

t10_1 = build_top10(release1)
t10_2 = build_top10(release2)
tbl_1 = build_table(release1)
tbl_2 = build_table(release2)
ab1 = build_bars(s1['agencies'], mx_a)
ab2 = build_bars(s2['agencies'], mx_a)

now = datetime.now().strftime('%d/%m/%Y %H:%M')

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>CENTRAL OVNIS - Comparativa Release 1 vs Release 2</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0a0e1a;--bg2:#111827;--card:#1a1f35;--card-hover:#222a45;--text:#e2e8f0;--text2:#94a3b8;--text-muted:#64748b;--accent:#00d4ff;--accent2:#7c3aed;--accent3:#f59e0b;--accent4:#10b981;--border:#1e293b;--r1:#3b82f6;--r2:#f59e0b}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;font-size:16px;line-height:1.5}}
body::before{{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 20% 50%,rgba(0,212,255,0.03) 0%,transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(124,58,237,0.03) 0%,transparent 50%);pointer-events:none;z-index:0}}
.container{{max-width:1500px;margin:0 auto;padding:16px;position:relative;z-index:1}}

/* HEADER */
.header{{text-align:center;padding:30px 16px 24px;border-bottom:1px solid var(--border);margin-bottom:24px}}
.header h1{{font-family:'Orbitron',sans-serif;font-size:clamp(1.3em,4vw,2.2em);font-weight:800;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px}}
.header .subtitle{{color:var(--text2);font-size:clamp(0.7em,2vw,1em);margin-top:6px;letter-spacing:2px;text-transform:uppercase}}
.header .badge-row{{display:flex;justify-content:center;gap:8px;margin-top:12px;flex-wrap:wrap}}
.header .badge{{display:inline-flex;align-items:center;gap:4px;padding:5px 10px;border-radius:20px;font-size:clamp(10px,2vw,12px);font-weight:600}}
.badge-r1{{background:rgba(59,130,246,0.15);color:var(--r1);border:1px solid rgba(59,130,246,0.3)}}
.badge-r2{{background:rgba(245,158,11,0.15);color:var(--r2);border:1px solid rgba(245,158,11,0.3)}}
.badge-total{{background:rgba(16,185,129,0.15);color:var(--accent4);border:1px solid rgba(16,185,129,0.3)}}

/* COMPARISON CARDS */
.comparison-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:24px}}
.comp-card{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;text-align:center}}
.comp-card.r1{{border-color:rgba(59,130,246,0.3)}}
.comp-card.r2{{border-color:rgba(245,158,11,0.3)}}
.comp-card .release-label{{font-family:'Orbitron',sans-serif;font-size:clamp(11px,2vw,14px);font-weight:700;letter-spacing:1px;margin-bottom:6px}}
.comp-card .big-number{{font-family:'Orbitron',sans-serif;font-size:clamp(2em,6vw,3em);font-weight:800}}
.comp-card .sub-text{{font-size:clamp(10px,1.5vw,12px);color:var(--text-muted);margin-top:4px}}
.comp-card .stats-row{{display:flex;justify-content:center;gap:clamp(8px,2vw,20px);margin-top:10px;flex-wrap:wrap}}
.comp-card .stat-item{{text-align:center;min-width:40px}}
.comp-card .stat-item .stat-number{{font-size:clamp(1em,3vw,1.3em);font-weight:700;font-family:'Orbitron',sans-serif}}
.comp-card .stat-item .stat-label{{font-size:clamp(8px,1.5vw,10px);color:var(--text-muted);text-transform:uppercase;letter-spacing:1px}}

/* VS DIVIDER */
.vs-divider{{display:flex;align-items:center;justify-content:center;gap:12px;margin:8px 0 24px}}
.vs-divider .line{{flex:1;height:1px;background:var(--border)}}
.vs-divider .vs-text{{font-family:'Orbitron',sans-serif;font-size:clamp(1em,3vw,1.5em);font-weight:800;color:var(--accent);text-shadow:0 0 20px rgba(0,212,255,0.3);padding:0 8px}}

/* SECTION TITLE */
.section-title{{font-family:'Orbitron',sans-serif;font-size:clamp(0.9em,2.5vw,1.3em);font-weight:700;color:var(--text);margin-bottom:16px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.section-title .dot{{width:8px;height:8px;border-radius:50%;display:inline-block;flex-shrink:0}}
.section-title .dot.r1{{background:var(--r1);box-shadow:0 0 10px var(--r1)}}
.section-title .dot.r2{{background:var(--r2);box-shadow:0 0 10px var(--r2)}}

/* SPLIT LAYOUT */
.split-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:32px}}
.split-card{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;overflow:hidden}}
.split-card.r1{{border-color:rgba(59,130,246,0.2)}}
.split-card.r2{{border-color:rgba(245,158,11,0.2)}}
.split-card .split-header{{display:flex;align-items:center;gap:8px;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border);flex-wrap:wrap}}
.split-card .split-header .split-icon{{width:10px;height:10px;border-radius:50%;flex-shrink:0}}
.split-card .split-header .split-icon.r1{{background:var(--r1)}}
.split-card .split-header .split-icon.r2{{background:var(--r2)}}
.split-card .split-header .split-label{{font-family:'Orbitron',sans-serif;font-size:clamp(11px,2vw,13px);font-weight:700;letter-spacing:1px}}
.split-card .split-header .split-count{{font-size:clamp(10px,1.5vw,12px);color:var(--text-muted);margin-left:auto}}

/* AGENCY BARS */
.bars-container{{display:flex;flex-direction:column;gap:4px}}
.bar-row{{display:flex;align-items:center;gap:6px}}
.bar-label{{font-size:clamp(9px,1.5vw,11px);color:var(--text2);width:clamp(70px,15vw,120px);text-align:right;flex-shrink:0;line-height:1.2;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.bar-track{{flex:1;height:clamp(12px,2vw,18px);background:var(--bg2);border-radius:4px;overflow:hidden;min-width:40px}}
.bar-fill{{height:100%;border-radius:4px;transition:width 1s ease;background:linear-gradient(90deg,var(--r1),rgba(59,130,246,0.4))}}
.bar-fill.r2-fill{{background:linear-gradient(90deg,var(--r2),rgba(245,158,11,0.4))}}
.bar-count{{font-size:clamp(9px,1.5vw,11px);color:var(--text-muted);width:clamp(20px,4vw,30px);text-align:left;flex-shrink:0}}

/* TOP 10 CARDS */
.top10-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(clamp(260px,40vw,320px),1fr));gap:12px}}
.top-card{{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;transition:all .3s;position:relative}}
.top-card:hover{{border-color:rgba(0,212,255,0.3);transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,0,0,0.4)}}
.top-card .top-rank{{position:absolute;top:8px;left:8px;width:28px;height:28px;background:rgba(0,0,0,0.7);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:clamp(10px,2vw,12px);font-weight:800;color:var(--accent);z-index:2;font-family:'Orbitron',sans-serif;border:1px solid rgba(0,212,255,0.3)}}
.top-card .score-badge{{position:absolute;top:8px;right:8px;padding:2px 8px;border-radius:10px;font-size:clamp(8px,1.5vw,10px);font-weight:700;z-index:2;letter-spacing:1px;background:rgba(16,185,129,0.2);color:var(--accent4);border:1px solid rgba(16,185,129,0.3)}}

/* Card Media (image or video) */
.card-media{{position:relative;width:100%;height:clamp(140px,30vw,200px);overflow:hidden;background:#000}}
.card-video{{width:100%;height:100%;object-fit:contain;background:#000;cursor:pointer}}
.video-badge{{position:absolute;bottom:8px;left:8px;padding:3px 8px;background:rgba(239,68,68,0.8);color:#fff;border-radius:4px;font-size:clamp(9px,1.5vw,11px);font-weight:700;letter-spacing:1px;z-index:2}}
.card-img{{width:100%;height:clamp(140px,30vw,200px);object-fit:cover;cursor:pointer;transition:transform .3s}}
.card-img:hover{{transform:scale(1.05)}}
.card-img-placeholder{{width:100%;height:clamp(140px,30vw,200px);display:flex;align-items:center;justify-content:center;font-size:2.5em;background:linear-gradient(135deg,var(--bg2),var(--card))}}
.card-body{{padding:12px}}
.card-type{{display:inline-block;padding:2px 6px;border-radius:3px;font-size:clamp(8px,1.5vw,10px);font-weight:700;letter-spacing:1px;margin-bottom:4px}}
.type-PDF{{background:rgba(239,68,68,0.2);color:#ef4444}}
.type-VID{{background:rgba(139,92,246,0.2);color:#8b5cf6}}
.type-IMG{{background:rgba(16,185,129,0.2);color:#10b981}}
.type-AUD{{background:rgba(245,158,11,0.2);color:#f59e0b}}
.card-title{{font-size:clamp(12px,2vw,14px);font-weight:600;color:var(--text);margin-bottom:4px;line-height:1.3}}
.card-meta{{display:flex;flex-wrap:wrap;gap:4px;font-size:clamp(9px,1.5vw,11px);color:var(--text-muted);margin-bottom:6px}}
.card-meta .card-agency{{color:var(--accent);font-weight:600}}
.card-desc{{font-size:clamp(10px,1.5vw,12px);color:var(--text2);line-height:1.4;margin-bottom:8px}}
.card-links{{display:flex;gap:6px;flex-wrap:wrap}}
.btn-pdf,.btn-video{{display:inline-flex;align-items:center;gap:3px;padding:5px 12px;border-radius:6px;font-size:clamp(9px,1.5vw,11px);font-weight:600;text-decoration:none;transition:all .2s}}
.btn-pdf{{background:rgba(239,68,68,0.15);color:#ef4444}}
.btn-pdf:hover{{background:rgba(239,68,68,0.3)}}
.btn-video{{background:rgba(139,92,246,0.15);color:#8b5cf6}}
.btn-video:hover{{background:rgba(139,92,246,0.3)}}

/* TABLE */
.table-wrapper{{overflow-x:auto;max-height:clamp(300px,60vh,500px);overflow-y:auto;-webkit-overflow-scrolling:touch}}
.data-table{{width:100%;border-collapse:collapse;font-size:clamp(10px,1.5vw,12px)}}
.data-table th{{background:var(--bg2);color:var(--text-muted);padding:8px 8px;text-align:left;font-weight:600;text-transform:uppercase;letter-spacing:1px;font-size:clamp(8px,1.2vw,10px);border-bottom:2px solid var(--border);position:sticky;top:0;z-index:2}}
.data-table td{{padding:6px 8px;border-bottom:1px solid var(--border);color:var(--text2)}}
.data-table tr:hover td{{background:var(--card-hover)}}
.table-type{{display:inline-block;padding:1px 5px;border-radius:3px;font-size:clamp(8px,1.2vw,10px);font-weight:600}}
.table-type.PDF{{background:rgba(239,68,68,0.15);color:#ef4444}}
.table-type.VID{{background:rgba(139,92,246,0.15);color:#8b5cf6}}
.table-type.IMG{{background:rgba(16,185,129,0.15);color:#10b981}}
.table-type.AUD{{background:rgba(245,158,11,0.15);color:#f59e0b}}
.score-cell{{font-family:'Orbitron',sans-serif;font-size:clamp(9px,1.5vw,11px);color:var(--accent4);font-weight:700}}

/* SEARCH */
.search-box{{margin-bottom:10px}}
.search-box input{{width:100%;padding:10px 14px;background:var(--bg2);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:clamp(12px,2vw,14px);font-family:'Inter',sans-serif;outline:none;transition:all .3s;-webkit-appearance:none}}
.search-box input:focus{{border-color:var(--accent);box-shadow:0 0 15px rgba(0,212,255,0.1)}}
.search-box input::placeholder{{color:var(--text-muted)}}

/* MODAL */
.modal-overlay{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.95);z-index:1000;align-items:center;justify-content:center;padding:10px}}
.modal-overlay.active{{display:flex}}
.modal-overlay img,.modal-overlay video{{max-width:98vw;max-height:90vh;border-radius:8px;object-fit:contain}}
.modal-close-btn{{position:absolute;top:10px;right:15px;font-size:clamp(24px,5vw,36px);color:white;cursor:pointer;background:none;border:none;z-index:1001;padding:5px 10px}}
.modal-title-text{{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);color:white;font-size:clamp(11px,2vw,14px);text-align:center;background:rgba(0,0,0,0.7);padding:6px 12px;border-radius:8px;max-width:90%}}

/* FOOTER */
.footer{{text-align:center;padding:24px 16px;border-top:1px solid var(--border);color:var(--text-muted);font-size:clamp(10px,1.5vw,12px);margin-top:16px}}
.footer a{{color:var(--accent);text-decoration:none}}

/* RESPONSIVE - Mobile */
@media(max-width:768px){{
  .container{{padding:10px}}
  .header{{padding:20px 10px 16px}}
  .comparison-grid{{grid-template-columns:1fr;gap:10px}}
  .split-grid{{grid-template-columns:1fr;gap:10px}}
  .top10-grid{{grid-template-columns:1fr}}
  .comp-card .big-number{{font-size:2em}}
  .bar-label{{width:80px;font-size:10px}}
  .bar-track{{height:14px}}
  .section-title{{font-size:0.9em}}
  .split-card{{padding:12px}}
  
  /* Tabla como cards en mobile */
  .data-table thead{{display:none}}
  .data-table tr{{display:block;margin-bottom:8px;border:1px solid var(--border);border-radius:8px;padding:8px}}
  .data-table td{{display:block;text-align:right;padding:4px 8px;border:none;font-size:12px}}
  .data-table td::before{{content:attr(data-label);float:left;font-weight:600;color:var(--text-muted);text-transform:uppercase;font-size:10px;letter-spacing:1px}}
  .data-table tr:hover td{{background:transparent}}
  .table-wrapper{{max-height:none;overflow-y:visible}}
}}

@media(max-width:480px){{
  .header h1{{font-size:1.2em}}
  .header .subtitle{{font-size:0.65em;letter-spacing:1px}}
  .comp-card{{padding:12px}}
  .comp-card .stats-row{{gap:6px}}
  .comp-card .stat-item{{min-width:30px}}
  .comp-card .stat-item .stat-number{{font-size:0.9em}}
  .bar-label{{width:60px;font-size:9px}}
  .bar-track{{height:12px}}
  .bar-count{{font-size:9px}}
  .top-card .top-rank{{width:24px;height:24px;font-size:10px}}
  .card-body{{padding:8px}}
  .card-title{{font-size:11px}}
  .card-desc{{font-size:10px}}
  .card-meta{{font-size:9px}}
}}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>🛸 CENTRAL OVNIS</h1>
<div class="subtitle">Comparativa Release 1 vs Release 2 · Datos Desclasificados del Gobierno de EE.UU.</div>
<div class="badge-row">
<span class="badge badge-r1">🔵 {s1['total']} registros · Release 1</span>
<span class="badge badge-r2">🟡 {s2['total']} registros · Release 2 (NUEVOS)</span>
<span class="badge badge-total">🟢 {s1['total']+s2['total']} registros totales</span>
</div>
</div>

<div class="comparison-grid">
<div class="comp-card r1">
<div class="release-label" style="color:var(--r1)">RELEASE 1</div>
<div class="big-number" style="color:var(--r1)">{s1['total']}</div>
<div class="sub-text">Registros desclasificados · Periodo anterior</div>
<div class="stats-row">
<div class="stat-item"><div class="stat-number" style="color:#ef4444">{s1['types'].get('PDF',0)}</div><div class="stat-label">PDF</div></div>
<div class="stat-item"><div class="stat-number" style="color:#8b5cf6">{s1['types'].get('VID',0)}</div><div class="stat-label">VID</div></div>
<div class="stat-item"><div class="stat-number" style="color:#10b981">{s1['types'].get('IMG',0)}</div><div class="stat-label">IMG</div></div>
<div class="stat-item"><div class="stat-number" style="color:#f59e0b">{s1['types'].get('AUD',0)}</div><div class="stat-label">AUD</div></div>
<div class="stat-item"><div class="stat-number" style="color:var(--accent4)">{s1['avg_score']}</div><div class="stat-label">Score Prom</div></div>
</div>
</div>
<div class="comp-card r2">
<div class="release-label" style="color:var(--r2)">RELEASE 2 · NUEVO</div>
<div class="big-number" style="color:var(--r2)">{s2['total']}</div>
<div class="sub-text">Nuevos registros · Publicado Mayo 2026</div>
<div class="stats-row">
<div class="stat-item"><div class="stat-number" style="color:#ef4444">{s2['types'].get('PDF',0)}</div><div class="stat-label">PDF</div></div>
<div class="stat-item"><div class="stat-number" style="color:#8b5cf6">{s2['types'].get('VID',0)}</div><div class="stat-label">VID</div></div>
<div class="stat-item"><div class="stat-number" style="color:#10b981">{s2['types'].get('IMG',0)}</div><div class="stat-label">IMG</div></div>
<div class="stat-item"><div class="stat-number" style="color:#f59e0b">{s2['types'].get('AUD',0)}</div><div class="stat-label">AUD</div></div>
<div class="stat-item"><div class="stat-number" style="color:var(--accent4)">{s2['avg_score']}</div><div class="stat-label">Score Prom</div></div>
</div>
</div>
</div>

<div class="vs-divider"><div class="line"></div><div class="vs-text">⚡ VS ⚡</div><div class="line"></div></div>

<div class="section-title"><span class="dot r1"></span> Agencias <span class="dot r2" style="margin-left:10px"></span></div>
<div class="split-grid">
<div class="split-card r1">
<div class="split-header"><div class="split-icon r1"></div><div class="split-label" style="color:var(--r1)">RELEASE 1</div><div class="split-count">{len(s1['agencies'])} agencias</div></div>
<div class="bars-container">{ab1}</div>
</div>
<div class="split-card r2">
<div class="split-header"><div class="split-icon r2"></div><div class="split-label" style="color:var(--r2)">RELEASE 2 · NUEVO</div><div class="split-count">{len(s2['agencies'])} agencias</div></div>
<div class="bars-container">{ab2}</div>
</div>
</div>

<div class="section-title"><span class="dot r1"></span> TOP 10 · Release 1 <span class="dot r2" style="margin-left:10px"></span> TOP 10 · Release 2 (Nuevos)</div>
<div class="split-grid">
<div class="split-card r1">
<div class="split-header"><div class="split-icon r1"></div><div class="split-label" style="color:var(--r1)">RELEASE 1</div><div class="split-count">Mejores puntuados</div></div>
<div class="top10-grid">{t10_1}</div>
</div>
<div class="split-card r2">
<div class="split-header"><div class="split-icon r2"></div><div class="split-label" style="color:var(--r2)">RELEASE 2 · NUEVO</div><div class="split-count">Mejores puntuados</div></div>
<div class="top10-grid">{t10_2}</div>
</div>
</div>

<div class="section-title"><span class="dot r1"></span> Todos los Registros · Release 1 ({s1['total']}) <span class="dot r2" style="margin-left:10px"></span> Todos los Registros · Release 2 ({s2['total']})</div>
<div class="split-grid">
<div class="split-card r1">
<div class="split-header"><div class="split-icon r1"></div><div class="split-label" style="color:var(--r1)">RELEASE 1</div><div class="split-count">{s1['total']} registros</div></div>
<div class="search-box"><input type="text" id="search1" placeholder="Buscar en Release 1..." onkeyup="filterTable('search1','table1')"></div>
<div class="table-wrapper"><table class="data-table" id="table1"><thead><tr><th>#</th><th>Titulo</th><th>Agencia</th><th>Fecha</th><th>Ubicacion</th><th>Tipo</th><th>Score</th></tr></thead><tbody>{tbl_1}</tbody></table></div>
</div>
<div class="split-card r2">
<div class="split-header"><div class="split-icon r2"></div><div class="split-label" style="color:var(--r2)">RELEASE 2 · NUEVO</div><div class="split-count">{s2['total']} registros</div></div>
<div class="search-box"><input type="text" id="search2" placeholder="Buscar en Release 2..." onkeyup="filterTable('search2','table2')"></div>
<div class="table-wrapper"><table class="data-table" id="table2"><thead><tr><th>#</th><th>Titulo</th><th>Agencia</th><th>Fecha</th><th>Ubicacion</th><th>Tipo</th><th>Score</th></tr></thead><tbody>{tbl_2}</tbody></table></div>
</div>
</div>

<div class="footer">
<p>🛸 <strong>CENTRAL OVNIS</strong> · Datos desclasificados del gobierno de EE.UU.</p>
<p style="margin-top:4px">Fuentes: <a href="https://www.war.gov" target="_blank">war.gov</a> · <a href="https://www.aaro.mil" target="_blank">AARO</a></p>
<p style="margin-top:4px;font-size:10px;color:var(--text-muted)">Generado el {now} · Comparativa Release 1 vs Release 2</p>
</div>
</div>

<div class="modal-overlay" id="imageModal" onclick="closeModal()">
<button class="modal-close-btn" onclick="closeModal()">&times;</button>
<img id="modalImage" src="" alt="">
<div class="modal-title-text" id="modalTitle"></div>
</div>

<script>
function openModal(src, title) {{
  document.getElementById('modalImage').src = src;
  document.getElementById('modalTitle').textContent = title;
  document.getElementById('imageModal').classList.add('active');
}}
function closeModal() {{
  document.getElementById('imageModal').classList.remove('active');
}}
function filterTable(inputId, tableId) {{
  var input = document.getElementById(inputId);
  var filter = input.value.toUpperCase();
  var table = document.getElementById(tableId);
  var rows = table.getElementsByTagName('tr');
  for (var i = 1; i < rows.length; i++) {{
    var cells = rows[i].getElementsByTagName('td');
    var found = false;
    for (var j = 0; j < cells.length; j++) {{
      if (cells[j]) {{
        var text = cells[j].textContent || cells[j].innerText;
        if (text.toUpperCase().indexOf(filter) > -1) {{
          found = true;
          break;
        }}
      }}
    }}
    rows[i].style.display = found ? '' : 'none';
  }}
}}
</script>
</body>
</html>'''

with open('dashboard_comparativo.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

print("✅ DASHBOARD COMPARATIVO generado!")
print(f"  Release 1: {len(release1)} registros")
print(f"  Release 2: {len(release2)} registros (NUEVOS)")
print(f"  Archivo: dashboard_comparativo.html")
