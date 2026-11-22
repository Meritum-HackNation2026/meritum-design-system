// Input check of the popup paste box. Keep in step with toRequest() in components/meritum/check-form.tsx
// (tests/test_popup_input.py compares the limits). Returns a CheckRequest or an `errors` key from copy/pl.json.
(() => {
  const MAX = 4000;
  const MAX_URL = 2083; // CheckRequest.url maxLength in the contract
  const toRequest = (raw, channel = 'extension') => {
    const value = raw.trim();
    if (/^\S+$/.test(value) && /^([a-z][a-z\d+.-]*:\/\/|www\.)/i.test(value)) {
      try {
        const url = new URL(value);
        if (url.protocol !== 'http:' && url.protocol !== 'https:') return 'invalid_url';
        return url.href.length > MAX_URL ? 'url_too_long' : { channel, url: url.href };
      } catch { return 'invalid_url'; }
    }
    if (value.length > MAX) return 'too_long';
    return value.length < 3 ? 'empty' : { channel, text: value };
  };
  globalThis.MeritumInput = { toRequest };
})();
