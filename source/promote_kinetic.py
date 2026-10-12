#!/usr/bin/env python3
"""Publish the KINETIC direction as home while retaining the site's SEO graph and routes."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
from datetime import datetime, timezone
import json, re, sys

DOMAIN = 'https://nichoagenciadigital.com'
RELEASE = 'nicho-kinetic-production-2026-10-12'
NAMES = ['Invicto OPS', 'RestoOps', 'Luminari', 'Agentes comerciales IA', 'Plataforma de seguros', 'Cuentas Carlos']
SLUGS = ['invicto-ops', 'restoops', 'luminari', 'agentes-ia', 'plataforma-seguros', 'cuentas-carlos']
DISPLAY = [('INVICTO','OPS.'),('RESTO','OPS.'),('LUMI','NARI.'),('AGENTES','IA.'),('SEGUROS','CRM.'),('CUENTAS','CARLOS.')]
COLORS = ['green','sand','steel','red','dark','sand']
MODULES = [('PEDIDOS','INVENTARIO','LOGÍSTICA'),('RECETAS','COMANDAS','CAJA'),('CLIENTES','COTIZACIÓN','PROYECTOS'),('ATENDER','CALIFICAR','ACTUAR'),('CLIENTES','PÓLIZAS','RENOVAR'),('ENTREGAS','ABONOS','SALDO')]
EXTRA = '''<section class="knowledge" id="criterio"><div class="wrap"><div class="eyebrow">TECNOLOGÍA CON CRITERIO / NICHO AGENCIA DIGITAL</div><div class="knowledge-heading"><h2>Entender primero.<br>Construir después.</h2><p>Diseñamos software a medida, agentes IA y automatización comercial desde Bucaramanga para empresas de Colombia y Latinoamérica. Cada solución parte de un proceso real y de un alcance acordado.</p></div><div class="knowledge-links"><a href="/recursos/software-a-medida-o-saas.html"><span>01 / SOFTWARE EMPRESARIAL</span><h3>¿Un sistema propio o una herramienta existente?</h3><p>Cuándo conviene desarrollar y cuándo es mejor integrar lo que ya funciona.</p><b>LEER LA GUÍA ↗</b></a><a href="/recursos/agentes-ia-ventas.html"><span>02 / INTELIGENCIA ARTIFICIAL</span><h3>Qué delegar a un agente. Y qué no.</h3><p>Atención, calificación y seguimiento con límites y supervisión humana.</p><b>LEER LA GUÍA ↗</b></a><a href="/recursos/automatizacion-comercial.html"><span>03 / PROCESOS COMERCIALES</span><h3>Menos tareas sueltas. Un proceso completo.</h3><p>Cómo conectar contactos, responsables y acciones sin perder el contexto.</p><b>LEER LA GUÍA ↗</b></a></div></div></section><section class="questions"><div class="wrap"><div class="eyebrow">ANTES DE EMPEZAR</div><h2>Preguntas reales.<br>Respuestas claras.</h2><details><summary>¿Necesito reemplazar todo el software de mi empresa?</summary><p>No. Primero revisamos las herramientas actuales, las tareas repetitivas y los puntos de fricción. Una integración o un módulo específico puede ser suficiente.</p></details><details><summary>¿Los agentes IA pueden atender y vender por WhatsApp?</summary><p>Pueden apoyar la atención, calificación y seguimiento cuando la plataforma y las integraciones lo permiten. Definimos qué información consultan, qué acciones tienen autorizadas y cuándo deben transferir la conversación a un asesor.</p></details><details><summary>¿Trabajan fuera de Bucaramanga?</summary><p>Sí. Nuestra oficina está en Bucaramanga y atendemos proyectos en Colombia, Latinoamérica y otros mercados. El alcance, las reuniones y la implementación se acuerdan según las necesidades de cada empresa.</p></details><details><summary>¿Cómo se cotiza un sistema a medida?</summary><p>Partimos del problema, los usuarios, los módulos y las integraciones. Después definimos una propuesta específica. No publicamos precios genéricos porque cada proyecto necesita un alcance distinto.</p></details><a href="/contacto.html" class="question-contact">Cuéntanos qué necesitas resolver ↗</a></div></section>'''
LINKS = [('soluciones.html','Soluciones'),('sistemas.html','Software a medida'),('agentes-ia.html','Agentes IA'),('automatizaciones.html','Automatización'),('desarrollo-web.html','Desarrollo web'),('crm-personalizado.html','CRM personalizado'),('whatsapp-api-empresas.html','WhatsApp API'),('portafolio.html','Portafolio'),('metodologia.html','Método'),('nosotros.html','Estudio'),('recursos.html','Ideas y recursos'),('bucaramanga.html','Bucaramanga'),('contacto.html','Contacto'),('privacidad.html','Privacidad')]
CSS = '''
/* Production additions: discoverable links, editorial content and mobile navigation. */
.mobile-nav{display:none}.hero-top{font-size:11px}.hero-explain p{font-size:17px}
.project-select{height:calc(100% - 40px)}.project-case{position:absolute;bottom:0;left:0;right:0;height:40px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;background:#11110f;color:#fffefa;font-size:10px;letter-spacing:.06em;z-index:5;border-top:1px solid #66675f}.project-case:focus-visible{outline-offset:-4px}.project-card .project-visual{bottom:8px}.project-track{overscroll-behavior-x:contain}.project-card.active{border-color:#fff}
.knowledge,.questions{padding:85px 0;background:var(--paper)}.knowledge-heading{display:grid;grid-template-columns:1.15fr .85fr;gap:65px;align-items:end;margin:34px 0 50px}.knowledge-heading h2,.questions h2{font-size:clamp(43px,5vw,76px);font-weight:400;line-height:1;letter-spacing:-.06em;margin:0}.knowledge-heading p{font-size:17px;line-height:1.7;color:#58594f;max-width:510px;margin:0}.knowledge-links{display:grid;grid-template-columns:repeat(3,1fr);gap:30px}.knowledge-links>a{border-top:1px solid var(--line);display:flex;flex-direction:column;padding:23px 0;gap:20px}.knowledge-links span{font-size:10px;letter-spacing:.09em;color:#58594f}.knowledge-links h3{font-size:clamp(26px,2.8vw,39px);font-weight:400;letter-spacing:-.05em;line-height:1.12;margin:0}.knowledge-links p{font-size:15px;line-height:1.6;color:#62615c;margin:0}.knowledge-links b{font-size:11px;font-weight:500;letter-spacing:.06em;margin-top:auto}.knowledge-links a:hover h3{color:#c52d09}.questions{padding-top:30px}.questions h2{margin:30px 0 50px}.questions details{border-top:1px solid var(--line);padding:25px 0}.questions details:last-of-type{border-bottom:1px solid var(--line)}.questions summary{cursor:pointer;font-size:clamp(18px,2vw,27px);line-height:1.3;letter-spacing:-.035em}.questions details p{font-size:16px;line-height:1.7;max-width:800px;color:#57594f;padding:8px 0}.question-contact{display:inline-block;border-bottom:1px solid;margin-top:28px;padding-bottom:10px;font-size:14px}.site-directory{display:grid;grid-template-columns:repeat(4,1fr);gap:18px 30px;margin-top:45px;border-top:1px solid var(--line);padding:30px 0}.site-directory a{font-size:13px}.site-directory a:hover{text-decoration:underline;text-underline-offset:5px}.closing-foot address{font-style:normal;line-height:1.8}.closing-foot a{overflow-wrap:anywhere}.site-version{font-size:10px;letter-spacing:.09em;margin:24px 0 0;color:#55564e}
.no-js .project-stage{height:auto}.no-js .project-track{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:25px;padding:30px max(20px,calc((100vw - 1380px)/2))}.no-js .project-card{width:100%;height:350px;transform:none;opacity:1}.no-js .project-select{pointer-events:none}.no-js .gallery-controls,.no-js .project-info,.no-js #motion{display:none}
@media(max-width:1050px){.header .nav{gap:18px}.navlinks{gap:16px;font-size:12px}.navcta{gap:12px}.hero-explain p{font-size:15px}}
@media(max-width:700px){.header .nav{gap:11px}.navcta{font-size:10px;gap:8px}.navcta b{font-size:17px}.motion{font-size:8px}.mobile-nav{display:block;position:static}.mobile-nav summary{cursor:pointer;list-style:none;font-size:10px;padding:12px 3px}.mobile-nav summary::-webkit-details-marker{display:none}.mobile-nav>nav{position:absolute;top:70px;left:0;right:0;background:var(--paper);border-bottom:1px solid #bab9af;padding:15px 20px;display:grid;grid-template-columns:1fr 1fr;gap:10px;max-height:calc(100svh - 80px);overflow:auto}.mobile-nav nav a{padding:12px 0;font-size:15px}.hero-explain p{font-size:13px}.hero-top{font-size:9px}.knowledge,.questions{padding:60px 0}.knowledge-heading{grid-template-columns:1fr;gap:24px;margin:28px 0 35px}.knowledge-heading h2,.questions h2{font-size:47px}.knowledge-heading p{font-size:15px}.knowledge-links{grid-template-columns:1fr;gap:18px}.knowledge-links h3{font-size:31px}.questions{padding-top:0}.questions summary{font-size:20px}.questions details p{font-size:15px}.site-directory{grid-template-columns:1fr 1fr;gap:17px}.site-directory a{font-size:12px}.no-js .project-track{grid-template-columns:1fr;padding:20px}.no-js .project-card{height:350px}.project-select .project-name{margin-top:25px}.project-case{font-size:10px}.service-header h2{font-size:clamp(43px,10vw,52px)}}
'''

def apply(root):
    root=Path(root).resolve()
    old=BeautifulSoup((root/'index.html').read_text(),'html.parser')
    s=BeautifulSoup((root/'qa/exploracion-kinetic.html').read_text(),'html.parser')
    assert 'noindex' in s.select_one('meta[name=robots]')['content']
    css=s.style.string+CSS
    script=s.select('script:not([src])')[-1].string
    head=BeautifulSoup(str(old.head),'html.parser').head
    for link in head.select('link[rel=stylesheet]'): link.decompose()
    for link in head.select('link[rel=preload]'): link.decompose()
    head.select_one('meta[name=robots]')['content']='index,follow,max-image-preview:large'
    head.select_one('meta[name=theme-color]')['content']='#e9e8e4'
    head.select_one('link[rel=canonical]')['href']=DOMAIN+'/'
    for script_tag in head.select('script:not([type="application/ld+json"])'): script_tag.decompose()
    for previous in head.select('meta[name=nicho-release]'): previous.decompose()
    meta=s.new_tag('meta');meta.attrs={'name':'nicho-release','content':RELEASE};head.append(meta)
    style=s.new_tag('link',rel='stylesheet',href='/assets/css/kinetic-home.css');head.append(style)
    s.head.replace_with(head)
    s.html['data-release']=RELEASE
    for ref in s.select('[href],[src],[data-src]'):
        for attr in ['href','src','data-src']:
            val=ref.get(attr,'')
            if val and not val.startswith(('/','#','http:','https:','mailto:','tel:','data:')):ref[attr]='/'+val
    track=s.select_one('#project-track');track.clear()
    for i,slug in enumerate(SLUGS):
        parts=''.join('<span>'+escape(m)+'</span>' for m in MODULES[i])
        card=f'<article class="project-card{" active" if i==0 else ""}" data-color="{COLORS[i]}"><button class="project-select" type="button" aria-label="Mostrar {NAMES[i]}" aria-pressed="{str(i==0).lower()}"><span class="eyebrow">NICHO / TRABAJO SELECCIONADO</span><span class="card-index">0{i+1}</span><div class="project-name">{DISPLAY[i][0]}<span>{DISPLAY[i][1]}</span></div><div class="project-visual" aria-hidden="true"><div class="pbar"><span>{NAMES[i]}</span><span>VISTA DEMO</span></div><div class="plines">{parts}</div></div></button><a class="project-case" href="/portafolio/{slug}.html">Ver caso: {NAMES[i]}<span aria-hidden="true">↗</span></a></article>'
        track.append(BeautifulSoup(card,'html.parser').article)
    start=script.index('data.forEach((d,i)=>')
    end=script.index("const cards=$$('.project-card');",start)+len("const cards=$$('.project-card');")
    script=script[:start]+"const cards=$$('.project-card');cards.forEach((card,i)=>card.querySelector('button').addEventListener('click',()=>select(i,true)));"+script[end:]
    script=script.replace(".href='portafolio/'",".href='/portafolio/'")
    script=script.replace("!track.contains(document.activeElement)","!$('.projects').contains(document.activeElement)")
    script=script.replace("behavior:enabled?'smooth':'instant'","behavior:enabled?'smooth':'auto'")
    script+="\n;(()=>{const d=document.querySelector('.mobile-nav');if(!d)return;d.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>d.open=false));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&d.open){d.open=false;d.querySelector('summary').focus()}})})();"
    for el in s.select('script'):
        if el.get('type')!='application/ld+json':el.decompose()
    for url in ['/assets/vendor/gsap.min.js','/assets/vendor/ScrollTrigger.min.js','/assets/js/kinetic-home.js']:
        node=s.new_tag('script',src=url);node['defer']='';s.body.append(node)
    closing=s.select_one('.closing')
    for section in BeautifulSoup(EXTRA,'html.parser').find_all('section',recursive=False):closing.insert_before(section)
    for n in s.select('.concept-note'):n.decompose()
    for a in s.select('.closing-foot>a[href="/index.html"]'):a.decompose()
    foot=s.select_one('.closing-foot')
    contact=foot.select_one('span')
    contact.replace_with(BeautifulSoup('<address><a href="mailto:nicho.agenciadigital@gmail.com">nicho.agenciadigital@gmail.com</a><br>Carrera 29 #39-39, barrio La Aurora, oficina 01<br>Bucaramanga, Santander, Colombia</address>','html.parser').address)
    directory='<nav class="site-directory" aria-label="Más sobre Nicho">'+''.join(f'<a href="/{path}">{label}</a>' for path,label in LINKS)+'</nav><p class="site-version">NICHO AGENCIA DIGITAL · COLOMBIA / LATAM</p>'
    for el in BeautifulSoup(directory,'html.parser').find_all(recursive=False):foot.insert_after(el);foot=el
    nav='<details class="mobile-nav"><summary aria-label="Abrir navegación">MENÚ</summary><nav aria-label="Navegación móvil">'+''.join(f'<a href="/{path}">{label}</a>' for path,label in LINKS[:11])+'</nav></details>'
    s.select_one('.header .nav').append(BeautifulSoup(nav,'html.parser').details)
    for v in s.select('video'):
        v['poster']='/assets/media/liquid-studio.webp';v['width']='160';v['height']='90'
    (root/'assets/css/kinetic-home.css').write_text(css,encoding='utf-8')
    (root/'assets/js/kinetic-home.js').write_text(script,encoding='utf-8')
    (root/'index.html').write_text(str(s),encoding='utf-8')
    sitemap=(root/'sitemap.xml').read_text()
    today=datetime.now(timezone.utc).date().isoformat()
    sitemap=re.sub(r'(<loc>https://nichoagenciadigital.com/</loc><lastmod>)[^<]+',lambda m:m[1]+today,sitemap)
    (root/'sitemap.xml').write_text(sitemap)
    robots=(root/'robots.txt').read_text()
    if 'Allow: /qa/exploracion-kinetic.html' not in robots:robots=robots.replace('Disallow: /qa/','Disallow: /qa/\nAllow: /qa/exploracion-kinetic.html')
    (root/'robots.txt').write_text(robots)
    build=root/'source/build.py'
    if build.exists() and '# KINETIC_PRODUCTION_HOOK' not in build.read_text():
        with build.open('a') as f:f.write("\n# KINETIC_PRODUCTION_HOOK\nif (SITE/'qa/exploracion-kinetic.html').is_file():\n import runpy\n runpy.run_path(str(ROOT/'source/promote_kinetic.py'))['apply'](SITE)\n")
    print(json.dumps({'release':RELEASE,'canonical':s.select_one('link[rel=canonical]')['href'],'robots':s.select_one('meta[name=robots]')['content'],'static_case_links':len(s.select('.project-case')),'h1':len(s.select('h1')),'routes_preserved':24},ensure_ascii=False))

if __name__=='__main__':apply(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
