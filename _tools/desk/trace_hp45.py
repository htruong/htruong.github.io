# Traces the HP-45 from the straightened photo (hp45-cut.png, 810 x 1470):
# every key's box comes from the photo's grid, every colour is sampled from it.
from PIL import Image
import numpy as np, sys
a=np.asarray(Image.open('hp45-cut.png').convert('RGB')).astype(int)
def sample(x,y,w,h):
    # median of the key's top face, ignoring its legend (the extreme pixels)
    p=a[y+6:y+int(h*0.75), x+8:x+w-8].reshape(-1,3); l=p.mean(1)
    p=p[(l>np.percentile(l,20))&(l<np.percentile(l,70))]
    return '#%02x%02x%02x'%tuple(np.median(p,0).astype(int))
def hexc(c): return '#%02x%02x%02x'%tuple(c)
X5=[96,229,360,491,624]; W5=93
rows5=[371,494,619]; H5=73
keys=[]  # (x,y,w,h,label,label colour)
r1=['¹/x','ln','eˣ','FIX','']; r2=['x²','→P','SIN','COS','TAN']; r3=['x⇄y','R↓','STO','RCL','%']
for r,(y,labels) in enumerate(zip(rows5,[r1,r2,r3])):
    for x,t in zip(X5,labels): keys.append((x,y,W5,H5,t))
keys.append((96,743,225,72,'ENTER ↑')); keys+= [(x,743,93,72,t) for x,t in zip(X5[2:],['CHS','EEX','CLx'])]
DX=[231,419,605]; DW=108
for y,ops,digs in zip([864,987,1111,1230],['−','+','×','÷'],[['7','8','9'],['4','5','6'],['1','2','3'],['0','·','Σ+']]):
    keys.append((96,y,74,71,ops)); keys+=[(x,y,DW,75,t) for x,t in zip(DX,digs)]
gold=[ # (x centre, baseline y, text, anchor)
 *[(x+W5/2,360,t,'middle') for x,t in zip(X5,['yˣ','log','10ˣ','SCI'])],
 *[(x+W5/2,483,t,'middle') for x,t in zip(X5,['√x','→R','SIN⁻¹','COS⁻¹','TAN⁻¹'])],
 *[(x+W5/2,608,t,'middle') for x,t in zip(X5,['n!','x̄, s','→D.MS','D.MS→','Δ%'])],
 (321-10,732,'DEG','end'), *[(x+W5/2,732,t,'middle') for x,t in zip(X5[2:],['RAD','GRD','CLEAR'])],
 *[(x+DW/2,853,t,'middle') for x,t in zip(DX,['cm/in','kg/lb','ltr/gal'])],
 *[(x+DW/2,1219,t,'middle') for x,t in zip(DX,['LAST x','π','Σ−'])],
]
GOLD=sample(624,371,94,74) if False else '#d6a43a'
body='#111111'; panel=hexc(np.median(a[560:600,40:90].reshape(-1,3),0).astype(int))
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 810 1470" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">',
 '<defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2a2a"/><stop offset=".08" stop-color="#151515"/><stop offset="1" stop-color="#0b0b0b"/></linearGradient>',
 '<linearGradient id="d" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a0507"/><stop offset=".5" stop-color="#5a080c"/><stop offset="1" stop-color="#2a0305"/></linearGradient>',
 '<linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f4ee"/><stop offset="1" stop-color="#8a8a86"/></linearGradient></defs>',
 f'<rect width="810" height="1470" rx="52" fill="url(#b)"/>',
 # display window and the chrome strip under it
 '<rect x="70" y="30" width="680" height="170" rx="6" fill="#120203"/>',
 '<rect x="88" y="52" width="644" height="128" rx="3" fill="url(#d)"/>',
 '<rect x="62" y="204" width="696" height="14" rx="3" fill="url(#c)"/>',
 # the key panel, with its thin bright edge
 f'<rect x="47" y="222" width="716" height="1212" rx="10" fill="{panel}" stroke="#8d8b86" stroke-width="4"/>',
 # OFF/ON switch
 '<text x="112" y="318" font-size="22" fill="#e9e6dc" text-anchor="middle">OFF</text><text x="292" y="318" font-size="22" fill="#e9e6dc" text-anchor="middle">ON</text>',
 '<rect x="150" y="292" width="110" height="34" rx="4" fill="#0d0d0d"/><rect x="172" y="286" width="52" height="46" rx="4" fill="#2b2b2b"/>',
]
for (x,y,w,h,t) in keys:
    c=sample(x,y,w,h); lum=np.mean([int(c[i:i+2],16) for i in (1,3,5)])
    fg='#111' if lum>110 else '#f2f0e8'
    # the skirt (front face, darker) and the top face
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#000" fill-opacity=".55"/>')
    out.append(f'<rect x="{x+3}" y="{y}" width="{w-6}" height="{h-12}" rx="6" fill="{c}"/>')
    if t:
        fs=44 if t in '−+×÷' else 34 if len(t)<=2 and t not in ('ln',) else 28
        out.append(f'<text x="{x+w/2}" y="{y+(h-12)/2+fs*0.36}" font-size="{fs}" font-weight="600" fill="{fg}" text-anchor="middle">{t}</text>')
for (x,y,t,anc) in gold:
    out.append(f'<text x="{x}" y="{y}" font-size="25" font-weight="600" fill="{GOLD}" text-anchor="{anc}">{t}</text>')
# nameplate: logo, maker and model, and the chrome rim at the foot
out+=['<rect x="76" y="1356" width="658" height="62" rx="3" fill="none" stroke="#8d8b86" stroke-width="3"/>','<rect x="80" y="1360" width="650" height="54" fill="#0c0c10"/>',
 '<rect x="92" y="1366" width="90" height="42" fill="#3baee6"/><text x="137" y="1396" font-size="26" font-style="italic" font-weight="700" fill="#0c0c10" text-anchor="middle">hp</text>',
 '<text x="420" y="1398" font-size="30" letter-spacing="6" fill="#ecebe6" text-anchor="middle">HEWLETT·PACKARD</text><text x="690" y="1398" font-size="30" fill="#ecebe6" text-anchor="middle">45</text>',
 '</svg>']
open(sys.argv[1],'w').write('\n'.join(out))
