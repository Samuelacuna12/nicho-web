(()=>{const header=document.querySelector('.nd-header'),menu=document.querySelector('#nd-menu-button'),links=document.querySelector('.nd-nav-links');if(!header)return;
 const scroll=()=>header.classList.toggle('nd-scrolled',window.scrollY>Math.max(240,window.innerHeight*.82));
 scroll();addEventListener('scroll',scroll,{passive:true});
 if(menu&&links){menu.addEventListener('click',()=>{const open=header.classList.toggle('nd-menu-open');menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Cerrar menú':'Abrir menú')});links.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{header.classList.remove('nd-menu-open');menu.setAttribute('aria-expanded','false')}))}
 const move=!matchMedia('(prefers-reduced-motion: reduce)').matches;
 if(move&&'IntersectionObserver'in window){const observer=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('nd-visible');observer.unobserve(e.target)}}),{threshold:.14});document.querySelectorAll('.nd-reveal').forEach(el=>observer.observe(el))}
 else document.querySelectorAll('.nd-reveal').forEach(el=>el.classList.add('nd-visible'));
 const hero=document.querySelector('.nd-stage'),art=document.querySelector('.nd-stage-art');
 if(hero&&art&&move&&matchMedia('(pointer:fine)').matches){let x=0,y=0;hero.addEventListener('pointermove',ev=>{x=(ev.clientX/innerWidth-.5)*36;y=(ev.clientY/innerHeight-.5)*22;art.style.setProperty('--nd-x',x.toFixed(1)+'px');art.style.setProperty('--nd-y',y.toFixed(1)+'px')},{passive:true})}
})();
;(()=>{'use strict';
 const prefersReduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const p=document.createElement('div');p.className='nd-motion-progress';p.setAttribute('aria-hidden','true');document.body.append(p);
 let raf=false;
 const update=()=>{const max=document.documentElement.scrollHeight-innerHeight;const percent=max>0?Math.max(0,Math.min(1,scrollY/max)):1;p.style.transform='scaleX('+percent.toFixed(4)+')';raf=false};
 const scroll=()=>{if(!raf){raf=true;requestAnimationFrame(update)}};
 addEventListener('scroll',scroll,{passive:true});addEventListener('resize',scroll,{passive:true});update();
 if(prefersReduced)return;
 const targets=document.querySelectorAll('.nd-work-case-info,.nd-gallery-heading,.nd-method-grid,.nd-end-bottom,.case-editorial-copy,.case-modules-header,.seo-resource');
 if('IntersectionObserver'in window){const o=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('nd-motion-visible');o.unobserve(e.target)}}),{threshold:.05,rootMargin:'0px 0px -30px 0px'});
 targets.forEach(el=>{el.classList.add('nd-motion-in');o.observe(el)})}
 const film=document.querySelector('.nd-film'),filmImg=film?.querySelector('img');
 if(film&&filmImg){let fRaf=false;const move=()=>{if(fRaf)return;fRaf=true;requestAnimationFrame(()=>{const r=film.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0){const pos=(innerHeight-r.top)/(innerHeight+r.height);filmImg.style.setProperty('--nd-film-zoom',String(1.04+pos*.11))}fRaf=false})};addEventListener('scroll',move,{passive:true});move()}
 const curtain=document.createElement('div');curtain.className='nd-page-curtain';curtain.setAttribute('aria-hidden','true');document.body.append(curtain);
 document.addEventListener('click',e=>{if(e.defaultPrevented||e.button!==0||e.ctrlKey||e.metaKey||e.altKey||e.shiftKey)return;
 const a=e.target.closest('a[href]');if(!a||a.target==='_blank'||a.hasAttribute('download'))return;
 const href=a.getAttribute('href');if(!href||href.startsWith('#')||href.startsWith('mailto:')||href.startsWith('tel:')||href.startsWith('javascript:'))return;
 let u;try{u=new URL(href,location.href)}catch{return}
 if(u.origin!==location.origin||u.pathname===location.pathname&&u.hash)return;
 e.preventDefault();curtain.classList.add('nd-closed');setTimeout(()=>{location.assign(u.href)},310);
 },{passive:false});
 addEventListener('pageshow',()=>curtain.classList.remove('nd-closed'));
})();
