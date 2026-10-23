// The calculator and the slide rule on the desk. Drag either to nudge it about;
// click it to pick it up and use it: it comes up level and large over a
// dimmed desk. The slide rule's slide and cursor drag along it; the HP-45
// switches on and calculates (assets/js/hp45.js). Esc or a click outside
// puts it back (the rule slides in under the page). Where things are left is
// remembered in this browser.
(function () {
  function load(key) {
    try { return JSON.parse(localStorage.getItem('desk:' + key)); } catch (e) { return null; }
  }
  function save(key, value) {
    try { localStorage.setItem('desk:' + key, JSON.stringify(value)); } catch (e) {}
  }

  // Drag handling shared by everything: onMove gets the pointer's travel in px
  function draggable(el, onStart, onMove, onEnd) {
    var start = null;
    el.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      var part = onStart(e);
      if (!part) return;
      e.preventDefault();
      e.stopPropagation();
      el.setPointerCapture(e.pointerId);
      start = { x: e.clientX, y: e.clientY, part: part };
    });
    el.addEventListener('pointermove', function (e) {
      if (start) onMove(start.part, e.clientX - start.x, e.clientY - start.y);
    });
    function end() {
      if (!start) return;
      onEnd(start.part);
      start = null;
    }
    el.addEventListener('pointerup', end);
    el.addEventListener('pointercancel', end);
  }

  // How far each prop may be moved from where it lies, in px: it can be
  // nudged about, but not lost off the desk or pushed out of sight under the
  // paper (the slide rule lies to the paper's left, so it mustn't go right)
  var REACH = {
    sliderule: { left: -90, right: 24, up: -160, down: 160 },
    calc: { left: -260, right: 60, up: -120, down: 260 }
  };
  function clamp(name, at) {
    var r = REACH[name] || { left: -150, right: 150, up: -150, down: 150 };
    var n = function (v) { return typeof v === 'number' && isFinite(v) ? v : 0; };
    return { x: Math.min(r.right, Math.max(r.left, n(at.x))), y: Math.min(r.down, Math.max(r.up, n(at.y))) };
  }

  // A prop moved about the desk, by translate (its rotation stays in the CSS)
  function movable(el) {
    var name = el.getAttribute('data-prop');
    var at = clamp(name, load(name) || {});
    function place() {
      el.style.setProperty('--dx', at.x + 'px');
      el.style.setProperty('--dy', at.y + 'px');
      el.classList.toggle('is-moved', !!(at.x || at.y));
    }
    place();
    var from;
    return {
      start: function () { from = { x: at.x, y: at.y }; el.classList.add('is-held', 'is-moved'); return true; },
      move: function (dx, dy) { at = clamp(name, { x: from.x + dx, y: from.y + dy }); place(); },
      end: function () { el.classList.remove('is-held'); save(name, at); },
      reset: function () { at = { x: 0, y: 0 }; place(); save(name, at); }
    };
  }

  // A prop that can be picked up and used. use = {
  //   fit(width, height): how much to enlarge it,
  //   down(event): the part pressed while in use (or null), move(part, dx, dy), up(part),
  //   hint: the line shown under it, under: slide back in under the page }
  var EASE = 'cubic-bezier(.2, .7, .2, 1)';
  function pickable(box, use) {
    var m = movable(box);
    var inUse = false, busy = false;
    var scrim = document.createElement('div');
    scrim.className = 'desk-scrim';
    scrim.innerHTML = '<p></p>';
    scrim.firstChild.textContent = use.hint;
    var restAt = function () {
      return { t: getComputedStyle(box).transform, r: box.getBoundingClientRect() };
    };
    function pickUp() {
      if (inUse || busy) return;
      busy = true;
      var rest = restAt();
      var w = parseFloat(getComputedStyle(box).width), h = parseFloat(getComputedStyle(box).height);
      var k = use.fit(w, h);
      document.body.appendChild(scrim);
      box.style.setProperty('--zoom', k);
      box.classList.add('is-zoomed');
      // laid out at the large size (so it's drawn sharp), flown in from its place shrunk
      var dx = rest.r.left + rest.r.width / 2 - innerWidth / 2, dy = rest.r.top + rest.r.height / 2 - innerHeight / 2;
      box.animate([{ transform: 'translate(' + dx + 'px, ' + dy + 'px) ' + rest.t + ' scale(' + 1 / k + ')' }, { transform: 'none' }],
                  { duration: 480, easing: EASE });
      scrim.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 480 });
      setTimeout(function () { inUse = true; busy = false; }, 480);
    }
    function putDown() {
      if (!inUse || busy) return;
      busy = true;
      var k = parseFloat(box.style.getPropertyValue('--zoom')) || 1;
      box.classList.remove('is-zoomed');
      var rest = restAt();
      box.classList.add('is-zoomed');
      var dx = rest.r.left + rest.r.width / 2 - innerWidth / 2, dy = rest.r.top + rest.r.height / 2 - innerHeight / 2;
      var fly = box.animate([{ transform: 'none' }, { transform: 'translate(' + dx + 'px, ' + dy + 'px) ' + rest.t + ' scale(' + 1 / k + ')' }],
                            { duration: 420, easing: EASE, fill: 'forwards' });
      scrim.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 420, fill: 'forwards' });
      fly.onfinish = function () {
        box.classList.remove('is-zoomed');
        fly.cancel();
        if (scrim.parentNode) scrim.parentNode.removeChild(scrim);
        if (use.under) {
          box.animate([{ translate: 'calc(var(--dx, 0px) - 3rem) var(--dy, 0px)' }, { translate: 'var(--dx, 0px) var(--dy, 0px)' }],
                      { duration: 260, easing: 'ease-out' });
        }
        inUse = false; busy = false;
        if (use.putDown) use.putDown();
      };
    }
    var moved;
    draggable(box, function (e) {
      if (busy) return null;
      if (!inUse) { moved = false; m.start(); return 'prop'; }
      return use.down(e);
    }, function (part, dx, dy) {
      if (part === 'prop') {
        if (!moved && Math.abs(dx) + Math.abs(dy) < 5) return;
        moved = true;
        return m.move(dx, dy);
      }
      if (use.move) use.move(part, dx, dy);
    }, function (part) {
      if (part === 'prop') { m.end(); if (!moved) pickUp(); }
      else if (use.up) use.up(part);
    });
    scrim.addEventListener('click', putDown);
    addEventListener('keydown', function (e) {
      if (!inUse) return;
      if (e.key === 'Escape') return putDown();
      if (use.key && use.key(e)) e.preventDefault();
    });
    return { inUse: function () { return inUse; } };
  }

  // The slide rule: its slide and cursor drag along it, the pointer's travel
  // turned into the rule's own direction and units
  function slideRule(box) {
    var drawing = box.querySelector('svg');
    var slide = box.querySelector('.rule-slide'), cursor = box.querySelector('.rule-cursor');
    var vb = drawing.viewBox.baseVal;
    // in drawing units: the slide out by up to a scale's length either way, the
    // cursor between the brackets
    var LIMIT = { slide: [-1340, 1340], cursor: [-933, 430] };
    var pos = load('sliderule-parts') || { slide: 0, cursor: 0 };
    function show() {
      slide.setAttribute('transform', 'translate(' + pos.slide + ' 0)');
      cursor.setAttribute('transform', 'translate(' + pos.cursor + ' 0)');
    }
    show();
    function along(dx, dy) {
      var t = getComputedStyle(box).transform, a = 1, b = 0;
      if (t && t !== 'none') { var v = t.match(/-?[\d.]+(e-?\d+)?/g).map(Number); a = v[0]; b = v[1]; }
      var k2 = a * a + b * b || 1;   // rotation and scale: (a, b) is the rule's x axis on screen
      return (dx * a + dy * b) / k2 * vb.width / parseFloat(getComputedStyle(box).width);
    }
    var from;
    pickable(box, {
      hint: 'Drag the slide or the cursor. Double-click to reset. Esc or click outside to put it back.',
      under: true,
      fit: function (w) { return Math.min(innerWidth * 0.94 / w, 2.6); },
      down: function (e) {
        var part = cursor.contains(e.target) ? 'cursor' : slide.contains(e.target) ? 'slide' : null;
        if (part) from = pos[part];
        return part;
      },
      move: function (part, dx, dy) {
        pos[part] = Math.min(LIMIT[part][1], Math.max(LIMIT[part][0], from + along(dx, dy)));
        show();
      },
      up: function () { save('sliderule-parts', pos); }
    });
    box.addEventListener('dblclick', function () {
      if (!box.classList.contains('is-zoomed')) return;
      pos = { slide: 0, cursor: 0 }; show(); save('sliderule-parts', pos);
    });
  }

  // The HP-45: off until its switch is slid to ON, then an RPN calculator
  var KEYS = { '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
               '.': 'dot', ',': 'dot', '+': 'add', '-': 'sub', '*': 'mul', 'x': 'mul', '/': 'div',
               'Enter': 'enter', 'Backspace': 'clx', 'Delete': 'clx', 'e': 'eex', 'n': 'chs', 's': 'swap' };
  function calculator(box) {
    var calc = new HP45(), on = false;
    var cells = box.querySelectorAll('.hp-cell');
    var sw = box.querySelector('.hp-switch');
    function show() {
      var shown = on ? calc.cells() : [];
      Array.prototype.forEach.call(cells, function (cell, i) {
        var c = shown[i] || { segs: '', dp: false };
        Array.prototype.forEach.call(cell.querySelectorAll('.hp-seg'), function (seg) {
          var s = seg.getAttribute('data-seg');
          seg.classList.toggle('hp-lit', s === 'p' ? c.dp : c.segs.indexOf(s) >= 0);
        });
      });
      box.querySelector('svg').classList.toggle('hp-on', on);
    }
    show();
    function press(key) {
      if (!on) return;
      calc.press(key);
      show();
    }
    pickable(box, {
      hint: 'Slide the switch to ON, then calculate in RPN: 2 ENTER 3 +. Keys work too. Esc or click outside to put it down.',
      fit: function (w, h) { return Math.min(innerHeight * 0.86 / h, innerWidth * 0.9 / w, 4); },
      down: function (e) {
        if (sw.contains(e.target)) return 'switch';
        var k = e.target.closest && e.target.closest('.hp-key');
        if (!k || !box.contains(k)) return null;
        k.classList.add('hp-down');
        press(k.getAttribute('data-key'));
        return k;
      },
      up: function (part) {
        if (part === 'switch') {
          on = !on;
          if (on) calc.reset();
          show();
        } else if (part.classList) {
          part.classList.remove('hp-down');
        }
      },
      key: function (e) {
        var k = KEYS[e.key];
        if (!k || e.metaKey || e.ctrlKey || e.altKey) return false;
        var el = box.querySelector('.hp-key[data-key="' + k + '"]');
        if (el && on) { el.classList.add('hp-down'); setTimeout(function () { el.classList.remove('hp-down'); }, 90); }
        press(k);
        return true;
      }
    });
  }

  // Swap the pictures of the live props for the drawings themselves, so their
  // parts can move. Each goes in a plain box that carries its place and turn:
  // Safari turns an <svg> about a different point than other browsers do.
  var LIVE = { sliderule: slideRule, calc: window.HP45 ? calculator : null };
  Array.prototype.forEach.call(document.querySelectorAll('.prop[data-prop]'), function (el) {
    var name = el.getAttribute('data-prop'), live = LIVE[name];
    function plain() {
      var m = movable(el);
      draggable(el, function () { return m.start(); }, function (p, dx, dy) { m.move(dx, dy); }, function () { m.end(); });
      el.addEventListener('dblclick', m.reset);
    }
    if (!live || !window.fetch) return plain();
    fetch(el.getAttribute('src')).then(function (r) { return r.text(); }).then(function (text) {
      var drawing = document.importNode(new DOMParser().parseFromString(text, 'image/svg+xml').documentElement, true);
      var box = document.createElement('div');
      box.className = el.className;
      box.setAttribute('data-prop', name);
      box.setAttribute('aria-hidden', 'true');
      box.appendChild(drawing);
      el.replaceWith(box);
      live(box);
    }).catch(plain);
  });
})();
