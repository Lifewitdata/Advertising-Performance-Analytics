# Data dictionary and metric definitions

## Source and grain
\`data/ads_daily.csv\` is deterministic synthetic data from 2025-01-01 to 2025-03-31. One row is date × campaign × geo × device. There are 6,480 source rows; no external source or personal data was used.

## Fields
| Field | Description |
|---|---|
| date | Synthetic reporting date |
| campaign_id | Campaign identifier |
| geo | Illustrative market code |
| device | mobile, desktop or tablet |
| audience_segment | prospecting, retargeting or lookalike |
| platform | Android, iOS or Web |
| app | Illustrative app/property |
| demand_partner | Illustrative monetisation partner |
| impressions | Paid-media impressions |
| clicks | Paid-media clicks |
| conversions | Paid-media attributed conversions |
| spend_usd | Paid-media cost |
| revenue_usd | Simulated paid-media attributed revenue |
| installs | Simulated app installs |
| ad_requests | In-app ad requests |
| ad_impressions | In-app served impressions |
| ad_revenue_usd | Separate simulated in-app ad revenue |

## Metrics
- CTR = SUM(clicks) / SUM(impressions)
- CVR = SUM(conversions) / SUM(clicks)
- CPC = SUM(spend_usd) / SUM(clicks)
- CPA = SUM(spend_usd) / SUM(conversions)
- ROAS = SUM(revenue_usd) / SUM(spend_usd)
- CPI = SUM(spend_usd) / SUM(installs)
- Fill rate = SUM(ad_impressions) / SUM(ad_requests)
- eCPM = SUM(ad_revenue_usd) / SUM(ad_impressions) × 1,000

Ratios use aggregate numerators and denominators; zero denominators yield null. \`revenue_usd\` powers paid-media ROAS; \`ad_revenue_usd\` powers in-app eCPM. Do not conflate them.

## Quality and statistical notes
Required fields are checked for nulls; measures for negatives; clicks ≤ impressions; conversions ≤ clicks; served impressions ≤ requests; and duplicate date/campaign/geo/device keys. Invalid rows are excluded. Daily totals are reconciled. CTR/CVR use Wilson 95% intervals. IQR anomaly flags are investigation prompts. The A/B test is a simulated randomized experiment, not an advertiser experiment; Holm adjustment is used for exploratory campaign comparisons.
