"""Draws Sally Ride's Post slide rule from what was traced off the Smithsonian
photo: the same eleven scales in the same order and colours (LL/1-LL/3 on top,
CF CIF CI C on the slide, D LL3 LL2 LL1 below), the brackets, cursor, maker's
mark and range notes. Every tick is placed by its scale's formula.

Each scale has a band of its own: ticks start at the band's edge, and numbers
sit past the end of the longest tick, so a number never touches a tick; a
number that would collide with its neighbour is left out.
Usage: render_rule.py out.svg"""
import math, sys

W = 1709                    # overall length, brackets included (as traced)
X0, L = 181, 1342           # left index and scale length (as traced)
BR = 88                     # bracket width
RED, BLK = '#b3352b', '#26262a'
TICK = {'label': 10, 'half': 7, 'minor': 4.5}
GAP = 3                     # space between a tick's end and a number
SIZE = 10                   # number size
lg = math.log10; LPI = lg(math.pi)

def C(v): return lg(v)
def CI(v): return 1 - lg(v)
def CF(v): return (lg(v) - LPI) % 1.0 if abs(v - math.pi) > 1e-9 else 0.0
def CIF(v): return (1 - lg(v) - LPI) % 1.0
def LL(k, neg=False):
    def f(v):
        t = (-math.log(v) if neg else math.log(v)) * k
        return lg(t) if t > 0 else None
    return f

def subdivide(pos, values, min_gap=4.5):
    """Labelled values, with as many even subdivisions between each pair as
    keep ticks at least min_gap px apart."""
    marks = [(v, 'label') for v in values]
    for a, b in zip(values, values[1:]):
        pa, pb = pos(a), pos(b)
        if pa is None or pb is None: continue
        span = abs(pb - pa) * L
        n = next((k for k in (20, 10, 5, 2) if span / k >= min_gap), 1)
        for i in range(1, n):
            kind = 'half' if i * 2 == n else 'minor'
            marks.append((a + (b - a) * i / n, kind))
    return marks

def cd_values():
    v = [1 + i/10 for i in range(10)] + [2 + i/2 for i in range(16)] + [10]
    return sorted(set(round(x, 6) for x in v))
CD_LABELS = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '1',
             1.5: '1.5'}

o = []
TICKS, BOXES = [], []      # every tick segment and number box, for the overlap check
def text(x, y, s, col, size=SIZE, anchor='middle', weight=400):
    o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>')

def scale(name, edge, d, col, pos, values, labels, sub=None):
    """A scale whose ticks start at y=edge and run in direction d (1 down, -1 up)."""
    marks = subdivide(pos, values)
    if sub: marks += sub
    path = []
    for v, kind in marks:
        p = pos(v)
        if p is None or p < -1e-4 or p > 1 + 1e-4: continue
        x = X0 + p * L
        path.append(f'M{x:.2f} {edge}v{d*TICK[kind]}')
        TICKS.append((x, min(edge, edge + d*TICK[kind]), max(edge, edge + d*TICK[kind])))
    o.append(f'<path d="{" ".join(path)}" stroke="{col}" stroke-width=".9" fill="none"/>')
    # numbers: past the longest tick; cap height ~0.72 of the size
    base = edge + d*(TICK['label'] + GAP) + (SIZE*0.72 if d > 0 else 0)
    placed = []
    for v, s in labels:
        p = pos(v)
        if p is None or p < -1e-4 or p > 1 + 1e-4: continue
        x = X0 + p * L; w = len(s) * SIZE * 0.55
        box = (x - w/2 - 2, x + w/2 + 2)
        if any(not (box[1] < b[0] or box[0] > b[1]) for b in placed): continue
        placed.append(box); text(x, base, s, col)
        BOXES.append((box[0], box[1], base - SIZE*0.74, base + 0.5, s))
    # the scale's name in the margin, level with its numbers
    text(158, base, name, col, 13, 'end')

H = 262
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -14 {W} {H+28}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">')
o.append('<defs><linearGradient id="m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#dcdcd7"/><stop offset=".5" stop-color="#b4b3ae"/><stop offset="1" stop-color="#cfcfca"/></linearGradient>'
         '<linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f6f1"/><stop offset="1" stop-color="#ebeae4"/></linearGradient></defs>')
# stators and slide (the slide 80-170)
o.append(f'<rect x="{BR}" y="0" width="{W-2*BR}" height="{H}" fill="url(#body)"/>')
o.append(f'<rect x="{BR}" y="80" width="{W-2*BR}" height="90" fill="#f1f0ea"/>')
o.append(f'<path d="M{BR} 80H{W-BR}M{BR} 170H{W-BR}" stroke="#c4c3bd" stroke-width="1.2"/>')

e = math.e
# upper stator: LL/1, LL/2 hang from their edges; LL/3 rises from the slide's edge
ll1n = [.99, .985, .98, .975, .97, .96, .95, .94, .93, .92, .91, .905]
ll2n = [.905, .90, .85, .80, .75, .70, .65, .60, .55, .50, .45, .40, 1/e]
ll3n = [1/e, .35, .30, .25, .20, .15, .10, .05, .03, .02, .01, .005, .002, .001, .0005, .0002, .0001, 4.54e-5]
fmt = lambda v: ('%g' % v)[1:] if v < 1 and v >= .001 else ('%g' % v)
fmt2 = lambda v: ('%.2f' % v)[1:]
scale('LL/1', 4, 1, RED, LL(100, True), ll1n, [(v, fmt(v)) for v in ll1n[:-1]])
scale('LL/2', 30, 1, RED, LL(10, True), ll2n, [(v, fmt2(v)) for v in ll2n[1:-1]])
scale('LL/3', 80, -1, RED, LL(1, True), ll3n, [(1/e, '1/e')] + [(v, fmt(v)) for v in ll3n[1:-1]])
# the slide: CF and CIF hang from its top, CI below them, C rises from its bottom
cdv = cd_values()
cfv = sorted(set([math.pi] + [v for v in cdv]))
scale('CF', 80, 1, BLK, CF, cfv, [(math.pi, 'π')] + [(v, s) for v, s in CD_LABELS.items() if v != 1.5])
scale('CIF', 102, 1, RED, CIF, cdv, [(v, s) for v, s in CD_LABELS.items() if v != 1.5])
scale('CI', 124, 1, RED, CI, cdv, [(v, s) for v, s in CD_LABELS.items()])
scale('C', 170, -1, BLK, C, cdv, list(CD_LABELS.items()) + [(math.pi, 'π')])
# lower stator: D hangs from the slide's edge, then LL3, LL2, LL1
scale('D', 170, 1, BLK, C, cdv, list(CD_LABELS.items()) + [(math.pi, 'π')])
ll3 = [e, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 22026]
ll2 = [1.105, 1.11, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.5, e]
ll1 = [1.01005, 1.015, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.08, 1.09, 1.10, 1.105]
scale('LL3', 196, 1, BLK, LL(1), ll3, [(v, 'e' if v == e else '%g' % v) for v in ll3[:-1]])
scale('LL2', 218, 1, BLK, LL(10), ll2, [(v, 'e' if v == e else '%g' % v) for v in ll2[1:]])
scale('LL1', 240, 1, BLK, LL(100), ll1, [(1.01005, '1.01')] + [(v, '%g' % v) for v in ll1[1:-1]])
# the sides of the formula: e^-x beside the reciprocal LLs, X by D, e^x by the LLs
text(110, 36, 'e<tspan font-size="8" dy="-5">−x</tspan>', RED, 12, 'end')
text(110, 236, 'e<tspan font-size="8" dy="-5">x</tspan>', BLK, 12, 'end')
text(104, 192, 'X', BLK, 12, 'end')
# right end: what range each LL covers, the maker's mark and number
for y, s in [(22, '−0.01 ← −0.1'), (48, '−0.1 ← −1.0'), (64, '−1.0 ← −10.0')]: text(1545, y, s, RED, 10, 'start')
for y, s in [(212, '1.0 → 10.0'), (234, '0.1 → 1.0'), (256, '0.01 → 0.1')]: text(1545, y, s, BLK, 10, 'start')
o.append('<ellipse cx="1578" cy="118" rx="26" ry="16" fill="none" stroke="#b3352b" stroke-width="2"/>')
text(1578, 124, 'POST', RED, 15, weight=700)
text(1578, 152, '625 372', '#8a8984', 10)
# end brackets with their rivets, and the slide's ends showing past them
for x in (0, W - BR):
    o.append(f'<rect x="{x}" y="-2" width="{BR}" height="{H+4}" rx="3" fill="url(#m)" stroke="#9a9994" stroke-width="1.2"/>')
    for ry in (20, H - 20): o.append(f'<circle cx="{x+BR/2}" cy="{ry}" r="5.5" fill="#d6d6d1" stroke="#8a8984"/>')
o.append(f'<rect x="-6" y="84" width="28" height="82" rx="3" fill="#f1f0ea" stroke="#c9c8c2"/><rect x="{W-22}" y="84" width="28" height="82" rx="3" fill="#f1f0ea" stroke="#c9c8c2"/>')
# the cursor (where the photo has it): glass in a metal frame, with a red hairline
cx0, cx1 = 1021, 1191
o.append(f'<rect x="{cx0}" y="-12" width="{cx1-cx0}" height="{H+24}" rx="5" fill="#ffffff" fill-opacity=".14" stroke="#a7a6a1" stroke-width="4"/>')
o.append(f'<rect x="{cx0-4}" y="-13" width="{cx1-cx0+8}" height="14" rx="4" fill="url(#m)"/><rect x="{cx0-4}" y="{H-1}" width="{cx1-cx0+8}" height="14" rx="4" fill="url(#m)"/>')
o.append(f'<path d="M{(cx0+cx1)/2} 2V{H-2}" stroke="#c33a2c" stroke-width="1"/>')
o.append('</svg>')
# no number may touch a tick (the box includes the 2 px either side)
hits = [(b[4], round(t[0])) for b in BOXES for t in TICKS if b[0] <= t[0] <= b[1] and not (t[2] < b[2] or t[1] > b[3])]
if hits:
    sys.exit(f'numbers touching ticks: {hits[:10]} ({len(hits)})')
open(sys.argv[1], 'w').write('\n'.join(o))
print(f'{len(TICKS)} ticks, {len(BOXES)} numbers, none touching')
