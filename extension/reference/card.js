// Meritum result card and analysis strip as HTML strings, shared by content.js (under a post) and the popup.
// Same structure as components/meritum/result-card.tsx and analysis-steps.tsx; styles in ../widget.css.
// Render inside a <meritum-root> shadow root that adopts widget.css. T is copy/pl.json.
(() => {
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const safeUrl = u => /^https:\/\//.test(u) ? esc(u) : '#';
  const mark = (s = 16) => `<svg class="m-mark" width="${s}" height="${s}" style="width:${s}px;height:${s}px" viewBox="0 0 48 48" aria-hidden="true"><path d="M10 40V25c0-5.5 3.1-9 7-9s7 3.5 7 9v15M24 25c0-5.5 3.1-9 7-9s7 3.5 7 9v15" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 25v15" fill="none" style="stroke:var(--m-sea)" stroke-width="4" stroke-linecap="round"/><circle cx="24" cy="7.6" r="3.5" style="fill:var(--m-sea)"/></svg>`;
  const fill = (tpl, v) => tpl.replace(/\{(\w+)\}/g, (m, k) => (k in v ? v[k] : m));
  const DATE = new Intl.DateTimeFormat('pl-PL', { day: 'numeric', month: 'long', year: 'numeric' });
  const day = iso => DATE.format(new Date(iso));
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  let T;
  const citation = c => {
    const s = c.source;
    const meta = s.published_at ? fill(T.result.source_meta, { publisher: s.publisher, date: day(s.published_at) }) : fill(T.result.source_undated, { publisher: s.publisher });
    return `<li><a href="${safeUrl(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)}</a>
      <span class="m-sub">${esc(meta)}. ${esc(cap(T.source_kind[s.kind]))}, ${esc(T.source_tier[s.tier])}${s.via === 'web_search' ? `, ${esc(T.result.via_web)}` : ''}.</span>
      <blockquote class="m-frag"><span class="m-sr">${esc(T.result.fragment)}: </span>„${esc(c.fragment)}”</blockquote></li>`;
  };
  const LEVEL = { strong: 3, moderate: 2, weak: 1 };

  function claimBlock(c) {
    const cits = c.citations || [];
    const conflict = c.verdict === 'insufficient_evidence' && cits.length > 0;
    const p = c.strength?.premises;
    const sources = conflict
      ? `<p class="m-expl" style="font-size:13.5px">${esc(fill(T.result.conflict, { difference: c.unresolved || '' }))}</p><div class="m-sides">${['supports', 'refutes']
          .map(side => `<div><h4 class="m-h">${side === 'supports' ? 'Źródła potwierdzające' : 'Źródła przeczące'}</h4><ul class="m-srcs">${cits.filter(x => x.stance === side).map(citation).join('')}</ul></div>`)
          .join('')}</div>`
      : cits.length ? `<h4 class="m-h">${esc(T.result.sources_title)}</h4><ul class="m-srcs">${cits.map(citation).join('')}</ul>` : '';
    const strength = c.strength
      ? `<p class="m-str">${esc(T.result.strength_title)}: ${esc(T.strength[c.strength.level])}<span class="lv" aria-hidden="true">${[1, 2, 3].map(n => `<i class="${n <= LEVEL[c.strength.level] ? 'on' : ''}" style="height:${4 + n * 3}px"></i>`).join('')}</span></p>
         <p class="m-sub">${esc(fill(T.result.premises, { independent: p.independent_sources, primary: p.primary_sources, agreement: T.result.agreement[p.agreement] }))}${
           p.newest_source_published_at && c.claim_date ? ' ' + esc(fill(T.result.newest, { source_date: day(p.newest_source_published_at), claim_date: day(c.claim_date), claim_date_source: T.result.claim_date_source[c.claim_date_source] })) : ''}</p>`
      : '';
    const notes = [
      c.unresolved && !conflict ? `<div class="m-note" style="display:block"><b style="font-size:12px;color:var(--m-ink2)">${esc(T.result.unresolved)}</b><br>${esc(c.unresolved)}</div>` : '',
      c.archival ? `<p class="m-note">${esc(T.result.archival)}</p>` : '',
      c.incident ? `<p class="m-note">${esc(fill(c.incident.matched_on === 'domain' ? T.result.incident_domain : T.result.incident, { title: c.incident.title, date: day(c.incident.date) }))} <a href="${safeUrl(c.incident.url)}" target="_blank" rel="noopener noreferrer">opis przypadku</a></p>` : '',
      c.technique ? `<p class="m-note">Technika: <span class="m-t" tabindex="0">${esc(T.techniques[c.technique].name)}<span class="m-tip l">${esc(T.techniques[c.technique].how_to_spot)}</span></span></p>` : '',
    ].join('');
    return `<article class="m-claim">
      <div class="m-claim-h"><h3><span class="m-sr">${esc(T.result.claim)}: </span>${esc(c.claim)}</h3><span class="m-badge ${c.verdict}">${esc(T.verdict[c.verdict])}</span></div>
      <p class="m-sub">${esc(T.verdict_hint[c.verdict])}</p>
      <p class="m-expl">${esc(c.explanation)}</p><p class="m-sub">${esc(T.result.explanation_hint)}</p>
      ${sources}${strength}${notes}</article>`;
  }

  function resultCard(r) {
    const body = r.status === 'done'
      ? (r.source_warning ? `<p class="m-note" style="margin:10px 14px 0">${esc(fill(T.source_warning.eu_sanctioned_entity, { entity: r.source_warning.entity }))} <a href="${safeUrl(r.source_warning.basis_url)}" target="_blank" rel="noopener noreferrer">podstawa</a></p>` : '') + (r.claims || []).map(claimBlock).join('')
      : `<div class="m-status"><svg class="m-ic" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.8" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M8 4.6v4.3M8 11.2v.1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg><div><b>${esc(T.status[r.status])}</b><p>${esc(r.message || T.status_hint[r.status])}</p></div></div>`;
    const e = r.escalation;
    const esc8n = e ? `<p class="esc">${esc(e.state === 'recommended' ? T.escalation.recommended : fill(T.escalation[e.state], { case: e.case_id || '' }))}</p>` : '';
    const lim = r.limitations?.length ? `<div><b>${esc(T.result.limitations)}</b><ul>${r.limitations.map(l => `<li>${esc(l)}</li>`).join('')}</ul></div>` : '';
    return `<section class="m-card" aria-label="Meritum: wynik sprawdzenia"><div class="m-top">${mark(14)}Meritum</div>${body}
      <footer class="m-foot">${esc8n}${lim}<p>${esc(T.result.ai_disclosure)}</p></footer></section>`;
  }

  const steps = status => `<div class="m-proc-h">${mark(14)}${esc(T.analysis.title)}</div><ol>${status.steps
    .map(s => {
      const stateIsVisible = s.status === 'skipped' || s.status === 'failed';
      const stateSeparator = stateIsVisible ? '<span class="m-sr">, </span>' : ', ';
      return `<li class="${s.status}"><i></i><span class="m-step-label">${esc(T.analysis.steps[s.code])}</span><span class="${stateIsVisible ? 'm-step-status' : 'm-sr'}">${stateSeparator}${esc(T.analysis.step_status[s.status])}</span></li>`;
    })
    .join('')}</ol>${status.draft ? `<p class="m-draft">${esc(T.analysis.draft)}</p>` : ''}`;

  globalThis.MeritumCard = {
    /** Must run once before rendering: the copy object from copy/pl.json. */
    use: copy => { T = copy; },
    card: result => resultCard(result),
    steps,
    mark,
  };
})();
