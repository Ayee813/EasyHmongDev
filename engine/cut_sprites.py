import cv2,numpy as np,os,sys,json
SHEET=sys.argv[1] if len(sys.argv)>1 else 'sheet.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'sprites'
# name: (x0,y0,x1,y1) on the 1254x1254 character sheet (labels excluded)
BOX={
 'front':(14,85,176,462),'side':(170,85,303,462),'back':(307,83,464,462),'three_quarter':(464,81,615,462),
 'face_happy':(630,88,778,252),'face_bigsmile':(783,86,931,252),'face_laughing':(932,84,1086,252),'face_wink':(1086,84,1245,252),
 'face_surprised':(630,299,779,464),'face_thinking':(788,301,934,464),'face_sad':(941,300,1086,464),'face_angry':(1090,300,1245,464),
 'wave':(20,575,192,854),'thumbs_up':(201,576,352,854),'pointing':(360,551,535,856),'jump':(540,551,724,856),
 'sit':(722,604,884,852),'working':(894,609,1086,855),'walk':(1079,566,1240,856),
 'laptop':(17,963,181,1190),'reading':(180,966,326,1190),'code':(328,940,505,1190),'coffee':(508,940,658,1190),'idea':(660,925,806,1190),'celebrate':(806,937,982,1190),
}
os.makedirs(OUT,exist_ok=True)
im=cv2.imread(SHEET);H,W=im.shape[:2]
patch=np.concatenate([im[5:30,5:30].reshape(-1,3),im[5:30,W-30:W-5].reshape(-1,3),im[H-30:H-5,5:30].reshape(-1,3)])
paper=np.median(patch,axis=0)
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
    n2,l2,st,_=cv2.connectedComponentsWithStats(cv2.dilate(fg,k))
    keep=np.zeros_like(fg)
    for i in range(1,n2):
        if st[i,4]>=60: keep[l2==i]=1
    fg=(keep&(cv2.dilate(fg,k)>0)).astype(np.uint8)
    a=cv2.erode(fg,np.ones((3,3),np.uint8)).astype(np.float32)
    a=cv2.GaussianBlur(a,(0,0),0.8)
    a=np.clip((a-0.15)/0.7,0,1)
    ys,xs=np.where(a>0.05)
    if len(xs)==0: continue
    bx0,bx1,by0,by1=max(xs.min()-3,0),min(xs.max()+4,a.shape[1]),max(ys.min()-3,0),min(ys.max()+4,a.shape[0])
    rgba=np.dstack([c,(a*255).astype(np.uint8)])[by0:by1,bx0:bx1]
    # 2x Lanczos upscale + light sharpen so it holds up at video size
    up=cv2.resize(rgba,None,fx=2,fy=2,interpolation=cv2.INTER_LANCZOS4)
    bgr=up[...,:3].astype(np.float32);bl=cv2.GaussianBlur(bgr,(0,0),1.4)
    bgr=np.clip(bgr+0.6*(bgr-bl),0,255)
    up=np.dstack([bgr.astype(np.uint8),up[...,3]])
    cv2.imwrite(f'{OUT}/{name}.png',up)
    meta[name]={'w':int(up.shape[1]),'h':int(up.shape[0])}
json.dump(meta,open(f'{OUT}/meta.json','w'));open(f'{OUT}/meta.js','w').write('Object.assign(SPR,'+json.dumps(meta)+');')
print(len(meta),'sprites')
