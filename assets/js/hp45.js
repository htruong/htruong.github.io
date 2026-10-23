// The HP-45's arithmetic: an RPN calculator with the four-level stack (X, Y, Z,
// T), ENTER, LAST x, nine storage registers, and the HP-45's keyboard, gold
// (shifted) functions included. Its display is 15 seven-segment cells, shown
// in FIX 2 when switched on, as the real one is. No page code in here.
var HP45 = (function () {
  // The gold function above each key, reached with the orange prefix key
  var GOLD = {
    recip: 'pow', ln: 'log', exp: 'tenx', fix: 'sci', sq: 'sqrt', polar: 'rect',
    sin: 'asin', cos: 'acos', tan: 'atan', swap: 'fact', roll: 'mean', sto: 'todms',
    rcl: 'fromdms', pct: 'dpct', enter: 'deg', chs: 'rad', eex: 'grd', clx: 'clear',
    '7': 'cmin', '8': 'kglb', '9': 'ltrgal', '0': 'lastx', dot: 'pi', sigma: 'sigmaminus'
  };
  var ANGLE = { deg: Math.PI / 180, rad: 1, grd: Math.PI / 200 };

  function fact(n) {
    if (n < 0 || n !== Math.floor(n) || n > 69) return NaN;
    var r = 1;
    for (var i = 2; i <= n; i++) r *= i;
    return r;
  }

  // Everything a function needs: x alone, or y and x, and the angle mode
  var UNARY = {
    recip: function (x) { return 1 / x; },
    sq: function (x) { return x * x; },
    sqrt: function (x) { return x < 0 ? NaN : Math.sqrt(x); },
    ln: function (x) { return x <= 0 ? NaN : Math.log(x); },
    log: function (x) { return x <= 0 ? NaN : Math.log10(x); },
    exp: function (x) { return Math.exp(x); },
    tenx: function (x) { return Math.pow(10, x); },
    fact: fact,
    sin: function (x, a) { return Math.sin(x * a); },
    cos: function (x, a) { return Math.cos(x * a); },
    tan: function (x, a) { return Math.tan(x * a); },
    asin: function (x, a) { return Math.asin(x) / a; },
    acos: function (x, a) { return Math.acos(x) / a; },
    atan: function (x, a) { return Math.atan(x) / a; },
    cmin: function (x) { return x * 2.54; },          // inches to centimetres
    kglb: function (x) { return x * 0.45359237; },    // pounds to kilograms
    ltrgal: function (x) { return x * 3.785411784; }  // US gallons to litres
  };
  var BINARY = {
    add: function (y, x) { return y + x; },
    sub: function (y, x) { return y - x; },
    mul: function (y, x) { return y * x; },
    div: function (y, x) { return x === 0 ? NaN : y / x; },
    pow: function (y, x) { return Math.pow(y, x); }
  };

  // Seven-segment glyphs: which of a-g each character lights
  var GLYPH = {
    '0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc', '5': 'afgcd',
    '6': 'afgedc', '7': 'abc', '8': 'abcdefg', '9': 'abcdfg', '-': 'g', 'E': 'afged',
    'r': 'eg', 'o': 'cdeg', ' ': ''
  };

  function Calc() { this.reset(); }

  Calc.prototype.reset = function () {
    this.x = this.y = this.z = this.t = 0;
    this.lastx = 0;
    this.reg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    this.lift = false;
    this.entry = null;
    this.gold = false;
    this.prefix = null;
    this.fix = 2;
    this.sci = false;
    this.angle = 'deg';
    this.error = false;
  };

  Calc.prototype.push = function (v) {
    if (this.lift) { this.t = this.z; this.z = this.y; this.y = this.x; }
    this.x = v;
    this.lift = true;
  };

  Calc.prototype.entryValue = function () {
    var e = this.entry;
    var s = (e.neg ? '-' : '') + (e.m === '' || e.m === '.' ? '0' : e.m);
    if (e.e !== null) s += 'e' + (e.eneg ? '-' : '') + (e.e || '0');
    return parseFloat(s);
  };

  Calc.prototype.finishEntry = function () {
    if (!this.entry) return;
    this.x = this.entryValue();
    this.entry = null;
    this.lift = true;
  };

  Calc.prototype.result = function (v) {
    if (!isFinite(v) || Math.abs(v) >= 1e100) { this.error = true; return; }
    this.x = Math.abs(v) < 1e-99 ? 0 : v;
    this.lift = true;
  };

  Calc.prototype.press = function (key) {
    if (this.error) { this.error = false; if (key === 'clx') { this.x = 0; this.lift = false; return; } }
    if (this.prefix) {
      var p = this.prefix;
      this.prefix = null;
      if (/^[0-9]$/.test(key)) {
        var n = +key;
        if (p === 'fix' || p === 'sci') { this.finishEntry(); this.fix = n; this.sci = p === 'sci'; }
        else if (p === 'sto') { this.finishEntry(); this.reg[n] = this.x; this.lift = true; }
        else if (p === 'rcl') { this.finishEntry(); this.push(this.reg[n]); }
        return;
      }
    }
    if (key === 'shift') { this.gold = !this.gold; return; }
    if (this.gold) { this.gold = false; key = GOLD[key] || key; }

    // number entry
    if (/^[0-9]$/.test(key) || key === 'dot' || key === 'eex') {
      if (!this.entry) {
        if (this.lift) { this.t = this.z; this.z = this.y; this.y = this.x; }
        this.entry = { m: '', neg: false, e: null, eneg: false };
        this.lift = false;
      }
      var e = this.entry;
      if (key === 'eex') {
        if (e.e === null) { if (e.m === '' || e.m === '.') e.m = '1'; e.e = ''; }
      } else if (e.e !== null) {
        if (key !== 'dot') e.e = (e.e + key).slice(-2);
      } else if (key === 'dot') {
        if (e.m.indexOf('.') < 0) e.m += (e.m === '' ? '0.' : '.');
      } else if (e.m.replace('.', '').length < 10) {
        e.m = (e.m === '0' ? '' : e.m) + key;
      }
      this.x = this.entryValue();
      return;
    }
    if (key === 'chs') {
      if (this.entry) {
        if (this.entry.e !== null) this.entry.eneg = !this.entry.eneg;
        else this.entry.neg = !this.entry.neg;
        this.x = this.entryValue();
      } else {
        this.x = -this.x;
      }
      return;
    }

    this.finishEntry();
    var x = this.x, y = this.y;
    if (BINARY[key]) {
      this.lastx = x;
      this.x = y; this.y = this.z; this.z = this.t;
      return this.result(BINARY[key](y, x));
    }
    if (UNARY[key]) {
      this.lastx = x;
      return this.result(UNARY[key](x, ANGLE[this.angle]));
    }
    switch (key) {
      case 'enter': this.t = this.z; this.z = this.y; this.y = x; this.lift = false; return;
      case 'clx': this.x = 0; this.lift = false; return;
      case 'clear': this.x = this.y = this.z = this.t = 0; this.lift = false; return;
      case 'swap': this.x = y; this.y = x; this.lift = true; return;
      case 'roll': this.x = y; this.y = this.z; this.z = this.t; this.t = x; this.lift = true; return;
      case 'lastx': this.push(this.lastx); return;
      case 'pi': this.push(Math.PI); return;
      case 'pct': this.lastx = x; return this.result(y * x / 100);        // y stays
      case 'dpct': this.lastx = x; return this.result((x - y) / y * 100); // y stays
      case 'deg': case 'rad': case 'grd': this.angle = key; return;
      case 'sto': case 'rcl': case 'fix': case 'sci': this.prefix = key; return;
    }
    // the rest (polar/rectangular, degrees-minutes-seconds, statistics) aren't modelled
    this.lift = true;
  };

  // What the display shows: 15 cells of { ch, dp }
  Calc.prototype.cells = function () {
    var out = [], i;
    function put(ch) { out.push({ ch: ch, dp: false }); }
    if (this.error) {
      'Error'.split('').forEach(put);
    } else if (this.entry) {
      var e = this.entry;
      put(e.neg ? '-' : ' ');
      for (i = 0; i < e.m.length; i++) {
        if (e.m[i] === '.') { if (out.length === 1) put('0'); out[out.length - 1].dp = true; }
        else put(e.m[i]);
      }
      if (e.m === '') put('0');
      if (e.e !== null) {
        while (out.length < 12) put(' ');
        put(e.eneg ? '-' : ' ');
        var ex = ('00' + e.e).slice(-2);
        put(ex[0]); put(ex[1]);
      }
    } else {
      var x = this.x, n = this.fix;
      var big = Math.abs(x) >= 1e10, small = x !== 0 && Math.abs(x) < 0.5 * Math.pow(10, -n);
      put(x < 0 ? '-' : ' ');
      if (this.sci || big || small) {
        var s = Math.abs(x).toExponential(Math.min(n, 8)), parts = s.split('e');
        var m = parts[0], exp = +parts[1];
        for (i = 0; i < m.length; i++) { if (m[i] === '.') out[out.length - 1].dp = true; else put(m[i]); }
        if (m.indexOf('.') < 0) out[out.length - 1].dp = true;
        while (out.length < 12) put(' ');
        put(exp < 0 ? '-' : ' ');
        var ed = ('00' + Math.abs(exp)).slice(-2);
        put(ed[0]); put(ed[1]);
      } else {
        // as many decimals as asked for, as long as the number fits in 10 digits
        var intDigits = Math.max(1, Math.floor(Math.log10(Math.abs(x) || 1)) + 1);
        var f = Math.abs(x).toFixed(Math.max(0, Math.min(n, 10 - intDigits)));
        for (i = 0; i < f.length; i++) { if (f[i] === '.') out[out.length - 1].dp = true; else put(f[i]); }
        if (f.indexOf('.') < 0) out[out.length - 1].dp = true;
      }
    }
    while (out.length < 15) put(' ');
    return out.slice(0, 15).map(function (c) { return { ch: c.ch, dp: c.dp, segs: GLYPH[c.ch] || '' }; });
  };

  return Calc;
})();
if (typeof module !== 'undefined') module.exports = HP45;
