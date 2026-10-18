const HC={red:'#e0302b'};
/* ---------- Hmong spiral motif (hand-drawn, original) ---------- */
function spiral(r,turns=2.6,flip=1){let d='';const n=64;for(let i=0;i<=n;i++){const a=i/n*turns*6.2832,rr=r*i/n;d+=(i?' L':'M')+(flip*rr*Math.cos(a)).toFixed(1)+','+(rr*Math.sin(a)).toFixed(1)}return d}
// ring of n spirals around (0,0) radius R; alternating red/blue/yellow. p=draw-on progress 0..1
function spiralRing(n,R,p=1,cols=[C.red,C.blu,C.yel]){
 const r=R*Math.sin(Math.PI/n)*.92;let s='';
 for(let i=0;i<n;i++){const a=i/n*6.2832-1.5708;const x=R*Math.cos(a),y=R*Math.sin(a);
  s+=`<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(a*57.3).toFixed(0)})">`+ln(spiral(r,2.4,i%2?-1:1),cols[i%cols.length],r*.2,P(p,i/n*.6,i/n*.6+.4))+'</g>'}
 return s;
}
// embroidery band (red cloth strip) local coords, top-left at 0,0
function band(w,h=90){
 let s=zig(R(0,0,w,h),0,0,w,h,HC.red,1,{sw:14})+ln(`M0,0 L${w},0 M0,${h} L${w},${h}`,C.ink,6);
 const cols=[C.yel,C.grn,C.blu,C.pink];
 for(let x=h/2,i=0;x<w;x+=h*.9,i++){const k=h*.26,y=h/2,c=cols[i%4];
  s+=`<path d="M${x},${y-k} L${x+k},${y} L${x},${y+k} L${x-k},${y} Z" fill="${c}" stroke="${C.ink}" stroke-width="4" stroke-linejoin="round"/>`}
 return s;
}
