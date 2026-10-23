// The calculator and the slide rule can be picked up and put down somewhere
// else on the desk, and the slide rule works: its slide and its cursor slide
// along it. Where you leave everything is remembered in this browser.
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

  // A prop moved about the desk, by translate (its rotation stays in the CSS)
  function movable(el) {
    var name = el.getAttribute('data-prop');
    var at = load(name) || { x: 0, y: 0 };
    function place() {
      el.style.setProperty('--dx', at.x + 'px');
      el.style.setProperty('--dy', at.y + 'px');
      el.classList.toggle('is-moved', !!(at.x || at.y));
    }
    place();
    var from;
    return {
      start: function () { from = { x: at.x, y: at.y }; el.classList.add('is-held', 'is-moved'); return true; },
      move: function (dx, dy) { at = { x: from.x + dx, y: from.y + dy }; place(); },
      end: function () { el.classList.remove('is-held'); save(name, at); },
      reset: function () { at = { x: 0, y: 0 }; place(); save(name, at); }
    };
  }

  function plainProp(el) {
    var m = movable(el);
    draggable(el, function () { return m.start(); }, function (p, dx, dy) { m.move(dx, dy); }, function () { m.end(); });
    el.addEventListener('dblclick', m.reset);
  }

  // The slide rule. On the desk, dragging it moves it and a click picks it up
  // to use: it comes up level and large, and its slide and cursor drag along it
  // (the pointer's travel is turned into the rule's own direction and units).
  // Click off it or press Esc and it goes back and slides under the page.
  function slideRule(svg) {
    var drawing = svg.querySelector('svg');
    var m = movable(svg);
    var slide = svg.querySelector('.rule-slide'), cursor = svg.querySelector('.rule-cursor');
    var vb = drawing.viewBox.baseVal;
    // in drawing units: the slide out by up to a scale's length either way, the
    // cursor between the brackets
    var LIMIT = { slide: [-1340, 1340], cursor: [-933, 430] };
    var pos = load('sliderule-parts') || { slide: 0, cursor: 0 };
    var zoomed = false, busy = false;
    var scrim = document.createElement('div');
    scrim.className = 'desk-scrim';
    scrim.innerHTML = '<p>Drag the slide or the cursor. Double-click to reset. Esc or click outside to put it back.</p>';
    function show() {
      slide.setAttribute('transform', 'translate(' + pos.slide + ' 0)');
      cursor.setAttribute('transform', 'translate(' + pos.cursor + ' 0)');
    }
    show();
    // the pointer's travel along the rule, in drawing units
    function along(dx, dy) {
      var t = getComputedStyle(svg).transform, a = 1, b = 0;
      if (t && t !== 'none') { var v = t.match(/-?[\d.]+(e-?\d+)?/g).map(Number); a = v[0]; b = v[1]; }
      var k2 = a * a + b * b || 1;   // rotation and scale: (a, b) is the rule's x axis on screen
      return (dx * a + dy * b) / k2 * vb.width / parseFloat(getComputedStyle(svg).width);
    }
    var EASE = 'cubic-bezier(.2, .7, .2, 1)';
    function restingTransform() {
      return getComputedStyle(svg).transform;
    }
    function zoomIn() {
      if (zoomed || busy) return;
      busy = true;
      var r0 = svg.getBoundingClientRect(), from = restingTransform();
      var w = parseFloat(getComputedStyle(svg).width);
      var k = Math.min(innerWidth * 0.94 / w, 2.6);
      document.body.appendChild(scrim);
      svg.classList.add('is-zoomed');
      svg.style.setProperty('--zoom', k);
      // where it was on the desk, relative to where it now sits (the middle of the window)
      var dx = r0.left + r0.width / 2 - innerWidth / 2, dy = r0.top + r0.height / 2 - innerHeight / 2;
      svg.animate([{ transform: 'translate(' + dx + 'px, ' + dy + 'px) ' + from }, { transform: 'scale(' + k + ')' }],
                  { duration: 480, easing: EASE });
      scrim.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 480 });
      setTimeout(function () { zoomed = true; busy = false; }, 480);
    }
    function zoomOut() {
      if (!zoomed || busy) return;
      busy = true;
      var k = parseFloat(svg.style.getPropertyValue('--zoom')) || 1;
      svg.classList.remove('is-zoomed');
      var r1 = svg.getBoundingClientRect(), rest = restingTransform();
      svg.classList.add('is-zoomed');
      var dx = r1.left + r1.width / 2 - innerWidth / 2, dy = r1.top + r1.height / 2 - innerHeight / 2;
      var fly = svg.animate([{ transform: 'scale(' + k + ')' }, { transform: 'translate(' + dx + 'px, ' + dy + 'px) ' + rest }],
                            { duration: 420, easing: EASE, fill: 'forwards' });
      scrim.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 420, fill: 'forwards' });
      fly.onfinish = function () {
        svg.classList.remove('is-zoomed');
        fly.cancel();
        if (scrim.parentNode) scrim.parentNode.removeChild(scrim);
        // and in under the edge of the paper
        svg.animate([{ translate: 'calc(var(--dx, 0px) - 3rem) var(--dy, 0px)' }, { translate: 'var(--dx, 0px) var(--dy, 0px)' }],
                    { duration: 260, easing: 'ease-out' });
        zoomed = false; busy = false;
        save('sliderule-parts', pos);
      };
    }
    var from, moved;
    draggable(svg, function (e) {
      if (busy) return null;
      if (!zoomed) { moved = false; m.start(); return 'rule'; }
      var part = cursor.contains(e.target) ? 'cursor' : slide.contains(e.target) ? 'slide' : null;
      if (part) from = pos[part];
      return part;
    }, function (part, dx, dy) {
      if (part === 'rule') {
        if (!moved && Math.abs(dx) + Math.abs(dy) < 5) return;
        moved = true;
        return m.move(dx, dy);
      }
      pos[part] = Math.min(LIMIT[part][1], Math.max(LIMIT[part][0], from + along(dx, dy)));
      show();
    }, function (part) {
      if (part === 'rule') { m.end(); svg.classList.remove('is-moved'); if (!moved) zoomIn(); }
    });
    svg.addEventListener('dblclick', function (e) {
      if (!zoomed) return;
      pos = { slide: 0, cursor: 0 }; show(); save('sliderule-parts', pos);
    });
    scrim.addEventListener('click', zoomOut);
    addEventListener('keydown', function (e) { if (e.key === 'Escape') zoomOut(); });
  }

  Array.prototype.forEach.call(document.querySelectorAll('.prop[data-prop]'), function (el) {
    if (el.getAttribute('data-prop') !== 'sliderule' || !window.fetch) return plainProp(el);
    // Swap the picture of the rule for the drawing itself, so its parts can move.
    // The drawing goes in a plain box that carries the rule's place and turn:
    // Safari turns an <svg> about a different point than other browsers do.
    fetch(el.getAttribute('src')).then(function (r) { return r.text(); }).then(function (text) {
      var drawing = document.importNode(new DOMParser().parseFromString(text, 'image/svg+xml').documentElement, true);
      var box = document.createElement('div');
      box.className = el.className;
      box.setAttribute('data-prop', 'sliderule');
      box.setAttribute('aria-hidden', 'true');
      box.appendChild(drawing);
      el.replaceWith(box);
      slideRule(box);
    }).catch(function () { plainProp(el); });
  });
})();
