// The calculator and the slide rule can be picked up and put down somewhere
// else on the desk. Where you leave them is remembered in this browser.
(function () {
  var props = document.querySelectorAll('.prop[data-prop]');
  function load(name) {
    try { return JSON.parse(localStorage.getItem('desk:' + name)); } catch (e) { return null; }
  }
  function save(name, at) {
    try { localStorage.setItem('desk:' + name, JSON.stringify(at)); } catch (e) {}
  }
  function place(el, at) {
    el.style.setProperty('--dx', at.x + 'px');
    el.style.setProperty('--dy', at.y + 'px');
  }
  Array.prototype.forEach.call(props, function (el) {
    var name = el.getAttribute('data-prop');
    var at = load(name) || { x: 0, y: 0 };
    if (at.x || at.y) { place(el, at); el.classList.add('is-moved'); }
    var start = null;
    el.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      e.preventDefault();
      el.setPointerCapture(e.pointerId);
      start = { px: e.clientX, py: e.clientY, x: at.x, y: at.y };
      el.classList.add('is-held', 'is-moved');
    });
    el.addEventListener('pointermove', function (e) {
      if (!start) return;
      at = { x: start.x + e.clientX - start.px, y: start.y + e.clientY - start.py };
      place(el, at);
    });
    function drop() {
      if (!start) return;
      start = null;
      el.classList.remove('is-held');
      save(name, at);
    }
    el.addEventListener('pointerup', drop);
    el.addEventListener('pointercancel', drop);
    // Double-click puts it back where it started
    el.addEventListener('dblclick', function () {
      at = { x: 0, y: 0 };
      place(el, at);
      el.classList.remove('is-moved');
      save(name, at);
    });
  });
})();
