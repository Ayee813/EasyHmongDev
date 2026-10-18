/* ---------- sprite hero: the ONE mascot, cut from the character sheet ---------- */
const SPR={};   // name -> {w,h}; filled from sprites/meta.json before rendering
// hero(name,t,{x,y,h,flip,bob,amp,sway,rot,op,pop,ph}) -> string for layer H (no filter: sprites already have crayon texture)
// (x,y) = feet / bottom-centre. h = height in px. pop = t0 -> springy pop-in at time t0.
function hero(name,t,o={}){
 const m=SPR[name];if(!m)return'';
 const h=o.h||620,s=h/m.h,w=m.w*s,ph=o.ph||0;
 const b=o.bob?Math.abs(Math.sin(t*o.bob*Math.PI+ph)):0;               // bounce 0..1
 const idle=Math.sin(t*2.2+ph);                                          // breathing
 let sc=o.pop!=null?pop(t,o.pop,.4):1;
 const sy=sc*(1+.018*idle+(o.bob?-.03*b:0)),sx=sc*(1-.012*idle)*(o.flip?-1:1);
 const rot=(o.rot||0)+(o.sway?Math.sin(t*2.6+ph)*o.sway:0);
 const y=o.y-(o.bob?b*(o.amp||26):0);
 const op=o.op??1;if(sc<=.01||op<=.01)return'';
 return `<g transform="translate(${o.x} ${y}) rotate(${rot}) scale(${sx} ${sy})" opacity="${op}"><image href="sprites/${name}.png" x="${-w/2}" y="${-h}" width="${w}" height="${h}"/></g>`;
}
// circular face badge (reaction inset): hero face sprite clipped to a ring, e.g. faceBadge('face_surprised',t,{x,y,r:150,pop:t0})
function faceBadge(name,t,o={}){
 const m=SPR[name];if(!m)return'';
 const r=o.r||150,k=o.pop!=null?pop(t,o.pop,.35):1;if(k<=.01)return'';
 const id='fb'+(uid++),s=(2.1*r)/Math.min(m.w,m.h*1.15),w=m.w*s,h=m.h*s;
 return `<g transform="translate(${o.x} ${o.y}) scale(${k})"><clipPath id="${id}"><circle r="${r}"/></clipPath><circle r="${r}" fill="${C.paper}"/><g clip-path="url(#${id})"><image href="sprites/${name}.png" x="${-w/2}" y="${-h*.52}" width="${w}" height="${h}"/></g><circle r="${r}" fill="none" stroke="${C.ink}" stroke-width="9"/></g>`;
}
// index.html must include <script src="sprites/meta.js"></script> AFTER the engine script declares SPR (or call loadSprites after Object.assign)
async function loadSprites(){await Promise.all(Object.keys(SPR).map(n=>{const i=new Image();i.src=`sprites/${n}.png`;return i.decode()}))}
