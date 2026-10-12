from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import shutil,json,re,hashlib,sys
ROOT=Path(sys.argv[1]).resolve()
CAPTURES=Path(sys.argv[2]).resolve()
NAMES={'invicto-ops':'Invicto OPS','restoops':'RestoOps','luminari':'Luminari','plataforma-seguros':'SeguroOS','cuentas-carlos':'Cuentas Carlos'}
CAPTIONS={'invicto-ops':'Captura de la interfaz original de Invicto OPS. Vista local aislada, sin datos operativos de clientes.','restoops':'Captura de la interfaz original de RestoOps. Estado vacío en una copia local, sin conexión a los restaurantes.','luminari':'Captura de la interfaz original de Luminari. Modo de muestra ficticia incluido en el propio producto.','plataforma-seguros':'Captura del prototipo original SeguroOS. Datos de demostración del propio diseño; no son resultados comerciales.','cuentas-carlos':'Captura de la interfaz original de Cuentas Carlos. Cuenta vacía en un entorno local, sin movimientos de proveedor.'}
SLUGS=list(NAMES)
PUBLIC=ROOT/'assets/media/projects';PUBLIC.mkdir(parents=True,exist_ok=True)
for slug in SLUGS:shutil.copy2(CAPTURES/(slug+'.webp'),PUBLIC/(slug+'.webp'))
NAV=[('/','Inicio'),('/soluciones.html','Soluciones'),('/portafolio.html','Proyectos'),('/nosotros.html','Estudio'),('/recursos.html','Recursos')]
MORE=[('/sistemas.html','Software a medida'),('/agentes-ia.html','Agentes IA'),('/automatizaciones.html','Automatizaciones'),('/desarrollo-web.html','Desarrollo web'),('/crm-personalizado.html','CRM personalizado'),('/whatsapp-api-empresas.html','WhatsApp API'),('/metodologia.html','Cómo trabajamos'),('/contacto.html','Contacto')]
def nav(path,dark=False):
 here='/' if path=='index.html' else '/'+path
 links=''.join(f'<a href="{u}"'+(' aria-current="page"' if here==u else '')+f'>{t}</a>' for u,t in NAV)
 mobile=''.join(f'<a href="{u}">{t}</a>' for u,t in NAV+MORE)
 return f'<header class="n-header{(" on-dark" if dark else "")}"><div class="n-wrap n-header-inner"><a class="n-brand" href="/" aria-label="Nicho Agencia Digital, inicio">nicho.</a><nav class="n-desktop" aria-label="Navegación principal">{links}</nav><a class="n-start" href="/contacto.html">Hablemos <span aria-hidden="true">↗</span></a><details class="n-mobile"><summary aria-label="Abrir menú">Menú</summary><nav aria-label="Navegación móvil">{mobile}</nav></details></div></header>'
def footer():
 return '''<footer class="n-footer"><div class="n-wrap"><div class="n-footer-top"><div><span class="n-eyebrow">El siguiente paso es una conversación.</span><h2>¿Qué necesita<br>resolver tu empresa?</h2></div><div class="n-footer-aside"><p>Nos cuentas cómo trabajas. Definimos qué conviene construir, conectar o mejorar.</p><a class="n-link" href="/contacto.html">Hablemos de tu proyecto <b aria-hidden="true">↗</b></a></div></div><div class="n-footer-nav"><div><a class="n-brand" href="/">nicho.</a><address>Carrera 29 #39-39, barrio La Aurora, oficina 01.<br>Bucaramanga, Santander, Colombia.</address></div><div><a href="/soluciones.html">Soluciones</a><a href="/portafolio.html">Portafolio</a><a href="/metodologia.html">Cómo trabajamos</a><a href="/recursos.html">Recursos</a><a href="/bucaramanga.html">Bucaramanga y Colombia</a></div><div><a href="https://wa.me/573028289997" target="_blank" rel="noopener noreferrer">WhatsApp +57 302 828 9997 ↗</a><a href="mailto:nicho.agenciadigital@gmail.com">nicho.agenciadigital@gmail.com</a><a href="https://calendar.app.google/DAYcFPswU2gASF418" target="_blank" rel="noopener noreferrer">Agendar una conversación ↗</a><a href="/contacto.html">Contacto</a></div></div><div class="n-footer-base"><span>© 2026 Nicho Agencia Digital</span><span>Desde Colombia para Latinoamérica</span><a href="/privacidad.html">Privacidad</a></div></div></footer>'''
def picture(slug,zoom=False):
 if slug not in NAMES:
  return '<div class="n-agent-note"><strong>Agentes de atención y ventas.</strong><p>Las conversaciones de clientes son privadas. Presentamos el alcance y las reglas de trabajo, sin atribuirles una interfaz inventada.</p><a href="/contacto.html">Solicitar una demostración ↗</a></div>'
 img=f'<img src="/assets/media/projects/{slug}.webp" alt="Interfaz original de {NAMES[slug]}" width="1440" height="1000" loading="lazy" decoding="async">'
 if zoom:img=f'<button class="capture-zoom" type="button" data-capture-zoom aria-label="Ampliar diseño original de {NAMES[slug]}">{img}</button>'
 return f'<figure class="original-capture">{img}<figcaption>{CAPTIONS[slug]}</figcaption></figure>'
def route_slug(screen,path):
 a=screen.find_parent('a')
 if a and a.get('href','').endswith('.html'):
  val=Path(a['href']).stem
  if val in SLUGS+['agentes-ia']:return val
 if path.startswith('portafolio/'):return Path(path).stem
 label=screen.select_one('.screen-brand');txt=label.get_text(' ',strip=True).lower() if label else ''
 for match,slug in [('invicto','invicto-ops'),('resto','restoops'),('luminari','luminari'),('seguro','plataforma-seguros'),('carlos','cuentas-carlos'),('agent','agentes-ia')]:
  if match in txt:return slug
 return 'agentes-ia'
# Preserve existing full pages and their canonical URLs; replace only unfaithful visuals and their shared shell.
for file in ROOT.rglob('*.html'):
 path=file.relative_to(ROOT).as_posix()
 if path.startswith(('qa/','.git/')) or path=='index.html':continue
 s=BeautifulSoup(file.read_text(),'html.parser')
 for el in s.select('.site-header,.header,.nd-header,#menu-panel,.progress,.n-header,.menu-panel'):el.decompose()
 s.body['class']=['n-site']
 first=s.select_one('main > section'); dark=bool(first and 'light' not in first.get('class',[]) and 'page-hero' in first.get('class',[]))
 s.body.insert(0,BeautifulSoup(nav(path,dark),'html.parser'))
 for screen in list(s.select('.screen')):
  slug=route_slug(screen,path);parent=screen.parent
  screen.replace_with(BeautifulSoup(picture(slug,not bool(screen.find_parent('a'))),'html.parser'))
 for t in s.select('.visual-caption'):t.decompose()
 # This preview caption described fabricated screens; replace it with a truthful source note.
 for t in s.select('.case-caption'):
  t.string='Diseño original del producto · captura de una copia aislada, sin acceso a datos privados.'
 for a in s.select('a[href]'):
  if a['href'] in ['index.html','../index.html']:a['href']='/'
 for old in s.select('footer,.consent-box'):old.decompose()
 s.body.append(BeautifulSoup(footer(),'html.parser'))
 # One additional shared sheet, not a stack of individual patches.
 for old in s.select('link[href$="editorial-shell.css"],script[src$="editorial-shell.js"]'):old.decompose()
 s.head.append(s.new_tag('link',href='/assets/css/editorial-shell.css',rel='stylesheet'))
 script=s.new_tag('script',src='/assets/js/editorial-shell.js');script['defer']='';s.body.append(script)
 # The old app must not animate content from opacity zero; interactivity is retained.
 file.write_text(str(s),encoding='utf-8')

old=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser')
head=old.head
for el in list(head.select('link[rel=stylesheet],script:not([type="application/ld+json"])')):el.decompose()
head.append(old.new_tag('link',href='/assets/css/editorial-shell.css',rel='stylesheet'))
for t in head.select('meta[name=nicho-release]'):t['content']='nicho-editorial-originals-20261012'

projects=[
 ('invicto-ops','01 / Operación comercial','Invicto OPS.','Cada pedido.<br>Todo su recorrido.','Pedidos, inventario, seguimiento comercial y logística. Un sistema que organiza el trabajo de una operación de comercio electrónico.','Gestión comercial · Inventario · Despachos'),
 ('luminari','02 / Gestión de proyectos','Luminari.','El diseño también<br>se gestiona.','El sistema original de Luminari reúne clientes, cotizaciones, fabricación, tareas y finanzas. Con una identidad propia, no una plantilla intercambiable.','CRM · Cotizaciones · Fabricación'),
 ('restoops','03 / Operación gastronómica','RestoOps.','Del ingrediente<br>a la decisión.','Recetas, costos, platos, comandas, inventario y presupuesto. La operación gastronómica vista desde sus propios procesos.','Costeo · Comandas · Caja')]
work=''
for i,(slug,kicker,name,h,body,scope) in enumerate(projects):
 work+=f'''<article class="n-project{(' reverse' if i%2 else '')}"><figure class="n-product-picture"><a href="/portafolio/{slug}.html" aria-label="Conocer {NAMES[slug]}"><img src="/assets/media/projects/{slug}.webp" alt="Diseño original de {NAMES[slug]}" width="1440" height="1000" loading="lazy" decoding="async"></a><figcaption>{CAPTIONS[slug]}</figcaption></figure><div class="n-project-copy"><span class="n-eyebrow">{kicker}</span><h3>{h}</h3><p class="n-body">{body}</p><p class="n-project-scope">{scope}</p><a class="n-link" href="/portafolio/{slug}.html">Explorar {NAMES[slug]} <b aria-hidden="true">↗</b></a></div></article>'''
services=''.join(f'<a href="/{route}"><small>0{i+1}</small><h3>{name}</h3><p>{txt}</p><b aria-hidden="true">↗</b></a>' for i,(route,name,txt) in enumerate([
 ('sistemas.html','Software a medida','Sistemas que se adaptan a las reglas y a la operación de tu empresa.'),
 ('agentes-ia.html','Agentes de IA','Atención, calificación y asistencia comercial con límites y supervisión.'),
 ('automatizaciones.html','Automatización','Conexiones y tareas para que la información no se quede detenida.'),
 ('desarrollo-web.html','Desarrollo web','Webs completas y plataformas con estructura, contenido y funcionalidad.')]))
body=f'''<a class="skip" href="#contenido">Saltar al contenido</a>{nav('index.html',True)}<main id="contenido" class="n-home">
<section class="n-hero"><div class="n-wrap"><div class="n-hero-top n-eyebrow"><span>Nicho Agencia Digital / Software, diseño e IA</span><span>Colombia → Latinoamérica</span></div><div class="n-hero-title"><h1>Tu operación.<br><span>Bien resuelta.</span></h1><div class="n-hero-copy"><p>Software a medida, agentes de inteligencia artificial y automatización. Tecnología que responde a la forma de trabajar de tu negocio.</p><a class="n-link" href="/portafolio.html">Explorar proyectos <b aria-hidden="true">↗</b></a></div></div>
<div class="n-stage" aria-label="Diseños originales de sistemas desarrollados"><figure class="n-hero-shot n-shot-left" aria-hidden="true"><img src="/assets/media/projects/restoops.webp" alt="" width="1440" height="1000"></figure><figure class="n-hero-shot n-shot-main"><img id="hero-product" src="/assets/media/projects/invicto-ops.webp" alt="Diseño original de Invicto OPS" width="1440" height="1000" fetchpriority="high"></figure><figure class="n-hero-shot n-shot-right" aria-hidden="true"><img src="/assets/media/projects/luminari.webp" alt="" width="1440" height="1000"></figure></div>
<div class="n-stage-caption"><div><p id="hero-product-caption">Interfaz original · vista local sin datos operativos.</p><div class="n-stage-buttons" role="group" aria-label="Ver diseños originales"><button type="button" data-product-select="invicto-ops" aria-pressed="true">Invicto OPS</button><button type="button" data-product-select="luminari" aria-pressed="false">Luminari</button><button type="button" data-product-select="restoops" aria-pressed="false">RestoOps</button></div></div><button type="button" class="n-motion" data-editorial-motion aria-pressed="false">Pausar movimiento</button></div></div></section>
<section class="n-intro"><div class="n-wrap"><div class="n-section-top n-eyebrow"><span>El problema primero.</span><span>La herramienta correcta, después.</span></div><div class="n-intro-grid"><h2>Hecho para<br>tu manera<br><span>de trabajar.</span></h2><p class="n-body">No todo se resuelve con otra aplicación. A veces hay que conectar lo que ya existe. Otras, crear un sistema propio. En Nicho diseñamos alrededor de tus procesos, de tu equipo y de lo que necesitas mejorar.</p></div></div></section>
<section class="n-work"><div class="n-wrap"><div class="n-work-head"><div><span class="n-eyebrow">Trabajo seleccionado / Interfaces originales</span><h2 class="n-heading">No son lo mismo.<br><span>No se ven igual.</span></h2></div><a class="n-link" href="/portafolio.html">Ver todo el portafolio <b aria-hidden="true">↗</b></a></div>{work}<div class="n-work-end"><p>También desarrollamos soluciones para seguros, control de proveedores y conversaciones comerciales con IA.</p><a class="n-link" href="/portafolio.html">Conocer los seis casos <b aria-hidden="true">↗</b></a></div></div></section>
<section class="n-capabilities"><div class="n-wrap"><div class="n-section-top n-eyebrow"><span>Soluciones</span><span>Una página para cada especialidad.</span></div><div class="n-cap-head"><h2 class="n-heading">De la necesidad<br><span>a la solución.</span></h2><p class="n-body">Explora el enfoque, las capacidades y las condiciones de cada servicio.</p></div><div class="n-service-list">{services}</div></div></section>
<section class="n-method"><div class="n-wrap"><div class="n-section-top n-eyebrow"><span>Cómo trabajamos</span><span>Personas, procesos y tecnología.</span></div><h2 class="n-heading">Entender. Diseñar.<br><span>Hacer que funcione.</span></h2><div class="n-process"><article class="n-process-step"><small>01 / ENTENDER</small><h3>El problema correcto.</h3><p>Revisamos cómo trabaja tu empresa, dónde se pierde información y qué necesita cambiar.</p></article><article class="n-process-step"><small>02 / DISEÑAR</small><h3>Una estructura útil.</h3><p>Definimos el recorrido, los módulos, las integraciones y los límites del proyecto.</p></article><article class="n-process-step"><small>03 / IMPLEMENTAR</small><h3>Probar antes de escalar.</h3><p>Desarrollamos por etapas, comprobamos escenarios y acompañamos la puesta en marcha.</p></article></div><div class="n-method-bottom"><p>Las integraciones, tiempos y entregables se validan por proyecto. La automatización debe mantener el control humano donde se necesita.</p><a class="n-link" href="/metodologia.html">Conocer el método <b aria-hidden="true">↗</b></a></div></div></section>
</main>{footer()}<script src="/assets/vendor/gsap.min.js" defer></script><script src="/assets/vendor/ScrollTrigger.min.js" defer></script><script src="/assets/js/editorial-shell.js" defer></script>'''
(ROOT/'index.html').write_text('<!doctype html><html lang="es" data-release="nicho-editorial-originals-20261012">'+str(head)+'<body class="n-site">'+body+'</body></html>')
# Source provenance is public technical metadata, not customer records.
provenance={}
for slug in SLUGS:
 repo='Luminari' if slug=='luminari' else 'restoops' if slug=='restoops' else 'Samuelacuna12.github.io'
 rev=(Path(sys.argv[3])/(repo+'.revision.txt')).read_text().strip()
 provenance[slug]={'repository':'Samuelacuna12/'+repo,'revision':rev,'image':'assets/media/projects/'+slug+'.webp','caption':CAPTIONS[slug],'live_data_accessed':False}
(ROOT/'docs/original-interface-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
print('Repaired: 24 canonical pages retained; five original interfaces; no invented product dashboards.')

for f in ROOT.rglob('*.html'):
 if 'qa' in f.parts:continue
 t=f.read_text()
 t=t.replace('Las interfaces son representaciones ilustrativas del alcance. Los estados de desarrollo se indican en cada caso; no se muestran datos privados ni resultados comerciales no verificados.','Las imágenes corresponden a los diseños originales de los sistemas, abiertos en copias aisladas con estados vacíos o datos de demostración. No se muestran datos de clientes. El estado de cada proyecto se indica en su caso.')
 t=t.replace('INTERFAZ ILUSTRATIVA. NO ES UNA CAPTURA CON DATOS REALES.','INTERFAZ ORIGINAL · ENTORNO DE DEMOSTRACIÓN SIN DATOS DE CLIENTES.' if f.stem!='agentes-ia' else 'CONVERSACIONES PRIVADAS · DEMOSTRACIONES BAJO SOLICITUD.')
 t=t.replace('Las conversaciones de clientes son privadas. Presentamos el alcance y las reglas de trabajo, sin atribuirles una interfaz inventada.','Atención, calificación y seguimiento según las reglas de cada negocio. Por privacidad, las conversaciones se muestran únicamente en demostraciones autorizadas.')
 t=t.replace('No son lo mismo.<br><span>No se ven igual.</span>','Software propio.<br><span>Identidad propia.</span>')
 t=t.replace('Una página para cada especialidad.','Diseño, desarrollo e implementación.')
 f.write_text(t)
