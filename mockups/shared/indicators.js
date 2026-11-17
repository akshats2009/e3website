/* Loads /api/economic-indicators (live FRED data on the deployed site). Without it, returns a smooth
   placeholder shape flagged live:false, so themes can label it and show no numbers. */
window.loadIndicators = async function () {
  try {
    const r = await fetch('/api/economic-indicators', { cache: 'no-store' });
    if (!r.ok) throw new Error(r.status);
    const d = await r.json();
    if (!d.series) throw new Error('no series');
    return { live: true, years: d.years, series: d.series, asOf: d.asOfDate };
  } catch (e) {
    const years = Array.from({ length: 27 }, (_, i) => 2000 + i);
    const shape = (seed) => years.map((_, i) => 1 + 0.35 * Math.sin(i / 4 + seed) + i * 0.03 + 0.12 * Math.sin(i * 1.7 + seed * 2));
    const series = {};
    ['cpi', 'core_cpi', 'ppi', 'core_pce', 'fed_funds', 'unemployment', 'payrolls', 'ten_year'].forEach((k, j) => series[k] = shape(j));
    return { live: false, years, series, asOf: null };
  }
};
window.fmtIndicator = (v, unit) => unit === '%' ? v.toFixed(2) + '%' : unit === 'M jobs' ? v.toFixed(1) + 'M' : v.toFixed(1);
