"""Draws the HP-45 from hp45.json (its keyboard as traced from the photo):
same keys, legends and colours, drawn clean, with shaded keycaps, a lit LED
display and a chrome-trimmed case. Usage: render_hp45.py out.svg"""
import json, sys, os
D = json.load(open(os.path.join(os.path.dirname(__file__), 'hp45.json')))
C = D['colours']; W, H = D['case']['w'], D['case']['h']
FONT = 'Helvetica Neue, Helvetica, Arial, sans-serif'

def shade(hexc, f):
    r, g, b = (int(hexc[i:i+2], 16) for i in (1, 3, 5))
    if f >= 1:
        r, g, b = (int(v + (255 - v) * (f - 1)) for v in (r, g, b))
    else:
        r, g, b = (int(v * f) for v in (r, g, b))
    return '#%02x%02x%02x' % (r, g, b)

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;')

def legend(s, size):
    # a^b sets b as a superscript; "1/x" is set as a small 1 over the slash
    if s == '1/x':
        return f'<tspan font-size="{size*.62:.0f}" dy="-{size*.3:.0f}">1</tspan><tspan dy="{size*.3:.0f}">/x</tspan>'
    if '^' in s:
        base, sup = s.split('^', 1)
        return f'{esc(base)}<tspan font-size="{size*.62:.0f}" dy="-{size*.38:.0f}">{esc(sup)}</tspan>'
    return esc(s)

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">')
defs = ['<linearGradient id="case" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c2c2b"/><stop offset=".04" stop-color="#1a1a1a"/><stop offset="1" stop-color="#0d0d0d"/></linearGradient>',
        '<linearGradient id="caseEdge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset=".08" stop-color="#fff" stop-opacity="0"/><stop offset=".92" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>',
        '<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbfbf8"/><stop offset=".45" stop-color="#c9c9c4"/><stop offset=".55" stop-color="#9b9b96"/><stop offset="1" stop-color="#dcdcd7"/></linearGradient>',
        '<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a0609"/><stop offset=".5" stop-color="#2c0305"/><stop offset="1" stop-color="#3a0507"/></linearGradient>',
        f'<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(C["panel"],1.08)}"/><stop offset="1" stop-color="{shade(C["panel"],.9)}"/></linearGradient>',
        '<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '<filter id="keyShadow" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="2.5" flood-color="#000" flood-opacity=".55"/></filter>']
for name in ('dark', 'black', 'orange', 'grey', 'cream'):
    f = C[name]['face']
    defs.append(f'<linearGradient id="k-{name}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(f,1.16)}"/><stop offset=".55" stop-color="{f}"/><stop offset="1" stop-color="{shade(f,.86)}"/></linearGradient>')
o.append('<defs>' + ''.join(defs) + '</defs>')

# the case
o.append(f'<rect width="{W}" height="{H}" rx="46" fill="url(#case)"/>')
o.append(f'<rect width="{W}" height="{H}" rx="46" fill="url(#caseEdge)"/>')
o.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="45" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="3"/>')

# the display: a recessed window, red filter glass, the LED digits lit
o.append('<rect x="64" y="34" width="682" height="164" rx="10" fill="#050505"/>')
o.append('<rect x="80" y="50" width="650" height="132" rx="5" fill="url(#glass)"/>')
o.append('<rect x="80" y="50" width="650" height="10" rx="5" fill="#fff" fill-opacity=".06"/>')
# seven-segment digits: cell 36 wide, the HP-45 shows " 0.00" from the left after power-on
SEG = {'0': 'abcdef'}
def digit(x, y, ch, s=1.0):
    w, h, t = 22*s, 46*s, 5*s
    segs = {'a': (x+t, y, w-2*t, t), 'd': (x+t, y+h-t, w-2*t, t), 'g': (x+t, y+h/2-t/2, w-2*t, t),
            'f': (x, y+t, t, h/2-1.5*t), 'b': (x+w-t, y+t, t, h/2-1.5*t),
            'e': (x, y+h/2+t/2, t, h/2-1.5*t), 'c': (x+w-t, y+h/2+t/2, t, h/2-1.5*t)}
    on = SEG.get(ch, '')
    cx, cy = x + w/2, y + h/2
    # the digit leans forward a little, about its own centre
    out = [f'<g transform="translate({cx:.1f} {cy:.1f}) skewX(-6) translate({-cx:.1f} {-cy:.1f})">']
    for k, (sx, sy, sw, sh) in segs.items():
        op = '1' if k in on else '.035'
        out.append(f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{sw:.1f}" height="{sh:.1f}" rx="{t/2:.1f}" fill="#ff3a26" fill-opacity="{op}"/>')
    out.append('</g>')
    return out
cells = 15; cx0 = 116; pitch = 41; y0 = 88
lit = []; dim = []
text = ' ' + D['display']   # the first cell is the sign
i = 0; dot_after = None
for ch in text:
    if ch == '.':
        dot_after = i - 1; continue
    i += 1
glyphs = [c for c in text if c != '.']
for n in range(cells):
    ch = glyphs[n] if n < len(glyphs) else ' '
    segs = digit(cx0 + n*pitch, y0, ch, 1.18)
    (lit if ch != ' ' else dim).extend(segs)
o.append('<g>' + ''.join(dim) + '</g>')
o.append('<g filter="url(#glow)">' + ''.join(lit))
if dot_after is not None:
    # the decimal point sits low between its digit and the next, under the slant
    o.append(f'<circle cx="{cx0 + dot_after*pitch + 30:.1f}" cy="{y0+50}" r="4.5" fill="#ff3a26"/>')
o.append('</g>')

# chrome trim under the display, then the keyboard panel
o.append('<rect x="56" y="206" width="698" height="12" rx="4" fill="url(#chrome)"/>')
o.append('<rect x="44" y="228" width="722" height="1208" rx="12" fill="url(#panel)"/>')
o.append('<rect x="44" y="228" width="722" height="1208" rx="12" fill="none" stroke="#a8a7a1" stroke-opacity=".55" stroke-width="3"/>')
# power switch
o.append(f'<text x="118" y="314" font-size="21" fill="#e8e5da" text-anchor="middle" letter-spacing="1">OFF</text><text x="288" y="314" font-size="21" fill="#e8e5da" text-anchor="middle" letter-spacing="1">ON</text>')
o.append('<rect x="150" y="290" width="104" height="30" rx="5" fill="#0a0a0a"/><rect x="156" y="284" width="48" height="42" rx="5" fill="#3a3a39"/><rect x="156" y="284" width="48" height="8" rx="4" fill="#fff" fill-opacity=".15"/>')
for i in range(6):
    o.append(f'<rect x="{162+i*7}" y="296" width="3" height="20" fill="#1d1d1d"/>')

def key(x, y, w, h, cls, text, shifted, shifted_anchor='middle'):
    face = C[cls]['face']; fg = C[cls]['legend']
    g = [f'<g filter="url(#keyShadow)">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{shade(face,.55)}"/>',   # the skirt
         f'<rect x="{x+4}" y="{y+1}" width="{w-8}" height="{h-15}" rx="7" fill="url(#k-{cls})"/>',  # the top face
         f'<rect x="{x+9}" y="{y+3}" width="{w-18}" height="2" rx="1" fill="#fff" fill-opacity=".28"/>',
         '</g>']
    if text:
        size = 46 if text in '−+×÷' else 34 if len(text) <= 2 else 27 if len(text) <= 4 else 26
        weight = 500 if text.isdigit() or text in '·' else 600
        g.append(f'<text x="{x+w/2}" y="{y+(h-15)/2+size*.36:.1f}" font-size="{size}" font-weight="{weight}" fill="{fg}" text-anchor="middle">{legend(text,size)}</text>')
    if shifted:
        sx = x + w/2 if shifted_anchor == 'middle' else x + w - 8
        g.append(f'<text x="{sx}" y="{y-11}" font-size="24" font-weight="600" fill="{C["gold"]}" text-anchor="{shifted_anchor}">{legend(shifted,24)}</text>')
    return ''.join(g)

U = D['upper']
for r, y in enumerate(U['rows']):
    col = 0
    for k in U['keys'][r]:
        cls, text, shifted = k[:3]; span = k[3] if len(k) > 3 else 1
        x = U['x0'] + col*U['pitch']; w = U['w'] + (span-1)*U['pitch']
        o.append(key(x, y, w, U['h'], cls, text, shifted, 'end' if span > 1 else 'middle'))
        col += span
L = D['lower']
for r, y in enumerate(L['rows']):
    for c, (cls, text, shifted) in enumerate(L['keys'][r]):
        if c == 0: x, w = L['op_x'], L['op_w']
        else: x, w = L['x0'] + (c-1)*L['pitch'], L['w']
        o.append(key(x, y, w, L['h'], cls, text, shifted))

# nameplate in its chrome frame
o.append('<rect x="70" y="1352" width="670" height="66" rx="5" fill="url(#chrome)"/>')
o.append('<rect x="76" y="1358" width="658" height="54" rx="3" fill="#0b0b0e"/>')
o.append('<rect x="88" y="1364" width="86" height="42" rx="4" fill="#38ace4"/>')
o.append('<text x="131" y="1395" font-size="27" font-style="italic" font-weight="700" fill="#0b0b0e" text-anchor="middle">hp</text>')
o.append('<text x="420" y="1397" font-size="29" font-weight="500" letter-spacing="7" fill="#eeede8" text-anchor="middle">HEWLETT·PACKARD</text>')
o.append('<text x="690" y="1397" font-size="29" font-weight="500" fill="#eeede8" text-anchor="middle">45</text>')
o.append('</svg>')
open(sys.argv[1], 'w').write('\n'.join(o))
