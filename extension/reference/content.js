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
  const CARD = globalThis.MeritumCard;
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
    // Deployed mocks (meritum-mocks): meritum-<platform>.gburek.app, dev with a -dev suffix.
    const mock = host.match(/^meritum-(x|facebook|instagram|reddit|tiktok)(?:-dev)?\.gburek\.app$/);
    if (mock) return mock[1];
    const map = { 'x.com': 'x', 'twitter.com': 'x', 'facebook.com': 'facebook', 'instagram.com': 'instagram', 'reddit.com': 'reddit', 'tiktok.com': 'tiktok' };
    for (const [d, p] of Object.entries(map)) if (host === d || host.endsWith('.' + d)) return p;
    return null;
  }

  // ---------- per-platform adapters (selectors from demo/platforms/SELECTORS.md) ----------
  // posts(): post elements; id(p): stable post id; ad(p): sponsored?; handle/excerpt: what a check sends;
  // mountButton(p, host): put the "Sprawdź" host in the action bar, false if the bar is not rendered yet;
  // mountSlot(p, host, btnHost): put the block host (analysis strip, result card) under the post.
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
      }
    }
  };
  const AD = ADAPTERS[PLATFORM];

  // ---------- inline SVG (no <use>: ids do not cross shadow roots) ----------
  const mark = (s = 16) => `<svg class="m-mark" width="${s}" height="${s}" style="width:${s}px;height:${s}px" viewBox="0 0 48 48" aria-hidden="true"><path d="M10 40V25c0-5.5 3.1-9 7-9s7 3.5 7 9v15M24 25c0-5.5 3.1-9 7-9s7 3.5 7 9v15" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 25v15" fill="none" style="stroke:var(--m-sea)" stroke-width="4" stroke-linecap="round"/><circle cx="24" cy="7.6" r="3.5" style="fill:var(--m-sea)"/></svg>`;

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


  // ---------- copy: strings from copy/pl.json (keys mirror the contract codes) ----------
  const COPY_URL = EXT ? chrome.runtime.getURL('pl.json') : new URL('../../copy/pl.json', document.currentScript?.src || location.href).href;
  let T;

  // ---------- scanning ----------
  const mounted = new WeakMap();  // post element -> { id, btn, slot }
  const checks = new Map();       // post id -> CheckResult (restores the card when the host re-renders the post)
  let lastHref = location.href;

  function scan() {
    if (location.href !== lastHref) lastHref = location.href;
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
    btnHost.shadowRoot.innerHTML = `<button class="m-check" type="button" title="${esc(T.extension.page_hint)}">${mark(18)}<span>${esc(T.extension.check)}</span></button>`;
    const b = btnHost.shadowRoot.querySelector('button');
    b.addEventListener('click', e => { e.preventDefault(); check(entry, b); });
    const done = checks.get(id);
    if (done) { markDone(b); reveal(entry, done, false); }
  }

  const markDone = b => { b.classList.add('done'); b.removeAttribute('aria-busy'); b.querySelector('span').textContent = T.extension.checked; };

  let timer = 0;
  const schedule = () => { if (!timer) timer = setTimeout(() => { timer = 0; scan(); }, 150); };

  // ---------- check: the post's text goes out only after the click ----------
  async function check(entry, btn) {
    if (btn.getAttribute('aria-busy') === 'true') return;
    if (checks.has(entry.id)) { entry.slot.shadowRoot.querySelector('.m-card')?.scrollIntoView({ block: 'nearest', behavior: RM.matches ? 'auto' : 'smooth' }); return; }
    btn.setAttribute('aria-busy', 'true');
    btn.querySelector('span').textContent = T.form.checking;
    const text = AD.excerpt(entry.post).trim();
    const proc = document.createElement('output');
    proc.className = 'm-proc';
    entry.slot.shadowRoot.querySelectorAll('.m-proc,.m-reveal').forEach(n => n.remove());
    entry.slot.shadowRoot.append(proc);
    let result;
    try {
      result = await API.check({ channel: 'extension', text, page_url: location.href }, status => { proc.innerHTML = CARD.steps(status); });
    } catch {
      result = { check_id: '', status: 'technical_failure', corpus_version: '', message: null };
    }
    proc.style.transition = `opacity ${RM.matches ? 0 : 250}ms`; proc.style.opacity = '0';
    await wait(250);
    proc.remove();
    if (result.status !== 'technical_failure') checks.set(entry.id, result); // a failure is never kept: the next click retries
    if (result.status === 'technical_failure') { btn.removeAttribute('aria-busy'); btn.querySelector('span').textContent = T.extension.check; }
    else { markDone(btn); remember(entry, text, result); }
    reveal(entry, result, true);
  }



  function reveal(entry, result, animate) {
    const root = entry.slot.shadowRoot;
    root.querySelectorAll('.m-reveal').forEach(n => n.remove());
    const rev = document.createElement('div');
    rev.className = 'm-reveal';
    rev.innerHTML = `<div>${CARD.card(result)}</div>`;
    root.append(rev);
    if (animate) {
      rev.offsetHeight; // commit the 0fr row before opening
      rev.classList.add('open');
      rev.addEventListener('transitionend', () => rev.classList.add('settled'), { once: true });
      if (RM.matches) rev.classList.add('settled');
      const main = result.claims?.[0];
      live(main ? `${T.verdict[main.verdict]}: ${main.claim}` : T.status[result.status]);
    } else {
      rev.classList.add('open', 'settled');
      rev.querySelector('.m-card').style.animation = 'none';
    }
  }

  // ---------- storage + popup bridge (extension only) ----------
  function remember(entry, text, result) {
    if (!EXT || !chrome.storage) return;
    const item = { id: result.check_id, platform: PLATFORM, handle: AD.handle(entry.post), excerpt: text.slice(0, 120), at: Date.now(), verdict: result.claims?.[0]?.verdict || null, status: result.status };
    chrome.storage.local.get({ checks: [] }, ({ checks: list }) => chrome.storage.local.set({ checks: [item, ...list].slice(0, 20) }));
  }
  if (EXT && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((msg, _s, reply) => {
      if (msg?.type !== 'meritum:summary') return;
      reply({ platform: PLATFORM, checked: checks.size });
    });
  }

  // ---------- start ----------
  async function start() {
    if (EXT && chrome.storage) {
      const { paused = [] } = await chrome.storage.local.get('paused');
      if (paused.includes(location.hostname.replace(/^www\./, ''))) return; // shortcut: needs a reload after "Włącz", fine for a reference
    }
    [, T] = await Promise.all([loadSheet(), fetch(COPY_URL).then(r => r.json())]);
    CARD.use(T);
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
  }
  start().catch(err => console.warn('[Meritum]', err));
})();
