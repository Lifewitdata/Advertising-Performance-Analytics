-- PostgreSQL analysis layer. Load data/ads_daily.csv into ads_daily first.
-- ROAS uses revenue_usd; eCPM uses separate ad_revenue_usd.
WITH cleaned AS (
 SELECT * FROM ads_daily
 WHERE date IS NOT NULL AND impressions>=0 AND clicks>=0 AND conversions>=0
 AND spend_usd>=0 AND revenue_usd>=0 AND installs>=0 AND ad_requests>=0
 AND ad_impressions>=0 AND ad_revenue_usd>=0
 AND clicks<=impressions AND conversions<=clicks AND ad_impressions<=ad_requests
),
campaign_dim AS (
 SELECT campaign_id, CASE campaign_id
 WHEN 'brand_search' THEN 'Search' WHEN 'social_prospect' THEN 'Paid social'
 WHEN 'video_awareness' THEN 'Video' WHEN 'display_retarget' THEN 'Display'
 WHEN 'app_install' THEN 'App install' ELSE 'In-app monetisation' END campaign_type
 FROM (SELECT DISTINCT campaign_id FROM cleaned) c
),
daily AS (
 SELECT date,campaign_id,geo,device,audience_segment,platform,app,demand_partner,
 SUM(impressions) impressions,SUM(clicks) clicks,SUM(conversions) conversions,
 SUM(spend_usd) spend_usd,SUM(revenue_usd) revenue_usd,SUM(installs) installs,
 SUM(ad_requests) ad_requests,SUM(ad_impressions) ad_impressions,SUM(ad_revenue_usd) ad_revenue_usd
 FROM cleaned GROUP BY date,campaign_id,geo,device,audience_segment,platform,app,demand_partner
),
metrics AS (
 SELECT d.*,cd.campaign_type,clicks::numeric/NULLIF(impressions,0) ctr,
 conversions::numeric/NULLIF(clicks,0) cvr,spend_usd/NULLIF(clicks,0) cpc_usd,
 spend_usd/NULLIF(conversions,0) cpa_usd,revenue_usd/NULLIF(spend_usd,0) roas,
 spend_usd/NULLIF(installs,0) cpi_usd,
 ad_impressions::numeric/NULLIF(ad_requests,0) fill_rate,
 ad_revenue_usd*1000/NULLIF(ad_impressions,0) ecpm_usd
 FROM daily d JOIN campaign_dim cd USING(campaign_id)
)
SELECT *,AVG(ctr) OVER(PARTITION BY campaign_id ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) ctr_7d_avg,
 SUM(spend_usd) OVER(PARTITION BY campaign_id ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) spend_7d
FROM metrics ORDER BY date,campaign_id;

-- Weekly roll-up with ratio-of-sums.
SELECT DATE_TRUNC('week',date)::date week_start,campaign_id,SUM(impressions) impressions,
 SUM(clicks) clicks,SUM(conversions) conversions,SUM(spend_usd) spend_usd,
 SUM(clicks)::numeric/NULLIF(SUM(impressions),0) ctr,
 SUM(conversions)::numeric/NULLIF(SUM(clicks),0) cvr,
 SUM(spend_usd)/NULLIF(SUM(conversions),0) cpa_usd
FROM ads_daily WHERE clicks BETWEEN 0 AND impressions AND conversions BETWEEN 0 AND clicks AND spend_usd>=0
GROUP BY 1,2 ORDER BY 1,2;

-- Campaign ranking with sample sizes and window rank.
SELECT campaign_id,SUM(impressions) impressions,SUM(clicks) clicks,SUM(conversions) conversions,
 SUM(spend_usd) spend_usd,SUM(clicks)::numeric/NULLIF(SUM(impressions),0) ctr,
 SUM(conversions)::numeric/NULLIF(SUM(clicks),0) cvr,
 SUM(spend_usd)/NULLIF(SUM(conversions),0) cpa_usd,
 SUM(revenue_usd)/NULLIF(SUM(spend_usd),0) roas,
 RANK() OVER(ORDER BY SUM(revenue_usd)/NULLIF(SUM(spend_usd),0) DESC) roas_rank
FROM ads_daily WHERE clicks<=impressions AND conversions<=clicks AND spend_usd>=0 GROUP BY campaign_id;

-- Monetisation roll-up by platform, app and demand partner.
SELECT platform,app,demand_partner,SUM(ad_requests) requests,SUM(ad_impressions) served,
 SUM(installs) installs,SUM(ad_revenue_usd) ad_revenue_usd,
 SUM(ad_impressions)::numeric/NULLIF(SUM(ad_requests),0) fill_rate,
 SUM(ad_revenue_usd)*1000/NULLIF(SUM(ad_impressions),0) ecpm_usd
FROM ads_daily GROUP BY platform,app,demand_partner;
