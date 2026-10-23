# Sally Ride's Post slide rule, traced: the body, brackets, cursor and the row of
# each scale are measured from the Smithsonian photo; the ticks are computed from
# each scale's own formula, so they fall where the real ones do.
import math, sys
X0, L = 181, 1342            # left index and the length of the C/D scales
RED, BLK = '#b3352b', '#232323'
out=[]
def T(x,y,s,size=11,col=BLK,anchor='middle',weight=400):
    out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>')
def ticks(pos, y, dirn, marks, col):
    # marks: list of (value, length)
    d=[]
    for v,l in marks:
        p=pos(v)
        if p is None or p< -0.0005 or p>1.0005: continue
        x=X0+p*L; d.append(f'M{x:.2f} {y}v{dirn*l}')
    out.append(f'<path d="{" ".join(d)}" stroke="{col}" stroke-width=".9" fill="none"/>')
def labels(pos, y, items, col, size=11):
    for v,s in items:
        p=pos(v)
        if p is None or p<-0.001 or p>1.001: continue
        T(X0+p*L, y, s, size, col)
def frange(a,b,step):
    n=int(round((b-a)/step)); return [a+i*step for i in range(n+1)]
def cd_marks():
    m=[]
    for v in frange(1,2,0.01): m.append((v, 7 if abs(v*10-round(v*10))<1e-6 else 5.5 if abs(v*20-round(v*20))<1e-6 else 3.5))
    for v in frange(2,4,0.02): m.append((v, 7 if abs(v*10-round(v*10))<1e-6 else 3.5))
    for v in frange(4,10,0.05): m.append((v, 7 if abs(v*10-round(v*10))<1e-6 else 3.5))
    for v in range(1,11): m.append((v,10))
    return m
ints=[(v,str(v if v<10 else 1)) for v in range(1,11)]
lg=math.log10; LPI=lg(math.pi)
C=lambda v: lg(v)
CI=lambda v: 1-lg(v)
CF=lambda v: lg(v)-LPI if v>=math.pi else lg(v)+1-LPI
CIF=lambda v: (1-lg(v)-LPI)%1.0
def LL(k, neg=False):
    # LL3: k=1, LL2: k=10, LL1: k=100; the reciprocal scales take -ln
    def f(v):
        t=(-math.log(v) if neg else math.log(v))*k
        return lg(t) if t>0 else None
    return f
def ll_marks(vals, pos):
    # between labelled values, as many even subdivisions as fit at about 7 px apart (up to 20)
    m=[(v,9) for v in vals]
    for a,b in zip(vals,vals[1:]):
        pa,pb=pos(a),pos(b)
        if pa is None or pb is None: continue
        n=max(2,min(20,int(abs(pb-pa)*L/7)))
        n=next((k for k in (20,10,5,4,2) if k<=n),2)
        for i in range(1,n): m.append((a+(b-a)*i/n, 6 if i*2==n else 4))
    return m
W, H = 1709, 237
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -16 {W} {H+32}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">')
out.append('<defs><linearGradient id="m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e6e6e2"/><stop offset=".5" stop-color="#a9a9a4"/><stop offset="1" stop-color="#d4d4cf"/></linearGradient></defs>')
# body: upper stator, slide, lower stator
out.append(f'<rect x="88" y="0" width="{1621-88}" height="{H}" fill="#f4f3ee"/>')
out.append(f'<rect x="88" y="75" width="{1621-88}" height="81" fill="#efeee8"/>')
out.append(f'<path d="M88 75H1621M88 156H1621" stroke="#b9b8b2" stroke-width="1.5"/>')
# upper stator: LL/1, LL/2, LL/3 (red)
ll1n=[.99,.985,.98,.97,.96,.95,.94,.93,.92,.91,.905]
ll2n=[.905,.90,.85,.80,.75,.70,.65,.60,.55,.50,.45,.40,1/math.e]
ll3n=[1/math.e,.35,.30,.25,.20,.15,.10,.05,.03,.02,.01,.005,.002,.001,.0005,.0002,.0001,0.0000454]
ticks(LL(100,True),21,1,ll_marks(ll1n,LL(100,True)),RED); labels(LL(100,True),17,[(v,('.%g'%v)[1:] if v<1 else '%g'%v) for v in ll1n[:-1]],RED,10.5)
ticks(LL(10,True),40,1,ll_marks(ll2n,LL(10,True)),RED); labels(LL(10,True),37,[(v,('%.2f'%v)[1:]) for v in ll2n[1:-1]],RED,10.5)
ticks(LL(1,True),75,-1,ll_marks(ll3n[1:-1],LL(1,True)),RED); labels(LL(1,True),60,[(v,('%g'%v)[1:] if v>=0.001 else ('%g'%v)) for v in ll3n[1:-1]],RED,10.5)
for y,s in [(25,'LL/1'),(45,'LL/2'),(66,'LL/3')]: T(150,y,s,15,RED,'end')
T(112,48,'e⁻ˣ',13,RED,'end')
# slide: CF, CIF (red), CI (red), C
ticks(CF,76,1,cd_marks(),BLK); labels(CF,95,[(v,s) for v,s in ints]+[(math.pi,'π')],BLK)
ticks(CIF,96,1,cd_marks(),RED); labels(CIF,110,ints,RED,10)
ticks(CI,122,1,cd_marks(),RED); labels(CI,120,ints,RED,10)
ticks(C,156,-1,cd_marks(),BLK); labels(C,144,ints+[(math.pi,'π')],BLK)
for y,s,c in [(92,'CF',BLK),(111,'CIF',RED),(131,'CI',RED),(150,'C',BLK)]: T(150,y,s,15,c,'end')
# lower stator: D, LL3, LL2, LL1
ticks(C,156,1,cd_marks(),BLK); labels(C,177,ints+[(math.pi,'π')],BLK)
ll3=[math.e,3,4,5,6,7,8,9,10,15,20,30,40,50,100,200,500,1000,2000,5000,10000,20000]
ll2=[1.105,1.11,1.15,1.2,1.25,1.3,1.35,1.4,1.5,1.6,1.7,1.8,1.9,2,2.5,math.e]
ll1=[1.01005,1.015,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09,1.10,1.105]
ticks(LL(1),180,1,ll_marks(ll3,LL(1)),BLK); labels(LL(1),197,[(v,'e' if v==math.e else '%g'%v) for v in ll3],BLK,10.5)
ticks(LL(10),199,1,ll_marks(ll2,LL(10)),BLK); labels(LL(10),215,[(v,'e' if v==math.e else '%g'%v) for v in ll2[1:]],BLK,10.5)
ticks(LL(100),218,1,ll_marks(ll1,LL(100)),BLK); labels(LL(100),234,[(1.01,'1.01')]+[(v,'%g'%v) for v in ll1[1:-1]],BLK,10.5)
for y,s in [(170,'D'),(192,'LL3'),(211,'LL2'),(230,'LL1')]: T(150,y,s,15,BLK,'end')
T(52,168,'X',14,BLK); T(112,214,'eˣ',13,BLK,'end')
# right end: ranges, maker, number
for y,s in [(25,'−0.01←−0.1'),(43,'−0.1←−1.0'),(61,'−1.0←−10.0')]: T(1550,y,s,12,RED,'start')
for y,s in [(200,'1.0 → 10.0'),(218,'0.1 → 1.0'),(236,'0.01 → 0.1')]: T(1550,y,s,12,BLK,'start')
out.append('<ellipse cx="1580" cy="115" rx="27" ry="17" fill="none" stroke="#b3352b" stroke-width="2.2"/>'); T(1580,121,'POST',16,RED,weight=700)
T(1580,148,'625 372',11,'#888884'); T(1540,100,'3.1',11,RED,'start')
# end brackets, with their rivets
for x in (0,1621):
    out.append(f'<rect x="{x}" y="-2" width="88" height="{H+4}" rx="3" fill="url(#m)" stroke="#8d8d88"/>')
    for ry in (18,H-18): out.append(f'<circle cx="{x+44}" cy="{ry}" r="6" fill="#c9c9c4" stroke="#7d7d78"/>')
out.append(f'<rect x="-6" y="80" width="30" height="72" rx="3" fill="#f1f0ea" stroke="#c9c8c2"/><rect x="{W-24}" y="80" width="30" height="72" rx="3" fill="#f1f0ea" stroke="#c9c8c2"/>')
# the cursor: glass in a metal frame, with its red hairline
cx0,cx1=1021,1191
out.append(f'<rect x="{cx0}" y="-14" width="{cx1-cx0}" height="{H+28}" rx="6" fill="#ffffff" fill-opacity=".18" stroke="#9a9a95" stroke-width="5"/>')
out.append(f'<rect x="{cx0-4}" y="-14" width="{cx1-cx0+8}" height="16" rx="5" fill="url(#m)"/><rect x="{cx0-4}" y="{H-2}" width="{cx1-cx0+8}" height="16" rx="5" fill="url(#m)"/>')
out.append(f'<path d="M{(cx0+cx1)/2} 4V{H-4}" stroke="#c33a2c" stroke-width="1.2"/>')
out.append('</svg>')
open(sys.argv[1],'w').write('\n'.join(out))
