"""Draws IBM 5081 cards from the layout traced off Rjluna2's scan (300 px to the
inch, 7 3/8 x 3 1/4 in): the corner cut, the 80 columns of printed 0-9, the
column numbers under the 0 and 9 rows, and the IBM 5081 mark, all at the scan's
measured positions. Each card is punched with its label in IBM 029 code
(0.055 x 0.125 in holes, cut out so the desk shows through) and the label is
printed along the top edge, one character over its column, as the keypunch does.

The script checks that nothing printed by the keypunch or on the card's margins
runs into a hole, and refuses to write a card if it does.
Usage: render_card.py out_dir LABEL..."""
import sys, os

W, H = 2230, 973
COL1, PITCH = 70.8, 26.31
ROW = {12: 61, 11: 136, 0: 211, **{d: 211 + 75.1*d for d in range(1, 10)}}
HOLE_W, HOLE_H = 16.5, 37.5
STOCK, STOCK_EDGE, INK, PRINT = '#f8f3d9', '#ece4c2', '#6f6a52', '#2a2834'
CUT = (72, 112)             # the top-left corner cut, as traced
SX = 0.56                   # the card's digits are tall and narrow
DIGIT = 35                  # printed digit size
COLNO = 18                  # column-number size
PUNCH_PRINT = 27            # keypunch print size
COLNO_Y = (256, 931)        # column numbers under the 0 row and under the 9 row

def holler(ch):
    ch = ch.upper()
    if ch.isdigit(): return [int(ch)]
    if 'A' <= ch <= 'I': return [12, ord(ch) - 64]
    if 'J' <= ch <= 'R': return [11, ord(ch) - 73]
    if 'S' <= ch <= 'Z': return [0, ord(ch) - 81]
    return []

def cx(c): return COL1 + PITCH*(c - 1)
def xs(vals): return ' '.join(f'{v/SX:.1f}' for v in vals)

def card(label):
    holes = [(cx(i+1) - HOLE_W/2, ROW[r] - HOLE_H/2, HOLE_W, HOLE_H)
             for i, ch in enumerate(label) for r in holler(ch)]
    # what must stay clear of the holes: the keypunch print, the column numbers,
    # the IBM mark (the printed digits are meant to be punched through)
    clear = [(cx(i+1) - 9, 34 - PUNCH_PRINT*.74, 18, PUNCH_PRINT*.74) for i in range(len(label))]
    clear += [(cx(c) - 10, y - COLNO*.74, 20, COLNO*.74) for c in range(1, 81) for y in COLNO_Y]
    clear += [(318, 940, 108, 24)]
    bad = [(round(b[0]), round(b[1])) for b in clear for h in holes
           if b[0] < h[0]+h[2] and h[0] < b[0]+b[2] and b[1] < h[1]+h[3] and h[1] < b[1]+b[3]]
    if bad: sys.exit(f'{label}: print runs into holes at {bad[:5]}')

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">']
    o.append('<defs>'
             f'<mask id="h"><rect width="{W}" height="{H}" fill="#fff"/><g fill="#000">'
             + ''.join(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="1.5"/>' for x, y, w, h in holes) +
             '</g></mask>'
             f'<linearGradient id="stock" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{STOCK}"/><stop offset=".7" stop-color="{STOCK}"/><stop offset="1" stop-color="{STOCK_EDGE}"/></linearGradient>'
             '<linearGradient id="hole" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".22"/><stop offset=".25" stop-color="#000" stop-opacity="0"/></linearGradient>'
             '</defs>')
    o.append('<g mask="url(#h)">')
    cut_x, cut_y = CUT
    o.append(f'<path d="M{cut_x} 0H{W-14}Q{W} 0 {W} 14V{H-14}Q{W} {H} {W-14} {H}H14Q0 {H} 0 {H-14}V{cut_y}Z" fill="url(#stock)"/>')
    # a hair of shadow along the card's edge, so it reads as a sheet of board
    o.append(f'<path d="M{cut_x} 0H{W-14}Q{W} 0 {W} 14V{H-14}Q{W} {H} {W-14} {H}H14Q0 {H} 0 {H-14}V{cut_y}Z" fill="none" stroke="#b9ae86" stroke-opacity=".6" stroke-width="3"/>')
    o.append(f'<g fill="{INK}" transform="scale({SX} 1)">')
    allx = xs([cx(c) for c in range(1, 81)])
    for d in range(10):
        o.append(f'<text x="{allx}" y="{ROW[d]+DIGIT*.33:.1f}" font-size="{DIGIT}" font-weight="600" text-anchor="middle">{str(d)*80}</text>')
    gx, gs = [], ''
    for c in range(1, 81):
        s = str(c)
        for k, ch in enumerate(s):
            gx.append(cx(c) + (k - (len(s)-1)/2) * COLNO * .6); gs += ch
    for y in COLNO_Y:
        o.append(f'<text x="{xs(gx)}" y="{y}" font-size="{COLNO}" font-weight="700" text-anchor="middle">{gs}</text>')
    o.append('</g>')
    o.append(f'<text x="318" y="958" font-size="17" fill="{INK}" font-weight="700">IBM</text>'
             f'<rect x="356" y="943" width="70" height="20" fill="none" stroke="{INK}" stroke-width="2"/>'
             f'<text x="391" y="959" font-size="16" fill="{INK}" text-anchor="middle">5081</text>')
    if label:
        o.append(f'<text x="{" ".join(f"{cx(i+1):.1f}" for i in range(len(label)))}" y="34" '
                 f'font-family="IBM Plex Mono, ui-monospace, Menlo, monospace" font-size="{PUNCH_PRINT}" '
                 f'fill="{PRINT}" text-anchor="middle">{label.upper()}</text>')
    o.append('</g>')
    # the inside edge of each hole, a little dark where the board was cut
    o.append('<g fill="url(#hole)">' + ''.join(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="1.5"/>' for x, y, w, h in holes) + '</g>')
    o.append('</svg>')
    return '\n'.join(o), len(holes)

out = sys.argv[1]
for label in sys.argv[2:]:
    svg, n = card(label)
    open(os.path.join(out, f'card-{label.lower()}.svg'), 'w').write(svg)
    print(f'{label}: {n} holes, print clear of them')
