import cv2,numpy as np,os,sys,json
SHEET=sys.argv[1] if len(sys.argv)>1 else 'speak.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'speak_sprites'
# name: (x0,y0,x1,y1) on the 1254x1254 character sheet (labels excluded)
BOX={}
Y1=(118,342);Y2=(382,606);XS=[(28,195),(215,380),(400,565),(585,750),(765,925),(945,1105)]
M1=['neutral','open_A','close_M','wide_E','round_O','narrow_FV']
M2=['smile_I','tongue_L_TH','ch_J','sh','w_Q','rest']
MW=176  # mouth heads use ONE fixed canvas so the sprites swap without jitter
for n,(x0,x1) in zip(M1,XS):cx=(x0+x1)//2;BOX['mouth_'+n]=(cx-MW//2,Y1[0],cx+MW//2,Y1[1])
for n,(x0,x1) in zip(M2,XS):cx=(x0+x1)//2;BOX['mouth_'+n]=(cx-MW//2,Y2[0],cx+MW//2,Y2[1])
# full speaking poses (y offset 680 from the inspected strip); speech bubbles are painted over with paper colour first
POSE={'say_greeting':((25,722,195,922),[(128,690,232,790)]),
 'say_introduce':((232,752,372,922),[(240,690,425,762),(342,762,425,792)]),
 'say_encourage':((412,745,565,922),[(526,690,600,790),(500,690,530,776)]),
 'say_list':((612,736,775,922),[(738,680,825,806)]),
 'say_finish':((820,742,972,922),[(922,690,1035,792)]),
 'say_goodbye':((1045,735,1222,922),[(1170,690,1297,792)]),
 'say_thanks':((1310,746,1432,922),[(1405,698,1510,778)])}
for n,(b,_) in POSE.items():BOX[n]=b
os.makedirs(OUT,exist_ok=True)
im=cv2.imread(SHEET);H,W=im.shape[:2]

patch=np.concatenate([im[5:30,5:30].reshape(-1,3),im[5:30,W-30:W-5].reshape(-1,3),im[H-30:H-5,5:30].reshape(-1,3)])
paper=np.median(patch,axis=0)
# erase speech bubbles, but PROTECT thick dark masses (hair/clothes) so hair tips are never clipped:
# thin bubble lines/text vanish under a 7x7 opening, thick hair survives it and is dilated into a protect zone
dist=np.linalg.norm(im.astype(np.float32)-paper,axis=2)
thick=cv2.morphologyEx((dist>45).astype(np.uint8),cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
protect=cv2.dilate(thick,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))>0
for _n,(_b,bbs) in POSE.items():
    for bb in bbs:
        reg=im[bb[1]:bb[3],bb[0]:bb[2]];m=~protect[bb[1]:bb[3],bb[0]:bb[2]]
        reg[m]=paper.astype(np.uint8)
meta={}
for name,(x0,y0,x1,y1) in BOX.items():
    c=im[y0:y1,x0:x1]
    d=np.linalg.norm(c.astype(np.float32)-paper,axis=2)
    pl=(d<40).astype(np.uint8)
    n,lab=cv2.connectedComponents(pl)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(border)).astype(np.uint8)
    # keep only foreground connected to the main sprite (drop stray specks)
    fg=1-bg
    k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    fg=cv2.morphologyEx(fg,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
    TOPCLEAN={'say_list':.26,'say_introduce':.12}   # thin bubble remnants near the top: open only that band so hair elsewhere is untouched
    if name in TOPCLEAN:
        r=int(fg.shape[0]*TOPCLEAN[name]);op=cv2.morphologyEx(fg,cv2.MORPH_OPEN,np.ones((6,6),np.uint8));fg[:r]=op[:r]
    n2,l2,st,_=cv2.connectedComponentsWithStats(cv2.dilate(fg,k))
    keep=np.zeros_like(fg)
    big=max(st[1:,4]) if n2>1 else 0
    thr=(big if name.startswith('say_') else 60)
    for i in range(1,n2):
        if st[i,4]>=thr: keep[l2==i]=1
    fg=(keep&(cv2.dilate(fg,k)>0)).astype(np.uint8)
    a=cv2.erode(fg,np.ones((3,3),np.uint8)).astype(np.float32)
    a=cv2.GaussianBlur(a,(0,0),0.8)
    a=np.clip((a-0.15)/0.7,0,1)
    ys,xs=np.where(a>0.05)
    if len(xs)==0: continue
    bx0,bx1,by0,by1=max(xs.min()-3,0),min(xs.max()+4,a.shape[1]),max(ys.min()-3,0),min(ys.max()+4,a.shape[0])
    rgba=np.dstack([c,(a*255).astype(np.uint8)])
    if name.startswith('mouth_'):
        if name!='mouth_neutral' and 'ref' in globals():
            sh,_=cv2.phaseCorrelate(ref,(a*255).astype(np.float32)*1.0);M=np.float32([[1,0,-sh[0]],[0,1,-sh[1]]])
            rgba=cv2.warpAffine(rgba,M,(rgba.shape[1],rgba.shape[0]),flags=cv2.INTER_LINEAR,borderValue=(0,0,0,0))
        elif name=='mouth_neutral': ref=(a*255).astype(np.float32)
    else: rgba=rgba[by0:by1,bx0:bx1]
    # 2x Lanczos upscale + light sharpen so it holds up at video size
    up=cv2.resize(rgba,None,fx=2,fy=2,interpolation=cv2.INTER_LANCZOS4)
    bgr=up[...,:3].astype(np.float32);bl=cv2.GaussianBlur(bgr,(0,0),1.4)
    bgr=np.clip(bgr+0.6*(bgr-bl),0,255)
    up=np.dstack([bgr.astype(np.uint8),up[...,3]])
    cv2.imwrite(f'{OUT}/{name}.png',up)
    meta[name]={'w':int(up.shape[1]),'h':int(up.shape[0])}
json.dump(meta,open(f'{OUT}/meta.json','w'));open(f'{OUT}/meta.js','w').write('Object.assign(SPR,'+json.dumps(meta)+');')
print(len(meta),'speak_sprites')
