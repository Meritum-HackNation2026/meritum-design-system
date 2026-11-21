// Shared by welcome.html and options.html: binds [data-setting] inputs to chrome.storage.local
// (falls back to localStorage when the page is opened outside the extension, e.g. for design review).
(async () => {
  const EXT = !!globalThis.chrome?.storage;
  const DEFAULTS = { theme: 'auto', paused: [], checks: [] };
  const local = {
    get: async () => { try { return { ...DEFAULTS, ...JSON.parse(localStorage.getItem('meritum-settings') || '{}') }; } catch { return { ...DEFAULTS }; } },
    set: async v => { try { localStorage.setItem('meritum-settings', JSON.stringify({ ...(await local.get()), ...v })); } catch {} }
  };
  const store = EXT ? { get: () => chrome.storage.local.get(DEFAULTS), set: v => chrome.storage.local.set(v) } : local;
  const q = new URLSearchParams(location.search);
  let s = await store.get();
  const saved = document.querySelector('[data-saved]');
  const say = msg => { if (saved) saved.textContent = msg; };

  const applyTheme = t => {
    if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t;
    else delete document.documentElement.dataset.theme;
  };
  applyTheme(q.get('theme') || s.theme);

  for (const el of document.querySelectorAll('[data-setting]')) {
    const key = el.dataset.setting;
    if (key === 'theme') el.checked = el.value === s.theme;
    else if (key === 'site') el.checked = !s.paused.includes(el.value);
    el.addEventListener('change', async () => {
      if (key === 'theme') { applyTheme(el.value); await store.set({ theme: el.value }); }
      if (key === 'site') {
        s = await store.get();
        const paused = el.checked ? s.paused.filter(h => h !== el.value) : [...new Set([...s.paused, el.value])];
        await store.set({ paused });
      }
      say('Zapisano.');
    });
  }

  document.querySelector('[data-clear]')?.addEventListener('click', async () => {
    await store.set({ checks: [] });
    say('Historia sprawdzeń na tym komputerze została usunięta.');
  });
  document.querySelector('[data-close]')?.addEventListener('click', () => window.close());
  const v = document.querySelector('[data-version]');
  if (v && EXT) v.textContent = chrome.runtime.getManifest().version;
})();
