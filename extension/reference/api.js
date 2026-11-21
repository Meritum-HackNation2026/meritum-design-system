// Meritum API mock. Same shape the real backend should return; swap the body of submitReport() for a
// message to background.js, which does the real fetch (content scripts are bound by the host page's CORS).
//
// submitReport(report) -> Promise<{ id, steps: string[], result: null | NoteResult | ScamResult }>
//   report = { platform, postId, kind: 'manip'|'scam', reasons: string[], text: string, source: string,
//              snapshot: { handle, excerpt, isAd, url } }
//   steps   = what the analysis strip shows, in order
//   result  = null when there is nothing to show yet (first report of an ordinary post)
(() => {
  const delay = ms => new Promise(r => setTimeout(r, ms));
  const FLAT = /płask|krzywizn/i;
  const SCAM = /Rewiński|inwest-polska24|Finanse Dziś|finanse_dzis/i;

  const NOTE = {
    type: 'note',
    status: 'verified',                // 'verified' -> „Zweryfikowany”, 'review' -> „W ocenie”
    title: 'Kontekst od społeczności',
    why: 'Szkic AI z uwag 57 osób i 3 źródeł. Opublikowany, bo zgodziły się dwie grupy, które zwykle oceniają inaczej.',
    statusTip: 'Obie grupy przekroczyły próg 70% ocen „pomocne”.',
    body: 'Kształt Ziemi zmierzono na wiele sposobów: zdjęcia z orbity, pomiary satelitów GPS i obserwacje, które każdy może powtórzyć, np. statki znikające za horyzontem od dołu. Z samolotu pasażerskiego krzywizna jest ledwo widoczna, bo leci on nisko w stosunku do rozmiaru Ziemi.',
    sources: [
      { label: 'NASA: fakty o Ziemi', url: 'https://science.nasa.gov/earth/facts/', domain: 'science.nasa.gov', kind: 'instytucja' },
      { label: 'ESA: obserwacje Ziemi z orbity', url: 'https://www.esa.int/Applications/Observing_the_Earth', domain: 'esa.int', kind: 'instytucja' },
      { label: 'Wikipedia: Ziemia', url: 'https://pl.wikipedia.org/wiki/Ziemia', domain: 'pl.wikipedia.org', kind: 'encyklopedia' }
    ],
    technique: { name: 'Fałszywy autorytet i teoria spiskowa', tip: '„Pilot z 20-letnim stażem” bez nazwiska i źródła, a każdy dowód przeciw nazwany fałszerstwem: to znak teorii spiskowej.' },
    consensus: { threshold: 70, a: { pct: 88, votes: 231 }, b: { pct: 84, votes: 198 }, tip: 'Kreska na każdym pasku to próg 70%. Głosy kont z klastrów botów nie są liczone.' },
    how: 'AI napisała szkic. O publikacji zdecydowali ludzie, a źródła są obowiązkowe.'
  };

  const scam = () => ({
    type: 'scam',
    title: 'Fałszywa reklama',
    why: 'Dwa niezależne sygnały: domena jest na liście ostrzeżeń CERT Polska, a reklama pasuje do znanej kampanii oszustów.',
    body: 'Tomasz Rewiński nie poleca tej inwestycji: jego wizerunek użyto bez zgody. Strona zbiera dane karty i numer telefonu. Nie podawaj tam żadnych danych.',
    campaign: { id: '#K-118', summary: '47 reklam, 23 domeny w 9 dni', tip: 'Ta sama twarz, ten sam szablon strony i ten sam wystawca certyfikatów co 46 innych reklam.' },
    sources: [
      { label: 'CERT Polska: lista ostrzeżeń', url: 'https://cert.pl/lista-ostrzezen/', domain: 'cert.pl', kind: 'instytucja' },
      { label: 'Oświadczenie T. Rewińskiego', url: 'https://example.org/oswiadczenie', domain: 'profil oficjalny', kind: 'przykład' }
    ],
    evidence: { at: new Date().toISOString(), summary: 'zrzut, adres, 3 przekierowania', tip: 'Reklama może zniknąć za kilka godzin. Dowód zostaje i da się go wysłać do CERT Polska.' },
    technique: { name: 'Fałszywy autorytet i presja czasu', tip: 'Znana twarz plus „zostało 12 miejsc”: prawdziwe inwestycje nie znikają do jutra.' },
    dispute: 'Każde ostrzeżenie można zakwestionować. Trafia wtedy do ponownej oceny przez ludzi.'
  });

  async function submitReport(report) {
    await delay(300);
    if (navigator.onLine === false) throw new Error('offline');
    const id = 'R-' + Math.random().toString(36).slice(2, 8).toUpperCase();
    const hay = `${report.snapshot?.handle || ''} ${report.snapshot?.excerpt || ''}`;
    if (SCAM.test(hay)) return { id, result: scam(), steps: ['Zapisujemy dowód: zrzut, adres, przekierowania', 'Porównujemy z kampaniami: pasuje #K-118', 'Sprawdzamy domenę na liście CERT Polska'] };
    if (FLAT.test(hay)) return { id, result: NOTE, steps: ['Łączymy z 56 podobnymi zgłoszeniami', 'Zbieramy źródła: NASA, ESA i 4 media', 'AI pisze szkic, oceniają dwie grupy'] };
    return { id, result: null, steps: ['Zapisujemy zgłoszenie'] };
  }

  globalThis.MeritumAPI = { submitReport };
})();
