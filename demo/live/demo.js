// Stage-demo control for demo/live/*: reset (R), theme (T), speed-up. Bottom-left, Meritum surface,
// clearly not part of the mocked platform. Speed-up sets window.MERITUM_SPEED, read by content.js.
(() => {
  let fast = false;
  try { fast = sessionStorage.getItem('meritum-live-fast') === '1'; } catch {}
  window.MERITUM_SPEED = fast ? 3 : 1;

  const host = document.createElement('meritum-root');
  host.setAttribute('data-part', 'demo');
  host.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:2147483500;display:block';
  const root = host.attachShadow({ mode: 'open' });
  root.innerHTML = `<link rel="stylesheet" href="../../../extension/widget.css">
  <style>
   .ctl{display:flex;align-items:center;gap:6px;padding:6px;border:1px solid var(--m-line);border-radius:999px;background:var(--m-card);box-shadow:var(--m-shadow);font:600 12px var(--m-brand);color:var(--m-ink2)}
   .ctl .who{display:flex;align-items:center;gap:6px;padding:0 6px 0 4px;color:var(--m-ink)}
   .m-btn{padding:5px 11px;font-size:12px}
   kbd{font:600 11px var(--m-mono);color:var(--m-ink2);margin-left:4px}
   .m-btn[aria-pressed="true"] kbd{color:inherit}
  </style>
  <div class="ctl" role="group" aria-label="Sterowanie pokazem Meritum (dane symulowane)">
   <span class="who"><svg width="16" height="16" viewBox="0 0 48 48" aria-hidden="true"><path d="M10 40V25c0-5.5 3.1-9 7-9s7 3.5 7 9v15M24 25c0-5.5 3.1-9 7-9s7 3.5 7 9v15" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 25v15" fill="none" style="stroke:var(--m-sea)" stroke-width="4" stroke-linecap="round"/><circle cx="24" cy="7.6" r="3.5" style="fill:var(--m-sea)"/></svg>Pokaz, dane symulowane</span>
   <button class="m-btn" type="button" data-a="reset">Od nowa<kbd>R</kbd></button>
   <button class="m-btn" type="button" data-a="theme">Motyw<kbd>T</kbd></button>
   <button class="m-btn" type="button" data-a="fast" aria-pressed="${fast}">Przyspiesz</button>
  </div>`;
  document.body.append(host);

  const sync = () => host.classList.toggle('dark', document.documentElement.dataset.mockTheme === 'dark');
  new MutationObserver(sync).observe(document.documentElement, { attributes: true, attributeFilter: ['data-mock-theme'] });
  sync();

  const act = a => {
    if (a === 'reset') location.reload();
    if (a === 'theme') document.querySelector('[data-mock-theme-toggle]')?.click();
    if (a === 'fast') {
      fast = !fast; window.MERITUM_SPEED = fast ? 3 : 1;
      root.querySelector('[data-a="fast"]').setAttribute('aria-pressed', String(fast));
      try { sessionStorage.setItem('meritum-live-fast', fast ? '1' : '0'); } catch {}
    }
  };
  root.addEventListener('click', e => { const b = e.target.closest('[data-a]'); if (b) act(b.dataset.a); });
  addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.composedPath()[0];
    if (t?.matches?.('input, textarea, [contenteditable]')) return;
    if (e.key === 'r' || e.key === 'R') act('reset');
    if (e.key === 't' || e.key === 'T') act('theme');
  });
})();
