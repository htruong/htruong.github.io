// The printouts on the desk form a pile. Opening a document from a listing
// puts its page down on top: the listing tips askew underneath as the new page
// slides in over it, and the address changes to the document's own (which
// still works on its own, reloaded or shared). Clicking the listing showing
// under a document takes the document away and straightens the listing again.
// Back and forward swap pages without the slide. Anything unusual (another
// site, a modifier key, no fetch) is left to the browser.
(function () {
  if (!window.fetch || !history.pushState || !document.querySelector('.stack')) return;
  var still = matchMedia('(prefers-reduced-motion: reduce)');
  var busy = false;
  var EASE = 'cubic-bezier(.2, .8, .25, 1)';
  var UNDER = 'translate(-2.4rem, 0.8rem) rotate(1.9deg)';   // as .under-sheet in desk70.scss

  function pageFrom(html) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    var stack = doc.querySelector('.stack');
    return stack && { stack: stack, title: doc.title, layout: doc.body.className };
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

  function finish(oldStack, fresh, page) {
    oldStack.replaceWith(fresh);
    document.body.className = page.layout;
    wakeScripts(fresh);
    if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
    busy = false;
  }

  // Run an animation, and carry on even if it never gets to run (a hidden tab)
  function play(anims, done) {
    var over = false;
    function end() { if (over) return; over = true; anims.forEach(function (a) { a.cancel(); }); done(); }
    if (anims.length) anims[0].onfinish = end;
    setTimeout(end, 1000);
  }

  // A document put down on top of what's open now
  function putDown(page) {
    var oldStack = document.querySelector('.stack');
    var oldMain = oldStack.querySelector('main.printout'), oldUnder = oldStack.querySelector('.under-sheet');
    var fresh = document.importNode(page.stack, true);
    var newMain = fresh.querySelector('main.printout');
    scrollTo({ top: 0, behavior: 'instant' });
    // Lay the new page in place over the old, and slide it up from below while
    // the old one tips over into the place of the sheet underneath
    fresh.classList.add('is-arriving');
    fresh.style.top = oldStack.offsetTop + 'px';
    oldStack.parentNode.insertBefore(fresh, oldStack.nextSibling);
    var drop = innerHeight - oldStack.getBoundingClientRect().top + 40;
    var anims = [newMain.animate([
      { transform: 'translateY(' + drop + 'px) rotate(2.5deg)' },
      { transform: 'translateY(-6px) rotate(-0.3deg)', offset: 0.82 },
      { transform: 'none' }
    ], { duration: 620, easing: EASE })];
    var newUnder = fresh.querySelector('.under-sheet');
    if (newUnder) newUnder.style.visibility = 'hidden';
    anims.push(oldMain.animate([{ transform: 'none' }, { transform: UNDER }], { duration: 520, easing: EASE, fill: 'forwards' }));
    if (oldUnder) anims.push(oldUnder.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 300, fill: 'forwards' }));
    play(anims, function () {
      fresh.classList.remove('is-arriving');
      fresh.style.top = '';
      if (newUnder) newUnder.style.visibility = '';
      finish(oldStack, fresh, page);
    });
  }

  // The document on top taken away, uncovering the listing under it
  function takeAway(page) {
    var oldStack = document.querySelector('.stack');
    var oldMain = oldStack.querySelector('main.printout'), oldUnder = oldStack.querySelector('.under-sheet');
    var fresh = document.importNode(page.stack, true);
    var y = scrollY;
    scrollTo({ top: 0, behavior: 'instant' });
    var lift = innerHeight + 80;
    var anims = [oldMain.animate([
      { transform: 'translateY(' + (-y) + 'px)' },
      { transform: 'translateY(' + (lift - y) + 'px) rotate(3deg)' }
    ], { duration: 520, easing: 'cubic-bezier(.5, 0, .75, .4)', fill: 'forwards' })];
    if (oldUnder) {
      oldUnder.classList.add('is-rising');
      anims.push(oldUnder.animate([{ transform: UNDER }, { transform: 'none' }], { duration: 560, easing: EASE, fill: 'forwards' }));
    }
    play(anims, function () { finish(oldStack, fresh, page); });
  }

  function go(url, push, how) {
    if (busy) return;
    busy = true;
    fetch(url, { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.text();
    }).then(function (html) {
      var page = pageFrom(html);
      if (!page) throw new Error('no printout');
      document.title = page.title;
      if (push) history.pushState({ desk: true }, '', url);
      if (how === 'down' && !still.matches) return putDown(page);
      if (how === 'away' && !still.matches) return takeAway(page);
      scrollTo(0, 0);
      finish(document.querySelector('.stack'), document.importNode(page.stack, true), page);
    }).catch(function () { location.href = url; });
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var t = e.target.closest && e.target.closest('.lp-rows a, .under-sheet');
    if (!t || t.target || t.origin !== location.origin || t.pathname === location.pathname) return;
    e.preventDefault();
    go(t.href, true, t.classList.contains('under-sheet') ? 'away' : 'down');
  });

  history.replaceState({ desk: true }, '');
  addEventListener('popstate', function (e) {
    if (!e.state || !e.state.desk) return;
    go(location.href, false, null);
  });
})();
