# Stakeholder brief — synthetic baseline

## Executive summary
This is a reproducible demonstration built from synthetic 90-day data, not a live ad-platform report. The source has 6,480 rows, six campaigns, four geos and three devices. Two deliberate quality exceptions are excluded, leaving 6,478 valid rows.

## Campaign results
The README lists campaign-level impressions, clicks, conversions, CTR, CPA and ROAS computed from generated data. For this synthetic data, \`display_retarget\` has the highest ROAS (5.32x), and \`social_prospect\` the lowest (1.82x). These are constructed outcomes, not client results.

## Quantified allocation scenario
A notional 10% shift from the lowest-ROAS campaign's synthetic spend to the highest-ROAS campaign is **$5,461.01**, from \`social_prospect\` to \`display_retarget\`. It is illustrative only; it is not advice to change a live budget.

## Decision controls for real data
1. Validate attribution, time zone, deduplication, revenue definitions and spend reconciliation.
2. Require adequate clicks and conversions; assess confidence intervals and business targets.
3. Pre-register one primary experiment metric, hypothesis, sample size, duration and stopping rule.
4. Randomize at user/account level and check sample-ratio mismatch.
5. Scale in small increments with a control group and guardrail metrics.

## Simulated randomized experiment results

The reproducible user-level simulation randomized 20,000 generated users. Control had 10,112 users and 813 conversions (8.05% CVR); treatment had 9,888 users and 870 conversions (8.80% CVR). The estimated lift was **+0.76 percentage points**, with a **95% Wald confidence interval of -0.01 to +1.53 percentage points** and a **two-sided p-value of 0.0533**. The sample-ratio mismatch diagnostic returned **p = 0.1132**. Under the simulated baseline rates of 8% versus 9%, the approximate sample-size calculation is **12,208 users per arm** for 80% power at a 5% two-sided significance level.

This single simulated run does not meet the conventional 0.05 significance threshold and is under the planned sample size. It is method demonstration only, not a live experiment and not proof of a real campaign effect.

## Limitations
Data, rankings, p-values, intervals, anomalies and budget scenarios are synthetic. The experiment did not run on an advertising platform. It establishes no causal impact, incrementality, fraud, margin, partner payout or real return.
## Reproducible synthetic baseline

| Measure | Value |
|---|---:|
| Date coverage | 90 days (2025-01-01 to 2025-03-31) |
| Input records | 6,480 |
| Campaigns / geos / devices / audience segments | 6 / 4 / 3 / 3 |
| Deliberately invalid records | 2 |
| Valid records after declared checks | 6,478 |

The two deliberate invalid test cases are one row with clicks exceeding impressions and one row with negative spend. They are flagged and excluded from performance calculations. All figures below are synthetic demonstrations, not actual campaign performance.

| Campaign | Impressions | Clicks | Conversions | CTR | CPA (USD) | ROAS |
|---|---:|---:|---:|---:|---:|---:|
| display_retarget | 1,736,317 | 106,065 | 11,880 | 6.11% | $3.40 | 5.32x |
| brand_search | 1,727,232 | 130,223 | 13,713 | 7.54% | $3.98 | 3.38x |
| app_install | 1,723,952 | 141,407 | 12,359 | 8.20% | $5.52 | 2.89x |
| video_awareness | 1,729,113 | 58,581 | 2,400 | 3.39% | $7.08 | 2.83x |
| native_monetize | 1,727,291 | 48,602 | 1,918 | 2.81% | $6.32 | 1.89x |
| social_prospect | 1,745,107 | 90,857 | 6,643 | 5.21% | $8.22 | 1.82x |

A purely illustrative 10% reallocation would transfer **$5,461.01** from \`social_prospect\` to \`display_retarget\`. This is a scenario only, not live budget advice.
