# Desk props

The calculator, slide rule and punch cards in `assets/images/desk` are drawings traced
from photographs of the real things, not made up:

- HP-45: photo by Joe Haupt, CC BY-SA 2.0 (Wikimedia Commons, file 11590594223),
  straightened to a top-down view; `trace_hp45.py` took each key's box and colour from it,
  and `hp45.json` keeps that keyboard (keys, legends, shifted functions, colours) as data.
  `render_hp45.py` draws the calculator from the data:
  `python3 render_hp45.py ../../assets/images/desk/hp45.svg`.
- Slide rule: Sally Ride's Post rule, Smithsonian, CC0 (Commons, DPLA 171e755a…, page 1),
  deskewed; `trace_rule.py` takes the body, brackets, cursor and scale rows from it and
  computes every tick from its scale's formula.
- Punch card: blank IBM 5081 scan by Rjluna2, CC BY-SA 4.0 (Commons); `trace_card.py`
  takes the outline and the digit grid from it and punches labels in IBM 029 code:
  `python3 trace_card.py ../../assets/images/desk BLOG PROJECTS BIO RSS COMMENTS`.

The scripts read the straightened photos (`hp45-cut.png`, `card-cut.png`) they were
traced from; those aren't kept here.
