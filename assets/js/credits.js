// CREDITS in the footer prints the credits: a short sheet comes up out of a
// line printer in front of the page, a whole line at a time, the paper
// feeding up a line after each. Click anywhere (or press
// Esc) and it goes away. Without this script the credits simply fold open.
(function () {
  var COLS = 46, LINE_MS = 140;
  var still = matchMedia('(prefers-reduced-motion: reduce)');

  function wrap(text, cols) {
    var out = [], line = '';
    text.split(/\s+/).forEach(function (w) {
      if (!w) return;
      if (line && (line + ' ' + w).length > cols) { out.push(line); line = w; }
      else line = line ? line + ' ' + w : w;
    });
    if (line) out.push(line);
    return out;
  }

  function lines(details) {
    var body = details.querySelector('.credits-text');
    var out = [{ t: 'CREDITS.TXT' + new Array(COLS - 20).join(' ') + 'PAGE 0001' }, { t: '' }];
    wrap(body.textContent, COLS).forEach(function (t) { out.push({ t: t }); });
    out.push({ t: '' });
    Array.prototype.forEach.call(body.querySelectorAll('a'), function (a) {
      // the link's words, then the site it goes to (a whole address won't fit)
      var t = a.textContent.toUpperCase() + ' \u2192 ' + a.hostname.replace(/^www\./, '');
      out.push({ t: t.slice(0, COLS), href: a.href });
    });
    out.push({ t: '' }, { t: '*** END OF CREDITS ***', c: 'end' }, { t: '' });
    return out;
  }

  function print(details) {
    if (document.querySelector('.printer')) return;
    var all = lines(details);
    var printer = document.createElement('div');
    printer.className = 'printer';
    printer.innerHTML = '<div class="printer-paper"><div class="printer-lines"></div></div>' +
                        '<div class="printer-bail"></div><p class="printer-hint">Click anywhere to dismiss</p>';
    document.body.appendChild(printer);
    var paper = printer.querySelector('.printer-paper'), box = printer.querySelector('.printer-lines');
    var done = false, timer = null;

    function addLine(l) {
      var el = document.createElement(l.href ? 'a' : 'p');
      el.className = 'printer-line' + (l.c ? ' printer-' + l.c : '');
      if (l.href) { el.href = l.href; el.rel = 'noopener'; }
      box.appendChild(el);
      return el;
    }
    var i = 0;
    function next() {
      if (i >= all.length) { done = true; printer.classList.add('is-done'); return; }
      var l = all[i++];
      addLine(l).textContent = l.t || '\u00a0';
      // the paper feeds up by the line just printed
      if (!still.matches) paper.animate([{ transform: 'translate(-50%, 1.5rem)' }, { transform: 'translate(-50%, 0)' }],
                                        { duration: 90, easing: 'ease-out' });
      timer = setTimeout(next, still.matches ? 0 : LINE_MS);
    }
    requestAnimationFrame(function () { printer.classList.add('is-on'); next(); });

    function dismiss(e) {
      if (e && e.target.closest && e.target.closest('a.printer-line')) return;
      clearTimeout(timer);
      document.removeEventListener('click', dismiss, true);
      document.removeEventListener('keydown', onKey);
      printer.classList.add('is-off');
      setTimeout(function () { printer.remove(); }, 350);
      if (e) { e.preventDefault(); e.stopPropagation(); }
    }
    function onKey(e) { if (e.key === 'Escape') dismiss(); }
    setTimeout(function () {
      document.addEventListener('click', dismiss, true);
      document.addEventListener('keydown', onKey);
    }, 0);
  }

  document.addEventListener('click', function (e) {
    var s = e.target.closest && e.target.closest('.print-foot .credits summary');
    if (!s) return;
    e.preventDefault();
    print(s.parentNode);
  });
})();
