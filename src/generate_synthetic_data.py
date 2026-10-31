"""Generate the deterministic synthetic advertising source CSV."""
from datetime import date, timedelta
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "ads_daily.csv"
CAMPAIGNS = ["brand_search", "social_prospect", "video_awareness", "display_retarget", "app_install", "native_monetize"]
GEOS = ["US", "GB", "IN", "DE"]
DEVICES = ["mobile", "desktop", "tablet"]
AUDIENCES = ["prospecting", "retargeting", "lookalike"]
PLATFORMS = ["Android", "iOS"]
APPS = ["ShopNow", "FitLife", "NewsLite"]
PARTNERS = ["GoogleAds", "Meta", "AdMob", "TradeDesk", "AppleSearchAds"]
HEADERS = [
    "date", "campaign_id", "geo", "device", "audience_segment", "platform", "app",
    "demand_partner", "impressions", "clicks", "conversions", "spend_usd",
    "revenue_usd", "installs", "ad_requests", "ad_impressions", "ad_revenue_usd"
]


def pseudo_random(seed):
    value = math.sin(seed * 999.91) * 10000
    return value - math.floor(value)


def round_positive(value):
    """Match positive JavaScript Math.round behaviour used by the initial generator."""
    return math.floor(value + 0.5)


def money(value, places):
    return float(f"{value:.{places}f}")


def generate():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    start = date(2025, 1, 1)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADERS)
        for day in range(90):
            event_date = (start + timedelta(days=day)).isoformat()
            for c, campaign in enumerate(CAMPAIGNS):
                for g, geo in enumerate(GEOS):
                    for v, device in enumerate(DEVICES):
                        seed = day * 100 + c * 20 + g * 4 + v
                        impressions = round_positive(
                            (650 + pseudo_random(seed + 1) * 1900)
                            * (1 + 0.12 * math.sin(day / 7 + c))
                        )
                        audience = AUDIENCES[(c + g + v) % 3]
                        platform = "Web" if device == "desktop" else PLATFORMS[(c + g) % 2]
                        app = APPS[c % 3]
                        partner = PARTNERS[c % 5]

                        ctr = [0.075, 0.052, 0.034, 0.061, 0.082, 0.028][c]
                        ctr *= 0.82 + pseudo_random(seed + 2) * 0.36
                        clicks = max(1, round_positive(impressions * ctr))
                        cvr = [0.105, 0.073, 0.041, 0.112, 0.087, 0.039][c]
                        cvr *= 0.8 + pseudo_random(seed + 3) * 0.4
                        conversions = max(1, round_positive(clicks * cvr))

                        cpc = [0.42, 0.60, 0.29, 0.38, 0.48, 0.25][c]
                        cpc *= 0.85 + pseudo_random(seed + 4) * 0.3
                        spend = money(clicks * cpc, 2)
                        revenue = money(
                            conversions * [13.5, 15, 20, 18, 16, 12][c]
                            * (0.82 + pseudo_random(seed + 5) * 0.36), 2
                        )
                        if c == 4:
                            installs = round_positive(clicks * (0.70 + pseudo_random(seed + 6) * 0.18))
                        elif c in (2, 5):
                            installs = round_positive(clicks * 0.25)
                        else:
                            installs = round_positive(conversions * 0.45)

                        requests = 0 if platform == "Web" else round_positive(
                            impressions * (1.28 + pseudo_random(seed + 7) * 0.4)
                        )
                        served = 0 if requests == 0 else round_positive(
                            requests * (0.66 + pseudo_random(seed + 8) * 0.16)
                        )
                        ecpm = [3.5, 4.2, 2.8, 3.8, 4.6][c]
                        ecpm *= 0.82 + pseudo_random(seed + 9) * 0.36
                        ad_revenue = money(served * ecpm / 1000, 4)

                        # Deliberate quality-test cases: one logical click error and one negative cost.
                        if day == 17 and c == 0 and g == 0 and v == 0:
                            clicks = impressions + 5
                        if day == 41 and c == 3 and g == 2 and v == 1:
                            spend = -2.0

                        writer.writerow([
                            event_date, campaign, geo, device, audience, platform, app, partner,
                            impressions, clicks, conversions, f"{spend:.2f}", f"{revenue:.2f}",
                            installs, requests, served, f"{ad_revenue:.4f}"
                        ])
    print(f"Wrote {90 * len(CAMPAIGNS) * len(GEOS) * len(DEVICES):,} synthetic rows to {OUTPUT}")


if __name__ == "__main__":
    generate()
