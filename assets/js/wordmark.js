/* NICHO wordmark: a real beveled, extruded mesh rendered with WebGL. No font file is delivered. */
(()=>{'use strict';const canvas=document.getElementById('wordmark-canvas');const box=canvas?.parentElement;const mesh=window.NICHO_WORDMARK;if(!canvas||!mesh)return;
let enabled=window.NICHO_APP?.motion()??!matchMedia('(prefers-reduced-motion: reduce)').matches;let visible=true,frame=0,last=0,tx=0,ty=0,mx=0,my=0,time=0;
let gl;try{gl=canvas.getContext('webgl',{alpha:true,antialias:true,powerPreference:'low-power',preserveDrawingBuffer:false})}catch{return}if(!gl)return;
const vert=`attribute vec3 aP;attribute vec3 aN;uniform vec2 uTilt;uniform float uScale;uniform float uAspect;varying vec3 vP;varying vec3 vN;
vec3 turn(vec3 p){float x=uTilt.y,y=uTilt.x;vec3 q=vec3(p.x,p.y*cos(x)-p.z*sin(x),p.y*sin(x)+p.z*cos(x));return vec3(q.x*cos(y)+q.z*sin(y),q.y,-q.x*sin(y)+q.z*cos(y));}
void main(){vec3 p=turn(aP);vP=p;vN=turn(aN);float perspective=1.0-p.z*.13;gl_Position=vec4(p.x*uScale/perspective,p.y*uScale*uAspect/perspective,-p.z*.5,1.0);}`;
const frag=`precision mediump float;varying vec3 vP;varying vec3 vN;uniform float uTime;
void main(){vec3 N=normalize(vN);vec3 V=normalize(vec3(0.,0.,5.)-vP);if(N.z>.83){N=normalize(N+vec3(sin(vP.x*2.1)*.035,vP.y*.15,0.));}vec3 R=reflect(-V,N);
float a=sin(uTime*.22)*.15;float box1=exp(-pow((R.y-.35-a)/.12,2.));float box2=exp(-pow((R.y+.44+a*.5)/.07,2.));float tall=exp(-pow((R.x-.5)/.11,2.));float gradient=smoothstep(-.85,.65,R.y);
float fresnel=pow(1.-max(0.,dot(N,V)),3.8);float light=.065+gradient*.60+box1*2.15+box2*1.25+tall*.7+fresnel*.52;
vec3 color=vec3(.90,.95,.94)*light;float edge=pow(max(0.,dot(N,normalize(vec3(-.4,.8,1.)))),24.);color+=vec3(.88,.93,1.)*edge*.5;
color=color/(color+.62);color=pow(color,vec3(.85));gl_FragColor=vec4(color,1.);}`;
function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error('shader');return s}
let program;try{program=gl.createProgram();gl.attachShader(program,shader(gl.VERTEX_SHADER,vert));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,frag));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))return}catch{return}
gl.useProgram(program);
function decode(b64,scale){const s=atob(b64),bytes=new Uint8Array(s.length);for(let i=0;i<s.length;i++)bytes[i]=s.charCodeAt(i);return Float32Array.from(new Int16Array(bytes.buffer),n=>n/scale)}
function bind(name,data){const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,data,gl.STATIC_DRAW);const loc=gl.getAttribLocation(program,name);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,3,gl.FLOAT,false,0,0)}
bind('aP',decode(mesh.position,10000));bind('aN',decode(mesh.normal,32767));
const tilt=gl.getUniformLocation(program,'uTilt'),scale=gl.getUniformLocation(program,'uScale'),aspect=gl.getUniformLocation(program,'uAspect'),clock=gl.getUniformLocation(program,'uTime');
gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);gl.clearColor(0,0,0,0);
function size(){const rect=box.getBoundingClientRect();const dpr=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.max(1,Math.round(rect.width*dpr));canvas.height=Math.max(1,Math.round(rect.height*dpr));gl.viewport(0,0,canvas.width,canvas.height);draw(0)}
function draw(ts){if(gl.isContextLost())return;if(ts){const dt=Math.min(50,ts-(last||ts));time+=dt*.001;last=ts}mx+=(tx-mx)*.08;my+=(ty-my)*.08;gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);const ar=canvas.width/canvas.height;const sc=Math.min(1.86/mesh.width,1.5/(mesh.height*ar));gl.uniform1f(scale,sc);gl.uniform1f(aspect,ar);gl.uniform2f(tilt,-.16+mx+.025*Math.sin(time*.2),.14+my);gl.uniform1f(clock,time);gl.drawArrays(gl.TRIANGLES,0,mesh.count);box.dataset.ready='true';}
function tick(ts){frame=0;if(!enabled||!visible||document.hidden)return;draw(ts);frame=requestAnimationFrame(tick)}
function start(){if(!frame&&enabled&&visible&&!document.hidden)frame=requestAnimationFrame(tick)}
function stop(){cancelAnimationFrame(frame);frame=0;last=0}
box.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||!enabled)return;const r=box.getBoundingClientRect();tx=((e.clientX-r.left)/r.width-.5)*.15;ty=((e.clientY-r.top)/r.height-.5)*.12},{passive:true});box.addEventListener('pointerleave',()=>{tx=0;ty=0});
if('ResizeObserver'in window)new ResizeObserver(size).observe(box);else addEventListener('resize',size,{passive:true});
if('IntersectionObserver'in window)new IntersectionObserver(es=>{visible=es[0].isIntersecting;if(visible)start();else stop()},{threshold:0}).observe(box);
document.addEventListener('visibilitychange',()=>document.hidden?stop():start());
document.addEventListener('nicho:motion',e=>{enabled=e.detail.enabled;if(enabled)start();else{stop();draw(0)}});
canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();stop();box.dataset.ready='false'});canvas.addEventListener('webglcontextrestored',()=>location.reload());
size();const fallback=document.getElementById('wordmark-video');if(fallback){fallback.pause();fallback.dataset.disabled='true';fallback.hidden=true;}if(enabled)start();window.NICHO_WORDMARK_RENDER={draw:()=>draw(0),context:gl,meshVertices:mesh.count};
})();
