from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from analyze_ads import load_and_validate,aggregate
st.set_page_config(page_title="Advertising Performance",layout="wide")
st.title("Advertising Performance Analytics")
st.caption("Synthetic demonstration data · 1 Jan–31 Mar 2025 · Not live platform reporting")
@st.cache_data
def load_data():
    return load_and_validate(ROOT/"data"/"ads_daily.csv")
df,quality=load_data()
st.sidebar.header("Filters")
campaigns=st.sidebar.multiselect("Campaign",sorted(df.campaign_id.unique()),default=sorted(df.campaign_id.unique()))
geos=st.sidebar.multiselect("Geo",sorted(df.geo.unique()),default=sorted(df.geo.unique()))
devices=st.sidebar.multiselect("Device",sorted(df.device.unique()),default=sorted(df.device.unique()))
view=df[df.campaign_id.isin(campaigns)&df.geo.isin(geos)&df.device.isin(devices)]
if view.empty:
    st.warning("No rows match the filters.");st.stop()
totals=aggregate(view.assign(scope="Selected"),["scope"]).iloc[0]
k1,k2,k3,k4,k5=st.columns(5)
k1.metric("Impressions",f"{int(totals.impressions):,}")
k2.metric("CTR",f"{totals.ctr:.2%}")
k3.metric("CVR",f"{totals.cvr:.2%}")
k4.metric("CPA","—" if pd.isna(totals.cpa_usd) else "$"+f"{totals.cpa_usd:.2f}")
k5.metric("ROAS",f"{totals.roas:.2f}x")
daily=aggregate(view,["date"]).sort_values("date")
campaign=aggregate(view,["campaign_id"]).sort_values("roas",ascending=False)
left,right=st.columns(2)
with left:
    st.subheader("Daily CTR");st.line_chart(daily.set_index("date")[["ctr"]])
with right:
    st.subheader("Campaign ROAS");st.bar_chart(campaign.set_index("campaign_id")[["roas"]])
st.subheader("Campaign performance with sample sizes")
st.dataframe(campaign[["campaign_id","impressions","clicks","conversions","ctr","cvr","cpa_usd","roas","cpi_usd"]],use_container_width=True)
st.subheader("Data-quality checks");st.json(quality)
st.info("All results are synthetic. Do not use these figures for live budget decisions.")
