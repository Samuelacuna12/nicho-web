
(function(){
 const canMove=!window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 const hero=document.querySelector('.nx-hero');
 if(hero&&canMove){let targetX=0,targetY=0,curX=0,curY=0;
   hero.addEventListener('pointermove',e=>{if(e.pointerType==='mouse'){targetX=(e.clientX/window.innerWidth-.5)*45;targetY=(e.clientY/window.innerHeight-.5)*32;}},{passive:true});
   const frame=()=>{if(!hero.isConnected)return;curX+=(targetX-curX)*.065;curY+=(targetY-curY)*.065;hero.style.setProperty('--orb-x',curX.toFixed(2)+'px');hero.style.setProperty('--orb-y',curY.toFixed(2)+'px');requestAnimationFrame(frame)};requestAnimationFrame(frame);
 }
 const definitions={
 ventas:{labels:['Nuevo contacto','Calificación IA','CRM actualizado'],result:'El cliente recibe respuesta y la oportunidad queda registrada.'},
 atencion:{labels:['Pregunta del cliente','Asistente IA','Respuesta o asesor'],result:'Una consulta resuelta o derivada con el contexto necesario.'},
 operacion:{labels:['Evento del negocio','Regla automática','Tarea ejecutada'],result:'Menos pasos manuales y un proceso trazable.'}
 };
 const buttons=[...document.querySelectorAll('.nx-flow-tab')];
 const canvas=document.getElementById('nx-flow-nodes');
 const line=document.getElementById('nx-flow-result');
 if(buttons.length&&canvas&&line){buttons.forEach(btn=>btn.addEventListener('click',()=>{
  const d=definitions[btn.dataset.flow];if(!d)return;
  buttons.forEach(b=>{let selected=b===btn;b.classList.toggle('active',selected);b.setAttribute('aria-selected',String(selected))});
  canvas.innerHTML=d.labels.map((label,i)=>'<div class="nx-flow-node"><span>0'+(i+1)+' / '+['ORIGEN','PROCESO','RESULTADO'][i]+'</span><strong>'+label+'</strong></div>').join('<div class="nx-flow-join" aria-hidden="true">→</div>');
  line.textContent=d.result;
 }))}
})();
