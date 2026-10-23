# An IBM 5081 card, traced from the scan (2230 x 973 px, 300 px to the inch):
# outline and corner cut, the 80 x 10 printed digits, the column numbers and
# the IBM 5081 mark are at the scan's measured positions. Holes are punched in
# IBM 029 Hollerith code, at 0.055 x 0.125 in, and are cut out (a mask), so
# whatever lies under the card shows through them.
import sys, os
W,H=2230,973
COL1,PITCH=70.8,26.31
ROW={12:61,11:136,0:211}; ROW.update({d:211+75.1*d for d in range(1,10)})
HW,HH=16.5,37.5
STOCK,INK,PRINT='#f8f3d8','#6f6a52','#2a2834'
SX=0.56   # the card's digits are tall and narrow: a condensed face, scaled
def holler(ch):
    ch=ch.upper()
    if ch.isdigit(): return [int(ch)]
    if 'A'<=ch<='I': return [12,ord(ch)-64]
    if 'J'<=ch<='R': return [11,ord(ch)-73]
    if 'S'<=ch<='Z': return [0,ord(ch)-81]
    return []
def cx(c): return COL1+PITCH*(c-1)
def xs(vals): return ' '.join(f'{v/SX:.1f}' for v in vals)
def card(label):
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">']
    holes=''.join(f'<rect x="{cx(i+1)-HW/2:.1f}" y="{ROW[r]-HH/2:.1f}" width="{HW}" height="{HH}"/>' for i,ch in enumerate(label) for r in holler(ch))
    o.append(f'<defs><mask id="h"><rect width="{W}" height="{H}" fill="#fff"/><g fill="#000">{holes}</g></mask></defs>')
    o.append(f'<g mask="url(#h)">')
    # the card: square corners lightly rounded, the top-left corner cut off
    o.append(f'<path d="M72 0H{W-14}Q{W} 0 {W} 14V{H-14}Q{W} {H} {W-14} {H}H14Q0 {H} 0 {H-14}V112Z" fill="{STOCK}"/>')
    o.append(f'<g fill="{INK}" transform="scale({SX} 1)">')
    allx=xs([cx(c) for c in range(1,81)])
    for d in range(10):
        o.append(f'<text x="{allx}" y="{ROW[d]+11:.1f}" font-size="35" font-weight="600" text-anchor="middle">{str(d)*80}</text>')
    # column numbers under the 0 row and under the 9 row
    gx=[];gs=''
    for c in range(1,81):
        s=str(c); w=8.2
        for k,chr_ in enumerate(s): gx.append(cx(c)+(k-(len(s)-1)/2)*w*1.3); gs+=chr_
    for y in (256,931):
        o.append(f'<text x="{xs(gx)}" y="{y}" font-size="18" font-weight="700" text-anchor="middle">{gs}</text>')
    o.append('</g>')
    o.append(f'<text x="318" y="958" font-size="17" fill="{INK}" font-weight="700">IBM</text><rect x="356" y="943" width="70" height="20" fill="none" stroke="{INK}" stroke-width="2"/><text x="391" y="959" font-size="16" fill="{INK}" text-anchor="middle">5081</text>')
    # what the keypunch printed along the top edge, one character over each column
    if label:
        o.append(f'<text x="{" ".join(f"{cx(i+1):.1f}" for i in range(len(label)))}" y="34" font-family="IBM Plex Mono, ui-monospace, Menlo, monospace" font-size="27" fill="{PRINT}" text-anchor="middle">{label.upper()}</text>')
    o.append('</g></svg>')
    return '\n'.join(o)
out=sys.argv[1]
for label in sys.argv[2:]:
    open(os.path.join(out,f'card-{label.lower()}.svg'),'w').write(card(label))
    print(label, os.path.getsize(os.path.join(out,f'card-{label.lower()}.svg')))
