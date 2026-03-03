# ============================================================
# 🌍 ClimateScope — Global Weather Analytics Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#Page setup ───────────────────────────────────────
st.set_page_config(
    page_title="ClimateScope 🌍",
    page_icon="🌤️",
    layout="wide"
)


# ================================
# BASIC THEME COLORS
# ================================

BACKGROUND_COLOR = "#f4f7fb"
PANEL_COLOR = "#ffffff"
TEXT_COLOR = "#2c3e50"
GRID_COLOR = "#dce6f2"


st.markdown(f"""
<style>
.stApp {{ background-color: {BACKGROUND_COLOR}; }}
</style>
""", unsafe_allow_html=True)



# Month order so charts show Jan → Dec (not A-Z alphabetical)
MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]

#Loaded and cleaned the data ─────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Dell\Downloads\GlobalWeatherRepository.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["year"]       = df["last_updated"].dt.year
    df["month"]      = df["last_updated"].dt.month
    df["month_name"] = df["last_updated"].dt.strftime("%b")

    numeric_cols = [
        "temperature_celsius", "temperature_fahrenheit",
        "humidity", "wind_kph", "pressure_mb",
        "air_quality_PM2.5", "air_quality_PM10",
        "air_quality_us-epa-index", "air_quality_gb-defra-index",
        "uv_index", "visibility_km", "cloud"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["temperature_celsius", "country"])
    return df

df = load_data()


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("🌍 ClimateScope — Global Weather Analytics")
st.write(f"Dataset contains **{len(df):,} records** "
         f"from **{df['country'].nunique()} countries**")
st.markdown("---")


# ============================================================
# SECTION 01 · KEY WEATHER INDICATORS (KPIs)
# ============================================================

st.subheader("01 · Key Weather Indicators")
st.caption("Average values across the entire dataset.")

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("🌡️ Avg Temp (°C)",      round(df["temperature_celsius"].mean(), 1))
col2.metric("💧 Avg Humidity (%)",    round(df["humidity"].mean(), 1))
col3.metric("💨 Avg Wind (kph)",      round(df["wind_kph"].mean(), 1))
col4.metric("🔵 Avg Pressure (mb)",   round(df["pressure_mb"].mean(), 1))
col5.metric("☀️ Avg UV Index",        round(df["uv_index"].mean(), 1))
col6.metric("👁️ Avg Visibility (km)", round(df["visibility_km"].mean(), 1))
st.markdown("---")


# ============================================================
# SECTION 02 · WORLD MAP (Choropleth)
# ============================================================

st.subheader("02 · Geographic Overview — Average Temperature by Country")
st.caption("Warmer/brighter colours = higher average temperature.")

country_avg_temp = (df.groupby("country")["temperature_celsius"]
                      .mean().reset_index())

fig_map = px.choropleth(
    country_avg_temp,
    locations="country",
    locationmode="country names",
    color="temperature_celsius",
    color_continuous_scale="Plasma",
    title="Global Average Temperature by Country",
    labels={"temperature_celsius": "Avg Temp (°C)"}
)
st.plotly_chart(fig_map, use_container_width=True)
st.markdown("---")


# ============================================================
# SECTION 03 · DATA DISTRIBUTIONS (TABS VERSION)
# ============================================================

st.subheader("03 · Data Distributions")
st.caption("Histograms show how values are spread across the dataset.")

# Created Tabs
tab1, tab2, tab3 = st.tabs([
    "🌡️ Temperature & Humidity",
    "🌬️ Wind & Pressure",
    "☀️ UV & Visibility"
])

# ------------------------------------------------------------
# TAB 1 · Temperature & Humidity
# ------------------------------------------------------------
with tab1:
    
    fig_temp = px.histogram(
        df,
        x="temperature_celsius",
        nbins=50,
        title="Temperature (°C) Distribution",
        labels={"temperature_celsius": "Temperature (°C)"},
        color_discrete_sequence=["tomato"]
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_humidity = px.histogram(
        df,
        x="humidity",
        nbins=50,
        title="Humidity (%) Distribution",
        labels={"humidity": "Humidity (%)"},
        color_discrete_sequence=["steelblue"]
    )
    st.plotly_chart(fig_humidity, use_container_width=True)


# ------------------------------------------------------------
# TAB 2 · Wind & Pressure
# ------------------------------------------------------------
with tab2:
    
    fig_wind = px.histogram(
        df,
        x="wind_kph",
        nbins=50,
        title="Wind Speed (kph) Distribution",
        labels={"wind_kph": "Wind Speed (kph)"},
        color_discrete_sequence=["mediumseagreen"]
    )
    st.plotly_chart(fig_wind, use_container_width=True)

    fig_pressure = px.histogram(
        df,
        x="pressure_mb",
        nbins=50,
        title="Pressure (mb) Distribution",
        labels={"pressure_mb": "Pressure (mb)"},
        color_discrete_sequence=["mediumpurple"]
    )
    st.plotly_chart(fig_pressure, use_container_width=True)


# ------------------------------------------------------------
# TAB 3 · UV & Visibility
# ------------------------------------------------------------
with tab3:
    
    fig_uv = px.histogram(
        df,
        x="uv_index",
        nbins=30,
        title="UV Index Distribution",
        labels={"uv_index": "UV Index"},
        color_discrete_sequence=["gold"]
    )
    st.plotly_chart(fig_uv, use_container_width=True)

    fig_visibility = px.histogram(
        df,
        x="visibility_km",
        nbins=50,
        title="Visibility (km) Distribution",
        labels={"visibility_km": "Visibility (km)"},
        color_discrete_sequence=["darkcyan"]
    )
    st.plotly_chart(fig_visibility, use_container_width=True)

st.markdown("---")


# ============================================================
# SECTION 04 · SEASONAL PATTERNS (Compact Layout)
# ============================================================

st.subheader("04 · Seasonal Patterns")
st.caption("Average values per calendar month across all countries and years.")

# Create 3 columns so charts sit side-by-side
col1, col2, col3 = st.columns(3)

# ------------------------------------------------------------
#1. Monthly Wind Speed Line
# ------------------------------------------------------------
with col1:
    monthly_wind = (
        df.groupby("month_name")["wind_kph"]
          .mean()
          .reindex(MONTH_ORDER)
          .reset_index()
    )

    fig_wind = px.line(
        monthly_wind,
        x="month_name",
        y="wind_kph",
        markers=True,
        title="Monthly Wind Speed",
        labels={"month_name": "Month",
                "wind_kph": "Avg Wind (kph)"}
    )

    fig_wind.update_layout(height=350)  # Reduce height
    st.plotly_chart(fig_wind, use_container_width=True)

# ------------------------------------------------------------
#2. Temperature Box Plot
# ------------------------------------------------------------
with col2:
    df["month_name"] = pd.Categorical(
        df["month_name"],
        categories=MONTH_ORDER,
        ordered=True
    )

    df_month_sorted = df.sort_values("month_name")

    fig_box = px.box(
        df_month_sorted,
        x="month_name",
        y="temperature_celsius",
        title="Temp Spread",
        labels={"month_name": "Month",
                "temperature_celsius": "Temp (°C)"}
    )

    fig_box.update_layout(height=350)
    st.plotly_chart(fig_box, use_container_width=True)

# ------------------------------------------------------------
#3. Monthly UV Index Bar
# ------------------------------------------------------------
with col3:
    monthly_uv = (
        df.groupby("month_name")["uv_index"]
          .mean()
          .reindex(MONTH_ORDER)
          .reset_index()
    )

    fig_uv = px.bar(
        monthly_uv,
        x="month_name",
        y="uv_index",
        title="Monthly UV Index",
        labels={"month_name": "Month",
                "uv_index": "Avg UV"}
    )

    fig_uv.update_layout(height=350)
    st.plotly_chart(fig_uv, use_container_width=True)

st.markdown("---")


# --- Temperature Heatmap: Top 15 Countries × Month ---
st.markdown("#### Temperature Heatmap — Top 15 Countries by Month")
st.caption("Each cell = average temperature for that country in that month. "
           "Red = hot, Blue = cold.")

top_countries = df["country"].value_counts().head(15).index
heatmap_data = (
    df[df["country"].isin(top_countries)]
    .pivot_table(values="temperature_celsius", index="country",
                 columns="month_name", aggfunc="mean")
    .reindex(columns=MONTH_ORDER)
)
fig_heat = px.imshow(heatmap_data, color_continuous_scale="RdYlBu_r",
                     title="Average Temperature by Country and Month",
                     labels={"color": "Temp (°C)"}, aspect="auto")
fig_heat.update_layout(height=450)
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown("---")


# ============================================================
# SECTION 05 · CORRELATION ANALYSIS
# ============================================================

st.subheader("05 · Correlation Analysis")
st.caption("**+1** = rise together · **-1** = opposite directions · **0** = no link")

corr_cols = ["temperature_celsius", "humidity", "wind_kph",
             "pressure_mb", "air_quality_PM2.5", "uv_index",
             "visibility_km", "cloud"]
fig_corr = px.imshow(df[corr_cols].corr(),
                     text_auto=True,
                     color_continuous_scale="RdBu_r",
                     zmin=-1, zmax=1,
                     title="Correlation Matrix — All Key Weather Variables")
st.plotly_chart(fig_corr, use_container_width=True)

# --- Scatter: PM2.5 vs PM10 ---
st.markdown("#### PM2.5 vs PM10 Air Pollutants")
st.caption("Each dot = one reading. Do both pollutants rise together?")

sample_data = df.sample(min(3000, len(df)), random_state=42)
fig_pm = px.scatter(sample_data,
                    x="air_quality_PM2.5", y="air_quality_PM10",
                    opacity=0.4, trendline="ols",
                    title="PM2.5 vs PM10 Concentration",
                    labels={"air_quality_PM2.5": "PM2.5",
                            "air_quality_PM10": "PM10"},
                    color_discrete_sequence=["darkorange"])
st.plotly_chart(fig_pm, use_container_width=True)

# --- Scatter: Temperature vs UV Index ---
st.markdown("#### Temperature vs UV Index")
st.caption("Do hotter places also have higher UV? The trendline tells the story.")

fig_uv_scatter = px.scatter(sample_data,
                             x="temperature_celsius", y="uv_index",
                             opacity=0.4, trendline="ols",
                             title="Temperature (°C) vs UV Index",
                             labels={"temperature_celsius": "Temperature (°C)",
                                     "uv_index": "UV Index"},
                             color_discrete_sequence=["gold"])
st.plotly_chart(fig_uv_scatter, use_container_width=True)
st.markdown("---")


# ============================================================
# SECTION 06 · REGIONAL COMPARISON
# ============================================================

st.subheader("06 · Regional Comparison")

# --- Hottest & Coldest ---
# Simple tables are easy to read and avoid chart clutter.
st.markdown("#### Top 10 Hottest & Coldest Countries")
st.caption("Average temperature per country, sorted to reveal extremes.")

country_avg = df.groupby("country")["temperature_celsius"].mean().reset_index()
country_avg.columns = ["Country", "Avg Temp (°C)"]
country_avg["Avg Temp (°C)"] = country_avg["Avg Temp (°C)"].round(1)

t1, t2 = st.columns(2)
with t1:
    top_hot = country_avg.sort_values("Avg Temp (°C)", ascending=False).head(10)
    top_hot = top_hot.reset_index(drop=True)
    top_hot.index += 1   # start rank from 1 instead of 0
    st.markdown("** Hottest Countries**")
    st.dataframe(top_hot, use_container_width=True)

with t2:
    top_cold = country_avg.sort_values("Avg Temp (°C)").head(10)
    top_cold = top_cold.reset_index(drop=True)
    top_cold.index += 1
    st.markdown("**Coldest Countries**")
    st.dataframe(top_cold, use_container_width=True)

# --- Violin Plot: Temperature distribution for Top 10 countries ---
# A violin plot shows the full shape of the distribution (not just the box).
# Wide = many readings at that value. Narrow = fewer readings.
st.markdown("#### Temperature Distribution — Top 10 Most Recorded Countries")
st.caption("The wider the violin, the more readings at that temperature level.")

top10_countries = df["country"].value_counts().head(10).index
df_top10 = df[df["country"].isin(top10_countries)]

fig_violin_temp = px.violin(df_top10, x="country", y="temperature_celsius",
                             box=True,       # showed a small box plot inside the violin
                             points=False,   # hid individual dots (too many)
                             title="Temperature Distribution by Country",
                             labels={"country": "Country",
                                     "temperature_celsius": "Temperature (°C)"},
                             color_discrete_sequence=["tomato"])
st.plotly_chart(fig_violin_temp, use_container_width=True)

# --- Temperature Volatility: ---
# Instead of just showing the standard deviation (one number),
# a box plot shows the actual spread of temperatures — much more informative
st.markdown("#### Temperature Spread — Top 10 Most Recorded Countries (Box Plot)")
st.caption("Taller box = bigger temperature range = more volatile climate.")

fig_box_country = px.box(df_top10, x="country", y="temperature_celsius",
                          title="Temperature Volatility by Country",
                          labels={"country": "Country",
                                  "temperature_celsius": "Temperature (°C)"},
                          color_discrete_sequence=["orange"])
st.plotly_chart(fig_box_country, use_container_width=True)

# --- Windiest Countries: Violin plot ---
st.markdown("#### Wind Speed Distribution — Top 10 Most Recorded Countries (Violin)")
st.caption("Shape shows how wind speeds are distributed — not just the average.")

fig_violin_wind = px.violin(df_top10, x="country", y="wind_kph",
                             box=True, points=False,
                             title="Wind Speed Distribution by Country",
                             labels={"country": "Country",
                                     "wind_kph": "Wind Speed (kph)"},
                             color_discrete_sequence=["mediumseagreen"])
st.plotly_chart(fig_violin_wind, use_container_width=True)

# --- Most Polluted Countries: Table ---
st.markdown("#### Top 10 Most Polluted Countries (PM2.5) — Table")
st.caption("Average PM2.5 concentration per country. Higher = worse air quality.")

pm25_table = (df.groupby("country")["air_quality_PM2.5"]
                .mean().sort_values(ascending=False)
                .head(10).reset_index())
pm25_table.columns = ["Country", "Avg PM2.5"]
pm25_table["Avg PM2.5"] = pm25_table["Avg PM2.5"].round(2)
pm25_table.index = range(1, len(pm25_table) + 1)
st.dataframe(pm25_table, use_container_width=True)

# --- UV Index by Country: Box plot ---
st.markdown("#### UV Index Distribution — Top 10 Most Recorded Countries")
st.caption("Box plots show the range of UV readings — not just the average.")

fig_box_uv = px.box(df_top10, x="country", y="uv_index",
                     title="UV Index Distribution by Country",
                     labels={"country": "Country", "uv_index": "UV Index"},
                     color_discrete_sequence=["goldenrod"])
st.plotly_chart(fig_box_uv, use_container_width=True)
st.markdown("---")


# ============================================================
# SECTION 07 · AIR QUALITY DEEP DIVE
# ============================================================

st.subheader("07 · Air Quality Deep Dive")
st.caption("Comparing PM2.5 and PM10 distributions in a single chart.")

# Convert wide → long format for single histogram
aq_data = df[["air_quality_PM2.5", "air_quality_PM10"]].melt(
    var_name="Pollutant",
    value_name="Concentration"
)

fig = px.histogram(
    aq_data,
    x="Concentration",
    color="Pollutant",
    nbins=60,
    barmode="overlay",   # overlays both histograms
    opacity=0.6,
    title="PM2.5 vs PM10 Distribution",
    labels={
        "Concentration": "Pollutant Concentration",
        "Pollutant": "Air Quality Metric"
    }
)

fig.update_layout(height=400)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")


# --- PM2.5 & PM10 by Country: Violin plot ---
# This shows the full shape of pollution data per country — far more insight
# than a simple average bar chart.
st.markdown("#### PM2.5 Distribution by Country")
st.caption("Wide = many readings at that pollution level. "
           "The inner box shows the median and middle 50% range.")

fig_violin_pm = px.violin(df_top10, x="country", y="air_quality_PM2.5",
                           box=True, points=False,
                           title="PM2.5 Pollution Distribution by Country",
                           labels={"country": "Country",
                                   "air_quality_PM2.5": "PM2.5 Concentration"},
                           color_discrete_sequence=["saddlebrown"])
st.plotly_chart(fig_violin_pm, use_container_width=True)

# --- US EPA vs UK DEFRA Air Quality Index Comparison ---
st.markdown("#### 🇺🇸 vs 🇬🇧 Air Quality Index Comparison (US EPA vs UK DEFRA)")
st.caption("Each index uses a different scale to rate air quality. "
           "Higher score = worse air. See how the two systems compare.")

epa_counts  = df["air_quality_us-epa-index"].value_counts().sort_index().reset_index()
epa_counts.columns  = ["Index Level", "Count"]
epa_counts["System"] = "US EPA"

defra_counts = df["air_quality_gb-defra-index"].value_counts().sort_index().reset_index()
defra_counts.columns  = ["Index Level", "Count"]
defra_counts["System"] = "UK DEFRA"

combined_aq = pd.concat([epa_counts, defra_counts])

fig_aq = px.bar(combined_aq, x="Index Level", y="Count", color="System",
                barmode="group",
                title="US EPA vs UK DEFRA Air Quality Index — Reading Counts by Level",
                labels={"Index Level": "AQI Level", "Count": "Number of Readings"},
                color_discrete_sequence=["royalblue", "crimson"])
st.plotly_chart(fig_aq, use_container_width=True)
st.markdown("---")


# ============================================================
# SECTION 08 · EXTREME WEATHER EVENTS
# ============================================================

st.subheader("08 · Extreme Weather Events")
st.caption("Heat > 95th percentile · Cold < 5th percentile · "
           "Wind > 95th percentile · Pollution > 95th percentile")

heat_threshold = df["temperature_celsius"].quantile(0.95)
cold_threshold = df["temperature_celsius"].quantile(0.05)
wind_threshold = df["wind_kph"].quantile(0.95)
poll_threshold = df["air_quality_PM2.5"].quantile(0.95)

e1, e2, e3, e4 = st.columns(4)
e1.metric("Extreme Heat Events",
          f"{(df['temperature_celsius'] >= heat_threshold).sum():,}",
          help=f"Temperature above {heat_threshold:.1f}°C")
e2.metric("Extreme Cold Events",
          f"{(df['temperature_celsius'] <= cold_threshold).sum():,}",
          help=f"Temperature below {cold_threshold:.1f}°C")
e3.metric("Extreme Wind Events",
          f"{(df['wind_kph'] >= wind_threshold).sum():,}",
          help=f"Wind above {wind_threshold:.1f} kph")
e4.metric("Extreme Pollution Events",
          f"{(df['air_quality_PM2.5'] >= poll_threshold).sum():,}",
          help=f"PM2.5 above {poll_threshold:.1f}")

# --- Extreme Heat Events per Country: Table instead of bar chart ---
st.markdown("#### Countries with Most Extreme Heat Events — Table")
st.caption(f"Readings where temperature exceeded {heat_threshold:.1f}°C (95th percentile).")

heat_df = df[df["temperature_celsius"] >= heat_threshold]
heat_table = (heat_df.groupby("country").size()
                     .sort_values(ascending=False).head(10).reset_index())
heat_table.columns = ["Country", "Extreme Heat Readings"]
heat_table.index = range(1, len(heat_table) + 1)
st.dataframe(heat_table, use_container_width=True)
st.markdown("---")


# ============================================================
# SECTION 09 · VISIBILITY & CLOUD COVER ANALYSIS
# ============================================================

st.subheader("09 · Visibility & Cloud Cover Analysis")
st.caption("Visibility shows how far you can see. Cloud cover shows how overcast the sky is.")

# --- Cloud Cover by Country: Violin plot ---
st.markdown("#### Cloud Cover Distribution — Top 10 Most Recorded Countries")
st.caption("Wide at the top = often very cloudy. Wide at the bottom = often clear skies.")

fig_violin_cloud = px.violin(df_top10, x="country", y="cloud",
                              box=True, points=False,
                              title="Cloud Cover (%) Distribution by Country",
                              labels={"country": "Country",
                                      "cloud": "Cloud Cover (%)"},
                              color_discrete_sequence=["slategray"])
st.plotly_chart(fig_violin_cloud, use_container_width=True)

# --- Scatter: Visibility vs Cloud Cover ---
st.markdown("#### Visibility vs Cloud Cover")
st.caption("Do cloudier skies reduce visibility? The scatter plot shows the relationship.")

fig_vis_cloud = px.scatter(sample_data,
                            x="cloud", y="visibility_km",
                            opacity=0.4, trendline="ols",
                            title="Cloud Cover (%) vs Visibility (km)",
                            labels={"cloud": "Cloud Cover (%)",
                                    "visibility_km": "Visibility (km)"},
                            color_discrete_sequence=["slateblue"])
st.plotly_chart(fig_vis_cloud, use_container_width=True)
st.markdown("---")


# ============================================================
# SECTION 10 · ANOMALY DETECTION
# ============================================================
# ── Z-Score Method ──────────────────────────────────────────
#   Formula:  z = (value − mean) / standard_deviation
#   If |z| > 3 → more than 3 std deviations away → unusual!
#
# ── IQR Method ──────────────────────────────────────────────
#   IQR = Q3 − Q1  (the range of the middle 50% of data)
#   Lower fence = Q1 − 1.5 × IQR
#   Upper fence = Q3 + 1.5 × IQR

st.subheader("10 · Anomaly Detection")
st.caption("Two standard methods for detecting unusual readings — applied to "
           "Temperature, Wind Speed, and PM2.5.")

# --- Temperature Anomalies ---
df["z_temp"] = ((df["temperature_celsius"] - df["temperature_celsius"].mean())
                 / df["temperature_celsius"].std())

Q1_t, Q3_t = df["temperature_celsius"].quantile(0.25), df["temperature_celsius"].quantile(0.75)
IQR_t      = Q3_t - Q1_t
z_count_temp   = (df["z_temp"].abs() > 3).sum()
iqr_count_temp = ((df["temperature_celsius"] < Q1_t - 1.5*IQR_t) |
                   (df["temperature_celsius"] > Q3_t + 1.5*IQR_t)).sum()

# --- Wind Speed Anomalies ---
df["z_wind"] = ((df["wind_kph"] - df["wind_kph"].mean())
                 / df["wind_kph"].std())

Q1_w, Q3_w = df["wind_kph"].quantile(0.25), df["wind_kph"].quantile(0.75)
IQR_w      = Q3_w - Q1_w
z_count_wind   = (df["z_wind"].abs() > 3).sum()
iqr_count_wind = ((df["wind_kph"] < Q1_w - 1.5*IQR_w) |
                   (df["wind_kph"] > Q3_w + 1.5*IQR_w)).sum()

# --- PM2.5 Anomalies ---
df["z_pm25"] = ((df["air_quality_PM2.5"] - df["air_quality_PM2.5"].mean())
                 / df["air_quality_PM2.5"].std())
z_count_pm25 = (df["z_pm25"].abs() > 3).sum()

an1, an2, an3, an4, an5 = st.columns(5)
an1.metric("Temp Z-Score Anomalies",  f"{z_count_temp:,}",   help="|z| > 3")
an2.metric("Temp IQR Anomalies",       f"{iqr_count_temp:,}", help="Outside IQR fences")
an3.metric("Wind Z-Score Anomalies",   f"{z_count_wind:,}",   help="|z| > 3")
an4.metric("Wind IQR Anomalies",        f"{iqr_count_wind:,}", help="Outside IQR fences")
an5.metric("PM2.5 Z-Score Anomalies", f"{z_count_pm25:,}",   help="|z| > 3")

# Histogram of temperature z-scores
fig_z = px.histogram(df, x="z_temp", nbins=80,
                     title="Temperature Z-Score Distribution — Red lines mark ±3 anomaly boundaries",
                     labels={"z_temp": "Z-Score"},
                     color_discrete_sequence=["mediumpurple"])
fig_z.add_vline(x= 3, line_dash="dash", line_color="red",
                annotation_text="z = +3 → anomaly zone")
fig_z.add_vline(x=-3, line_dash="dash", line_color="red",
                annotation_text="z = −3 → anomaly zone")
st.plotly_chart(fig_z, use_container_width=True)

# Histogram of wind z-scores
fig_zw = px.histogram(df, x="z_wind", nbins=80,
                      title="Wind Speed Z-Score Distribution — Red lines mark ±3 anomaly boundaries",
                      labels={"z_wind": "Z-Score"},
                      color_discrete_sequence=["mediumseagreen"])
fig_zw.add_vline(x= 3, line_dash="dash", line_color="red",
                 annotation_text="z = +3 → anomaly zone")
fig_zw.add_vline(x=-3, line_dash="dash", line_color="red",
                 annotation_text="z = −3 → anomaly zone")
st.plotly_chart(fig_zw, use_container_width=True)
st.markdown("---")


# ============================================================
# SECTION 11 · ROLLING AVERAGE TRENDS (Single Combined Graph)
# ============================================================

st.subheader("11 · 30-Day Rolling Average Trends")
st.caption("Temperature, Wind Speed and PM2.5 shown together for trend comparison.")

# Sort by date first
df_sorted = df.sort_values("last_updated")

# Calculate rolling averages
df_sorted["rolling_temp_30"] = df_sorted["temperature_celsius"].rolling(30).mean()
df_sorted["rolling_wind_30"] = df_sorted["wind_kph"].rolling(30).mean()
df_sorted["rolling_pm25_30"] = df_sorted["air_quality_PM2.5"].rolling(30).mean()

# Drop rows where rolling values are missing
df_rolling = df_sorted.dropna(subset=["rolling_temp_30",
                                      "rolling_wind_30",
                                      "rolling_pm25_30"])

# Create one combined line graph
fig_rolling = px.line(
    df_rolling,
    x="last_updated",
    y=["rolling_temp_30", "rolling_wind_30", "rolling_pm25_30"],
    title="30-Day Rolling Averages (Temperature, Wind & PM2.5)",
    labels={
        "last_updated": "Date",
        "value": "Rolling Average",
        "variable": "Metric"
    }
)

st.plotly_chart(fig_rolling, use_container_width=True)

st.markdown("---")

# ============================================================
# FOOTER
# ============================================================
st.caption("🌍 ClimateScope · Global Weather Analytics · "
           "Built with Streamlit & Plotly · Rachel Ferns")