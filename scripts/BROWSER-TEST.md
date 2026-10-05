# Labeled browser validation

On GitHub, open **Actions → Labeled browser validation → Run workflow**.
Use 3 sessions for the first test. Each session loads the homepage, railroad
article, and citations page. The hard limit is 20 sessions (60 page loads).
This is manual-only: no recurring traffic generation or monthly audience target.

Runs execute on GitHub, so your Mac does not need to stay online. GitHub Actions
usage limits apply. Download the run's artifact for JSON results and screenshots.
All URLs retain `stress_test / synthetic` and campaign `e3_github_validation`.
The browser remains openly automated; no fingerprint spoofing or filter bypass.

`collectionResponses` means successful GA4 HTTP responses, **not** confirmed GA4
views or active users. Check GA4 separately for attributed test events. The
workflow does not authenticate to Analytics or read its reports.

This workflow does not move or stop the older local 24-hour runner.
