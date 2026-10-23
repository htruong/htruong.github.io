# Desk props

The calculator, slide rule and punch cards in `assets/images/desk` are drawings traced
from photographs of the real things, not made up:

- HP-45: photo by Joe Haupt, CC BY-SA 2.0 (Wikimedia Commons, file 11590594223),
  straightened to a top-down view; `trace_hp45.py` took each key's box and colour from it,
  and `hp45.json` keeps that keyboard (keys, legends, shifted functions, colours) as data.
  `render_hp45.py` draws the calculator from the data:
  `python3 render_hp45.py ../../assets/images/desk/hp45.svg`.
- Slide rule: Sally Ride's Post rule, Smithsonian, CC0 (Commons, DPLA 171e755a…, page 1),
  deskewed; `trace_rule.py` took the body, brackets, cursor and scale rows from it.
  `render_rule.py` draws the same eleven scales, in the same order and colours, with
  every tick from its scale's formula; numbers sit past the longest tick of their band,
  and the script refuses to write the file if any number touches a tick:
  `python3 render_rule.py ../../assets/images/desk/sliderule.svg`.
- Punch card: blank IBM 5081 scan by Rjluna2, CC BY-SA 4.0 (Commons); `trace_card.py`
  took the outline and the digit grid from it. `render_card.py` draws the card from that
  layout and punches each label in IBM 029 code; it refuses to write a card if the
  keypunch print, the column numbers or the IBM mark would run into a hole:
  `python3 render_card.py ../../assets/images/desk BLOG PROJECTS BIO RSS COMMENTS`.

The scripts read the straightened photos (`hp45-cut.png`, `card-cut.png`) they were
traced from; those aren't kept here.

- Coffee ring: photo of a real one on a paper towel by Nevit Dilmen, CC BY-SA 3.0
  (Commons, "Coffee Stain P1000065.JPG"). `coffee_ring.py` reads the stain's density
  from its colour (the towel's grey emboss drops out), and writes it as coffee brown
  with that density as alpha, multiplied onto a post's first page.
