// Meritum marks: shared SVG symbols (#m-a … #m-h), 48×48 grid, 4px stroke, round caps and joins.
// Accent colour comes from the inherited CSS variable --m-sea, so marks follow light/dark tokens.
(() => {
  const S = 'fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"';
  const dot = (cx, cy, r) => `<circle cx="${cx}" cy="${cy}" r="${r}" style="fill:var(--m-sea)"/>`;
  const acc = (d, w = 4) => `<path d="${d}" fill="none" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" style="stroke:var(--m-sea)"/>`;
  const comma = 'M0 -5.5a5.5 5.5 0 0 1 5.5 5.5c0 5.4-3.3 9.8-7.8 12.5a1.3 1.3 0 0 1-1.6-2c1.8-1.9 2.9-3.8 3.2-5.7A5.5 5.5 0 0 1 0 -5.5z';
  const marks = {
    'm-a': `<path ${S} d="M39.8 22.2A16 16 0 1 1 26.8 9.2"/>${dot(35.3, 13.7, 4.6)}`,
    'm-b': `<path ${S} d="M10 40V25c0-5.5 3.1-9 7-9s7 3.5 7 9v15M24 25c0-5.5 3.1-9 7-9s7 3.5 7 9v15"/>${acc('M24 25v15')}${dot(24, 7.6, 3.5)}`,
    'm-c': `<path ${S} d="M22 22.5V41"/>${dot(22, 13, 3.4)}${acc('M23.7 6.7A6.5 6.5 0 0 1 28.3 14.7M24.8 2.4A11 11 0 0 1 32.6 15.8', 2.8)}`,
    'm-d': `<path ${S} d="M6 38c3-9 5.5-18 7.6-24.4.8-2.4 2.4-2.2 3.3-.1L24 30l7.1-16.5c.9-2.1 2.5-2.3 3.3.1C36.5 20 39 29 42 38"/>${dot(24, 30, 4.4)}`,
    'm-e': `<path d="M10 31L24 24M16.5 12.5L24 24M32 12L24 24M39 30.5L24 24M24 39L24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" opacity=".5"/>` +
      `<g fill="currentColor"><circle cx="10" cy="31" r="3"/><circle cx="16.5" cy="12.5" r="3"/><circle cx="32" cy="12" r="3"/><circle cx="39" cy="30.5" r="3"/><circle cx="24" cy="39" r="3"/></g>${dot(24, 24, 4.8)}`,
    'm-f': `<path d="${comma}" transform="translate(15 25)" fill="currentColor"/><path d="${comma}" transform="translate(32 25)" style="fill:var(--m-sea)"/>`,
    'm-g': `<path ${S} d="M17 7C9.5 15 9.5 33 17 41M31 7c7.5 8 7.5 26 0 34"/>${dot(24, 24, 4.8)}`,
    'm-h': `<path ${S} d="M8 17v-5a4 4 0 0 1 4-4h5M31 8h5a4 4 0 0 1 4 4v5M40 31v5a4 4 0 0 1-4 4h-5M17 40h-5a4 4 0 0 1-4-4v-5"/>${dot(24, 24, 4.8)}`,
  };
  const defs = Object.entries(marks).map(([id, body]) => `<symbol id="${id}" viewBox="0 0 48 48">${body}</symbol>`).join('');
  document.body.insertAdjacentHTML('afterbegin', `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${defs}</defs></svg>`);
  window.MERITUM_MARKS = [
    ['A', 'Sedno', 'm-a'], ['B', 'Dwa łuki', 'm-b'], ['C', 'Kropka nad i', 'm-c'], ['D', 'Ślad M', 'm-d'],
    ['E', 'Konstelacja', 'm-e'], ['F', 'Cudzysłów', 'm-f'], ['G', 'Nawias', 'm-g'], ['H', 'Klamry', 'm-h'],
  ];
})();
