/* Interactive layer for the Group 4 infographic.
   Static PNG/PDF is produced from the same DOM with body.static. */
(function () {
  'use strict';

  var B = window.BOARD || {panels: {}, symbols: {}};
  var dlg = document.getElementById('modal');
  var dlgBody = document.getElementById('modal-body');
  var dlgHead = document.getElementById('modal-head');

  /* ---------- fit to viewport (interactive only) ---------- */
  function fit() {
    if (document.body.classList.contains('static')) return;
    var stage = document.querySelector('.stage');
    var w = (stage && stage.offsetWidth) || 2400;
    var s = Math.min(1, (window.innerWidth - 24) / w);
    document.documentElement.style.setProperty('--fit', s);
    document.body.classList.add('fit');
  }
  window.addEventListener('resize', fit);
  fit();

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function paras(arr) {
    return (arr || []).map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('');
  }
  function list(arr, cls) {
    if (!arr || !arr.length) return '';
    return '<ul class="' + (cls || '') + '">' + arr.map(function (x) {
      return '<li>' + esc(x) + '</li>';
    }).join('') + '</ul>';
  }

  function openPanel(id) {
    var p = B.panels[id];
    if (!p) return;
    var media = (p.images || []).map(function (im) {
      var src = im.src || ('../media/' + encodeURIComponent(im.f));
      var cap = im.cap || im.caption || '';
      return '<figure><img src="' + src + '" alt="' + esc(cap) + '">' +
             '<figcaption>' + esc(cap) + '</figcaption></figure>';
    }).join('');
    dlgHead.innerHTML =
      '<div><div class="k">PANEL ' + esc(p.num) + ' / 10 · ' + esc(p.tag || 'EVIDENCE FILE') + '</div>' +
      '<h2>' + esc(p.title) + '</h2><div class="era2">' + esc(p.era) + '</div></div>' +
      '<button class="m-close" data-close>CLOSE ✕</button>';
    dlgBody.innerHTML =
      (media ? '<div class="m-media">' + media + '</div>' : '') +
      '<div class="m-text">' +
        (p.arg ? '<p class="arg2">' + p.arg + '</p>' : '') +
        paras(p.notes) +
        (p.facts ? '<h3>On the panel</h3><p>' + p.facts + '</p>' : '') +
        (p.questions && p.questions.length ? '<h3>Ask the room</h3>' + list(p.questions, 'qs') : '') +
        (p.sources && p.sources.length ? '<h3>Sources</h3>' + list(p.sources, 'srcs') : '') +
        (p.note ? '<p class="note">' + esc(p.note) + '</p>' : '') +
      '</div>';
    dlg.classList.toggle('no-media', !media);
    show();
  }

  function openSymbol(key) {
    var s = B.symbols[key];
    if (!s) return;
    var src = document.querySelector('.sym[data-sym="' + key + '"] svg');
    dlgHead.innerHTML =
      '<div><div class="k">SYMBOL KEY · ' + esc(s.num) + '</div>' +
      '<h2>' + esc(s.name) + '</h2><div class="era2">' + esc(s.era) + '</div></div>' +
      '<button class="m-close" data-close>CLOSE ✕</button>';
    dlgBody.innerHTML =
      '<div class="m-media">' +
        (src ? '<div class="m-sym-icon">' + src.outerHTML + '</div>' : '') +
        (s.images || []).map(function (im) {
          return '<figure><img src="' + im.src + '" alt="' + esc(im.caption) + '">' +
                 '<figcaption>' + esc(im.caption) + '</figcaption></figure>';
        }).join('') +
      '</div>' +
      '<div class="m-text">' +
        '<p class="arg2">' + esc(s.meaning) + '</p>' +
        paras(s.notes) +
        (s.questions ? '<h3>Ask the room</h3>' + list(s.questions, 'qs') : '') +
      '</div>';
    dlg.classList.toggle('no-media', false);
    show();
  }

  function show() {
    if (typeof dlg.showModal === 'function') { try { dlg.showModal(); } catch (e) { dlg.setAttribute('open', ''); } }
    else dlg.setAttribute('open', '');
  }
  function close() {
    if (typeof dlg.close === 'function') { try { dlg.close(); } catch (e) {} }
    dlg.removeAttribute('open');
  }

  /* ---------- wiring ---------- */
  document.addEventListener('click', function (e) {
    var closeBtn = e.target.closest('[data-close]');
    if (closeBtn) { close(); return; }
    var panel = e.target.closest('[data-panel]');
    if (panel) { openPanel(panel.getAttribute('data-panel')); return; }
    var sk = e.target.closest('[data-symkey]');
    if (sk) { openSymbol(sk.getAttribute('data-symkey')); return; }
    var sy = e.target.closest('[data-sym]');
    if (sy) { openSymbol(sy.getAttribute('data-sym')); return; }
  });

  dlg.addEventListener('click', function (e) {
    if (e.target === dlg) close();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
    if ((e.key === 'Enter' || e.key === ' ') && document.activeElement &&
        document.activeElement.hasAttribute('data-panel')) {
      e.preventDefault();
      openPanel(document.activeElement.getAttribute('data-panel'));
    }
  });

  var xray = document.getElementById('xray');
  if (xray) xray.addEventListener('click', function () {
    document.body.classList.toggle('xray');
    xray.classList.toggle('on');
    xray.textContent = document.body.classList.contains('xray') ? 'RETURN TO BOARD' : 'X-RAY THE COLLAGE';
  });

  var qbtn = document.getElementById('qtoggle');
  if (qbtn) qbtn.addEventListener('click', function () {
    document.body.classList.toggle('hide-questions');
    qbtn.classList.toggle('on');
  });

  // Idle X-ray: after 3-7s of no interaction, show the collage behind the
  // panels (same effect as the X-ray button) until the pointer moves again.
  var idleTimer = null;
  var IDLE_MIN = 3000, IDLE_MAX = 7000;
  function idleDelay() { return IDLE_MIN + Math.random() * (IDLE_MAX - IDLE_MIN); }
  function clearIdleXray() { document.body.classList.remove('idle-xray'); }
  function armIdle() {
    if (idleTimer) clearTimeout(idleTimer);
    idleTimer = setTimeout(function () {
      // never fire in static/print mode, or while a panel dialog is open
      if (document.body.classList.contains('static') ||
          document.querySelector('dialog[open]')) { armIdle(); return; }
      document.body.classList.add('idle-xray');
    }, idleDelay());
  }
  function onActivity() { clearIdleXray(); armIdle(); }
  ['pointermove', 'pointerdown', 'mousemove', 'wheel', 'keydown',
   'touchstart', 'touchmove', 'focusin'].forEach(function (ev) {
    window.addEventListener(ev, onActivity, { passive: true });
  });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { if (idleTimer) clearTimeout(idleTimer); }
    else onActivity();
  });
  armIdle();

  // allow keyboard opening of banner/panels
  Array.prototype.forEach.call(document.querySelectorAll('[data-panel]'), function (el) {
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openPanel(el.getAttribute('data-panel')); }
    });
  });
})();
