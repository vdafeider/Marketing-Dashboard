import pandas as pd
import numpy as np

np.random.seed(42)

# =========================
# CONFIG
# =========================
N_IMPRESSIONS = 100000

campaigns = ["FB_Prospecting", "GG_Search", "TT_Scale"]
sources = ["Facebook", "Google", "TikTok"]
devices = ["Mobile", "Desktop"]
geos = ["US", "UK", "DE", "IN"]
placements = ["Feed", "Story", "Search"]
languages = ["EN", "DE", "ES"]

base_date = pd.to_datetime("2024-01-01")

# Mapping campaign → source
campaign_source_map = {
    "FB_Prospecting": "Facebook",
    "GG_Search": "Google",
    "TT_Scale": "TikTok"
}

# =========================
# 1. IMPRESSIONS
# =========================
impressions = pd.DataFrame({
    "impression_id": range(1, N_IMPRESSIONS + 1),
    "user_id": np.random.randint(1, 20000, N_IMPRESSIONS),
    "timestamp": base_date + pd.to_timedelta(np.random.randint(0, 90, N_IMPRESSIONS), unit="D")
                 + pd.to_timedelta(np.random.randint(0, 24, N_IMPRESSIONS), unit="h"),
    "campaign": np.random.choice(list(campaign_source_map.keys()), N_IMPRESSIONS),
    "device": np.random.choice(devices, N_IMPRESSIONS, p=[0.7, 0.3]),
    "geo": np.random.choice(geos, N_IMPRESSIONS, p=[0.4,0.2,0.2,0.2]),
    "placement": np.random.choice(placements, N_IMPRESSIONS),
    "language": np.random.choice(languages, N_IMPRESSIONS)
})

# Assign source based on campaign
impressions["source"] = impressions["campaign"].map(campaign_source_map)

# frequency (user fatigue)
impressions = impressions.sort_values(["user_id", "timestamp"])
impressions["frequency"] = impressions.groupby("user_id").cumcount() + 1

# cost (CPM → per impression)
base_cpm = {
    "FB_Prospecting": 8,
    "GG_Search": 15,
    "TT_Scale": 5
}
impressions["cost"] = impressions["campaign"].map(base_cpm) / 1000
impressions["cost"] *= (1 + np.random.normal(0, 0.1, len(impressions)))

# =========================
# 2. CTR → CLICKS
# =========================
base_ctr = 0.03
ctr_mod = (
    (impressions["placement"] == "Search") * 0.04 +
    (impressions["device"] == "Mobile") * 0.01
)
impressions["ctr"] = (base_ctr + ctr_mod).clip(0.01, 0.15)

click_mask = np.random.rand(len(impressions)) < impressions["ctr"]
clicks = impressions[click_mask].copy()
clicks["click_id"] = range(1, len(clicks) + 1)
clicks["session_id"] = np.random.randint(1, 50000, len(clicks))

# =========================
# 3. CLICK CONVERSIONS
# =========================
base_cr = 0.1
cr_mod = (
    (clicks["campaign"] == "GG_Search") * 0.05 +
    (clicks["geo"] == "US") * 0.03 -
    clicks["frequency"] * 0.003
)
clicks["conv_prob"] = (base_cr + cr_mod).clip(0.01, 0.4)

conv_mask = np.random.rand(len(clicks)) < clicks["conv_prob"]
click_conversions = clicks[conv_mask].copy()
click_conversions["conversion_id"] = range(1, len(click_conversions)+1)
click_conversions["conversion_type"] = "purchase"

# revenue (depends on quality)
quality = np.random.beta(2, 5, len(click_conversions))
click_conversions["revenue"] = quality * np.random.uniform(20, 200, len(click_conversions))

# lag
lag_days = np.random.randint(0, 4, len(click_conversions))
click_conversions["conversion_time"] = click_conversions["timestamp"] + pd.to_timedelta(lag_days, unit="D")
click_conversions["attribution_type"] = "click"

# =========================
# 4. VIEW-THROUGH CONVERSIONS
# =========================
base_view = 0.02
view_mod = (
    (impressions["geo"] == "US") * 0.02 +
    (impressions["campaign"] == "FB_Prospecting") * 0.01
)
impressions["view_prob"] = (base_view + view_mod).clip(0.005, 0.1)

view_mask = np.random.rand(len(impressions)) < impressions["view_prob"]
view_conversions = impressions[view_mask].copy()
view_conversions["conversion_id"] = range(len(click_conversions)+1,
                                          len(click_conversions)+len(view_conversions)+1)
view_conversions["conversion_type"] = "purchase"
view_conversions["click_id"] = np.nan

quality_v = np.random.beta(2, 6, len(view_conversions))
view_conversions["revenue"] = quality_v * np.random.uniform(10, 150, len(view_conversions))

lag_days_v = np.random.randint(0, 3, len(view_conversions))
view_conversions["conversion_time"] = view_conversions["timestamp"] + pd.to_timedelta(lag_days_v, unit="D")
view_conversions["attribution_type"] = "view"

# =========================
# 5. MERGE CONVERSIONS
# =========================
fact_conversions = pd.concat([click_conversions, view_conversions], ignore_index=True)

# =========================
# 6. PRODUCT COST (COGS)
# =========================
geo_margin = {"US": 0.5, "UK": 0.45, "DE": 0.4, "IN": 0.3}
fact_conversions["geo_margin"] = fact_conversions["geo"].map(geo_margin)
noise = np.random.normal(0, 0.05, len(fact_conversions))
fact_conversions["product_cost"] = (fact_conversions["revenue"] *
                                    (fact_conversions["geo_margin"] + noise).clip(0.2, 0.8))
fact_conversions = fact_conversions.drop(columns=["geo_margin"])

# =========================
# 7. FINAL TABLES
# =========================
fact_impressions = impressions[[
    "impression_id","user_id","timestamp","campaign","source",
    "device","geo","placement","language","frequency","cost"
]]

fact_clicks = clicks[[
    "click_id","impression_id","user_id","timestamp","campaign",
    "source","device","geo","placement","language","session_id"
]]

fact_conversions = fact_conversions[[
    "conversion_id","user_id","click_id","impression_id",
    "conversion_time","conversion_type","revenue",
    "product_cost","attribution_type"
]]


# =========================
# SAVE
# =========================
fact_impressions.to_csv("../dataset/fact_impressions.csv", index=False)
fact_clicks.to_csv("../dataset/fact_clicks.csv", index=False)
fact_conversions.to_csv("../dataset/fact_conversions.csv", index=False)

print("Done")