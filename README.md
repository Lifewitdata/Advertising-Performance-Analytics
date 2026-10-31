# Advertising Performance Analytics

## Interactive Tableau Dashboard

[Open the interactive Tableau Public dashboard](https://public.tableau.com/app/profile/isfaque.ansari5273/viz/Ad_Performance_Intelligence/01PerformanceCommandCentre).

The published view opens the **Performance Command Centre**. Use the dashboard tabs to explore all four views:

- Performance Command Centre
- Monetisation Intelligence
- Acquisition Efficiency
- Supply & Risk Observatory

To obtain a local copy of the packaged workbook, open the Tableau Public page and use **Download → Tableau Workbook** when that option is enabled.

The workbook contains synthetic demonstration data only. It is a portfolio project and is not connected to any company, advertiser, production account or live ad platform.

---
A reproducible portfolio project covering paid-media campaign performance and in-app ad monetisation. It uses **synthetic demonstration data** and is not connected to GreedyGame, Google Ads, Meta or any production account.

## Scope

- 90 days × 6 campaigns × 4 geographies × 3 devices = **6,480 daily segment records**.
- Paid media: impressions, clicks, conversions, spend and attributed revenue.
- App monetisation: requests, served impressions, separate ad revenue, installs, platform, app and demand partner.
- Data-quality test cases, time trends, segmented rankings, outlier screening, a simulated randomized A/B test, SQL and a Streamlit dashboard.

## Dataset and limitations

**File:** \`data/ads_daily.csv\`  
**Date range:** 2025-01-01 to 2025-03-31.  
**Rows:** 6,480.  
**Source:** deterministically generated synthetic data; no personal or real advertiser data.

Paid campaign attributed revenue (\`revenue_usd\`) is distinct from in-app ad revenue (\`ad_revenue_usd\`). Two deliberately invalid source rows are reported and excluded. Synthetic data does not represent real delivery, benchmarks, GreedyGame reporting, billing, partner payouts or commercial outcomes.

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

## Metric definitions

| Metric | Formula |
|---|---|
| CTR | clicks / impressions |
| CVR | conversions / clicks |
| CPC | spend_usd / clicks |
| CPA | spend_usd / conversions |
| ROAS | revenue_usd / spend_usd |
| CPI | spend_usd / installs |
| Fill rate | ad_impressions / ad_requests |
| eCPM | ad_revenue_usd / ad_impressions × 1,000 |

All ratios use grouped sums. Zero denominators return null. eCPM uses in-app ad revenue, not paid-media attributed revenue.

## Quick start

Python 3.11 is recommended.

\`\`\`bash
git clone https://github.com/Lifewitdata/Advertising-Performance-Analytics.git
cd Advertising-Performance-Analytics
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# Optional: regenerate the deterministic synthetic CSV
python src/generate_synthetic_data.py

# Validate, analyse and write outputs/
python src/analyze_ads.py
jupyter lab
\`\`\`

Open \`Advertising Performance Analytics.ipynb\` in the repository root. The data path is repository-relative, not Colab-specific.

Launch the interactive dashboard:

\`\`\`bash
streamlit run dashboard/app.py
\`\`\`

Generated tables and JSON summaries are written to \`outputs/\`.

## Run the Streamlit dashboard

From the repository root, create and activate a virtual environment, install the pinned dependencies, and launch Streamlit through the active Python interpreter. Using `python -m streamlit` avoids the common Windows error where the `streamlit` command is not recognised because its Scripts folder is not on PATH.

**Windows (PowerShell or Command Prompt):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run dashboard/app.py
```

If PowerShell blocks virtual-environment activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or skip activation and use `.venv\Scripts\python.exe -m pip install -r requirements.txt` followed by `.venv\Scripts\python.exe -m streamlit run dashboard/app.py`.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run dashboard/app.py
```

In VS Code, select the same `.venv` interpreter via **Python: Select Interpreter** before running the dashboard. The app reads `data/ads_daily.csv` using a path relative to the repository, so launch it from the project checkout.

## SQL

\`sql/analysis.sql\` contains CTEs, a campaign metadata join, GROUP BY aggregations, weekly/date rollups and window functions. It targets PostgreSQL; load the CSV into a staging table named \`ads_daily\`.

## Authentication

This is an offline analytics repository. It contains no application login, OAuth flow, user sessions, API client or secrets. No authentication is required to run the notebook, SQL or dashboard locally. GitHub write access is supplied separately by the connected GitHub account, not by project code. Never commit tokens or passwords.

## Interpretation

Rankings include sample sizes and Wilson 95% intervals for CTR/CVR. IQR flags are investigation prompts, not proof of fraud. The A/B experiment is a simulated user-level exercise; no live test ran. Synthetic findings must not be used to move real budget.

