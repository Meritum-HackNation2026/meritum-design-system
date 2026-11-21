// Meritum background service worker (stub).
// Real build: this is where API calls go (content scripts are bound by the host page's CORS and CSP),
// e.g. chrome.runtime.onMessage 'meritum:submit' -> fetch(API + '/reports') -> reply with { id, steps, result }.
chrome.runtime.onInstalled.addListener(({ reason }) => {
  if (reason !== 'install') return;
  chrome.storage.local.set({ paused: [], reports: [], theme: 'auto', guardian: false });
  chrome.tabs.create({ url: chrome.runtime.getURL('onboarding/welcome.html') });
});
