(()=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
const els=document.querySelectorAll('.case-editorial,.case-detail-bisect>div,.case-module-grid article,.case-flow-step,.case-portfolio-statement');
if(!('IntersectionObserver'in window))return;
const io=new IntersectionObserver(entries=>{for(const e of entries){if(e.isIntersecting){e.target.classList.add('case-visible');io.unobserve(e.target)}}},{threshold:.06});
els.forEach(e=>{e.classList.add('case-reveal');io.observe(e)});
})();
;(()=>{'use strict';
const filters=[...document.querySelectorAll('.pf-filter')];
const cases=[...document.querySelectorAll('.case-editorial[data-category]')];
const count=document.querySelector('#pf-result-count');
if(filters.length && cases.length){
  filters.forEach(button=>button.addEventListener('click',()=>{
    const v=button.dataset.filter;
    filters.forEach(b=>{const yes=b===button;b.classList.toggle('active',yes);b.setAttribute('aria-pressed',String(yes))});
    let shown=0;
    cases.forEach(c=>{const match=v==='all'||c.dataset.category===v;c.hidden=!match;if(match){shown++;c.classList.add('case-visible')}});
    if(count)count.textContent=String(shown).padStart(2,'0')+(shown===1?' PROYECTO':' PROYECTOS');
  }));
}
const previews=[...document.querySelectorAll('.case-detail-screen')];
function resize(){
for(const p of previews){const width=p.clientWidth;const scale=Math.min(1,width/950);p.style.setProperty('--case-scale',scale.toFixed(5));p.style.setProperty('--case-preview-height',Math.ceil(540*scale)+'px')}
}
if(previews.length){resize();addEventListener('resize',resize,{passive:true});if('ResizeObserver'in window){const ro=new ResizeObserver(resize);previews.forEach(p=>ro.observe(p))}}
})();