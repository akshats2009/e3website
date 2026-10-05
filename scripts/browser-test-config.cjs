function sessionCount(value) {
  if (!/^\d+$/.test(String(value)) || Number(value) < 1 || Number(value) > 20) {
    throw new Error('Sessions must be an integer from 1 to 20');
  }
  return Number(value);
}
function testUrl(path, run) {
  const url = new URL(path, 'https://e3-initiative.org');
  if (url.origin !== 'https://e3-initiative.org') throw new Error('Off-site navigation rejected');
  url.searchParams.set('utm_source', 'stress_test');
  url.searchParams.set('utm_medium', 'synthetic');
  url.searchParams.set('utm_campaign', 'e3_github_validation');
  url.searchParams.set('test_run', run);
  return url.toString();
}
function isPageView(address, body) {
  const url = new URL(address);
  const params = new URLSearchParams(url.search);
  const posted = new URLSearchParams(body || '');
  return /(^|\.)google-analytics\.com$/.test(url.hostname)
    && url.pathname === '/g/collect'
    && (params.get('tid') || posted.get('tid')) === 'G-JJDGPY8QCB'
    && (params.get('en') || posted.get('en')) === 'page_view';
}
module.exports = { sessionCount, testUrl, isPageView };
