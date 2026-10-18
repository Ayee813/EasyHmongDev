import os,re,json,asyncio,random,math,sys
from playwright.async_api import async_playwright
D='node_modules/@tabler/icons/icons/outline/'
CAT={ # category: (light,strong, [(file,label)])
 'Hardware':('#CFE8F7','#3A9AD9',[('device-desktop','Computer'),('device-laptop','Laptop'),('mouse','Mouse'),('keyboard','Keyboard'),('device-tv','Monitor'),('headphones','Headphones'),('headset','Headset'),('camera','Webcam'),('microphone','Mic'),('device-speaker','Speaker'),('cpu','CPU'),('memory','RAM'),('printer','Printer'),('usb','USB'),('server-2','Hard Drive'),('circuit-resistor','Circuit')]),
 'Mobile':('#FBD3E1','#F0709E',[('device-mobile','Phone'),('device-tablet','Tablet'),('device-watch','Watch'),('battery-charging','Charging'),('plug','Charger'),('bluetooth','Bluetooth'),('cast','Cast'),('qrcode','QR Code'),('device-gamepad-2','Game'),('augmented-reality','VR'),('drone','Drone'),('video','Video')]),
 'Network':('#D5EFBF','#5FAE2E',[('wifi','Wi-Fi'),('router','Router'),('world','Internet'),('antenna-bars-5','Signal'),('satellite','Satellite'),('network','Network'),('topology-star-3','LAN'),('world-www','Domain'),('link','Link'),('cast','Share Screen'),('antenna','Tower'),('plug-connected','Connected')]),
 'Server & Cloud':('#FFE9A3','#F7BE1F',[('server','Server'),('database','Database'),('cloud','Cloud'),('cloud-upload','Upload'),('cloud-download','Download'),('api','API'),('browser','Browser'),('app-window','Window'),('layout-dashboard','Dashboard'),('git-branch','Git'),('serverless','Serverless'),('error-404','404')]),
 'Code':('#F6B2A4','#E04B35',[('code','Code'),('braces','Braces'),('terminal-2','Terminal'),('bug','Bug'),('bug-off','Fix Bug'),('binary','Binary'),('number-123','Numbers'),('refresh','Update'),('player-play','Run'),('folder','Folder'),('click','Click'),('cursor-text','Cursor')]),
 'AI & Apps':('#E5D4F4','#8E55C8',[('robot','Robot'),('brain','AI Brain'),('message-circle','Chat'),('sparkles','Magic'),('settings','Settings'),('apps','Apps'),('chart-bar','Chart'),('chart-line','Growth'),('loader-2','Loading'),('bulb','Idea'),('rocket','Launch'),('microphone-2','Voice')]),
 'Security':('#FFD9A8','#FF9F1C',[('lock','Locked'),('lock-open','Unlocked'),('shield-check','Secure'),('shield-lock','Protected'),('fingerprint','Fingerprint'),('key','Key'),('mask','Hacker'),('virus','Virus'),('firewall-check','Firewall'),('alert-triangle','Warning'),('scan-eye','Scan'),('eye-off','Private')]),
 'Social':('#F6B2A4','#E04B35',[('mail','Email'),('bell','Alert'),('heart','Like'),('share','Share'),('hash','Hashtag'),('trophy','Trophy'),('at','Mention'),('user-circle','Profile'),('clock','Time'),('hourglass','Timer'),('ghost-2','Ghost'),('bolt','Fast')]),
}
import sys
EXTRA=[a for a in sys.argv[1:] if ':' in a]   # python3 build_icons.py coffee:Coffee:Social  -> render ONLY these extra icons (file:Label:Category)
if EXTRA:
    CAT={c:(lt,st,[]) for c,(lt,st,_) in CAT.items()}
    for a in EXTRA:
        f,lab,c=a.split(':');CAT[c][2].append((f,lab))
seen=set();items=[]
for cat,(lt,st,L) in CAT.items():
    for f,lab in L:
        if not os.path.exists(D+f+'.svg'):print('missing',f);continue
        k=f+'|'+lab
        if f in seen:continue
        seen.add(f);items.append((cat,lt,st,f,lab))
print(len(items),'icons')
def blob(seed,r=215):
    rnd=random.Random(seed);n=14;pts=[]
    for i in range(n):
        a=i/n*math.tau;rr=r*(0.9+rnd.random()*0.16);pts.append((256+rr*math.cos(a),256+rr*math.sin(a)))
    d=''
    for i in range(n):
        p0=pts[i];p1=pts[(i+1)%n];mx,my=(p0[0]+p1[0])/2,(p0[1]+p1[1])/2
        d+=(f'M{mx:.1f},{my:.1f} ' if i==0 else '')+f'Q{p1[0]:.1f},{p1[1]:.1f} '+f'{((p1[0]+pts[(i+2)%n][0])/2):.1f},{((p1[1]+pts[(i+2)%n][1])/2):.1f} '
    return d+'Z'
def inner(svg):
    m=re.search(r'<svg[^>]*>(.*)</svg>',svg,re.S);s=m.group(1)
    return re.sub(r'<path stroke="none" d="M0 0h24v24H0z" fill="none"\s*/>','',s)
HTML='''<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}</style></head><body>
<svg id="s" xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><defs>
<filter id="crayon" filterUnits="userSpaceOnUse" x="0" y="0" width="512" height="512" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="4" result="warp"/>
<feDisplacementMap in="SourceGraphic" in2="warp" scale="9" xChannelSelector="R" yChannelSelector="G" result="wob"/>
<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="9" result="grain"/>
<feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  3.2 0 0 0 -0.75" result="holes"/>
<feComposite in="wob" in2="holes" operator="in"/></filter>
<pattern id="pat" width="15" height="15" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect id="pl" width="15" height="15"/><rect id="ps" width="9" height="15"/></pattern>
</defs><g id="g" filter="url(#crayon)" stroke-linejoin="round" stroke-linecap="round"></g></svg></body></html>'''
async def main():
    os.makedirs('png',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--disable-gpu'])
        pg=await b.new_page(viewport={'width':512,'height':512})
        await pg.set_content(HTML)
        for i,(cat,lt,st,f,lab) in enumerate(items):
            ic=inner(open(D+f+'.svg').read())
            ink='#4A3A32'
            g=f'''<path d="{blob(i)}" fill="url(#pat)" />
<g transform="translate(70 70) scale(15)" fill="none" stroke="{st}" stroke-width="2.1" opacity=".9" transform-origin="0 0"><g transform="translate(.8 .8)">{ic}</g></g>
<g transform="translate(70 70) scale(15)" fill="none" stroke="{ink}" stroke-width="1.9">{ic}</g>'''
            await pg.evaluate('''([g,lt,st])=>{document.getElementById('g').innerHTML=g;document.getElementById('pl').setAttribute('fill',lt);document.getElementById('ps').setAttribute('fill',st)}''',[g,lt,st])
            await pg.screenshot(path=f'png/{f}.png',omit_background=True)
        await b.close()
    if not EXTRA: json.dump([{'file':f,'label':lab,'category':cat} for cat,lt,st,f,lab in items],open('icons.json','w'),indent=1)
    names=[e[3] for e in items] if not EXTRA else None
asyncio.run(main())
