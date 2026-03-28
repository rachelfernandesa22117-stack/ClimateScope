# ============================================================
# SiteGuard — Construction Weather Risk Dashboard
# ============================================================
# A simple Streamlit dashboard for civil engineering site
# managers to check weather suitability for outdoor
# construction work across different countries.
# ============================================================


# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# Page title and layout
st.set_page_config(page_title="Construction Weather Risk", layout="wide")

# ── Custom CSS styling ────────────────────────────────────────
BACKGROUND_COLOR = "#f5f5f0"    # off-white like site paper
ACCENT_COLOR     = "#e67e22"    # construction orange
SAFE_COLOR       = "#27ae60"    # green = safe to work
RISK_COLOR       = "#e74c3c"    # red = danger / stop work

st.markdown(f"""
<style>
    .stApp {{ background-color: {BACKGROUND_COLOR}; }}

    /* Orange left-border info box — general site notes */
    .site-note {{
        background-color: #fef9ef;
        border-left: 5px solid {ACCENT_COLOR};
        padding: 12px 16px;
        border-radius: 6px;
        margin: 8px 0 14px 0;
        color: #5a3e0a;
        font-size: 0.95rem;
    }}

    /* Red warning box — danger / stop-work advice */
    .danger-box {{
        background-color: #fdecea;
        border-left: 5px solid {RISK_COLOR};
        padding: 12px 16px;
        border-radius: 6px;
        margin: 8px 0 14px 0;
        color: #7b1a1a;
        font-size: 0.95rem;
    }}

    /* Green safe box — go-ahead advice */
    .safe-box {{
        background-color: #eafaf1;
        border-left: 5px solid {SAFE_COLOR};
        padding: 12px 16px;
        border-radius: 6px;
        margin: 8px 0 14px 0;
        color: #145a32;
        font-size: 0.95rem;
    }}
</style>
""", unsafe_allow_html=True)


# ── Reusable alert box functions ──────────────────────────────

def site_note(text):
    """Orange info box — general construction site notes."""
    st.markdown(f'<div class="site-note">📋 {text}</div>', unsafe_allow_html=True)

def danger_alert(text):
    """Red warning box — stop-work or high-risk conditions."""
    st.markdown(f'<div class="danger-box">🚨 {text}</div>', unsafe_allow_html=True)

def safe_alert(text):
    """Green box — safe-to-schedule conditions."""
    st.markdown(f'<div class="safe-box">🟢 {text}</div>', unsafe_allow_html=True)


# ── Construction safety thresholds ───────────────────────────
# These numbers come from international construction guidelines.
THRESHOLDS = {
    "temp_max":       40,   # °C  — too hot, stop-work risk
    "temp_min":        0,   # °C  — freezing (concrete curing, ice)
    "wind_caution":   40,   # kph — crane / elevated work gets risky
    "wind_stop":      60,   # kph — must stop cranes and scaffolding
    "pm25_caution":   35,   # µg/m³ — WHO 24h guideline
    "pm25_danger":    75,   # µg/m³ — hazardous for outdoor workers
    "uv_caution":      6,   # UV index — high sun exposure
    "uv_danger":      10,   # UV index — very high / extreme
    "humidity_max":   85,   # % — affects concrete cure & worker fatigue
    "visibility_min":  1,   # km — unsafe for operating machinery
}

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Dell\Downloads\GlobalWeatherRepository.csv")

    # Parse dates and pull out month info
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["year"]         = df["last_updated"].dt.year
    df["month"]        = df["last_updated"].dt.month
    df["month_name"]   = df["last_updated"].dt.strftime("%b")

    # Convert columns to numbers (bad values become NaN)
    numeric_cols = [
        "temperature_celsius", "humidity", "wind_kph",
        "pressure_mb", "air_quality_PM2.5", "air_quality_PM10",
        "air_quality_us-epa-index", "air_quality_gb-defra-index",
        "uv_index", "visibility_km", "cloud"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows missing temperature or country
    df = df.dropna(subset=["temperature_celsius", "country"])

    # Classify each reading as SAFE / CAUTION / DANGER
    def classify_risk(row):
        danger = (
            row["temperature_celsius"] >= THRESHOLDS["temp_max"] or
            row["temperature_celsius"] <= THRESHOLDS["temp_min"] or
            row["wind_kph"]            >= THRESHOLDS["wind_stop"] or
            row.get("air_quality_PM2.5", 0) >= THRESHOLDS["pm25_danger"]
        )
        caution = (
            row["wind_kph"] >= THRESHOLDS["wind_caution"] or
            row.get("air_quality_PM2.5", 0) >= THRESHOLDS["pm25_caution"] or
            row.get("uv_index", 0) >= THRESHOLDS["uv_caution"] or
            row["humidity"] >= THRESHOLDS["humidity_max"]
        )
        if danger:
            return "DANGER"
        elif caution:
            return "CAUTION"
        else:
            return "SAFE"

    df["risk_level"] = df.apply(classify_risk, axis=1)
    return df


df = load_data()


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.title("🏗️ SiteGuard — Construction Weather Risk Dashboard")
st.markdown(
    "**Who this is for:** Civil engineers and site managers scheduling "
    "outdoor construction work across multiple countries.  \n"
    "**How to use it:** Filter by country and month, then read each section "
    "to understand weather risk for your project location."
)
st.write(
    f"Dataset: **{len(df):,} weather readings** from "
    f"**{df['country'].nunique()} countries**"
)
st.markdown("---")



# ============================================================
# FILTER CONTROLS
# ============================================================

# st.expander() makes a collapsible panel — keeps the page tidy

with st.expander("🔍 Filter by Project Country & Month  (click to expand/collapse)", expanded=True):

    fc1, fc2 = st.columns(2)

    with fc1:
        all_countries = sorted(df["country"].unique())
        selected_countries = st.multiselect(
            label="🌍 Project Countries  (leave empty = ALL countries)",
            options=all_countries,
            default=[],
            placeholder="Start typing a country name…"
        )

    with fc2:
        selected_months = st.multiselect(
            label="📅 Planned Work Months  (leave empty = ALL months)",
            options=MONTH_ORDER,
            default=[]
        )

st.markdown("---")


# Apply filters
filtered_df = df.copy()
if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]
if selected_months:
    filtered_df = filtered_df[filtered_df["month_name"].isin(selected_months)]

if filtered_df.empty:
    st.warning("No data matches your filters. Try removing one of your selections.")
    st.stop()

if selected_countries or selected_months:
    site_note(
        f"Filters active — showing <strong>{len(filtered_df):,} records</strong> "
        f"from <strong>{filtered_df['country'].nunique()} countries</strong>."
    )

# Small sample for scatter plots (keeps the browser fast)
sample_data = filtered_df.sample(min(3000, len(filtered_df)), random_state=42)


# ============================================================
# SECTION 01 — SITE CONDITIONS AT A GLANCE (KPIs)
# ============================================================

st.subheader("01 · Site Conditions at a Glance")
st.caption("Average values from the filtered data.")

avg_temp = round(filtered_df["temperature_celsius"].mean(), 1)
avg_hum  = round(filtered_df["humidity"].mean(), 1)
avg_wind = round(filtered_df["wind_kph"].mean(), 1)
avg_pm25 = round(filtered_df["air_quality_PM2.5"].mean(), 1)
avg_uv   = round(filtered_df["uv_index"].mean(), 1)
avg_vis  = round(filtered_df["visibility_km"].mean(), 1)

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("🌡️ Avg Temp (°C)",      avg_temp, f"Limit: {THRESHOLDS['temp_max']}°C", delta_color="off")
k2.metric("💧 Avg Humidity (%)",    avg_hum,  f"Limit: {THRESHOLDS['humidity_max']}%", delta_color="off")
k3.metric("💨 Avg Wind (kph)",      avg_wind, f"Stop-work: {THRESHOLDS['wind_stop']} kph", delta_color="off")
k4.metric("☠️ Avg PM2.5",           avg_pm25, f"Danger: {THRESHOLDS['pm25_danger']} µg/m³", delta_color="off")
k5.metric("☀️ Avg UV Index",        avg_uv,   f"High: {THRESHOLDS['uv_caution']}+", delta_color="off")
k6.metric("👁️ Avg Visibility (km)", avg_vis,  f"Min safe: {THRESHOLDS['visibility_min']} km", delta_color="off")

# Risk count summary
n_safe    = (filtered_df["risk_level"] == "SAFE").sum()
n_caution = (filtered_df["risk_level"] == "CAUTION").sum()
n_danger  = (filtered_df["risk_level"] == "DANGER").sum()
total     = len(filtered_df)

st.subheader("Overall Risk Breakdown")
r1, r2, r3 = st.columns(3)
r1.metric("🟢 SAFE readings",    f"{n_safe:,}",    f"{n_safe/total*100:.1f}% of data")
r2.metric("⚠️ CAUTION readings", f"{n_caution:,}", f"{n_caution/total*100:.1f}% of data")
r3.metric("🛑 DANGER readings",  f"{n_danger:,}",  f"{n_danger/total*100:.1f}% of data")

# Contextual alert based on overall danger rate
danger_pct = n_danger / total * 100
if danger_pct >= 20:
    danger_alert(
        f"High overall danger rate detected ({danger_pct:.1f}% of readings). "
        "Review site scheduling carefully and ensure all stop-work protocols are in place."
    )
elif danger_pct >= 10:
    site_note(
        f"Moderate danger rate ({danger_pct:.1f}% of readings). "
        "Monitor conditions closely before committing to outdoor schedules."
    )
else:
    safe_alert(
        f"Low overall danger rate ({danger_pct:.1f}% of readings). "
        "Conditions are broadly favourable — standard site precautions apply."
    )

st.markdown("---")


# ============================================================
# SECTION 02 — GLOBAL RISK MAP
# ============================================================

st.subheader("02 · Global Risk Map — Where Is It Safe to Build?")
st.caption(
    "Risk score = % DANGER readings + (0.5 × % CAUTION readings) per country. "
    "Higher score = more risky."
)

# Calculate risk score per country*
risk_by_country = (
    filtered_df
    .groupby("country")["risk_level"]
    .value_counts(normalize=True)
    .mul(100)
    .rename("pct")
    .reset_index()
    .pivot_table(index="country", columns="risk_level", values="pct", fill_value=0)
    .reset_index()
)

for col in ["SAFE", "CAUTION", "DANGER"]:
    if col not in risk_by_country.columns:
        risk_by_country[col] = 0

risk_by_country["risk_score"] = (
    risk_by_country["DANGER"] + 0.5 * risk_by_country["CAUTION"]
).round(1)

# Merge in average temperature
avg_temp_country = (
    filtered_df.groupby("country")["temperature_celsius"]
    .mean().round(1).reset_index()
    .rename(columns={"temperature_celsius": "avg_temp"})
)
risk_by_country = risk_by_country.merge(avg_temp_country, on="country", how="left")

m1, m2 = st.columns(2)

with m1:
    st.write("#### Construction Risk Score by Country")
    fig_risk_map = px.choropleth(
        risk_by_country,
        locations="country",
        locationmode="country names",
        color="risk_score",
        color_continuous_scale=["#2a9d8f", "#e9c46a", "#e76f51"],
        title="Risk Score (0 = safe · 100 = very risky)",
        labels={"risk_score": "Risk Score"},
        hover_data={"SAFE": ":.1f", "CAUTION": ":.1f", "DANGER": ":.1f"}
    )
    fig_risk_map.update_layout(height=380)
    st.plotly_chart(fig_risk_map, use_container_width=True)

with m2:
    st.write("#### Average Temperature by Country")
    fig_temp_map = px.choropleth(
        risk_by_country,
        locations="country",
        locationmode="country names",
        color="avg_temp",
        color_continuous_scale="RdYlBu_r",
        title="Average Temperature (°C)",
        labels={"avg_temp": "Avg Temp (°C)"}
    )
    fig_temp_map.update_layout(height=380)
    st.plotly_chart(fig_temp_map, use_container_width=True)

if not risk_by_country.empty:
    riskiest = risk_by_country.sort_values("risk_score", ascending=False).iloc[0]
    safest   = risk_by_country.sort_values("risk_score").iloc[0]
    danger_alert(
        f"<strong>{riskiest['country']}</strong> has the highest construction risk score "
        f"({riskiest['risk_score']:.1f}). Detailed risk mitigation plans are essential "
        "before scheduling outdoor work here."
    )
    safe_alert(
        f"<strong>{safest['country']}</strong> has the lowest risk score "
        f"({safest['risk_score']:.1f}) — most suitable for year-round outdoor work."
    )

st.markdown("---")


# ============================================================
# SECTION 03 — SEASONAL PLANNING
# ============================================================

st.subheader("03 · Seasonal Planning — Best Months to Build")
st.caption("Monthly averages help choose the safest scheduling windows.")

monthly_agg = (
    filtered_df.groupby("month_name")
    .agg(
        avg_temp   = ("temperature_celsius", "mean"),
        avg_wind   = ("wind_kph", "mean"),
        avg_hum    = ("humidity", "mean"),
        avg_pm25   = ("air_quality_PM2.5", "mean"),
        avg_uv     = ("uv_index", "mean"),
        pct_danger = ("risk_level", lambda x: (x == "DANGER").mean() * 100)
    )
    .reindex(MONTH_ORDER)
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    fig_mw = px.line(
        monthly_agg, x="month_name", y="avg_wind",
        markers=True,
        title="Monthly Average Wind Speed (kph)",
        labels={"month_name": "Month", "avg_wind": "Avg Wind (kph)"}
    )
    fig_mw.add_hline(y=THRESHOLDS["wind_stop"], line_dash="dash", line_color="red",
                     annotation_text=f"Stop-work: {THRESHOLDS['wind_stop']} kph")
    fig_mw.add_hline(y=THRESHOLDS["wind_caution"], line_dash="dot", line_color="orange",
                     annotation_text=f"Caution: {THRESHOLDS['wind_caution']} kph")
    fig_mw.update_layout(height=360)
    st.plotly_chart(fig_mw, use_container_width=True)

with col2:
    fig_mt = px.line(
        monthly_agg, x="month_name", y="avg_temp",
        markers=True,
        title="Monthly Average Temperature (°C)",
        labels={"month_name": "Month", "avg_temp": "Avg Temp (°C)"},
        color_discrete_sequence=["tomato"]
    )
    fig_mt.add_hline(y=THRESHOLDS["temp_max"], line_dash="dash", line_color="red",
                     annotation_text=f"Heat limit: {THRESHOLDS['temp_max']}°C")
    fig_mt.add_hline(y=THRESHOLDS["temp_min"], line_dash="dash", line_color="blue",
                     annotation_text=f"Freeze limit: {THRESHOLDS['temp_min']}°C")
    fig_mt.update_layout(height=360)
    st.plotly_chart(fig_mt, use_container_width=True)

fig_danger_month = px.bar(
    monthly_agg, x="month_name", y="pct_danger",
    title="% of DANGER Readings per Month",
    labels={"month_name": "Month", "pct_danger": "% DANGER Readings"},
    color="pct_danger",
    color_continuous_scale=["#2a9d8f", "#e9c46a", "#e76f51"]
)
fig_danger_month.update_layout(height=340, coloraxis_showscale=False)
st.plotly_chart(fig_danger_month, use_container_width=True)

safest_month   = monthly_agg.dropna(subset=["pct_danger"]).sort_values("pct_danger").iloc[0]
riskiest_month = monthly_agg.dropna(subset=["pct_danger"]).sort_values("pct_danger", ascending=False).iloc[0]
safe_alert(
    f"Best scheduling month: <strong>{safest_month['month_name']}</strong> "
    f"({safest_month['pct_danger']:.1f}% DANGER readings) — prioritise major pours and lifts here."
)
danger_alert(
    f"Highest-risk month: <strong>{riskiest_month['month_name']}</strong> "
    f"({riskiest_month['pct_danger']:.1f}% DANGER readings) — avoid scheduling critical outdoor work."
)

st.markdown("---")


# ============================================================
# SECTION 04 — SEASONAL HEATMAP
# ============================================================

st.subheader("04 · Seasonal Heatmap — Temperature by Country & Month")
st.caption(
    "Each cell shows the average temperature. "
    "Red = dangerously hot · Blue = freezing risk."
)

top15 = filtered_df["country"].value_counts().head(15).index
heatmap_data = (
    filtered_df[filtered_df["country"].isin(top15)]
    .pivot_table(
        values="temperature_celsius",
        index="country",
        columns="month_name",
        aggfunc="mean"
    )
    .reindex(columns=MONTH_ORDER)
)

fig_heat = px.imshow(
    heatmap_data,
    color_continuous_scale="RdYlBu_r",
    title="Average Temperature (°C) — Top 15 Countries by Month",
    labels={"color": "Avg Temp (°C)"},
    aspect="auto"
)
fig_heat.update_layout(height=480)
st.plotly_chart(fig_heat, use_container_width=True)

site_note(
    "Countries near the equator stay warm all year. "
    "Countries at higher latitudes have seasonal windows (10–30°C) "
    "ideal for most construction work."
)

st.markdown("---")


# ============================================================
# SECTION 05 — WIND RISK ANALYSIS
# ============================================================
st.subheader("05 · Wind Risk Analysis — Cranes, Scaffolding & Elevated Work")
st.caption(
    f"Caution threshold: {THRESHOLDS['wind_caution']} kph  ·  "
    f"Stop-work threshold: {THRESHOLDS['wind_stop']} kph"
)

fig_scatter = px.scatter(
    sample_data,
    x="wind_kph",
    y="pressure_mb",
    opacity=0.4,
    color="risk_level",
    color_discrete_map={
        "SAFE":    "#2a9d8f",
        "CAUTION": "#e9c46a",
        "DANGER":  "#e76f51"
    },
    title="Wind Speed vs Air Pressure",
    labels={
        "wind_kph":    "Wind Speed (kph)",
        "pressure_mb": "Air Pressure (mb)"
        }
)
# Red line = stop-work wind speed
fig_scatter.add_vline(
    x=THRESHOLDS["wind_stop"],
    line_dash="dash", line_color="red",
    annotation_text="🛑 Stop-work"
)
fig_scatter.update_layout(height=400)  # ← increased from 400
st.plotly_chart(fig_scatter, use_container_width=True)

danger_alert(
    "Low pressure + high wind = storm conditions. "
    "If pressure drops below <strong>990 mb</strong> and wind exceeds "
    f"<strong>{THRESHOLDS['wind_stop']} kph</strong>, "
    "suspend all crane and elevated work immediately."
)

st.markdown("---")


# ============================================================
# SECTION 06 — AIR QUALITY & WORKER HEALTH
# ============================================================

st.subheader("06 · Air Quality — Worker Health & Safety on Site")
st.caption(
    "Construction sites generate dust. Combined with background PM2.5/PM10, "
    "this can exceed safe limits and require PPE upgrades or work suspension."
)

aq1, aq2 = st.columns(2)

with aq1:
    fig_pm = px.histogram(
        filtered_df, x="air_quality_PM2.5", nbins=60,
        title="PM2.5 Distribution — All Readings",
        labels={"air_quality_PM2.5": "PM2.5 Concentration (µg/m³)"},
        color_discrete_sequence=["saddlebrown"]
    )
    fig_pm.add_vline(x=THRESHOLDS["pm25_caution"], line_dash="dot",
                     line_color="orange", annotation_text=f"⚠️ Caution ({THRESHOLDS['pm25_caution']})")
    fig_pm.add_vline(x=THRESHOLDS["pm25_danger"], line_dash="dash",
                     line_color="red", annotation_text=f"🛑 Danger ({THRESHOLDS['pm25_danger']})")
    fig_pm.update_layout(height=360)
    st.plotly_chart(fig_pm, use_container_width=True)

with aq2:
    fig_pm_sc = px.scatter(
        sample_data,
        x="air_quality_PM2.5", y="air_quality_PM10",
        opacity=0.4, trendline="ols",
        title="PM2.5 vs PM10 (do both rise together?)",
        labels={"air_quality_PM2.5": "PM2.5 (µg/m³)", "air_quality_PM10": "PM10 (µg/m³)"},
        color_discrete_sequence=["darkorange"]
    )
    fig_pm_sc.update_layout(height=360)
    st.plotly_chart(fig_pm_sc, use_container_width=True)

pm25_country = (
    filtered_df.groupby("country")["air_quality_PM2.5"]
    .mean().sort_values(ascending=False)
    .head(12).reset_index()
)
pm25_country.columns = ["Country", "Avg PM2.5"]

fig_pm_bar = px.bar(
    pm25_country, x="Country", y="Avg PM2.5",
    title="Top 12 Countries by Average PM2.5",
    labels={"Country": "Country", "Avg PM2.5": "Avg PM2.5 (µg/m³)"},
    color="Avg PM2.5",
    color_continuous_scale=["#e9c46a", "#e76f51"]
)
fig_pm_bar.add_hline(y=THRESHOLDS["pm25_danger"], line_dash="dash",
                     line_color="red", annotation_text="🛑 Danger threshold")
fig_pm_bar.update_layout(height=360, coloraxis_showscale=False)
st.plotly_chart(fig_pm_bar, use_container_width=True)

if not pm25_country.empty:
    worst_aq = pm25_country.iloc[0]
    danger_alert(
        f"<strong>{worst_aq['Country']}</strong> has the highest average PM2.5 "
        f"({worst_aq['Avg PM2.5']:.1f} µg/m³). Site managers there should "
        "enforce mandatory respirator use during prolonged earthworks."
    )

st.markdown("---")


# ============================================================
# SECTION 07 — STOP-WORK EVENT TRACKER
# ============================================================

st.subheader("07 · Stop-Work Event Tracker — Extreme Conditions")
st.caption("Counts of readings that exceed construction stop-work thresholds.")

n_heat    = int((filtered_df["temperature_celsius"] >= THRESHOLDS["temp_max"]).sum())
n_cold    = int((filtered_df["temperature_celsius"] <= THRESHOLDS["temp_min"]).sum())
n_wind    = int((filtered_df["wind_kph"]             >= THRESHOLDS["wind_stop"]).sum())
n_poll    = int((filtered_df["air_quality_PM2.5"]    >= THRESHOLDS["pm25_danger"]).sum())
n_low_vis = int((filtered_df["visibility_km"]        <= THRESHOLDS["visibility_min"]).sum())

sw1, sw2, sw3, sw4, sw5 = st.columns(5)
sw1.metric("🔥 Extreme Heat",   f"{n_heat:,}",    f"Temp ≥ {THRESHOLDS['temp_max']}°C")
sw2.metric("🧊 Freezing Risk",  f"{n_cold:,}",    f"Temp ≤ {THRESHOLDS['temp_min']}°C")
sw3.metric("🌪️ High Wind",      f"{n_wind:,}",    f"Wind ≥ {THRESHOLDS['wind_stop']} kph")
sw4.metric("☠️ Poor Air",       f"{n_poll:,}",    f"PM2.5 ≥ {THRESHOLDS['pm25_danger']} µg/m³")
sw5.metric("🌫️ Low Visibility", f"{n_low_vis:,}", f"Vis ≤ {THRESHOLDS['visibility_min']} km")

extreme_summary = pd.DataFrame({
    "Stop-Work Trigger": ["Extreme Heat", "Freezing Risk", "High Wind",
                          "Poor Air Quality", "Low Visibility"],
    "Number of Readings": [n_heat, n_cold, n_wind, n_poll, n_low_vis]
})

fig_sw = px.bar(
    extreme_summary, x="Stop-Work Trigger", y="Number of Readings",
    title="Stop-Work Events by Trigger Type",
    color="Stop-Work Trigger"
)
fig_sw.update_layout(height=380, showlegend=False)
st.plotly_chart(fig_sw, use_container_width=True)

st.write("#### Countries Most Affected by Extreme Heat (> 40°C)")
heat_df = filtered_df[filtered_df["temperature_celsius"] >= THRESHOLDS["temp_max"]]

if heat_df.empty:
    safe_alert("No extreme heat readings in the filtered data.")
else:
    heat_table = (
        heat_df.groupby("country").size()
        .sort_values(ascending=False).head(10).reset_index()
    )
    heat_table.columns = ["Country", "Extreme Heat Readings"]
    heat_table.index = range(1, len(heat_table) + 1)

    st.dataframe(heat_table, use_container_width=True)  # ← only once

    danger_alert(
        f"<strong>{heat_table.iloc[0]['Country']}</strong> has the most extreme heat readings "
        f"({heat_table.iloc[0]['Extreme Heat Readings']:,} records above 40°C). "
        "Outdoor concrete placement in extreme heat risks rapid moisture loss and cracking."
    )

st.markdown("---")


# ============================================================
# SECTION 08 — STATISTICAL ANALYSIS & ANOMALY DETECTION
# ============================================================

st.subheader("08 · Statistical Analysis & Anomaly Detection")
st.caption(
    "Z-scores flag readings unusually far from the average. "
    "IQR fences catch outliers regardless of distribution shape. "
    "Skewness shows whether extreme values skew high or low."
)

fdf = filtered_df.copy()

# Z-scores
fdf["z_temp"] = (fdf["temperature_celsius"] - fdf["temperature_celsius"].mean()) / fdf["temperature_celsius"].std()
fdf["z_wind"] = (fdf["wind_kph"] - fdf["wind_kph"].mean()) / fdf["wind_kph"].std()
fdf["z_pm25"] = (fdf["air_quality_PM2.5"] - fdf["air_quality_PM2.5"].mean()) / fdf["air_quality_PM2.5"].std()

# IQR fences
Q1_t, Q3_t = fdf["temperature_celsius"].quantile([0.25, 0.75])
IQR_t = Q3_t - Q1_t
Q1_w, Q3_w = fdf["wind_kph"].quantile([0.25, 0.75])
IQR_w = Q3_w - Q1_w

# Skewness
skew_temp = fdf["temperature_celsius"].skew()
skew_wind = fdf["wind_kph"].skew()
skew_pm25 = fdf["air_quality_PM2.5"].skew()

# Counts
z_temp_n   = int((fdf["z_temp"].abs() > 3).sum())
iqr_temp_n = int(((fdf["temperature_celsius"] < Q1_t - 1.5 * IQR_t) | (fdf["temperature_celsius"] > Q3_t + 1.5 * IQR_t)).sum())
z_wind_n   = int((fdf["z_wind"].abs() > 3).sum())
iqr_wind_n = int(((fdf["wind_kph"] < Q1_w - 1.5 * IQR_w) | (fdf["wind_kph"] > Q3_w + 1.5 * IQR_w)).sum())
z_pm25_n   = int((fdf["z_pm25"].abs() > 3).sum())

a1, a2, a3, a4, a5 = st.columns(5)
a1.metric("Temp Z Anomalies",   f"{z_temp_n:,}",   "|z| > 3")
a2.metric("Temp IQR Anomalies", f"{iqr_temp_n:,}", "Outside IQR fences")
a3.metric("Wind Z Anomalies",   f"{z_wind_n:,}",   "|z| > 3")
a4.metric("Wind IQR Anomalies", f"{iqr_wind_n:,}", "Outside IQR fences")
a5.metric("PM2.5 Z Anomalies",  f"{z_pm25_n:,}",   "|z| > 3")

sk1, sk2, sk3 = st.columns(3)
sk1.metric("Temp Skewness",  f"{skew_temp:.2f}", "Positive = more extreme-heat days")
sk2.metric("Wind Skewness",  f"{skew_wind:.2f}", "Positive = rare but very high winds")
sk3.metric("PM2.5 Skewness", f"{skew_pm25:.2f}", "Positive = occasional very bad air quality")

h1, h2 = st.columns(2)
with h1:
    fig_zt = px.histogram(
        fdf, x="z_temp", nbins=80,
        title="Temperature Z-Score Distribution",
        labels={"z_temp": "Z-Score (Temperature)"},
        color_discrete_sequence=["tomato"]
    )
    fig_zt.add_vline(x= 3, line_dash="dash", line_color="red", annotation_text="+3 (anomaly)")
    fig_zt.add_vline(x=-3, line_dash="dash", line_color="red", annotation_text="-3 (anomaly)")
    fig_zt.update_layout(height=360)
    st.plotly_chart(fig_zt, use_container_width=True)

with h2:
    fig_zw = px.histogram(
        fdf, x="z_wind", nbins=80,
        title="Wind Speed Z-Score Distribution",
        labels={"z_wind": "Z-Score (Wind)"},
        color_discrete_sequence=["steelblue"]
    )
    fig_zw.add_vline(x= 3, line_dash="dash", line_color="red", annotation_text="+3 (anomaly)")
    fig_zw.add_vline(x=-3, line_dash="dash", line_color="red", annotation_text="-3 (anomaly)")
    fig_zw.update_layout(height=360)
    st.plotly_chart(fig_zw, use_container_width=True)

site_note(
    f"Filtered data has <strong>{z_temp_n:,}</strong> temperature anomalies and "
    f"<strong>{z_wind_n:,}</strong> wind anomalies (Z-score method). "
    "These are days far outside the normal range — review these before scheduling outdoor work."
)

st.markdown("---")


# ============================================================
# SECTION 09 — CORRELATION MATRIX
# ============================================================

st.subheader("09 · Correlation Matrix — How Weather Factors Relate")
st.caption(
    "+1 = always move together · -1 = opposite directions · 0 = no relationship."
)

# ── Pick only the variables that actually relate to each other ──
# Pressure and cloud cover were dropped — they showed weak/noisy
# relationships with the construction-relevant variables below.
corr_cols = [
    "temperature_celsius",   # heat risk
    "uv_index",              # sun exposure (closely tied to temperature)
    "humidity",              # affects concrete curing + worker fatigue
    "visibility_km",         # machinery safety
    "air_quality_PM2.5",     # air quality / dust
]

# Friendly display names so the chart is easy to read
corr_labels = {
    "temperature_celsius": "Temperature",
    "uv_index":            "UV Index",
    "humidity":            "Humidity",
    "visibility_km":       "Visibility",
    "air_quality_PM2.5":   "PM2.5",
}

# Calculate the correlation matrix
# .corr() gives every variable a score between -1 and +1 vs every other
corr_matrix = filtered_df[corr_cols].corr()

# Replace the raw column names with the friendly labels
corr_matrix.index   = [corr_labels[c] for c in corr_matrix.index]
corr_matrix.columns = [corr_labels[c] for c in corr_matrix.columns]

# Plot — red = strong positive, blue = strong negative, white = no link
fig_corr = px.imshow(
    corr_matrix,
    text_auto=".2f",              # show 2 decimal places in each cell
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    title="Correlation Matrix — Key Construction Weather Variables",
    width=500,                    # smaller and more focused than before
    height=420,
)

# Clean up axis labels and centre the chart
fig_corr.update_layout(
    coloraxis_colorbar=dict(title="r value"),
    margin=dict(l=20, r=20, t=50, b=20),
)

st.plotly_chart(fig_corr, use_container_width=False)   # False keeps the fixed width above

# ── Plain-English explanation of the key relationships ──────
site_note(
    "<strong>Temperature ↔ UV Index</strong> — strong positive link: hot days are sunny days. "
    "Both peak at midday, so schedule heavy outdoor work for early morning."
)
site_note(
    "<strong>Humidity ↔ Visibility</strong> — negative link: foggy, humid air cuts visibility, "
    "raising machinery risk. Watch for this combination on overcast mornings."
)
danger_alert(
    "<strong>PM2.5 ↔ Visibility</strong> — negative link: dusty air also reduces visibility. "
    "If PM2.5 is high AND visibility is dropping, pause machinery and issue respirators."
)

st.markdown("---")

# ============================================================
# SECTION 10 — VISIBILITY & CLOUD COVER
# ============================================================

st.subheader("10 · Visibility & Cloud Cover — Machinery Operation Safety")
st.caption(
    "Low visibility is a direct safety hazard for heavy machinery, "
    "reversing vehicles, and crane lifts."
)

vc1, vc2 = st.columns(2)

with vc1:
    fig_vis = px.scatter(
        sample_data, x="cloud", y="visibility_km",
        opacity=0.35, trendline="ols",
        title="Cloud Cover (%) vs Visibility (km)",
        labels={"cloud": "Cloud Cover (%)", "visibility_km": "Visibility (km)"},
        color_discrete_sequence=["slateblue"]
    )
    fig_vis.add_hline(y=THRESHOLDS["visibility_min"], line_dash="dash",
                      line_color="red",
                      annotation_text=f"🛑 Min safe: {THRESHOLDS['visibility_min']} km")
    fig_vis.update_layout(height=360)
    st.plotly_chart(fig_vis, use_container_width=True)

with vc2:
    fig_vih = px.histogram(
        filtered_df, x="visibility_km", nbins=50,
        title="Visibility Distribution",
        labels={"visibility_km": "Visibility (km)"},
        color_discrete_sequence=["darkcyan"]
    )
    fig_vih.add_vline(x=THRESHOLDS["visibility_min"], line_dash="dash",
                      line_color="red", annotation_text="🛑 Min safe")
    fig_vih.update_layout(height=360)
    st.plotly_chart(fig_vih, use_container_width=True)

top10_countries = filtered_df["country"].value_counts().head(10).index
df_top10        = filtered_df[filtered_df["country"].isin(top10_countries)]

fig_vc = px.violin(
    df_top10, x="country", y="cloud",
    box=True, points=False,
    title="Cloud Cover Distribution — Top 10 Most Recorded Countries",
    labels={"country": "Country", "cloud": "Cloud Cover (%)"},
    color_discrete_sequence=["slategray"]
)
fig_vc.update_layout(height=380)
st.plotly_chart(fig_vc, use_container_width=True)

danger_alert(
    f"Readings below {THRESHOLDS['visibility_min']} km should trigger a "
    "machinery pause until conditions improve. Cloudy, humid days are most likely to drop visibility to unsafe levels."
)

st.markdown("---")


# ============================================================
# SECTION 11 — ROLLING TREND MONITOR
# ============================================================

st.subheader("11 · Rolling Trend Monitor — Is Risk Improving or Worsening?")
st.caption(
    "30-reading rolling averages smooth out daily spikes and reveal the underlying trend. "
    "Select one country in the filter above for a clearer picture."
)

df_sorted = filtered_df.sort_values("last_updated").copy()

df_sorted["rolling_temp"] = df_sorted["temperature_celsius"].rolling(30).mean()
df_sorted["rolling_wind"] = df_sorted["wind_kph"].rolling(30).mean()
df_sorted["rolling_pm25"] = df_sorted["air_quality_PM2.5"].rolling(30).mean()

df_roll = df_sorted.dropna(subset=["rolling_temp", "rolling_wind", "rolling_pm25"])

r1_tab, r2_tab, r3_tab = st.tabs(["🌡Temperature Trend", "🌫️ Wind Trend", "☠️ PM2.5 Trend"])

with r1_tab:
    fig_rt = px.line(
        df_roll, x="last_updated", y="rolling_temp",
        title="30-Reading Rolling Average — Temperature (°C)",
        labels={"last_updated": "Date", "rolling_temp": "Rolling Avg Temp (°C)"},
        color_discrete_sequence=["tomato"]
    )
    fig_rt.add_hline(y=THRESHOLDS["temp_max"], line_dash="dash", line_color="red",
                     annotation_text=f"🛑 Heat limit: {THRESHOLDS['temp_max']}°C")
    st.plotly_chart(fig_rt, use_container_width=True)

with r2_tab:
    fig_rw = px.line(
        df_roll, x="last_updated", y="rolling_wind",
        title="30-Reading Rolling Average — Wind Speed (kph)",
        labels={"last_updated": "Date", "rolling_wind": "Rolling Avg Wind (kph)"},
        color_discrete_sequence=["steelblue"]
    )
    fig_rw.add_hline(y=THRESHOLDS["wind_stop"], line_dash="dash", line_color="red",
                     annotation_text=f"🛑 Stop-work: {THRESHOLDS['wind_stop']} kph")
    st.plotly_chart(fig_rw, use_container_width=True)

with r3_tab:
    fig_rp = px.line(
        df_roll, x="last_updated", y="rolling_pm25",
        title="30-Reading Rolling Average — PM2.5 (µg/m³)",
        labels={"last_updated": "Date", "rolling_pm25": "Rolling Avg PM2.5"},
        color_discrete_sequence=["saddlebrown"]
    )
    fig_rp.add_hline(y=THRESHOLDS["pm25_danger"], line_dash="dash", line_color="red",
                     annotation_text=f"🛑 Danger: {THRESHOLDS['pm25_danger']} µg/m³")
    st.plotly_chart(fig_rp, use_container_width=True)

site_note(
    "Select a single country in the top filter to see its own trend clearly. "
    "A rising rolling temperature or PM2.5 line is a signal to prepare "
    "additional precautions — or re-schedule."
)

st.markdown("---")


# ============================================================
# SECTION 12 — COUNTRY SUITABILITY SUMMARY TABLE
# ============================================================

st.subheader("12 · Country Suitability Summary — Quick Planning Reference")
st.caption("Compare key construction weather indicators per country.")

summary = (
    filtered_df.groupby("country")
    .agg(
        avg_temp   = ("temperature_celsius", "mean"),
        avg_wind   = ("wind_kph", "mean"),
        avg_hum    = ("humidity", "mean"),
        avg_pm25   = ("air_quality_PM2.5", "mean"),
        avg_vis    = ("visibility_km", "mean"),
        pct_danger = ("risk_level", lambda x: round((x == "DANGER").mean() * 100, 1)),
        pct_safe   = ("risk_level", lambda x: round((x == "SAFE").mean() * 100, 1))
    )
    .reset_index()
)

summary.columns = [
    "Country", "Avg Temp (°C)", "Avg Wind (kph)", "Avg Humidity (%)",
    "Avg PM2.5", "Avg Visibility (km)", "% DANGER", "% SAFE"
]
summary = summary.round(1)

# Highlight functions
def colour_danger(val):
    if val >= 20:
        return "background-color: #fee2e2; color: #991b1b"
    elif val >= 10:
        return "background-color: #fef3c7; color: #92400e"
    return ""

def colour_safe(val):
    if val >= 70:
        return "background-color: #d1fae5; color: #065f46"
    return ""

sort_col  = st.selectbox("Sort table by:", ["% SAFE", "% DANGER", "Avg Temp (°C)", "Avg Wind (kph)", "Avg PM2.5"], index=0)
ascending = st.checkbox("Sort ascending?", value=False)

display_summary = summary.sort_values(sort_col, ascending=ascending).reset_index(drop=True)
display_summary.index = range(1, len(display_summary) + 1)

st.dataframe(
    display_summary.style
    .applymap(colour_danger, subset=["% DANGER"])
    .applymap(colour_safe,   subset=["% SAFE"]),
    use_container_width=True
)

safe_alert(
    "Green cells (% SAFE ≥ 70%) highlight the most construction-friendly climates — "
    "ideal candidates for year-round scheduling without additional weather contingency."
)
danger_alert(
    "Red cells (% DANGER ≥ 20%) flag locations requiring detailed risk mitigation plans, "
    "enhanced PPE protocols, and flexible rescheduling windows built into the project programme."
)

st.markdown("---")


# ============================================================
# FOOTER
# ============================================================

st.write("---")
st.write(
    "🏗️ **SiteGuard** — Construction Weather Risk Dashboard | "
    "Built with Streamlit & Plotly · Rachel Fernades | "
    "Data: GlobalWeatherRepository | "
    "Thresholds based on international construction safety guidelines"
)
