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