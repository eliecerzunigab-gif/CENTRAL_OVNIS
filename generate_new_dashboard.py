#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de DASHBOARD COMPARATIVO - Central Ovnis
Release 1 (antiguos) vs Release 2 (nuevos) lado a lado
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
    return s.replace('&','&').replace('<','<').replace('>','>').replace('"','"').replace("'",'&#39;')

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
        r.append(f'<div class="bar-row"><span class="bar-lbl" style="width:{w}">{esc(n)}</span><div class="bar-trk"><div class="bar-fill {cls}" style="width:{p:.0f}%"></div></div><span class="bar-cnt">{c}</span></div>')
    return '\n'.join(r)

def build_top10(recs):
    c = []
    for i,r in enumerate(sorted(recs, key=lambda x:-x.get('score',0))[:10]):
        rank=i+1; img=r.get('modal_image','')
        if img: ih=f'<img class="cimg" src="{esc(img)}" alt="{esc(r["title"])}" onclick="openModal(\'{esc(img)}\',\'{esc(r["title"])}\')">'
        else: ih='<div class="cipl">🛸</div>'
        pl = r.get('pdf_link','')
        pb = f'<a href="{esc(pl)}" target="_blank" class="bpdf">📄 PDF</a>' if pl else ''
        dv=r.get('incident_date',''); lv=r.get('incident_location',''); dv2=r.get('description','')[:150]; sc=r.get('score',0)
        card=f'<div class="tcard"><div class="rk">{rank}</div><div class="sbadge">{sc}</div>{ih}<div class="cbody"><div class="ctype type-{r["type"]}">{r["type"]}</div><div class="ctit">{esc(r["title"])}</div><div class="cmeta"><span class="cag">{esc(r["agency"])}</span><span>{esc(dv)}</span><span>{esc(lv)}</span></div><div class="cdsc">{esc(dv2)}</div><div class="clnk">{pb}</div></div></div>'
        c.append(card)
    return '\n'.join(c)

def build_table(recs):
    r = []
    for i,rec in enumerate(recs):
        n=i+1; t=rec.get('title','?'); a=rec.get('agency','?'); d=rec.get('incident_date','?'); l=rec.get('incident_location','?'); tp=rec.get('type','PDF'); sc=rec.get('score',0)
        r.append(f'<tr><td>{n}</td><td>{esc(t)}</td><td>{esc(a)}</td><td>{esc(d)}</td><td>{esc(l)}</td><td><span class="ttype {tp}">{tp}</span></td><td><span class="scell">{sc}</span></td></tr>')
    return '\n'.join(r)

def build_types(d):
    return '\n'.join([f'<div class="titem {t}"><span class="tcnt">{c}</span> {t}</div>' for t,c in sorted(d.items(), key=lambda x:-x[1])])

def build_slides(imgs):
    return '\n'.join([f'<div class="slide"><img src="{esc(u)}" alt="S" onclick="openModal(\'{esc(u)}\',\'Slide\')"></div>' for u in imgs[:15]])

mx_a = max(max(s1['agencies'].values()) if s1['agencies'] else 1, max(s2['agencies'].values()) if s2['agencies'] else 1)
mx_l = max(max(s1['locs'].values()) if s1['locs'] else 1, max(s2['locs'].values()) if s2['locs'] else 1)

t10_1 = build_top10(release1)
t10_2 = build_top10(release2)
tbl_1 = build_table(release1)
tbl_2 = build_table(release2)
ab1 = build_bars(s1['agencies'], mx_a)
ab2 = build_bars(s2['agencies'], mx_a)
lb1 = build_bars(s1['locs'], mx_l, '140px', 'loc')
lb2 = build_bars(s2['locs'], mx_l, '140px', 'loc')
ty1 = build_types(s1['types'])
ty2 = build_types(s2['types'])
sl1 = build_slides([r.get('modal_image','') for r in release1 if r.get('modal_image')])
sl2 = build_slides([r.get('modal_image','') for r in release2 if r.get('modal_image')])

now = datetime.now().strftime('%d/%m/%Y %H:%M')

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CENTRAL OVNIS - Comparativa Release 1 vs Release 2</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0a0e1a;--bg2:#111827;--card:#1a1f35;--ch:#222a45;--tx:#e2e8f0;--tx2:#94a3b8;--txm:#64748b;--ac:#00d4ff;--ac2:#7c3aed;--ac3:#f59e0b;--ac4:#10b981;--bd:#1e293b;--r1:#3b82f6;--r2:#f59e0b}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--tx);min-height:100vh}}
body::before{{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 20% 50%,rgba(0,212,255,0.03) 0%,transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(124,58,237,0.03) 0%,transparent 50%);pointer-events:none;z-index:0}}
.c{{max-width:1500px;margin:0 auto;padding:20px;position:relative;z-index:1}}
.hdr{{text-align:center;padding:40px 20px 30px;border-bottom:1px solid var(--bd);margin-bottom:30px}}
.hdr h1{{font-family:'Orbitron',sans-serif;font-size:2.2em;font-weight:800;background:linear-gradient(135deg,var(--ac),var(--ac2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px}}
.hdr .sub{{color:var(--tx2);font-size:1em;margin-top:8px;letter-spacing:4px;text-transform:uppercase}}
.hdr .br{{display:flex;justify-content:center;gap:15px;margin-top:15px;flex-wrap:wrap}}
.hdr .bdg{{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600}}
.b1{{background:rgba(59,130,246,0.15);color:var(--r1);border:1px solid rgba(59,130,246,0.3)}}
.b2{{background:rgba(245,158,11,0.15);color:var(--r2);border:1px solid rgba(245,158,11,0.3)}}
.bt{{background:rgba(16,185,129,0.15);color:var(--ac4);border:1px solid rgba(16,185,129,0.3)}}
.cr{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:30px}}
.cc{{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:20px;text-align:center}}
.cc.r1c{{border-color:rgba(59,130,246,0.3)}}
.cc.r2c{{border-color:rgba(245,158,11,0.3)}}
.cc .rl{{font-family:'Orbitron',sans-serif;font-size:14px;font-weight:700;letter-spacing:2px;margin-bottom:8px}}
.cc .bn{{font-family:'Orbitron',sans-serif;font-size:3em;font-weight:800}}
.cc .st{{font-size:12px;color:var(--txm);margin-top:4px}}
.cc .sr{{display:flex;justify-content:center;gap:20px;margin-top:12px;flex-wrap:wrap}}
.cc .si{{text-align:center}}
.cc .si .n{{font-size:1.3em;font-weight:700;font-family:'Orbitron',sans-serif}}
.cc .si .l{{font-size:10px;color:var(--txm);text-transform:uppercase;letter-spacing:1px}}
.vs{{display:flex;align-items:center;justify-content:center;gap:20px;margin:10px 0 30px}}
.vs .ln{{flex:1;height:1px;background:var(--bd)}}
.vs .vt{{font-family:'Orbitron',sans-serif;font-size:1.5em;font-weight:800;color:var(--ac);text-shadow:0 0 20px rgba(0,212,255,0.3);padding:0 10px}}
.st{{font-family:'Orbitron',sans-serif;font-size:1.3em;font-weight:700;color:var(--tx);margin-bottom:20px;display:flex;align-items:center;gap:10px}}
.st .dt{{width:8px;height:8px;border-radius:50%;display:inline-block}}
.st .dt.r1{{background:var(--r1);box-shadow:0 0 10px var(--r1)}}
.st .dt.r2{{background:var(--r2);box-shadow:0 0 10px var(--r2)}}
.sp{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:40px}}
.sc{{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:20px;overflow:hidden}}
.sc.r1s{{border-color:rgba(59,130,246,0.2)}}
.sc.r2s{{border-color:rgba(245,158,11,0.2)}}
.sc .sh{{display:flex;align-items:center;gap:10px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid var(--bd)}}
.sc .sh .ic{{width:10px;height:10px;border-radius:50%}}
.sc .sh .ic.r1{{background:var(--r1)}}
.sc .sh .ic.r2{{background:var(--r2)}}
.sc .sh .lb{{font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700;letter-spacing:1px}}
.sc .sh .cn{{font-size:12px;color:var(--txm);margin-left:auto}}
.bars{{display:flex;flex-direction:column;gap:5px}}
.bar-row{{display:flex;align-items:center;gap:8px}}
.bar-lbl{{font-size:10px;color:var(--tx2);width:100px;text-align:right;flex-shrink:0;line-height:1.2}}
.bar-trk{{flex:1;height:16px;background:var(--bg2);border-radius:4px;overflow:hidden}}
.bar-fill{{height:100%;border-radius:4px;transition:width 1s ease;background:linear-gradient(90deg,var(--r1),rgba(59,130,246,0.4))}}
.bar-fill.r2f{{background:linear-gradient(90deg,var(--r2),rgba(245,158,11,0.4))}}
.bar-fill.loc{{background:linear-gradient(90deg,var(--ac4),rgba(16,185,129,0.4))}}
.bar-cnt{{font-size:10px;color:var(--txm);width:25px;text-align:left;flex-shrink:0}}
.tdist{{display:flex;gap:6px;flex-wrap:wrap}}
.titem{{display:flex;align-items:center;gap:4px;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:600}}
.titem.PDF{{background:rgba(239,68,68,0.15);color:#ef4444}}
.titem.VID{{background:rgba(139,92,246,0.15);color:#8b5cf6}}
.titem.IMG{{background:rgba(16,185,129,0.15);color:#10b981}}
.titem.AUD{{background:rgba(245,158,11,0.15);color:#f59e0b}}
.titem .tcnt{{font-family:'Orbitron',sans-serif;font-size:13px}}
.sc2{{overflow:hidden;margin-bottom:30px;border-radius:16px;border:1px solid var(--bd);background:var(--card)}}
.sct{{display:flex;gap:12px;padding:16px;overflow-x:auto;scroll-behavior:smooth;scrollbar-width:thin;scrollbar-color:var(--ac) var(--bg2)}}
.sct::-webkit-scrollbar{{height:6px}}
.sct::-webkit-scrollbar-track{{background:var(--bg2);border-radius:3px}}
.sct::-webkit-scrollbar-thumb{{background:var(--ac);border-radius:3px}}
.slide{{flex:0 0 auto;width:260px;height:160px;border-radius:12px;overflow:hidden;cursor:pointer;transition:transform .3s;border:1px solid var(--bd)}}
.slide:hover{{transform:scale(1.03);border-color:var(--ac)}}
.slide img{{width:100%;height:100%;object-fit:cover}}
.t10g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}}
.tcard{{background:var(--card);border:1px solid var(--bd);border-radius:14px;overflow:hidden;transition:all .3s;position:relative}}
.tcard:hover{{border-color:rgba(0,212,255,0.3);transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,0.4)}}
.tcard .rk{{position:absolute;top:8px;left:8px;width:28px;height:28px;background:rgba(0,0,0,0.7);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:var(--ac);z-index:2;font-family:'Orbitron',sans-serif;border:1px solid rgba(0,212,255,0.3)}}
.tcard .sbadge{{position:absolute;top:8px;right:8px;padding:2px 8px;border-radius:10px;font-size:9px;font-weight:700;z-index:2;letter-spacing:1px;background:rgba(16,185,129,0.2);color:var(--ac4);border:1px solid rgba(16,185,129,0.3)}}
.cimg{{width:100%;height:160px;object-fit:cover;cursor:pointer;transition:transform .3s}}
.cimg:hover{{transform:scale(1.05)}}
.cipl{{width:100%;height:160px;display:flex;align-items:center;justify-content:center;font-size:2.5em;background:linear-gradient(135deg,var(--bg2),var(--card))}}
.cbody{{padding:12px}}
.ctype{{display:inline-block;padding:2px 6px;border-radius:3px;font-size:9px;font-weight:700;letter-spacing:1px;margin-bottom:4px}}
.type-PDF{{background:rgba(239,68,68,0.2);color:#ef4444}}
.type-VID{{background:rgba(139,92,246,0.2);color:#8b5cf6}}
.type-IMG{{background:rgba(16,185,129,0.2);color:#10b981}}
.type-AUD{{background:rgba(245,158,11,0.2);color:#f59e0b}}
.ctit{{font-size:13px;font-weight:600;color:var(--tx);margin-bottom:4px;line-height:1.3}}
.cmeta{{display:flex;flex-wrap:wrap;gap:4px;font-size:10px;color:var(--txm);margin-bottom:6px}}
.cmeta .cag{{color:var(--ac);font-weight:600}}
.cdsc{{font-size:11px;color:var(--tx2);line-height:1.4;margin-bottom:8px}}
.clnk{{display:flex;gap:6px}}
.bpdf{{display:inline-flex;align-items:center;gap:3px;padding:4px 10px;background:rgba(239,68,68,0.15);color:#ef4444;border-radius:5px;font-size:10px;font-weight:600;text-decoration:none;transition:all .2s}}
.bpdf:hover{{background:rgba(239,68,68,0.3)}}
.tc2{{overflow-x:auto;max-height:500px;overflow-y:auto}}
.dtbl{{width:100%;border-collapse:collapse;font-size:11px}}
.dtbl th{{background:var(--bg2);color:var(--txm);padding:8px 10px;text-align:left;font-weight:600;text-transform:uppercase;letter-spacing:1px;font-size:9px;border-bottom:2px solid var(--bd);position:sticky;top:0;z-index:2}}
.dtbl td{{padding:6px 10px;border-bottom:1px solid var(--bd);color:var(--tx2)}}
.dtbl tr:hover td{{background:var(--ch)}}
.ttype{{display:inline-block;padding:1px 5px;border-radius:3px;font-size:9px;font-weight:600}}
.ttype.PDF{{background:rgba(239,68,68,0.15);color:#ef4444}}
.ttype.VID{{background:rgba(139,92,246,0.15);color:#8b5cf6}}
.ttype.IMG{{background:rgba(16,185,129,0.15);color:#10b981}}
.ttype.AUD{{background:rgba(245,158,11,0.15);color:#f59e0b}}
.scell{{font-family:'Orbitron',sans-serif;font-size:10px;color:var(--ac4);font-weight:700}}
.srch{{margin-bottom:12px}}
.srch input{{width:100%;padding:10px 14px;background:var(--bg2);border:1px solid var(--bd);border-radius:10px;color:var(--tx);font-size:12px;font-family:'Inter',sans-serif;outline:none;transition:all .3s}}
.srch input:focus{{border-color:var(--ac);box-shadow:0 0 15px rgba(0,212,255,0.1)}}
.srch input::placeholder{{color:var(--txm)}}
.modal{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);z-index:1000;align-items:center;justify-content:center;padding:20px}}
.modal.active{{display:flex}}
.modal img{{max-width:90vw;max-height:85vh;border-radius:8px;object-fit:contain}}
.modal-close{{position:absolute;top:20px;right:30px;font-size:30px;color:white;cursor:pointer;background:none;border:none;z-index:1001}}
.modal-title{{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);color:white;font-size:14px;text-align:center;background:rgba(0,0,0,0.7);padding:8px 16px;border-radius:8px;max-width:80%}}
.ftr{{text-align:center;padding:30px;border-top:1px solid var(--bd);color:var(--txm);font-size:12px;margin-top:20px}}
.ftr a{{color:var(--ac);text-decoration:none}}
@media(max-width:900px){{.cr,.sp{{grid-template-columns:1fr}}.hdr h1{{font-size:1.5em}}.cc .bn{{font-size:2em}}.bar-lbl{{width:70px;font-size:9px}}.slide{{width:200px;height:130px}}}}
</style>
</head>
<body>
<div class="c">
<div class="hdr">
<h1>🛸 CENTRAL OVNIS</h1>
<div class="sub">Comparativa Release 1 vs Release 2 · Datos Desclasificados del Gobierno de EE.UU.</div>
<div class="br">
<span class="bdg b1">🔵 {s1['total']} registros · Release 1</span>
<span class="bdg b2">🟡 {s2['total']} registros · Release 2 (NUEVOS)</span>
<span class="bdg bt">🟢 {s1['total']+s2['total']} registros totales</span>
</div>
</div>

<div class="cr">
<div class="cc r1c">
<div class="rl" style="color:var(--r1)">RELEASE 1</div>
<div class="bn" style="color:var(--r1)">{s1['total']}</div>
<div class="st">Registros desclasificados · Periodo anterior</div>
<div class="sr">
<div class="si"><div class="n" style="color:#ef4444">{s1['types'].get('PDF',0)}</div><div class="l">PDF</div></div>
<div class="si"><div class="n" style="color:#8b5cf6">{s1['types'].get('VID',0)}</div><div class="l">VID</div></div>
<div class="si"><div class="n" style="color:#10b981">{s1['types'].get('IMG',0)}</div><div class="l">IMG</div></div>
<div class="si"><div class="n" style="color:#f59e0b">{s1['types'].get('AUD',0)}</div><div class="l">AUD</div></div>
<div class="si"><div class="n" style="color:var(--ac4)">{s1['avg_score']}</div><div class="l">Score Prom</div></div>
</div>
</div>
<div class="cc r2c">
<div class="rl" style="color:var(--r2)">RELEASE 2 · NUEVO</div>
<div class="bn" style="color:var(--r2)">{s2['total']}</div>
<div class="st">Nuevos registros · Publicado Mayo 2026</div>
<div class="sr">
<div class="si"><div class="n" style="color:#ef4444">{s2['types'].get('PDF',0)}</div><div class="l">PDF</div></div>
<div class="si"><div class="n" style="color:#8b5cf6">{s2['types'].get('VID',0)}</div><div class="l">VID</div></div>
<div class="si"><div class="n" style="color:#10b981">{s2['types'].get('IMG',0)}</div><div class="l">IMG</div></div>
<div class="si"><div class="n" style="color:#f59e0b">{s2['types'].get('AUD',0)}</div><div class="l">AUD</div></div>
<div class="si"><div class="n" style="color:var(--ac4)">{s2['avg_score']}</div><div class="l">Score Prom</div></div>
</div>
</div>
</div>

<div class="vs"><div class="ln"></div><div class="vt">⚡ VS ⚡</div><div class="ln"></div></div>

<div class="st"><span class="dt r1"></span> Agencias <span class="dt r2" style="margin-left:15px"></span></div>
<div class="sp">
<div class="sc r1s"><div class="sh"><div class="ic r1"></div><div class="lb" style="color:var(--r1)">RELEASE 1</div><div class="cn">{len(s1['agencies'])} agencias</div></div><div class="bars">{ab1}</div></div>
<div class="sc r2s"><div class="sh"><div class="ic r2"></div><div class="lb" style="color:var(--r2)">RELEASE 2 · NUEVO</div><div class="cn">{len(s2['agencies'])} agencias</div></div><div class="bars">{ab2}</div></div>
</div>

<div class="st"><span class="dt r1"></span> TOP 10 · Release 1 <span class="dt r2" style="margin-left:15px"></span> TOP 10 · Release 2 (Nuevos)</div>
<div class="sp">
<div class="sc r1s"><div class="sh"><div class="ic r1"></div><div class="lb" style="color:var(--r1)">RELEASE 1</div><div class="cn">Mejores puntuados</div></div><div class="t10g">{t10_1}</div></div>
<div class="sc r2s"><div class="sh"><div class="ic r2"></div><div class="lb" style="color:var(--r2)">RELEASE 2 · NUEVO</div><div class="cn">Mejores puntuados</div></div><div class="t10g">{t10_2}</div></div>
</div>

<div class="st"><span class="dt r1"></span> Todos los Registros · Release 1 ({s1['total']}) <span class="dt r2" style="margin-left:15px"></span> Todos los Registros · Release 2 ({s2['total']})</div>
<div class="sp">
<div class="sc r1s">
<div class="sh"><div class="ic r1"></div><div class="lb" style="color:var(--r1)">RELEASE 1</div><div class="cn">{s1['total']} registros</div></div>
<div class="srch"><input type="text" id="s1" placeholder="Buscar en Release 1..." onkeyup="filtro('s1','t1')"></div>
<div class="tc2"><table class="dtbl" id="t1"><thead><tr><th>#</th><th>Titulo</th><th>Agencia</th><th>Fecha</th><th>Ubicacion</th><th>Tipo</th><th>Score</th></tr></thead><tbody>{tbl_1}</tbody></table></div>
</div>
<div class="sc r2s">
<div class="sh"><div class="ic r2"></div><div class="lb" style="color:var(--r2)">RELEASE 2 · NUEVO</div><div class="cn">{s2['total']} registros</div></div>
<div class="srch"><input type="text" id="s2" placeholder="Buscar en Release 2..." onkeyup="filtro('s2','t2')"></div>
<div class="tc2"><table class="dtbl" id="t2"><thead><tr><th>#</th><th>Titulo</th><th>Agencia</th><th>Fecha</th><th>Ubicacion</th><th>Tipo</th><th>Score</th></tr></thead><tbody>{tbl_2}</tbody></table></div>
</div>
</div>

<div class="ftr">
<p>🛸 <strong>CENTRAL OVNIS</strong> · Datos desclasificados del gobierno de EE.UU.</p>
<p style="margin-top:4px">Fuentes: <a href="https://www.war.gov" target="_blank">war.gov</a> · <a href="https://www.aaro.mil" target="_blank">AARO</a></p>
<p style="margin-top:4px;font-size:10px;color:var(--txm)">Generado el {now} · Comparativa Release 1 vs Release 2</p>
</div>
</div>

<div class="modal" id="imageModal" onclick="closeModal()">
<button class="modal-close" onclick="closeModal()">&times;</button>
<img id="modalImage" src="" alt="">
<div class="modal-title" id="modalTitle"></div>
</div>

<script>
function openModal(s,t){{document.getElementById('modalImage').src=s;document.getElementById('modalTitle').textContent=t;document.getElementById('imageModal').classList.add('active')}}
function closeModal(){{document.getElementById('imageModal').classList.remove('active')}}
function filtro(inp,tbl){{
var i=document.getElementById(inp),f=i.value.toUpperCase(),tb=document.getElementById(tbl),tr=tb.getElementsByTagName('tr');
for(var x=1;x<tr.length;x++){{var td=tr[x].getElementsByTagName('td'),fo=false;for(var y=0;y<td.length;y++){{if(td[y]){{if((td[y].textContent||td[y].innerText).toUpperCase().indexOf(f)>-1){{fo=true;break}}}}}}tr[x].style.display=fo?'':'none'}}
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
