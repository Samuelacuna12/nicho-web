/* Nicho Agencia Digital: progressive interactions. No trackers enabled by default. */
(()=>{'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const root=document.documentElement;
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const storage={get(k){try{return localStorage.getItem(k)}catch{return null}},set(k,v){try{localStorage.setItem(k,v)}catch{}}};
const config=window.NICHO_CONFIG||{};
let motion=!reduced.matches&&storage.get('nicho.motion')!=='off';
let gsapContext=null;
let consent=storage.get('nicho.analytics')==='granted',analyticsLoaded=false;
function updateMotion(){
 root.dataset.motion=motion?'on':'off';
 $$('[data-motion-toggle]').forEach(b=>{b.setAttribute('aria-pressed',String(!motion));$('[data-motion-label]',b).textContent=motion?'Pausar movimiento':'Activar movimiento'});
 document.dispatchEvent(new CustomEvent('nicho:motion',{detail:{enabled:motion}}));
 $$('video[data-ambient]').forEach(v=>setVideoState(v,v.dataset.inview==='true'));
 if(gsapContext){gsapContext.revert();gsapContext=null}
 if(motion&&window.gsap&&window.ScrollTrigger){
  try{window.gsap.registerPlugin(window.ScrollTrigger);
   gsapContext=window.gsap.context(()=>{
    $$('.reveal').forEach(el=>{gsap.from(el,{y:30,opacity:0,duration:.8,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 94%',once:true}})});
    if(matchMedia('(min-width: 901px)').matches){
     $$('[data-drift]').forEach(el=>gsap.fromTo(el,{y:30},{y:-25,ease:'none',scrollTrigger:{trigger:el.parentElement,start:'top bottom',end:'bottom top',scrub:.8}}));
    }
   });
  }catch(error){if(gsapContext)gsapContext.revert();gsapContext=null}
 }
}
$$('[data-motion-toggle]').forEach(b=>b.addEventListener('click',()=>{motion=!motion;storage.set('nicho.motion',motion?'on':'off');updateMotion()}));
reduced.addEventListener('change',e=>{motion=!e.matches&&storage.get('nicho.motion')!=='off';updateMotion()});
updateMotion();
// Off-canvas navigation: explicit focus management, Esc, no scroll manipulation on the page.
const panel=$('#menu-panel'),opener=$('[data-menu-open]'),closer=$('[data-menu-close]');let lastFocus=null;
function closeMenu(){if(!panel)return;panel.hidden=true;document.body.classList.remove('menu-open');opener?.setAttribute('aria-expanded','false');if(lastFocus?.isConnected)lastFocus.focus()}
function openMenu(){if(!panel)return;lastFocus=document.activeElement;panel.hidden=false;document.body.classList.add('menu-open');opener?.setAttribute('aria-expanded','true');closer?.focus()}
opener?.addEventListener('click',openMenu);closer?.addEventListener('click',closeMenu);
panel?.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();closeMenu()}if(e.key==='Tab'){const items=$$('a,button,[tabindex="0"]',panel).filter(el=>!el.hidden);const first=items[0],last=items[items.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}});
$$('a',panel||document.createElement('div')).forEach(a=>a.addEventListener('click',closeMenu));
// Scroll progress uses one scheduled frame; no continuous offscreen loop.
const progress=$('.progress');let scheduled=false;
function measureScroll(){scheduled=false;$('.site-header')?.classList.toggle('is-scrolled',scrollY>90);const max=root.scrollHeight-innerHeight;if(progress)progress.style.transform=`scaleX(${max>0?Math.min(1,scrollY/max):0})`}
addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(measureScroll)}},{passive:true});addEventListener('resize',measureScroll,{passive:true});measureScroll();
// Ambient footage is loaded near the viewport, silenced, paused offscreen and respects motion choice.
const videos=$$('video[data-ambient]');
function setVideoState(v,inview){if(v.dataset.disabled==='true')return;v.dataset.inview=String(inview);if(inview&&motion){if(!v.src&&v.dataset.src){v.src=v.dataset.src;v.load()}if(v.dataset.userpause!=='true')v.play().catch(()=>{})}else{v.pause()}}
if('IntersectionObserver'in window){const io=new IntersectionObserver(entries=>entries.forEach(e=>setVideoState(e.target,e.isIntersecting)),{rootMargin:'120px 0px',threshold:.02});videos.forEach(v=>io.observe(v))}
document.addEventListener('visibilitychange',()=>{videos.forEach(v=>{if(document.hidden)v.pause();else if(v.dataset.disabled!=='true'&&v.dataset.inview==='true'&&motion&&v.dataset.userpause!=='true')v.play().catch(()=>{})})});
$$('[data-video-toggle]').forEach(b=>b.addEventListener('click',()=>{const v=document.getElementById(b.dataset.videoToggle);if(!v)return;const pause=!v.paused;if(pause){v.pause();v.dataset.userpause='true'}else{v.dataset.userpause='false';if(!v.src&&v.dataset.src){v.src=v.dataset.src;v.load()}v.play().catch(()=>{})}b.textContent=pause?'Reproducir video':'Pausar video';b.setAttribute('aria-pressed',String(pause))}));
// Workflow demo: true tab semantics and keyboard navigation. No AI or client API is called.
$$('[data-flow]').forEach(group=>{const tabs=$$('[role=tab]',group),panels=$$('[role=tabpanel]',group);function select(i,focus=false){tabs.forEach((t,j)=>{const on=i===j;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;panels[j].hidden=!on});if(focus)tabs[i].focus();track('demo_step',{step:tabs[i].dataset.step||String(i)})}tabs.forEach((t,i)=>{t.addEventListener('click',()=>select(i));t.addEventListener('keydown',e=>{let n=null;if(e.key==='ArrowRight'||e.key==='ArrowDown')n=(i+1)%tabs.length;if(e.key==='ArrowLeft'||e.key==='ArrowUp')n=(i+tabs.length-1)%tabs.length;if(e.key==='Home')n=0;if(e.key==='End')n=tabs.length-1;if(n!==null){e.preventDefault();select(n,true)}})});if(tabs.length)select(0)});
// Portfolio filters; all cases are visible without JavaScript.
const filterButtons=$$('[data-filter]'),caseCards=$$('[data-category]');
filterButtons.forEach(b=>b.addEventListener('click',()=>{let count=0;const filter=b.dataset.filter;filterButtons.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));caseCards.forEach(c=>{const on=filter==='all'||c.dataset.category===filter;c.hidden=!on;if(on)count++});const label=$('#filter-count');if(label)label.textContent=`${count} ${count===1?'proyecto':'proyectos'}`;track('portfolio_filter',{filter});requestAnimationFrame(()=>window.ScrollTrigger?.refresh())}));
// Fit illustrative desktop UIs to phones without horizontal scrolling or negative margins.
$$('.case-exhibit-inner').forEach(el=>{function fit(){el.style.setProperty('--screen-scale',String(Math.min(1,el.clientWidth/760)))}fit();if('ResizeObserver'in window)new ResizeObserver(fit).observe(el);else addEventListener('resize',fit,{passive:true})});
// Brief builder never claims submission. It prepares an editable WhatsApp message only.
const brief=$('#project-brief');brief?.addEventListener('submit',e=>{e.preventDefault();if(!brief.reportValidity())return;const data=new FormData(brief);const clean=k=>String(data.get(k)||'').trim().slice(0,k==='objetivo'?800:100);const name=clean('nombre'),company=clean('empresa'),service=clean('servicio'),objective=clean('objetivo');const message=`Hola, Nicho Agencia Digital. Soy ${name}${company?' de '+company:''}.\n\nMe interesa: ${service}.\nMi objetivo: ${objective}\n\nQuisiera conversar sobre el alcance y los siguientes pasos.`;const result=$('#brief-result');const target=$('#brief-whatsapp');target.href=`https://wa.me/573028289997?text=${encodeURIComponent(message)}`;result.hidden=false;$('#brief-preview').textContent=message;target.focus();track('brief_prepared',{service})});
// Privacy-conscious analytics hook. No PII is put into events, and no request is made until consent + a real ID.
function track(event,params={}){document.dispatchEvent(new CustomEvent('nicho:event',{detail:{event,...params}}));if(consent&&analyticsLoaded&&typeof window.gtag==='function')window.gtag('event',event,params)}
function loadAnalytics(){if(!consent||!/^G-[A-Z0-9]+$/.test(config.ga4MeasurementId||''))return;window['ga-disable-'+config.ga4MeasurementId]=false;if(analyticsLoaded){window.gtag?.('consent','update',{analytics_storage:'granted'});return;}window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments)};window.gtag('consent','default',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});window.gtag('js',new Date());window.gtag('config',config.ga4MeasurementId,{send_page_view:true});const s=document.createElement('script');s.async=true;s.src=`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(config.ga4MeasurementId)}`;document.head.append(s);analyticsLoaded=true}
const consentPanel=$('#analytics-consent');if(config.ga4MeasurementId){if(storage.get('nicho.analytics')===null&&consentPanel)consentPanel.hidden=false;loadAnalytics()}
$$('[data-consent]').forEach(b=>b.addEventListener('click',()=>{consent=b.dataset.consent==='accept';storage.set('nicho.analytics',consent?'granted':'denied');if(consentPanel)consentPanel.hidden=true;if(consent){loadAnalytics()}else{window['ga-disable-'+config.ga4MeasurementId]=true;window.gtag?.('consent','update',{analytics_storage:'denied'})}}));
$$('[data-cookie-settings]').forEach(b=>{b.hidden=!config.ga4MeasurementId;b.addEventListener('click',()=>{if(consentPanel)consentPanel.hidden=false})});
document.addEventListener('click',e=>{const a=e.target.closest('a[data-track]');if(a)track(a.dataset.track,{location:a.dataset.trackLocation||'site'})});
window.NICHO_APP={motion:()=>motion,track};
})();
