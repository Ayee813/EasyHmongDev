/* ---------- speaking keyframes: lip-sync from the audio envelope ---------- */
// ENV = normalised speech loudness 0..1, 30 samples/s, smoothed (see env.py); a plain array in env.js: const ENV=[...]
const MOUTH={rest:'mouth_rest',neutral:'mouth_neutral',A:'mouth_open_A',M:'mouth_close_M',E:'mouth_wide_E',O:'mouth_round_O',FV:'mouth_narrow_FV',I:'mouth_smile_I',L:'mouth_tongue_L_TH',CH:'mouth_ch_J',SH:'mouth_sh',WQ:'mouth_w_Q'};
const envAt=t=>{if(typeof ENV==='undefined')return 0;const i=t*30,a=Math.floor(i),f=i-a;return (ENV[a]??0)*(1-f)+(ENV[a+1]??0)*f};
const hs=k=>{let x=Math.imul(k+1,2654435761)>>>0;x^=x>>>15;x=Math.imul(x,2246822519)>>>0;return (x>>>8)/16777216};
// which mouth key at time t. ~9 changes/s while speaking; level decides how open; M closes just before a pause.
function mouthKey(t){
 const e=envAt(t);
 if(e<.07)return (envAt(t-.35)<.07&&envAt(t+.35)<.07)?'rest':'neutral';        // silence: rest (long) / neutral (short gap)
 if(envAt(t+.12)<.07)return 'M';                                                  // lips close before a pause
 const k=Math.floor(t*9),pick=(a,j)=>a[Math.floor(hs(j)*a.length)];
 const lvl=envAt((k+.5)/9);
 const pool=lvl>.55?['A','O','E','A','WQ']:lvl>.28?['E','I','L','CH','SH','A','FV']:['I','M','neutral','FV'];
 let m=pick(pool,k);if(m===pick(pool,k-1))m=pool[(pool.indexOf(m)+1)%pool.length];  // never repeat the same mouth twice in a row
 return m;
}
// talking head (bust). o as hero(): {x,y,h,bob,sway,pop,op,flip}. emphasis nudges scale with loudness for a little bounce.
function talkHead(t,o={}){const e=envAt(t);return hero(MOUTH[mouthKey(t)],t,{...o,h:(o.h||620)*(1+.025*e),y:o.y-6*e})}
// full-body speaking pose + loudness bounce (the pose keeps its own open mouth; use talkHead for exact lip-sync)
function talkPose(name,t,o={}){const e=envAt(t);return hero(name,t,{...o,h:(o.h||560)*(1+.02*e),y:o.y-8*e})}
// crayon speech bubble: returns {shape(for layer M), text(for layer T)}; tail='l'|'r' side the tail points to; lines = array of strings
function bubble(lines,x,y,o={}){ // (x,y)=bubble centre
 const fs=o.fs||52,w=Math.max(...lines.map(s=>s.length))*fs*.56+70,h=lines.length*fs*1.18+50,l=o.tail==='r'?1:-1;
 const rr=`M${-w/2+30},${-h/2} H${w/2-30} Q${w/2},${-h/2} ${w/2},${-h/2+30} V${h/2-30} Q${w/2},${h/2} ${w/2-30},${h/2} H${l*(w*.18)+30} L${l*(w*.34)},${h/2+46} L${l*(w*.18)-20},${h/2} H${-w/2+30} Q${-w/2},${h/2} ${-w/2},${h/2-30} V${-h/2+30} Q${-w/2},${-h/2} ${-w/2+30},${-h/2} Z`;
 const k=o.pop!=null?pop(o.t,o.pop,.35):1;
 const shape=G(`<path d="${rr}" fill="${C.paper}" stroke="${C.ink}" stroke-width="7" stroke-linejoin="round"/>`,x,y,k);
 const text=G(lines.map((s,i)=>txt(s,0,(i-(lines.length-1)/2)*fs*1.18+fs*.34,fs,C.ink,'PH')).join(''),x,y,k);
 return {shape,text};
}
