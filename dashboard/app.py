"""Interactive dashboard for the synthetic advertising analytics project.

Run from the repository root:
    python -m streamlit run dashboard/app.py
"""
from pathlib import Path
import sys

import pandas as pd

try:
    import streamlit as st
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Streamlit is not installed in this Python environment. From the repository "
        "root, run: python -m pip install -r requirements.txt. Then launch with: "
        "python -m streamlit run dashboard/app.py"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "ads_daily.csv"
SRC_PATH = ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

try:
    from analyze_ads import aggregate, load_and_validate
except ImportError as exc:
    st.error(
        "Could not import the project analysis module from src/analyze_ads.py. "
        "Run this app from the repository checkout and make sure the src folder "
        "is present."
    )
    st.exception(exc)
    st.stop()


st.set_page_config(
    page_title="Advertising Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Loading and validating the demonstration dataset...")
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}. Make sure data/ads_daily.csv "
            "is present in the repository."
        )
    return load_and_validate(DATA_PATH)


def pct(value):
    return "—" if pd.isna(value) else f"{value:.2%}"


def currency(value):
    return "—" if pd.isna(value) else f"${value:,.2f}"


def ratio(value):
    return "—" if pd.isna(value) else f"{value:.2f}x"


st.title("Advertising Performance Analytics")
st.caption(
    "Synthetic demonstration dataset · 1 January–31 March 2025 · "
    "Not live advertiser or platform reporting"
)

try:
    df, quality = load_data()
except Exception as exc:  # show actionable errors inside the Streamlit page
    st.error("The dashboard could not load its data.")
    st.exception(exc)
    st.stop()

if df.empty:
    st.error("No valid rows are available after the data-quality checks.")
    st.stop()

# ------------------------------- Sidebar filters -------------------------------
st.sidebar.header("Analysis filters")
min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_value = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_value, (tuple, list)) and len(date_value) == 2:
    start_date, end_date = date_value
else:
    start_date = end_date = date_value

def filter_options(label, column):
    options = sorted(df[column].dropna().astype(str).unique().tolist())
    return st.sidebar.multiselect(label, options, default=options)

campaigns = filter_options("Campaign", "campaign_id")
geos = filter_options("Geography", "geo")
devices = filter_options("Device", "device")
platforms = filter_options("Platform", "platform")
apps = filter_options("App", "app")
partners = filter_options("Demand partner", "demand_partner")

mask = (
    df["date"].dt.date.between(start_date, end_date)
    & df["campaign_id"].isin(campaigns)
    & df["geo"].isin(geos)
    & df["device"].isin(devices)
    & df["platform"].isin(platforms)
    & df["app"].isin(apps)
    & df["demand_partner"].isin(partners)
)
view = df.loc[mask].copy()

if view.empty:
    st.warning("No records match the selected filters. Adjust the filters in the sidebar.")
    st.stop()

totals = aggregate(view.assign(_scope="Selected"), ["_scope"]).iloc[0]

# --------------------------------- KPI strip ------------------------------------
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Impressions", f"{int(totals.impressions):,}")
k2.metric("Clicks", f"{int(totals.clicks):,}")
k3.metric("CTR", pct(totals.ctr))
k4.metric("Spend", currency(totals.spend_usd))
k5.metric("Attributed ROAS", ratio(totals.roas))
k6.metric("Publisher eCPM", currency(totals.ecpm_usd))

overview_tab, monetisation_tab, segments_tab, quality_tab = st.tabs(
    ["Performance overview", "Ad monetisation", "App & partner analysis", "Data quality"]
)

with overview_tab:
    daily = aggregate(view, ["date"]).sort_values("date")
    campaign = aggregate(view, ["campaign_id"]).sort_values("roas", ascending=False)

    left, right = st.columns(2)
    with left:
        st.subheader("Daily performance trend")
        st.line_chart(daily.set_index("date")[["ctr"]])
        st.caption("CTR = total clicks ÷ total impressions for each day.")
    with right:
        st.subheader("Attributed ROAS by campaign")
        st.bar_chart(campaign.set_index("campaign_id")[["roas"]])
        st.caption("Attributed ROAS = paid-media attributed revenue ÷ spend.")

    st.subheader("Campaign performance")
    display_cols = [
        "campaign_id", "impressions", "clicks", "conversions",
        "ctr", "cvr", "spend_usd", "cpa_usd", "roas", "cpi_usd",
    ]
    st.dataframe(
        campaign[display_cols].style.format({
            "impressions": "{:,.0f}",
            "clicks": "{:,.0f}",
            "conversions": "{:,.0f}",
            "ctr": "{:.2%}",
            "cvr": "{:.2%}",
            "spend_usd": "${:,.2f}",
            "cpa_usd": "${:,.2f}",
            "roas": "{:.2f}x",
            "cpi_usd": "${:,.2f}",
        }, na_rep="—"),
        use_container_width=True,
        hide_index=True,
    )

with monetisation_tab:
    monetisation = aggregate(view, ["app", "demand_partner"]).sort_values(
        "ecpm_usd", ascending=False
    )
    fill_by_partner = aggregate(view, ["demand_partner"]).sort_values(
        "fill_rate", ascending=False
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Ad requests", f"{int(totals.ad_requests):,}")
    m2.metric("Served impressions", f"{int(totals.ad_impressions):,}")
    m3.metric("Fill rate", pct(totals.fill_rate))

    left, right = st.columns(2)
    with left:
        st.subheader("Fill rate by demand partner")
        st.bar_chart(fill_by_partner.set_index("demand_partner")[["fill_rate"]])
    with right:
        st.subheader("Publisher ad revenue by app and partner")
        st.bar_chart(monetisation.set_index("app")[["ad_revenue_usd"]])

    st.subheader("Monetisation detail")
    st.dataframe(
        monetisation[
            ["app", "demand_partner", "ad_requests", "ad_impressions",
             "ad_revenue_usd", "fill_rate", "ecpm_usd"]
        ].style.format({
            "ad_requests": "{:,.0f}",
            "ad_impressions": "{:,.0f}",
            "ad_revenue_usd": "${:,.2f}",
            "fill_rate": "{:.2%}",
            "ecpm_usd": "${:,.2f}",
        }, na_rep="—"),
        use_container_width=True,
        hide_index=True,
    )
    st.info(
        "Publisher eCPM uses ad_revenue_usd ÷ ad_impressions × 1,000. "
        "It is separate from paid-media attributed revenue used for ROAS."
    )

with segments_tab:
    st.subheader("Performance by platform")
    by_platform = aggregate(view, ["platform"]).sort_values("roas", ascending=False)
    st.bar_chart(by_platform.set_index("platform")[["roas"]])

    st.subheader("App performance")
    by_app = aggregate(view, ["app"]).sort_values("ad_revenue_usd", ascending=False)
    st.dataframe(
        by_app[
            ["app", "impressions", "clicks", "spend_usd", "revenue_usd",
             "roas", "ad_requests", "ad_impressions", "ad_revenue_usd",
             "fill_rate", "ecpm_usd"]
        ].style.format({
            "impressions": "{:,.0f}",
            "clicks": "{:,.0f}",
            "spend_usd": "${:,.2f}",
            "revenue_usd": "${:,.2f}",
            "roas": "{:.2f}x",
            "ad_requests": "{:,.0f}",
            "ad_impressions": "{:,.0f}",
            "ad_revenue_usd": "${:,.2f}",
            "fill_rate": "{:.2%}",
            "ecpm_usd": "${:,.2f}",
        }, na_rep="—"),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Demand partner performance")
    by_partner = aggregate(view, ["demand_partner"]).sort_values(
        "ad_revenue_usd", ascending=False
    )
    st.dataframe(
        by_partner[
            ["demand_partner", "ad_requests", "ad_impressions",
             "ad_revenue_usd", "fill_rate", "ecpm_usd"]
        ].style.format({
            "ad_requests": "{:,.0f}",
            "ad_impressions": "{:,.0f}",
            "ad_revenue_usd": "${:,.2f}",
            "fill_rate": "{:.2%}",
            "ecpm_usd": "${:,.2f}",
        }, na_rep="—"),
        use_container_width=True,
        hide_index=True,
    )

with quality_tab:
    st.subheader("Validation summary")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Input rows", f"{quality.get('input_rows', 0):,}")
    q2.metric("Valid rows", f"{quality.get('valid_rows', 0):,}")
    q3.metric("Excluded rows", f"{quality.get('excluded_rows', 0):,}")
    q4.metric("Duplicate keys", f"{quality.get('duplicate_keys', 0):,}")
    st.json(quality)
    st.caption(
        "Invalid demonstration records are excluded from the analysis. "
        "See docs/data_dictionary.md for field definitions and validation rules."
    )

st.divider()
st.caption(
    "All figures are synthetic portfolio data. They do not represent real campaign "
    "delivery, billing, advertiser performance, partner payouts or production results."
)
