const test = require('node:test');
const assert = require('node:assert/strict');
const { sessionCount, testUrl, isPageView } = require('./browser-test-config.cjs');
test('limits sessions to integer counts between 1 and 20', () => {
  assert.equal(sessionCount('3'), 3);
  for (const value of ['0', '21', '1.5', '', 'abc']) assert.throws(() => sessionCount(value));
});
test('labels every page and prevents off-site navigation', () => {
  const url = new URL(testUrl('/articles/chinese-labor-transcontinental-railroad.html', 'run1'));
  assert.equal(url.origin, 'https://e3-initiative.org');
  assert.equal(url.searchParams.get('utm_medium'), 'synthetic');
  assert.equal(url.searchParams.get('utm_source'), 'stress_test');
  assert.equal(url.searchParams.get('utm_campaign'), 'e3_github_validation');
  assert.throws(() => testUrl('https://example.com', 'run1'));
});
test('recognizes only matching GA4 page views', () => {
  assert.equal(isPageView('https://www.google-analytics.com/g/collect?tid=G-JJDGPY8QCB&en=page_view', ''), true);
  assert.equal(isPageView('https://example.com/g/collect?tid=G-JJDGPY8QCB&en=page_view', ''), false);
  assert.equal(isPageView('https://www.google-analytics.com/g/collect?tid=G-OTHER&en=page_view', ''), false);
});
