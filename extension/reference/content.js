// Meritum reference content script (Manifest V3, no framework).
// Runs as an extension content script on the real sites and on the local mocks, and as a plain <script>
// on demo/live/* (then api.js must be loaded first and widget.css sits at ../widget.css next to this file).
(() => {
  // One instance per document, even if both the demo page and the installed extension load it (two JS worlds, one DOM).
  if (document.documentElement.hasAttribute('data-meritum-active')) return;

  const PLATFORM = detectPlatform();
  if (!PLATFORM) return;
  document.documentElement.setAttribute('data-meritum-active', PLATFORM);

  const EXT = !!globalThis.chrome?.runtime?.getURL;
  const CSS_URL = EXT ? chrome.runtime.getURL('widget.css') : new URL('../widget.css', document.currentScript?.src || location.href).href;
  const API = globalThis.MeritumAPI;
  const RM = matchMedia('(prefers-reduced-motion: reduce)');
  // demo pages may set window.MERITUM_SPEED (e.g. 3); the extension always runs at 1
  const wait = ms => new Promise(r => setTimeout(r, RM.matches ? Math.min(ms, 120) : ms / (window.MERITUM_SPEED || 1)));
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const safeUrl = u => /^https:\/\//.test(u) ? esc(u) : '#';
  const textId = s => { let h = 0; for (const c of s.slice(0, 300)) h = (h * 31 + c.charCodeAt(0)) | 0; return 'h' + (h >>> 0).toString(36); };

  function detectPlatform() {
    const m = location.pathname.match(/\/demo\/(?:platforms|live)\/(x|facebook|instagram|reddit|tiktok)\//);
    if (m) return m[1];
    const host = location.hostname;
    const map = { 'x.com': 'x', 'twitter.com': 'x', 'facebook.com': 'facebook', 'instagram.com': 'instagram', 'reddit.com': 'reddit', 'tiktok.com': 'tiktok' };
    for (const [d, p] of Object.entries(map)) if (host === d || host.endsWith('.' + d)) return p;
    return null;
  }

  // ---------- per-platform adapters (selectors from demo/platforms/SELECTORS.md) ----------
  // posts(): post elements; id(p): stable post id; ad(p): sponsored?; handle/excerpt: for the report;
  // mountButton(p, host): put the "Zgłoś" host in the action bar, false if the bar is not rendered yet;
  // mountSlot(p, host, btnHost): put the block host (analysis strip, card) under the post; hideTarget(p): what "Ukryj reklamę" hides.
  const SPONSORED = /^(Sponsorowane|Sponsored|Reklama|Promowane|Promoted|Ad)$/;
  const hasLabel = (p, sel) => $$(sel, p).some(e => SPONSORED.test(e.textContent.trim()));
  const ADAPTERS = {
    x: {
      posts: () => $$('article[data-testid="tweet"]'),
      id: p => $('a[href*="/status/"]', p)?.getAttribute('href').replace(/\/(analytics|photo).*$/, '') || textId(p.textContent),
      ad: p => !!p.closest('[data-testid="placementTracking"]'),
      handle: p => $$('[data-testid="User-Name"] a', p).map(a => a.textContent.trim()).find(t => t.startsWith('@')) || '',
      excerpt: p => $('[data-testid="tweetText"]', p)?.innerText || '',
      mountButton: (p, host) => {
        const g = $('[role="group"]', p); if (!g) return false;
        const bm = $('[data-testid="bookmark"]', g);
        g.insertBefore(host, bm ? [...g.children].find(c => c.contains(bm)) : null);
        return true;
      },
      mountSlot: (p, host) => $('[role="group"]', p).after(host),
      hideTarget: p => p
    },
    facebook: {
      posts: () => [...new Set($$('[data-ad-rendering-role="profile_name"]').map(n => n.closest('[data-virtualized]')).filter(p => p && p.dataset.virtualized !== 'true'))],
      id: p => $('a[href*="/posts/"],a[href*="/videos/"],a[href*="story_fbid"]', p)?.getAttribute('href') || textId(p.textContent),
      // FB splits "Sponsorowane" into hidden letters, so read the link's aria-label, not textContent
      ad: p => !!$('a[aria-label="Sponsorowane"],a[aria-label="Sponsored"]', p),
      handle: p => $('[data-ad-rendering-role="profile_name"]', p)?.textContent.trim() || '',
      excerpt: p => $('[data-ad-preview="message"]', p)?.innerText || '',
      mountButton: (p, host) => {
        const share = $('[data-ad-rendering-role="share_button"]', p)?.closest('[role="button"]'); if (!share) return false;
        share.parentElement.append(host); return true;
      },
      mountSlot: (p, host, btn) => btn.parentElement.after(host),
      hideTarget: p => p
    },
    instagram: {
      posts: () => $$('main article'),
      id: p => $('a[href*="/p/"],a[href*="/reel/"]', p)?.getAttribute('href') || textId(p.textContent),
      ad: p => hasLabel(p, 'span'),
      handle: p => $('a[role="link"]', p)?.textContent.trim() || '',
      excerpt: p => $$('span[dir="auto"]', p).map(s => s.innerText).join(' '),
      mountButton: (p, host) => {
        const share = $('svg[aria-label="Udostępnij"],svg[aria-label="Share"]', p)?.closest('[role="button"]'); if (!share) return false;
        share.parentElement.append(host); return true;
      },
      mountSlot: (p, host, btn) => btn.closest('section').after(host),
      hideTarget: p => p
    },
    reddit: {
      // the action row lives in the post's shadow root and may be re-rendered, so we add our own light-DOM row after the post
      posts: () => $$('shreddit-post, shreddit-ad-post'),
      id: p => p.id || p.getAttribute('permalink') || textId(p.textContent),
      ad: p => p.localName === 'shreddit-ad-post' || p.hasAttribute('promoted'),
      handle: p => p.getAttribute('subreddit-prefixed-name') || ('u/' + (p.getAttribute('author') || '')),
      excerpt: p => `${p.getAttribute('post-title') || ''} ${$('[slot="text-body"]', p)?.innerText || ''}`,
      mountButton: (p, host) => { p.after(host); return true; },
      mountSlot: (p, host, btn) => btn.after(host),
      hideTarget: p => p.closest('article') || p
    },
    tiktok: {
      posts: () => $$('article[data-e2e="recommend-list-item-container"]'),
      id: p => ($('a[href*="/video/"]', p)?.getAttribute('href')) || textId(($('[data-e2e="video-desc"]', p)?.textContent || '') + p.id),
      ad: p => hasLabel(p, 'span'),
      handle: p => $('a[href*="/@"]:not([data-e2e])', p)?.textContent.trim() || '',
      excerpt: p => $('[data-e2e="video-desc"]', p)?.innerText || '',
      mountButton: (p, host) => {
        const share = $('[data-e2e="share-icon"]', p); if (!share) return false;
        share.after(host); return true;
      },
      // no room under a full-height video: the slot floats over the bottom of the video
      mountSlot: (p, host) => {
        const media = $('[data-e2e="feed-video"]', p)?.parentElement || p;
        if (getComputedStyle(media).position === 'static') media.style.position = 'relative';
        // inline, because host-page CSS outranks :host rules
        host.style.cssText = 'position:absolute;left:12px;right:12px;bottom:12px;z-index:5;max-height:calc(100% - 24px);overflow:auto;border-radius:8px';
        media.append(host);
      },
      hideTarget: p => $('[data-e2e="feed-video"]', p)?.parentElement || p
    }
  };
  const AD = ADAPTERS[PLATFORM];

  // ---------- inline SVG (no <use>: ids do not cross shadow roots) ----------
  const mark = (s = 16) => `<svg class="m-mark" width="${s}" height="${s}" style="width:${s}px;height:${s}px" viewBox="0 0 48 48" aria-hidden="true"><path d="M10 40V25c0-5.5 3.1-9 7-9s7 3.5 7 9v15M24 25c0-5.5 3.1-9 7-9s7 3.5 7 9v15" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 25v15" fill="none" style="stroke:var(--m-sea)" stroke-width="4" stroke-linecap="round"/><circle cx="24" cy="7.6" r="3.5" style="fill:var(--m-sea)"/></svg>`;
  const ICONS = {
    x: '<svg class="m-ic" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2l8 8M10 2l-8 8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    lock: '<svg class="m-ic" viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>',
    check: '<svg class="m-ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
  };

  // ---------- styles: one constructed sheet shared by every shadow root ----------
  let SHEET;
  async function loadSheet() {
    const text = await (await fetch(CSS_URL)).text();
    const fonts = new CSSStyleSheet();
    fonts.replaceSync((text.match(/@font-face\s*{[^}]*}/g) || []).join('\n'));
    document.adoptedStyleSheets = [...document.adoptedStyleSheets, fonts];
    SHEET = new CSSStyleSheet();
    SHEET.replaceSync(text);
  }

  // ---------- theme: luminance of the computed page background ----------
  let dark = false;
  function pageIsDark() {
    for (const el of [document.body, document.documentElement]) {
      if (!el) continue;
      const c = getComputedStyle(el).backgroundColor;
      const n = (c.match(/[\d.]+/g) || []).map(Number);
      if (n.length < 3 || (n.length > 3 && n[3] < 0.5)) continue;
      const k = c.startsWith('color(') ? 255 : 1;
      const lin = v => { v = v * k / 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * lin(n[0]) + 0.7152 * lin(n[1]) + 0.0722 * lin(n[2]) < 0.4;
    }
    return matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function applyTheme() {
    const d = pageIsDark();
    if (d === dark) return;
    dark = d;
    for (const h of document.querySelectorAll('meritum-root')) h.classList.toggle('dark', dark);
  }

  // ---------- hosts ----------
  // <meritum-root> is a valid custom element name, so attachShadow works without customElements.define
  // (content scripts have no customElements registry) and host CSS like `div[role=group] > div` never matches it.
  function mkHost(part) {
    const el = document.createElement('meritum-root');
    el.dataset.part = part; el.dataset.host = PLATFORM;
    el.classList.toggle('dark', dark);
    const root = el.attachShadow({ mode: 'open' }); // shortcut: open for debugging, switch to 'closed' in production
    root.adoptedStyleSheets = [SHEET];
    if (part !== 'overlay') {
      // keep our clicks and keys away from the host (X opens the post on click and has single-key shortcuts)
      for (const t of ['click', 'keydown', 'keyup', 'keypress']) root.addEventListener(t, e => e.stopPropagation());
    }
    return el;
  }

  let overlay;
  function ov() {
    if (overlay?.isConnected) return overlay.shadowRoot;
    overlay = mkHost('overlay');
    overlay.shadowRoot.innerHTML = '<div class="m-sr" role="status" aria-live="polite"></div>';
    document.body.append(overlay);
    return overlay.shadowRoot;
  }
  const live = msg => { ov().querySelector('[role="status"]').textContent = msg; };
  function toast(msg) {
    const r = ov();
    r.querySelectorAll('.m-toast').forEach(t => t.remove());
    const t = document.createElement('div');
    t.className = 'm-toast'; t.setAttribute('role', 'status');
    t.innerHTML = `${mark(16)}<span>${esc(msg)}</span>`;
    r.append(t);
    setTimeout(() => t.remove(), 3300);
  }

  // ---------- scanning ----------
  const mounted = new WeakMap();  // post element -> { id, btn, slot }
  const reports = new Map();      // post id -> { result } after a successful send (restores cards on re-render)
  let lastHref = location.href;

  function scan() {
    if (location.href !== lastHref) { lastHref = location.href; closePop(false); }
    for (const p of AD.posts()) {
      const id = AD.id(p), m = mounted.get(p);
      if (m && m.id === id && m.btn.isConnected) continue;  // already done
      if (m) { m.btn.remove(); m.slot.remove(); }           // node recycled for another post, or host re-rendered it
      // a cloned post (cloneNode copies our element but not its shadow root) carries dead hosts: drop them
      for (const dead of (p.parentElement || p).querySelectorAll('meritum-root')) if (!dead.shadowRoot) dead.remove();
      inject(p, id);
    }
  }

  function inject(p, id) {
    const btnHost = mkHost('button');
    if (!AD.mountButton(p, btnHost)) return;
    const slotHost = mkHost('slot');
    AD.mountSlot(p, slotHost, btnHost);
    const entry = { id, post: p, btn: btnHost, slot: slotHost };
    mounted.set(p, entry);
    btnHost.shadowRoot.innerHTML = `<button class="m-report" type="button" aria-haspopup="dialog" aria-expanded="false" title="Zgłoś treść do Meritum">${mark(18)}<span>Zgłoś</span></button>`;
    const b = btnHost.shadowRoot.querySelector('button');
    b.addEventListener('click', e => { e.preventDefault(); openReport(entry); });
    const done = reports.get(id);
    if (done) { markDone(b); if (done.result) reveal(entry, done.result, false); }
  }

  const markDone = b => { b.classList.add('done'); b.setAttribute('aria-disabled', 'true'); b.querySelector('span').textContent = 'Zgłoszono'; };

  let timer = 0;
  const schedule = () => { if (!timer) timer = setTimeout(() => { timer = 0; scan(); }, 150); };

  // ---------- report popover ----------
  const REASONS = {
    manip: ['Fałszywa informacja', 'Teoria spiskowa', 'Wyrwane z kontekstu', 'Fałszywy autorytet', 'Zmanipulowane zdjęcie lub wideo'],
    scam: ['Fałszywy wizerunek znanej osoby', 'Podejrzana inwestycja', 'Podszywanie się pod bank lub urząd', 'Fałszywy sklep lub zbiórka']
  };
  let open = null;
  let busy = false; // a send is running; the popover stays put until it finishes

  function closePop(restoreFocus = true) {
    if (!open || busy) return;
    const { pop, btn, onMove } = open; open = null;
    btn.setAttribute('aria-expanded', 'false');
    removeEventListener('scroll', onMove, true); removeEventListener('resize', onMove);
    pop.classList.add('out');
    setTimeout(() => pop.remove(), RM.matches ? 0 : 320);
    if (restoreFocus) btn.focus();
  }

  // the spec wants the popover under the button; above it only when the page cannot scroll to make room (TikTok)
  function place(pop, btn, forceBelow) {
    const r = btn.getBoundingClientRect(), w = pop.offsetWidth, h = pop.offsetHeight, m = 12;
    const below = r.bottom + 6, above = r.top - 6 - h;
    const up = !forceBelow && below + h > innerHeight - m && above >= m;
    pop.classList.toggle('up', up);
    pop.style.top = Math.max(m, Math.min(up ? above : below, innerHeight - h - m)) + 'px';
    pop.style.left = Math.max(m, Math.min(r.right - w, innerWidth - w - m)) + 'px';
  }

  function openReport(entry) {
    const btn = entry.btn.shadowRoot.querySelector('button');
    if (open && open.btn === btn) return closePop();
    closePop(false);
    if (busy) return;
    if (reports.has(entry.id)) return toast('To zgłoszenie już wysłałeś. Dziękujemy.');
    const isAd = AD.ad(entry.post), kind = isAd ? 'scam' : 'manip';
    const handle = AD.handle(entry.post);
    const pop = document.createElement('div');
    pop.className = 'm-pop'; pop.setAttribute('role', 'dialog'); pop.setAttribute('aria-modal', 'true'); pop.setAttribute('aria-labelledby', 'm-pop-t');
    pop.innerHTML = `
     <div class="m-pop-h">${mark(20)}<div><strong id="m-pop-t">Zgłoś treść</strong><div class="who">${isAd ? 'Reklama' : 'Post'} ${esc(handle)}</div></div>
      <button class="m-x" type="button" aria-label="Zamknij">${ICONS.x}</button></div>
     <form novalidate>
      <div class="m-seg" role="radiogroup" aria-label="Rodzaj zgłoszenia">
       <label><input type="radio" name="k" value="manip" ${kind === 'manip' ? 'checked' : ''}>Manipulacja</label>
       <label><input type="radio" name="k" value="scam" ${kind === 'scam' ? 'checked' : ''}>Oszustwo</label></div>
      <fieldset><legend class="m-lbl">Co jest nie tak? Wybierz jedno lub więcej</legend><div class="m-chips"></div></fieldset>
      <label><span class="m-lbl">Albo opisz własnymi słowami</span><textarea class="m-field" rows="2" placeholder="Np. to nagranie jest z 2019 roku"></textarea></label>
      <label><span class="m-lbl">Link do źródła (opcjonalnie)</span><input class="m-field" type="url" inputmode="url" placeholder="https://"></label>
      <div class="m-hint">${ICONS.lock}<span>Dowód zapiszemy sami: zrzut ekranu, adres i czas. Zgłoszenie jest anonimowe.</span></div>
      <div class="m-err" role="alert" hidden>Nie udało się wysłać. Sprawdź połączenie i spróbuj ponownie; twoje odpowiedzi zostały w formularzu.</div>
      <button class="m-send" type="submit" disabled><span class="bar"></span><span class="lab">Wyślij zgłoszenie</span></button>
     </form>`;
    ov().append(pop);
    const onMove = () => requestAnimationFrame(() => { if (!btn.isConnected) return closePop(false); if (open) place(pop, btn, open.below); });
    open = { pop, btn, entry, onMove, below: false };
    btn.setAttribute('aria-expanded', 'true');

    const chips = $('.m-chips', pop), ta = $('textarea', pop), url = $('input[type="url"]', pop), send = $('.m-send', pop);
    const validate = () => { send.disabled = !(chips.querySelector('input:checked') || ta.value.trim().length >= 3); };
    const fill = k => { chips.innerHTML = REASONS[k].map(r => `<label class="m-chip"><input type="checkbox" value="${esc(r)}">${esc(r)}</label>`).join(''); validate(); };
    fill(kind);
    // no room below: scroll the page up to make room, if it can scroll that far (onMove re-places during the scroll)
    const r = btn.getBoundingClientRect(), need = r.bottom + 6 + pop.offsetHeight + 12 - innerHeight;
    const root = document.scrollingElement;
    if (need > 0 && root.scrollHeight - innerHeight - root.scrollTop >= need) {
      open.below = true;
      scrollBy({ top: need, behavior: RM.matches ? 'auto' : 'smooth' });
    }
    place(pop, btn, open.below);
    addEventListener('scroll', onMove, true);  // capture: also catches TikTok's inner scroll container
    addEventListener('resize', onMove);

    pop.addEventListener('change', e => { if (e.target.name === 'k') fill(e.target.value); else validate(); });
    ta.addEventListener('input', validate);
    $('.m-x', pop).addEventListener('click', () => closePop());
    for (const t of ['keyup', 'keypress']) pop.addEventListener(t, e => e.stopPropagation());
    pop.addEventListener('keydown', e => {
      e.stopPropagation();
      if (e.key !== 'Tab') return;
      // focus trap: Tab cycles inside the dialog
      const f = $$('button:not(:disabled), input, textarea', pop).filter(el => el.type !== 'radio' || el.checked);
      const first = f[0], last = f[f.length - 1], cur = pop.getRootNode().activeElement;
      if (e.shiftKey && cur === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && cur === last) { e.preventDefault(); first.focus(); }
    });
    $('form', pop).addEventListener('submit', e => {
      e.preventDefault();
      if (send.disabled) return;
      submit(entry, btn, pop, send, {
        platform: PLATFORM, postId: entry.id,
        kind: $('.m-seg input:checked', pop).value,
        reasons: $$('.m-chips input:checked', pop).map(i => i.value),
        text: ta.value.trim(), source: url.value.trim(),
        snapshot: { handle, isAd, excerpt: AD.excerpt(entry.post).slice(0, 500), url: location.href }
      });
    });
    setTimeout(() => $('.m-seg input:checked', pop).focus(), 30);
  }

  async function submit(entry, btn, pop, send, report) {
    busy = true;
    const err = $('.m-err', pop), lab = $('.lab', send);
    err.hidden = true;
    send.disabled = true; send.classList.add('sending');
    lab.textContent = 'Wysyłanie…'; live('Wysyłanie zgłoszenia');
    let res;
    try { [res] = await Promise.all([API.submitReport(report), wait(950)]); }
    catch {
      busy = false;
      send.classList.remove('sending'); send.disabled = false; lab.textContent = 'Wyślij zgłoszenie';
      err.hidden = false; live('Nie udało się wysłać zgłoszenia');
      return;
    }
    send.classList.remove('sending'); send.classList.add('sent');
    lab.innerHTML = `${ICONS.check}Wysłane`;
    live('Zgłoszenie wysłane');
    await wait(650);
    busy = false;
    closePop(false);
    reports.set(entry.id, { result: res.result });
    remember(report, res);
    markDone(btn);
    btn.focus();
    analyse(entry, res);
  }

  async function analyse(entry, res) {
    const proc = document.createElement('div');
    proc.className = 'm-proc'; proc.setAttribute('role', 'status');
    proc.innerHTML = `<div class="m-proc-h">${mark(14)}Meritum analizuje zgłoszenie</div><ol>${res.steps.map(s => `<li><i></i>${esc(s)}</li>`).join('')}</ol>`;
    entry.slot.shadowRoot.append(proc);
    for (const li of proc.querySelectorAll('li')) { li.className = 'on'; live(li.textContent); await wait(1000); li.className = 'ok'; }
    await wait(350);
    if (!res.result) {
      proc.outerHTML = `<div class="m-inline">${mark(16)}<span>Dziękujemy. To pierwsze zgłoszenie tego posta. Notatka powstaje, gdy podobnych zgłoszeń będzie więcej.</span></div>`;
      live('Zgłoszenie przyjęte');
      return;
    }
    proc.style.transition = `opacity ${RM.matches ? 0 : 250}ms`; proc.style.opacity = '0';
    await wait(250);
    proc.remove();
    reveal(entry, res.result, true);
  }

  // ---------- cards ----------
  const sourceRows = sources => sources.map(s => `<div class="m-row"><span class="k">Źródło</span><a href="${safeUrl(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.label)}</a><small>${esc(s.domain)}, ${esc(s.kind)}</small></div>`).join('');
  const techRow = t => `<div class="m-row m-t" tabindex="0"><span class="k">Technika</span><span>${esc(t.name)}</span><small>jak rozpoznać?</small><span class="m-tip l">${esc(t.tip)}</span></div>`;

  function noteCard(n) {
    const c = n.consensus, verified = n.status === 'verified';
    return `<section class="m-card" aria-label="Meritum: kontekst od społeczności">
     <div class="m-top">${mark(14)}Meritum<span class="m-t why" tabindex="0">Dlaczego to widzę?<span class="m-tip r">${esc(n.why)}</span></span></div>
     <div class="m-ttl"><b>${esc(n.title)}</b><span class="m-badge ${verified ? 'ok' : 'pend'} m-t" tabindex="0">${verified ? 'Zweryfikowany' : 'W ocenie'}<span class="m-tip r">${esc(n.statusTip)}</span></span></div>
     <p>${esc(n.body)}</p>
     <div class="m-rows">${sourceRows(n.sources)}${n.technique ? techRow(n.technique) : ''}</div>
     <div class="m-cons"><div class="bars m-t" tabindex="0"><i><b style="width:${+c.a.pct}%"></b><u style="right:${+c.threshold}%"></u></i><em></em><i><b style="width:${+c.b.pct}%"></b><u style="left:${+c.threshold}%"></u></i><span class="m-tip">${esc(c.tip)}</span></div>
      <div class="lab"><span>Grupa A: ${+c.a.pct}% pomocne, <span class="m-num">${+c.a.votes}</span> ocen</span><span>Grupa B: ${+c.b.pct}%, <span class="m-num">${+c.b.votes}</span> ocen</span></div></div>
     <div class="m-acts"><button class="m-btn" type="button" aria-pressed="false" data-vote>Pomocne</button><button class="m-btn" type="button" aria-pressed="false" data-vote>Niepomocne</button>
      <span class="m-t why" tabindex="0">Jak powstała?<span class="m-tip r">${esc(n.how)}</span></span></div>
    </section>`;
  }

  function scamCard(s) {
    const at = new Date(s.evidence.at).toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    return `<section class="m-card scam" aria-label="Meritum: ostrzeżenie o oszustwie">
     <div class="m-top">${mark(14)}Meritum<span class="m-t why" tabindex="0">Dlaczego to widzę?<span class="m-tip r">${esc(s.why)}</span></span></div>
     <div class="m-ttl"><b>${esc(s.title)}</b><span class="m-badge bad">Oszustwo</span></div>
     <p>${esc(s.body)}</p>
     <div class="m-rows">
      <div class="m-row m-t" tabindex="0"><span class="k">Kampania</span><span><b class="m-num">${esc(s.campaign.id)}</b>: ${esc(s.campaign.summary)}</span><small><a href="#" data-camp>zobacz kampanię</a></small><span class="m-tip l">${esc(s.campaign.tip)}</span></div>
      ${sourceRows(s.sources)}
      <div class="m-row m-t" tabindex="0"><span class="k">Dowód</span><span>Zapisany o <span class="m-num">${esc(at)}</span>: ${esc(s.evidence.summary)}</span><small>${ICONS.lock}</small><span class="m-tip l">${esc(s.evidence.tip)}</span></div>
      ${techRow(s.technique)}
     </div>
     <div class="m-acts"><button class="m-btn p" type="button" data-hide>Ukryj reklamę</button><button class="m-btn" type="button" data-platform>Zgłoś platformie</button>
      <span class="m-t why" tabindex="0">To pomyłka?<span class="m-tip r">${esc(s.dispute)}</span></span></div>
    </section>`;
  }

  function reveal(entry, result, animate) {
    const root = entry.slot.shadowRoot;
    root.querySelectorAll('.m-reveal').forEach(n => n.remove());
    const rev = document.createElement('div');
    rev.className = 'm-reveal';
    rev.innerHTML = `<div>${result.type === 'scam' ? scamCard(result) : noteCard(result)}</div>`;
    root.append(rev);
    if (animate) {
      rev.offsetHeight; // commit the 0fr row before opening
      rev.classList.add('open');
      rev.addEventListener('transitionend', () => rev.classList.add('settled'), { once: true });
      if (RM.matches) rev.classList.add('settled');
      live(result.type === 'scam' ? 'Oznaczono reklamę jako oszustwo' : 'Opublikowano notatkę kontekstową');
    } else {
      rev.classList.add('open', 'settled');
      rev.querySelector('.m-card').style.animation = 'none';
    }
    rev.querySelectorAll('[data-vote]').forEach(b => b.addEventListener('click', () => {
      rev.querySelectorAll('[data-vote]').forEach(o => o.setAttribute('aria-pressed', String(o === b && o.getAttribute('aria-pressed') !== 'true')));
      if (b.getAttribute('aria-pressed') === 'true') toast('Dziękujemy za ocenę. Liczy się w twojej grupie perspektyw.');
    }));
    rev.querySelector('[data-camp]')?.addEventListener('click', e => { e.preventDefault(); toast(`Widok kampanii ${result.campaign.id} otwiera się w panelu analityka.`); });
    rev.querySelector('[data-platform]')?.addEventListener('click', () => toast('Paczka dowodów gotowa dla platformy i CERT Polska.'));
    rev.querySelector('[data-hide]')?.addEventListener('click', () => hideAd(entry, result));
  }

  function hideAd(entry, result) {
    const target = AD.hideTarget(entry.post);
    const ph = mkHost('placeholder');
    if (PLATFORM === 'tiktok') { const r = target.getBoundingClientRect(); ph.style.cssText = `display:block;width:${r.width}px;height:${r.height}px;flex:none`; }
    ph.shadowRoot.innerHTML = `<div class="hidden-ad">${mark(16)}<span>Reklama ukryta przez Meritum: fałszywa reklama z kampanii <span class="m-num">${esc(result.campaign?.id || '')}</span>.</span><button class="m-btn" type="button">Pokaż</button></div>`;
    target.before(ph);
    const prev = target.style.display;
    target.style.display = 'none';
    const show = ph.shadowRoot.querySelector('button');
    show.addEventListener('click', () => { ph.remove(); target.style.display = prev; });
    show.focus();
    live('Reklama ukryta');
  }

  // ---------- storage + popup bridge (extension only) ----------
  const STATUS = { note: 'verified', scam: 'scam' };
  function remember(report, res) {
    if (!EXT || !chrome.storage) return;
    const item = { id: res.id, platform: PLATFORM, handle: report.snapshot.handle, excerpt: report.snapshot.excerpt.slice(0, 120), at: Date.now(), status: STATUS[res.result?.type] || 'review' };
    chrome.storage.local.get({ reports: [] }, ({ reports: list }) => chrome.storage.local.set({ reports: [item, ...list].slice(0, 20) }));
  }
  if (EXT && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((msg, _s, reply) => {
      if (msg?.type !== 'meritum:summary') return;
      let scam = 0, notes = 0;
      for (const r of reports.values()) { if (r.result?.type === 'scam') scam++; else if (r.result) notes++; }
      reply({ platform: PLATFORM, scam, notes });
    });
  }

  // ---------- start ----------
  async function start() {
    if (EXT && chrome.storage) {
      const { paused = [] } = await chrome.storage.local.get('paused');
      if (paused.includes(location.hostname.replace(/^www\./, ''))) return; // shortcut: needs a reload after "Włącz", fine for a reference
    }
    await loadSheet();
    dark = pageIsDark();
    scan();
    // one observer for the feed; throttled, so a burst of React commits costs one scan
    new MutationObserver(muts => {
      if (muts.every(m => [...m.addedNodes, ...m.removedNodes].every(n => n.localName === 'meritum-root'))) return;
      schedule();
    }).observe(document.body, { childList: true, subtree: true });
    // theme hooks: X = body style, FB/IG/Reddit = class on <html>, TikTok = data-theme
    const themeObs = new MutationObserver(() => requestAnimationFrame(applyTheme));
    for (const el of [document.documentElement, document.body]) themeObs.observe(el, { attributes: true, attributeFilter: ['class', 'style', 'data-theme'] });
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
    // Esc closes the popover wherever focus is (capture: runs before the host page and before our stopPropagation)
    addEventListener('keydown', e => { if (e.key === 'Escape' && open) { e.preventDefault(); e.stopPropagation(); closePop(); } }, true);
    // outside click closes the popover (capture, because our own hosts stop click propagation)
    addEventListener('pointerdown', e => {
      const path = e.composedPath();
      if (open && !path.includes(open.pop) && !path.includes(open.entry.btn)) closePop(false);
    }, true);
  }
  start().catch(err => console.warn('[Meritum]', err));
})();
