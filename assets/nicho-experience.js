(()=>{'use strict';
const root=document.querySelector('#xl-demo');if(!root)return;
const stages=[
 {head:'01 / AGENTE IA',speaker:'CONSULTA RECIBIDA',question:'Necesito una solución para organizar mis ventas.',speaker2:'AGENTE / RESPUESTA',answer:'Entiendo. ¿Cómo recibes y haces seguimiento a tus clientes actualmente?',in:'Conversación',out:'Necesidad identificada',status:'ESPERANDO SIGUIENTE ETAPA'},
 {head:'02 / CRM',speaker:'CONTEXTO IDENTIFICADO',question:'Un equipo necesita centralizar consultas, oportunidades y seguimientos.',speaker2:'CRM / ACCIÓN',answer:'La oportunidad se clasifica y queda asociada a una etapa y a un responsable.',in:'Oportunidad comercial',out:'Registro organizado',status:'INFORMACIÓN ESTRUCTURADA'},
 {head:'03 / AUTOMATIZACIÓN',speaker:'EVENTO COMERCIAL',question:'Una nueva oportunidad necesita seguimiento después de la primera conversación.',speaker2:'FLUJO / ACCIÓN',answer:'El sistema crea una tarea de seguimiento y prepara el siguiente paso para el asesor.',in:'Evento detectado',out:'Siguiente tarea',status:'PROCESO ACTIVADO'}
];
const buttons=[...root.querySelectorAll('[data-stage]')];let active=0;
const $=id=>document.getElementById(id);
const panel=$('xl-demo-conversation'),system=$('xl-demo-system'),status=$('xl-demo-status'),head=$('xl-current-stage');
function make(s){
 const speaker1=document.createElement('span');speaker1.className='xl-speaker';speaker1.textContent=s.speaker;
 const q=document.createElement('p');q.textContent=s.question;
 const speaker2=document.createElement('span');speaker2.className='xl-speaker xl-speaker-ai';speaker2.textContent=s.speaker2;
 const a=document.createElement('p');a.textContent=s.answer;
 panel.replaceChildren(speaker1,q,speaker2,a);
 const first=document.createElement('div');first.className='xl-demo-system-item';
 const second=document.createElement('div');second.className='xl-demo-system-item';
 for(const [el,label,value,badge] of [[first,'ENTRADA',s.in,'01'],[second,'RESULTADO',s.out,'↗']]){
  const small=document.createElement('span');small.textContent=label;
  const strong=document.createElement('strong');strong.textContent=value;
  const mark=document.createElement('b');mark.textContent=badge;
  el.append(small,strong,mark);
 }
 system.replaceChildren(first,second);
 panel.classList.remove('xl-swap');void panel.offsetWidth;panel.classList.add('xl-swap');
}
function select(index){active=((index%stages.length)+stages.length)%stages.length;buttons.forEach((b,i)=>{b.classList.toggle('active',i===active);b.setAttribute('aria-pressed',String(i===active))});const s=stages[active];head.textContent=s.head;status.textContent=s.status;make(s)}
buttons.forEach((b,i)=>b.addEventListener('click',()=>select(i)));
const next=$('xl-demo-next');if(next)next.addEventListener('click',()=>select(active+1));
const observer=('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches)
 ?new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('xl-in-view');observer.unobserve(entry.target)}}),{threshold:.1}):null;
document.querySelectorAll('.xl-cap-rows>a,.xl-cap-head,.xl-proof-intro,.xl-demo').forEach(el=>{if(observer){el.classList.add('xl-enter');observer.observe(el)}else{el.classList.add('xl-in-view')}});
})();