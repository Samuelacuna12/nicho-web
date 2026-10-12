/* Presentation only. No live product requests, visitor tracking or synthetic client data. */
(()=>{'use strict';
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
// Remove the old preview marker, preserving campaign and other meaningful parameters.
try{const u=new URL(location.href);if(u.searchParams.get('v')==='kinetic'){u.searchParams.delete('v');history.replaceState(history.state,'',u.pathname+u.search+u.hash)};if(['/', '/index.html'].includes(u.pathname)){const legacy={'#proyectos':'/portafolio.html','#servicios':'/soluciones.html','#como':'/metodologia.html'};if(legacy[u.hash]){location.replace(legacy[u.hash]+u.search);return}}}catch{}
const header=$('.n-header'),mobile=$('.n-mobile');const onscroll=()=>header?.classList.toggle('scrolled',scrollY>55);addEventListener('scroll',onscroll,{passive:true});onscroll();
mobile?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>mobile.open=false));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&mobile?.open){mobile.open=false;mobile.querySelector('summary').focus()}});
const reduced=matchMedia('(prefers-reduced-motion: reduce)');let moving=!reduced.matches,ctx=null;
const toggle=$('[data-editorial-motion]');
function motion(){if(toggle){toggle.textContent=moving?'Pausar movimiento':'Activar movimiento';toggle.setAttribute('aria-pressed',String(!moving))}if(ctx){ctx.revert();ctx=null}if(!moving||!window.gsap||!window.ScrollTrigger)return;
 gsap.registerPlugin(ScrollTrigger);ctx=gsap.context(()=>{
  // Only product images move. Text never waits at reduced opacity or under a pin.
  $$('.n-hero-shot').forEach((el,i)=>gsap.from(el,{y:38+i*14,scale:.97,duration:1.25,delay:i*.12,ease:'power3.out',clearProps:'transform'}));
  $$('.n-product-picture img').forEach(el=>gsap.fromTo(el,{scale:1.02},{scale:1,ease:'none',scrollTrigger:{trigger:el,start:'top bottom',end:'center center',scrub:.6}}));
  $$('.n-process-step').forEach(el=>gsap.to(el,{'--process-progress':1,ease:'none',scrollTrigger:{trigger:el,start:'top 85%',end:'center 55%',scrub:.4}}));
 });
}
toggle?.addEventListener('click',()=>{moving=!moving;motion()});reduced.addEventListener('change',()=>{moving=!reduced.matches;motion()});motion();
const sources={
 'invicto-ops':{name:'Invicto OPS',caption:'Interfaz original · vista local sin datos operativos.'},
 'restoops':{name:'RestoOps',caption:'Interfaz original · estado vacío, sin conexión a los restaurantes.'},
 'luminari':{name:'Luminari',caption:'Interfaz original · modo de muestra ficticia incluido en el producto.'}
};
$$('[data-product-select]').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.productSelect,entry=sources[id],img=$('#hero-product');if(!entry||!img)return;img.src='/assets/media/projects/'+id+'.webp';img.alt='Diseño original de '+entry.name;$('#hero-product-caption').textContent=entry.caption;$$('[data-product-select]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));if(moving&&window.gsap)gsap.fromTo(img,{scale:.985},{scale:1,duration:.45,ease:'power2.out',clearProps:'transform'})}));
// Native dialog keeps focus trapped; Escape and backdrop close without altering app screenshots.
const buttons=$$('[data-capture-zoom]');if(buttons.length){const d=document.createElement('dialog');d.className='n-capture-dialog';d.innerHTML='<div class="capture-controls"><strong></strong><button type="button" aria-label="Cerrar captura">Cerrar ×</button></div><img alt=""><p></p>';document.body.append(d);let origin=null;
 buttons.forEach(b=>b.addEventListener('click',()=>{const img=b.querySelector('img');if(!img)return;origin=b;d.querySelector('img').src=img.src;d.querySelector('img').alt=img.alt;d.querySelector('strong').textContent=img.alt;d.querySelector('p').textContent=b.closest('figure')?.querySelector('figcaption')?.textContent||'';d.showModal()}));
 d.querySelector('button').addEventListener('click',()=>d.close());d.addEventListener('click',e=>{if(e.target===d)d.close()});d.addEventListener('close',()=>origin?.focus({preventScroll:true}));
}
})();
