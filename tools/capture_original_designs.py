from pathlib import Path
from urllib.parse import urlsplit, unquote
from playwright.sync_api import sync_playwright
import mimetypes,json, re, base64,sys,os
from bs4 import BeautifulSoup
ROOT=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve();OUT.mkdir(parents=True,exist_ok=True)
STUB=r'''(()=>{
 const fake={id:'00000000-0000-4000-8000-000000000001',full_name:'Equipo de demostración',username:'demo',role:'admin',active:true,can_receive_sales:false,must_change_password:false};
 const builder=()=>new Proxy({}, {get(t,k){if(k==='then')return (resolve,reject)=>Promise.resolve({data:[],error:null,count:0}).then(resolve,reject);if(k==='single'||k==='maybeSingle')return ()=>Promise.resolve({data:fake,error:null});return ()=>builder();}});
 const auth={getSession:async()=>({data:{session:null},error:null}),onAuthStateChange:()=>({data:{subscription:{unsubscribe(){}}}}),signOut:async()=>({error:null})};
 const sb={from:()=>builder(),rpc:async()=>({data:[],error:null}),auth,channel:()=>({on(){return this},subscribe(){return this},unsubscribe(){}}),removeChannel(){},storage:{from:()=>builder()}};
 window.supabase={createClient:()=>sb};window.XLSX={};
 window.fetch=async()=>new Response(JSON.stringify([]),{status:200,headers:{'Content-Type':'application/json'}});
 window.WebSocket=class {close(){} addEventListener(){} send(){}};
 const memory={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>memory[k]??null,setItem:(k,v)=>memory[k]=String(v),removeItem:k=>delete memory[k],clear:()=>Object.keys(memory).forEach(k=>delete memory[k])}});
 window.__snapshot={network:'blocked',data:'no production connection'};
})();'''

def capture():
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE'),headless=True,args=['--no-sandbox'])
  for slug,url in [
   ('restoops','/restoops/index.html'),
   ('luminari','/Luminari/index.html?demo=1'),
   ('invicto-ops','/Samuelacuna12.github.io/invicto-ops/index.html'),
   ('cuentas-carlos','/Samuelacuna12.github.io/cuentas-carlos/index.html'),
   ('plataforma-seguros','/Samuelacuna12.github.io/dashboardseguros/index.html')]:
   context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1,locale='es-CO')
   def handle(route):
    u=urlsplit(route.request.url)
    if u.hostname=='preview.invalid':
     f=ROOT/unquote(u.path).lstrip('/')
     if f.is_file():
      route.fulfill(status=200,content_type=mimetypes.guess_type(f)[0] or 'text/plain',body=f.read_bytes());return
     route.fulfill(status=404,body='not found');return
    route.abort()
   context.route('**/*',handle);context.add_init_script(STUB)
   page=context.new_page();errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
   try:
    file=ROOT/urlsplit(url).path.lstrip('/')
    soup=BeautifulSoup(file.read_text(),'html.parser')
    for link in soup.select('link[rel="stylesheet"]'):
     href=link.get('href','')
     if href.startswith('http'):link.decompose();continue
     f=file.parent/urlsplit(href).path
     tag=soup.new_tag('style');tag.string=f.read_text();link.replace_with(tag)
    for script in soup.select('script[src]'):
     href=script['src']
     if href.startswith('http'):script.decompose();continue
     f=file.parent/urlsplit(href).path
     script.attrs.pop('src',None);script.attrs.pop('defer',None);script.string=f.read_text()
    for script in soup.select('script:not([src])'):
     if slug=='luminari' and script.string:script.string=script.string.replace('new URLSearchParams(location.search)',"new URLSearchParams('demo=1')")
    for image in soup.select('img[src]'):
     ref=image['src']; f=file.parent/urlsplit(ref).path
     if not ref.startswith(('http','data:')) and f.is_file():image['src']='data:'+str(mimetypes.guess_type(f)[0] or 'image/png')+';base64,'+base64.b64encode(f.read_bytes()).decode()
    stub=soup.new_tag('script');stub.string=STUB;soup.head.insert(0,stub)
    page.set_content(str(soup),wait_until='load',timeout=20000);page.wait_for_timeout(1400)
    if slug=='invicto-ops':
     page.evaluate("""()=>{session={id:'00000000-0000-4000-8000-000000000001',name:'Equipo de demostración',username:'demo',role:'Administrador',roleCode:'admin',mustChangePassword:false};invictoAuthReadyV12=true;render();}""")
     page.wait_for_timeout(1500)
    if slug=='plataforma-seguros':
     # Redact built-in demonstration names; production network calls are blocked above.
     page.evaluate("""()=>{const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);while(walker.nextNode()){const n=walker.currentNode;if(n.parentElement.closest('script,style'))continue;n.textContent=n.textContent.replace(/Ana Martínez|Juan Pérez|Carlos Ramírez|María López/g,'Cliente de ejemplo').replace(/\b\d{1,3}(?:\.\d{3}){2,3}\b/g,'—')}}""")
    if slug=='invicto-ops':
     page.evaluate("""()=>{document.querySelectorAll('.mode-chip').forEach(el=>el.textContent='VISTA LOCAL · SIN DATOS');const walk=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);while(walk.nextNode()){const n=walk.currentNode;if(n.parentElement.closest('script,style'))continue;if(n.textContent.includes('DATOS EN VIVO'))n.textContent=n.textContent.replace('DATOS EN VIVO · SUPABASE','VISTA LOCAL · SIN DATOS')}}""")
    page.screenshot(path=str(OUT/(slug+'.png')))
    from PIL import Image
    Image.open(OUT/(slug+'.png')).save(OUT/(slug+'.webp'),quality=86,method=6)
    print(slug,'ORIGINAL INTERFACE RENDERED; offline only. Errors in source:',len(errs))
    (OUT/(slug+'.json')).write_text(json.dumps({'slug':slug,'errors':errs,'offline':True},ensure_ascii=False))
   except Exception as e:print(slug,'FAILED',e)
   context.close()
  browser.close()
if __name__=='__main__':capture()
