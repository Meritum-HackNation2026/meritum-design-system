// Meritum API mock for the reference extension and demo/live. Same shapes as the contracts (contracts/meritum.ts):
//   check(request: CheckRequest, onStatus: (AnalysisStatus & { draft?: boolean }) => void) -> Promise<CheckResult>
// The real build sends POST /api/v1/checks through background.js (content scripts are bound by the host page's CORS)
// and follows AnalysisStatus until `result` arrives.
//
// The answers below are fixed examples for the stage demo: their sources are real institutions, but the fragments
// are illustrative, which every card says in "Ograniczenia". Nothing here may reach the jury's evaluation.
(() => {
  const SPEED = () => window.MERITUM_SPEED || 1;
  const delay = ms => new Promise(r => setTimeout(r, ms / SPEED()));
  const NOW = new Date().toISOString().slice(0, 10);
  const EXAMPLE = 'Przykład do pokazu: fragmenty źródeł są ilustracyjne, a nie pobrane w tym sprawdzeniu.';

  const src = (id, title, publisher, publisher_id, url, kind, tier, published_at) => ({
    id, title, publisher, publisher_id, url, domain: new URL(url).hostname, kind, tier, published_at, fetched_at: `${NOW}T08:00:00+01:00`,
  });

  // "Ziemia jest płaska": settled by two fact-checkers (secondary): moderate strength by rule.
  const FLAT = {
    status: 'done',
    claims: [{
      claim: 'Z samolotu pasażerskiego nie widać krzywizny Ziemi, bo Ziemia jest płaska.',
      claim_date: NOW, claim_date_source: 'today', verdict: 'false',
      strength: { level: 'moderate', premises: { independent_sources: 2, primary_sources: 0, newest_source_published_at: '2025-03-14T00:00:00+01:00', validity: 'past_event', agreement: 'consistent' } },
      citations: [
        { source: src('demagog-plaska-ziemia', 'Demagog: płaska Ziemia (wyniki wyszukiwania)', 'Stowarzyszenie Demagog', 'demagog', 'https://demagog.org.pl/?s=p%C5%82aska+ziemia', 'fact_check', 'secondary', '2025-03-14T00:00:00+01:00'),
          fragment: 'Krzywizna Ziemi jest słabo widoczna z wysokości przelotowej samolotu, co nie oznacza, że Ziemia jest płaska.', stance: 'refutes', validity: 'past_event' },
        { source: src('afp-sprawdzam-ziemia', 'AFP Sprawdzam: kształt Ziemi (wyniki wyszukiwania)', 'AFP Sprawdzam', 'afp-sprawdzam', 'https://sprawdzam.afp.com/list?search=ziemia', 'fact_check', 'secondary', '2024-09-02T00:00:00+02:00'),
          fragment: 'Zdjęcia satelitarne i pomiary geodezyjne potwierdzają, że Ziemia ma kształt zbliżony do kuli.', stance: 'refutes', validity: 'past_event' },
      ],
      explanation: 'Z wysokości około 10 km krzywizna jest ledwo widoczna, bo samolot leci nisko względem rozmiaru Ziemi. Fact-checkerzy opisują to jako znany argument zwolenników płaskiej Ziemi.',
      technique: 'conspiracy_theory',
    }],
    limitations: ['Opieramy się na ustaleniach fact-checkerów, nie na pomiarach.', EXAMPLE],
  };

  // Celebrity investment ad: nothing in the catalogue, so an honest abstention and a moderator case.
  const AD = {
    status: 'done',
    claims: [{
      claim: 'Tomasz Rewiński poleca inwestycję, na której zarabia 1 200 zł dziennie.',
      claim_date: NOW, claim_date_source: 'input_published_at', verdict: 'insufficient_evidence',
      citations: [],
      explanation: 'W zatwierdzonych źródłach nie ma wypowiedzi tej osoby o takiej inwestycji. Nie rozstrzygamy, czy reklama kłamie, dopóki źródło tego nie potwierdzi.',
      unresolved: 'Czy Tomasz Rewiński wypowiadał się o tej inwestycji w swoich oficjalnych kanałach.',
      technique: 'impersonation',
      incident: { incident_id: 'cert-inwestycje', matched_on: 'domain', title: 'Fałszywe inwestycje z wizerunkiem znanych osób', date: '2025-06-10', url: 'https://cert.pl/lista-ostrzezen/', similarity: 0.82 },
    }],
    escalation: { state: 'created', case_id: '#S-4' },
    limitations: ['Nie oceniamy samej reklamy ani firmy, tylko twierdzenie o wypowiedzi.', EXAMPLE],
  };

  const OUT = { status: 'out_of_scope', claims: [], message: null, limitations: [] };

  const RULES = [
    [/płask|krzywizn/i, FLAT],
    [/Rewiński|inwest-polska24|1 200 zł/i, AD],
  ];

  const STEPS = ['receive', 'fetch_url', 'screen_injection', 'extract_claims', 'search_corpus', 'search_web', 'search_fact_checks', 'assess_evidence', 'verify_citations', 'write_answer', 'save_record'];
  const PARALLEL = ['search_corpus', 'search_web', 'search_fact_checks'];

  async function check(request, onStatus) {
    if (navigator.onLine === false) throw new Error('offline');
    const check_id = 'c_' + Math.random().toString(36).slice(2, 8);
    const steps = STEPS.map(code => ({ code, status: 'pending' }));
    const set = (codes, status) => { for (const s of steps) if (codes.includes(s.code)) s.status = status; };
    const emit = draft => onStatus?.({ check_id, steps: steps.map(s => ({ ...s })), draft });
    const answer = RULES.find(([re]) => re.test(request.text || ''))?.[1] || OUT;

    for (const code of STEPS.slice(0, 4)) {
      set([code], code === 'fetch_url' && !request.url ? 'skipped' : 'active'); emit();
      if (steps.find(s => s.code === code).status === 'active') { await delay(450); set([code], 'done'); }
    }
    if (answer === OUT) {
      set(STEPS.slice(4, 10), 'skipped'); set(['save_record'], 'done'); emit(); await delay(300);
    } else {
      set(PARALLEL, 'active'); emit(); await delay(900);
      set(['search_corpus', 'search_fact_checks'], 'done'); emit(); await delay(500);
      set(['search_web'], 'done'); set(['assess_evidence'], 'active'); emit(); await delay(700);
      set(['assess_evidence'], 'done'); set(['verify_citations'], 'active'); emit(true); await delay(700);
      for (const code of ['verify_citations', 'write_answer', 'save_record']) { set([code], 'done'); emit(); await delay(250); }
    }
    return { check_id, corpus_version: `${NOW}.1`, ai_disclosure: true, ...structuredClone(answer) };
  }

  globalThis.MeritumAPI = { check };
})();
