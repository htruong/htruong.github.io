// Opening a document from a listing puts its printout down on the desk, on top
// of the one you're reading: the new page is fetched, slid in over the old one,
// and the address changes to the document's own (which still works on its own,
// reloaded or shared). Back and forward swap pages the same way, without the
// slide. Anything unusual (another site, a modifier key, no fetch) is left to
// the browser.
(function () {
  if (!window.fetch || !history.pushState || !document.querySelector('main.printout')) return;
  var still = matchMedia('(prefers-reduced-motion: reduce)');
  var busy = false;

  function pageFrom(html) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    var main = doc.querySelector('main.printout');
    return main && { main: main, title: doc.title, layout: doc.body.className };
  }

  // Scripts in fetched markup don't run by themselves (the comments loader)
  function wakeScripts(el) {
    Array.prototype.forEach.call(el.querySelectorAll('script'), function (old) {
      var s = document.createElement('script');
      Array.prototype.forEach.call(old.attributes, function (a) { s.setAttribute(a.name, a.value); });
      s.textContent = old.textContent;
      old.replaceWith(s);
    });
  }

  function swapIn(page, url, push, slide) {
    var old = document.querySelector('main.printout');
    var fresh = document.importNode(page.main, true);
    document.title = page.title;
    if (push) history.pushState({ desk: true }, '', url);
    var settled = false;
    function settle() {
      if (settled) return;
      settled = true;
      fresh.classList.remove('is-arriving');
      fresh.style.top = '';
      old.replaceWith(fresh);
      document.body.className = page.layout;
      wakeScripts(fresh);
      if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
      busy = false;
    }
    if (!slide || still.matches) { scrollTo(0, 0); settle(); return; }
    // Lay the new sheet over the old one, where the old one's top is now
    // (after going back to the top of the page), and slide it in from below
    scrollTo({ top: 0, behavior: 'instant' });
    var top = old.getBoundingClientRect().top;
    fresh.classList.add('is-arriving');
    fresh.style.top = top + 'px';
    old.parentNode.insertBefore(fresh, old.nextSibling);
    var a = fresh.animate([
      { transform: 'translate(-50%, 0) translateY(' + (innerHeight - top + 40) + 'px) rotate(2.5deg)' },
      { transform: 'translate(-50%, 0) translateY(-6px) rotate(-0.3deg)', offset: 0.82 },
      { transform: 'translate(-50%, 0)' }
    ], { duration: 620, easing: 'cubic-bezier(.2, .8, .25, 1)' });
    a.onfinish = settle;
    // and settle anyway if the animation never gets to run (a hidden tab)
    setTimeout(function () { a.cancel(); settle(); }, 900);
  }

  function go(url, push, slide) {
    if (busy) return;
    busy = true;
    fetch(url, { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.text();
    }).then(function (html) {
      var page = pageFrom(html);
      if (!page) throw new Error('no printout');
      swapIn(page, url, push, slide);
    }).catch(function () { location.href = url; });
  }

  // Documents opened from a listing: the index, a topic, See also
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.lp-rows a');
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.target || a.origin !== location.origin || a.pathname === location.pathname) return;
    e.preventDefault();
    go(a.href, true, true);
  });

  history.replaceState({ desk: true }, '');
  addEventListener('popstate', function (e) {
    if (!e.state || !e.state.desk) return;
    go(location.href, false, false);
  });
})();
