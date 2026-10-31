"""Reproducible analysis for the synthetic advertising dataset."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import chi2, norm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ads_daily.csv"
OUT = ROOT / "outputs"
KEY = ["date", "campaign_id", "geo", "device"]
NUMERIC = ["impressions","clicks","conversions","spend_usd","revenue_usd","installs","ad_requests","ad_impressions","ad_revenue_usd"]

def divide(a, b):
    return a / b.replace(0, np.nan)

def wilson(successes, trials):
    successes, trials = np.asarray(successes, float), np.asarray(trials, float)
    z = norm.ppf(.975)
    p = np.divide(successes, trials, out=np.full_like(successes, np.nan), where=trials > 0)
    den = 1 + z*z/trials
    centre = (p + z*z/(2*trials))/den
    half = z*np.sqrt(p*(1-p)/trials + z*z/(4*trials*trials))/den
    return centre-half, centre+half

def load_and_validate(path=DATA):
    df = pd.read_csv(path, parse_dates=["date"])
    required = KEY + ["audience_segment","platform","app","demand_partner"] + NUMERIC
    missing = sorted(set(required)-set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    checks = {
        "input_rows": int(len(df)),
        "missing_cells": int(df[required].isna().sum().sum()),
        "duplicate_keys": int(df.duplicated(KEY).sum()),
        "negative_measure_rows": int((df[NUMERIC] < 0).any(axis=1).sum()),
        "clicks_gt_impressions": int((df.clicks > df.impressions).sum()),
        "conversions_gt_clicks": int((df.conversions > df.clicks).sum()),
        "ad_impressions_gt_requests": int((df.ad_impressions > df.ad_requests).sum()),
        "date_min": str(df.date.min().date()), "date_max": str(df.date.max().date()),
        "campaigns": int(df.campaign_id.nunique()), "geos": int(df.geo.nunique()),
        "devices": int(df.device.nunique()), "audiences": int(df.audience_segment.nunique())
    }
    valid = (df[required].notna().all(axis=1) & (df[NUMERIC] >= 0).all(axis=1)
             & (df.clicks <= df.impressions) & (df.conversions <= df.clicks)
             & (df.ad_impressions <= df.ad_requests) & ~df.duplicated(KEY, keep=False))
    checks["valid_rows"], checks["excluded_rows"] = int(valid.sum()), int((~valid).sum())
    return df.loc[valid].copy(), checks

def aggregate(df, dimensions):
    g = df.groupby(dimensions, dropna=False, as_index=False).agg(
        impressions=("impressions","sum"), clicks=("clicks","sum"),
        conversions=("conversions","sum"), spend_usd=("spend_usd","sum"),
        revenue_usd=("revenue_usd","sum"), installs=("installs","sum"),
        ad_requests=("ad_requests","sum"), ad_impressions=("ad_impressions","sum"),
        ad_revenue_usd=("ad_revenue_usd","sum"))
    g["ctr"], g["cvr"] = divide(g.clicks,g.impressions), divide(g.conversions,g.clicks)
    g["cpc_usd"], g["cpa_usd"] = divide(g.spend_usd,g.clicks), divide(g.spend_usd,g.conversions)
    g["roas"], g["cpi_usd"] = divide(g.revenue_usd,g.spend_usd), divide(g.spend_usd,g.installs)
    g["fill_rate"] = divide(g.ad_impressions,g.ad_requests)
    g["ecpm_usd"] = divide(g.ad_revenue_usd*1000,g.ad_impressions)
    lo,hi = wilson(g.clicks,g.impressions)
    g["ctr_ci95_low"],g["ctr_ci95_high"] = lo,hi
    lo,hi = wilson(g.conversions,g.clicks)
    g["cvr_ci95_low"],g["cvr_ci95_high"] = lo,hi
    return g

def holm(p_values):
    p = np.asarray(p_values,float)
    order = np.argsort(p)
    adj, running = np.empty_like(p), 0.0
    for rank,idx in enumerate(order):
        running = max(running,(len(p)-rank)*p[idx])
        adj[idx] = min(running,1.0)
    return adj

def prop_test(x1,n1,x2,n2):
    p1,p2=x1/n1,x2/n2
    pooled=(x1+x2)/(n1+n2)
    se0=np.sqrt(pooled*(1-pooled)*(1/n1+1/n2))
    z=(p2-p1)/se0 if se0 else 0.0
    diff=p2-p1
    se=np.sqrt(p1*(1-p1)/n1+p2*(1-p2)/n2)
    return diff,[diff-1.96*se,diff+1.96*se],float(2*norm.sf(abs(z)))

def required_sample(p0=.08,p1=.09,power=.80,alpha=.05):
    za,zp=norm.ppf(1-alpha/2),norm.ppf(power)
    pm=(p0+p1)/2
    a=za*np.sqrt(2*pm*(1-pm))+zp*np.sqrt(p0*(1-p0)+p1*(1-p1))
    return int(np.ceil((a/(p1-p0))**2))

def simulate_ab(seed=2025, users_per_arm=10000):
    rng=np.random.default_rng(seed)
    n=users_per_arm*2
    arm=rng.choice(["control","treatment"],size=n,p=[.5,.5])
    converted=rng.binomial(1,np.where(arm=="control",.08,.09))
    users=pd.DataFrame({"variant":arm,"converted":converted})
    counts=users.groupby("variant").agg(users=("converted","size"),conversions=("converted","sum"))
    c,t=counts.loc["control"],counts.loc["treatment"]
    diff,ci,p=prop_test(int(c.conversions),int(c.users),int(t.conversions),int(t.users))
    observed=np.array([c.users,t.users],float); expected=np.array([n/2,n/2],float)
    srm=float(chi2.sf(np.sum((observed-expected)**2/expected),1))
    result=pd.DataFrame([{
        "control_users":int(c.users),"control_conversions":int(c.conversions),
        "control_cvr":float(c.conversions/c.users),"treatment_users":int(t.users),
        "treatment_conversions":int(t.conversions),"treatment_cvr":float(t.conversions/t.users),
        "absolute_cvr_difference":float(diff),"ci95_low":float(ci[0]),"ci95_high":float(ci[1]),
        "p_value_two_sided":p,"srm_p_value":srm,
        "required_users_per_arm_for_1pp_lift":required_sample()
    }])
    return users,result

def main():
    OUT.mkdir(exist_ok=True)
    df,checks=load_and_validate()
    source_totals=df[NUMERIC].sum()
    daily=aggregate(df,["date"])
    daily_totals=daily[NUMERIC].sum()
    reconciliation={c:bool(np.isclose(source_totals[c],daily_totals[c])) for c in NUMERIC}
    if not all(reconciliation.values()):
        raise AssertionError("Daily roll-up does not reconcile to valid source totals")
    checks["metric_reconciliation_passed"]=all(reconciliation.values())
    (OUT/"data_quality.json").write_text(json.dumps(checks,indent=2))
    daily=daily.sort_values("date")
    daily["ctr_7d_avg"]=daily.ctr.rolling(7,min_periods=7).mean()
    daily["cpa_7d_avg"]=daily.cpa_usd.rolling(7,min_periods=7).mean()
    daily.to_csv(OUT/"daily_metrics.csv",index=False)
    weekly_source=df.assign(week_start=df.date.dt.to_period("W-SUN").dt.start_time)
    aggregate(weekly_source,["week_start"]).to_csv(OUT/"weekly_metrics.csv",index=False)
    campaign=aggregate(df,["campaign_id"]).sort_values("roas",ascending=False)
    campaign.to_csv(OUT/"campaign_ranking.csv",index=False)
    for dim in ["geo","device","audience_segment","platform","app","demand_partner"]:
        aggregate(df,[dim]).to_csv(OUT/(dim+"_performance.csv"),index=False)
    dc=aggregate(df,["date","campaign_id"])
    def iqr_flag(s):
        q1,q3=s.quantile(.25),s.quantile(.75); spread=q3-q1
        return (s<q1-1.5*spread)|(s>q3+1.5*spread)
    dc["spend_iqr_flag"]=dc.groupby("campaign_id").spend_usd.transform(iqr_flag)
    dc["ctr_iqr_flag"]=dc.groupby("campaign_id").ctr.transform(iqr_flag)
    dc.to_csv(OUT/"anomaly_flags.csv",index=False)
    bycvr=aggregate(df,["campaign_id"]).sort_values("cvr",ascending=False)
    ref=bycvr.iloc[0]; comparisons=[]
    for _,r in bycvr.iloc[1:].iterrows():
        _,_,p=prop_test(int(ref.conversions),int(ref.clicks),int(r.conversions),int(r.clicks))
        comparisons.append({"reference_campaign":ref.campaign_id,"campaign_id":r.campaign_id,
            "reference_clicks":int(ref.clicks),"campaign_clicks":int(r.clicks),
            "reference_conversions":int(ref.conversions),"campaign_conversions":int(r.conversions),"p_value":p})
    if comparisons:
        tests=pd.DataFrame(comparisons);tests["p_value_holm"]=holm(tests.p_value)
        tests.to_csv(OUT/"campaign_tests.csv",index=False)
    users,ab=simulate_ab()
    users.to_csv(OUT/"simulated_ab_user_level.csv",index=False)
    ab.to_csv(OUT/"ab_test_results.csv",index=False)
    donor=campaign.sort_values("roas").iloc[0];receiver=campaign.iloc[0]
    budget={"scenario":"illustrative_only_not_a_live_recommendation",
        "donor_campaign_lowest_roas":str(donor.campaign_id),
        "receiver_campaign_highest_roas":str(receiver.campaign_id),
        "donor_campaign_synthetic_spend_usd":float(donor.spend_usd),
        "reallocation_pct_of_donor_spend":10.0,
        "illustrative_shift_usd":float(donor.spend_usd*.10)}
    summary={"quality":checks,"budget_scenario":budget,
        "experiment":ab.iloc[0].to_dict(),
        "note":"Synthetic demonstration only; do not use as real budget evidence."}
    (OUT/"analysis_summary.json").write_text(json.dumps(summary,indent=2,default=float))
    print(json.dumps(summary,indent=2,default=float))

if __name__=="__main__":
    main()
