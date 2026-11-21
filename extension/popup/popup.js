// Toolbar popup. Preview outside the extension: popup.html?state=active|paused|unsupported|offline&theme=light|dark
// (sample data from the markup). Inside the extension it reads the active tab, chrome.storage and the content script.
(async () => {
  const q = new URLSearchParams(location.search);
  const EXT = !!globalThis.chrome?.storage;
  const $ = s => document.querySelector(s);
  const PLATFORMS = { 'x.com': 'X', 'twitter.com': 'X', 'facebook.com': 'Facebook', 'instagram.com': 'Instagram', 'reddit.com': 'Reddit', 'tiktok.com': 'TikTok' };
  const platformOf = host => Object.entries(PLATFORMS).find(([d]) => host === d || host.endsWith('.' + d))?.[1];
  const STATUS = { verified: ['ok', 'Zweryfikowany'], scam: ['bad', 'Oszustwo'], review: ['pend', 'W ocenie'] };
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const plural = (n, one, few, many) => n === 1 ? one : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) ? few : many;

  let theme = q.get('theme'), state = q.get('state'), host = q.get('host') || 'x.com', tab;
  if (EXT) {
    const s = await chrome.storage.local.get({ theme: 'auto', paused: [], reports: [], guardian: false });
    theme = theme || s.theme;
    [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    try { host = new URL(tab.url).hostname.replace(/^www\./, ''); } catch { host = ''; }
    if (!state) state = !navigator.onLine ? 'offline' : !platformOf(host) ? 'unsupported' : s.paused.includes(host) ? 'paused' : 'active';
    $('[data-guard]').textContent = s.guardian ? 'Włączony' : 'Wyłączony';
    renderReports(s.reports);
    if (state === 'active') {
      const sum = await chrome.tabs.sendMessage(tab.id, { type: 'meritum:summary' }).catch(() => null);
      if (sum) renderSummary(sum);
    }
  }
  if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme;
  render(state || 'active');

  function render(st) {
    document.body.dataset.state = st;
    $('#site-name').textContent = host;
    $('[data-host-name]').textContent = host;
    const sw = $('[data-site-switch] input');
    sw.checked = st === 'active' || st === 'offline';
    $('[data-site-switch]').hidden = st === 'unsupported';
    $('[data-site-state]').textContent = {
      active: 'Meritum działa na tej stronie', paused: 'Wstrzymane na tej stronie',
      unsupported: 'Ta strona nie jest obsługiwana', offline: 'Meritum działa, ale nie ma połączenia'
    }[st];
    $('[data-offline]').hidden = st !== 'offline';
    $('[data-found]').hidden = st !== 'active';
    $('[data-paused]').hidden = st !== 'paused';
    $('[data-unsupported]').hidden = st !== 'unsupported';
  }

  function renderSummary({ scam, notes }) {
    const parts = [];
    if (scam) parts.push(`${scam} ${plural(scam, 'ostrzeżenie', 'ostrzeżenia', 'ostrzeżeń')} o oszustwie`);
    if (notes) parts.push(`${notes} ${plural(notes, 'notatka', 'notatki', 'notatek')}`);
    $('[data-summary]').textContent = parts.join(', ') || 'Na razie nic. Zgłoś post, który budzi wątpliwości.';
    $('[data-found-list]').hidden = true; // shortcut: per-item list needs the content script to send items, not counts
  }

  function renderReports(list) {
    if (!list.length) { $('[data-reports]').innerHTML = '<li class="m">Jeszcze nic nie zgłosiłeś. Przycisk „Zgłoś” jest pod każdym postem.</li>'; return; }
    $('[data-reports]').innerHTML = list.slice(0, 3).map(r => {
      const [cls, word] = STATUS[r.status] || STATUS.review;
      const t = new Date(r.at).toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' });
      return `<li><span class="grow"><span class="t">${esc(r.excerpt)}</span><span class="m">${esc(PLATFORMS[r.platform + '.com'] || r.platform)}, <span class="num">${esc(r.handle)}</span>, <span class="num">${t}</span></span></span><span class="badge ${cls}">${word}</span></li>`;
    }).join('');
  }

  async function setPaused(paused) {
    if (EXT) {
      const { paused: list = [] } = await chrome.storage.local.get('paused');
      await chrome.storage.local.set({ paused: paused ? [...new Set([...list, host])] : list.filter(h => h !== host) });
      chrome.tabs.reload(tab.id); // the content script reads the setting on load
    }
    render(paused ? 'paused' : 'active');
  }
  $('[data-site-switch] input').addEventListener('change', e => setPaused(!e.target.checked));
  $('[data-resume]').addEventListener('click', () => setPaused(false));
  $('[data-retry]').addEventListener('click', () => render(navigator.onLine ? 'active' : 'offline'));
})();
