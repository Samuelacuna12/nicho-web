
(function(){
  const bar=document.querySelector('.topbar');
  const nav=document.querySelector('.nav-links');
  const toggle=document.querySelector('.menu-toggle');
  const scroll=()=>bar&&bar.classList.toggle('is-scrolled',window.scrollY>20);
  scroll();window.addEventListener('scroll',scroll,{passive:true});
  if(toggle&&nav){toggle.addEventListener('click',()=>{let open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.textContent=open?'×':'☰'});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.textContent='☰'}))}
  document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
  if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
    const o=new IntersectionObserver((els)=>{els.forEach(e=>{if(e.isIntersecting){e.target.classList.add('show');o.unobserve(e.target)}})},{threshold:.1});
    document.querySelectorAll('.reveal').forEach(el=>o.observe(el));
  }else document.querySelectorAll('.reveal').forEach(el=>el.classList.add('show'));
})();
