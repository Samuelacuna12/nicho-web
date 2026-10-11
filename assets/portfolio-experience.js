(()=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
const els=document.querySelectorAll('.case-editorial,.case-detail-bisect>div,.case-module-grid article,.case-flow-step,.case-portfolio-statement');
if(!('IntersectionObserver'in window))return;
const io=new IntersectionObserver(entries=>{for(const e of entries){if(e.isIntersecting){e.target.classList.add('case-visible');io.unobserve(e.target)}}},{threshold:.06});
els.forEach(e=>{e.classList.add('case-reveal');io.observe(e)});
})();