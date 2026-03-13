# ============================================================
# 🌍 ClimateScope — Global Weather Analytics Dashboard
# ============================================================



#Import the libraries we need ────────────────────

import streamlit as st        # builds the web dashboard
import pandas as pd           # reads & processes CSV data
import numpy as np            # maths helpers (mean, std, etc.)
import plotly.express as px   # draws beautiful interactive charts


#Page configuration ──────────────────────────────

st.set_page_config(
    page_title="ClimateScope 🌍",
    page_icon="🌤️",
    layout="wide"
)


#Custom CSS styling ──────────────────────────────
#injected a small block here to set colours and style


BACKGROUND_COLOR = "#f0f4f8"   # very light blue-grey
ACCENT_COLOR     = "#2563eb"   # bold blue used for highlights

st.markdown(f"""
<style>
    /* Set the main page background colour */
    .stApp {{ background-color: {BACKGROUND_COLOR}; }}

    /* Style the blue insight/finding boxes */
    .insight-box {{
        background-color: #dbeafe;
        border-left: 5px solid {ACCENT_COLOR};
        padding: 12px 16px;
        border-radius: 6px;
        margin: 8px 0 14px 0;
        color: #1e3a5f;
        font-size: 0.95rem;
    }}
</style>
""", unsafe_allow_html=True)


#Reusable insight box function ───────────────────

def insight(text):
    """Displays a styled blue insight box with a lightbulb emoji."""
    st.markdown(
        f'<div class="insight-box">💡 {text}</div>',
        unsafe_allow_html=True
    )


#Month order list ─────────────────────────────────

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


#Load and clean the data ─────────────────────────

@st.cache_data
def load_data():
    # ── Read the CSV file ────────────────────────────────────

    df = pd.read_csv(r"C:\Users\Dell\Downloads\GlobalWeatherRepository.csv")

    # Convert the date column from plain text into real Python dates.
    
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    # Extract the year, month number and short month name
    
    df["year"]       = df["last_updated"].dt.year
    df["month"]      = df["last_updated"].dt.month
    df["month_name"] = df["last_updated"].dt.strftime("%b")

    
    # pd.to_numeric converts them and errors="coerce" turns any text/blank into NaN instead of crashing.
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

    # Removed rows where temperature or country is missing —
    
    df = df.dropna(subset=["temperature_celsius", "country"])
    return df


# Load the data once and stored it in the variable `df`
df = load_data()


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("🌍 ClimateScope — Global Weather Analytics")
st.write(
    f"Dataset contains **{len(df):,} records** "
    f"from **{df['country'].nunique()} countries**"
)
st.markdown("---")


# ============================================================
# FILTER CONTROLS
# ============================================================
# st.expander() creates a collapsible panel.

with st.expander("🔍 Filter the Data  (click to expand / collapse)", expanded=True):

    # Two columns side by side so both filters sit on one row
    fc1, fc2 = st.columns(2)

    with fc1:
        all_countries = sorted(df["country"].unique())

        selected_countries = st.multiselect(
            label="🌍 Select Countries  (leave empty = show ALL countries)",
            options=all_countries,
            default=[],
            placeholder="Start typing a country name..."
        )

    with fc2:
        selected_months = st.multiselect(
            label="📅 Select Months  (leave empty = show ALL months)",
            options=MONTH_ORDER,
            default=[]
        )

st.markdown("---")


# ── Applied the filters ────────────────────────────────────────


filtered_df = df.copy()   # copy so we never modify the original

# Only filter by country if the user actually selected some
if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

# Only filter by month if the user actually selected some
if selected_months:
    filtered_df = filtered_df[filtered_df["month_name"].isin(selected_months)]

# Safety check — if both filters together remove all data, warn the user
if filtered_df.empty:
    st.warning(
        "No data matches your current filters. "
        "Try removing one of the selections above."
    )
    st.stop()


# Shows a small banner whenever filters are active
if selected_countries or selected_months:
    st.info(
        f"Filters active — showing **{len(filtered_df):,} records** "
        f"from **{filtered_df['country'].nunique()} countries**. "
        f"All charts below reflect the filtered data."
    )


# ============================================================
# SECTION 01 · KEY WEATHER INDICATORS (KPIs)
# ============================================================

st.subheader("01 · Key Weather Indicators")
st.caption("Global averages calculated from the currently selected data.")

col1, col2, col3, col4, col5, col6 = st.columns(6)


col1.metric("🌡️ Avg Temp (°C)",      round(filtered_df["temperature_celsius"].mean(), 1))
col2.metric("💧 Avg Humidity (%)",    round(filtered_df["humidity"].mean(), 1))
col3.metric("💨 Avg Wind (kph)",      round(filtered_df["wind_kph"].mean(), 1))
col4.metric("🔵 Avg Pressure (mb)",   round(filtered_df["pressure_mb"].mean(), 1))
col5.metric("☀️ Avg UV Index",        round(filtered_df["uv_index"].mean(), 1))
col6.metric("👁️ Avg Visibility (km)", round(filtered_df["visibility_km"].mean(), 1))

st.markdown("---")


# ============================================================
# SECTION 02 · WORLD MAP — Average Temperature by Country
# ============================================================

st.subheader("02 · Geographic Overview — Average Temperature by Country")
st.caption("Brighter colour = hotter country. Hover over any country to see the value.")

# Calculates the average temperature per country (full dataset)
country_avg_temp = (
    df
    .groupby("country")["temperature_celsius"]
    .mean()
    .reset_index()
)

fig_map = px.choropleth(
    country_avg_temp,
    locations="country",
    locationmode="country names",
    color="temperature_celsius",
    color_continuous_scale="Plasma",   # dark purple → yellow gradient
    title="Global Average Temperature by Country",
    labels={"temperature_celsius": "Avg Temp (°C)"}
)
st.plotly_chart(fig_map, use_container_width=True)

# Dynamic insight — automatically finds the hottest country
hottest = country_avg_temp.sort_values("temperature_celsius", ascending=False).iloc[0]
insight(
    f"The hottest country in the full dataset is <b>{hottest['country']}</b> "
    f"with an average temperature of {hottest['temperature_celsius']:.1f}°C."
)

st.markdown("---")


# ============================================================
# SECTION 03 · DATA DISTRIBUTIONS
# ============================================================

st.subheader("03 · Data Distributions")
st.caption("How often does each value appear? Tall bar = that value is very common.")

tab1, tab2, tab3 = st.tabs([
    "🌡️ Temperature & Humidity",
    "🌬️ Wind & Pressure",
    "☀️ UV & Visibility"
])

# ── Tab 1: Temperature & Humidity ────────────────────────────
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig_t = px.histogram(
            filtered_df, x="temperature_celsius", nbins=50,
            title="Temperature Distribution",
            labels={"temperature_celsius": "Temperature (°C)"},
            color_discrete_sequence=["tomato"]
        )
        st.plotly_chart(fig_t, use_container_width=True)
    with c2:
        fig_h = px.histogram(
            filtered_df, x="humidity", nbins=50,
            title="Humidity Distribution",
            labels={"humidity": "Humidity (%)"},
            color_discrete_sequence=["steelblue"]
        )
        st.plotly_chart(fig_h, use_container_width=True)

    insight(
        "Temperature readings spread widely across the dataset — this reflects "
        "tropical, temperate, and polar climates all mixed together."
    )

# ── Tab 2: Wind & Pressure ───────────────────────────────────
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fig_w = px.histogram(
            filtered_df, x="wind_kph", nbins=50,
            title="Wind Speed Distribution",
            labels={"wind_kph": "Wind Speed (kph)"},
            color_discrete_sequence=["mediumseagreen"]
        )
        st.plotly_chart(fig_w, use_container_width=True)
    with c2:
        fig_pr = px.histogram(
            filtered_df, x="pressure_mb", nbins=50,
            title="Pressure Distribution",
            labels={"pressure_mb": "Pressure (mb)"},
            color_discrete_sequence=["mediumpurple"]
        )
        st.plotly_chart(fig_pr, use_container_width=True)

    insight(
        "Most wind speeds sit below 40 kph. "
        "Very high readings represent storms — they are rare but real."
    )

# ── Tab 3: UV & Visibility ───────────────────────────────────
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        fig_uv = px.histogram(
            filtered_df, x="uv_index", nbins=30,
            title="UV Index Distribution",
            labels={"uv_index": "UV Index"},
            color_discrete_sequence=["gold"]
        )
        st.plotly_chart(fig_uv, use_container_width=True)
    with c2:
        fig_vi = px.histogram(
            filtered_df, x="visibility_km", nbins=50,
            title="Visibility Distribution",
            labels={"visibility_km": "Visibility (km)"},
            color_discrete_sequence=["darkcyan"]
        )
        st.plotly_chart(fig_vi, use_container_width=True)

    insight(
        "A UV Index above 8 is rated 'Very High' — sun protection is essential. "
        "Most readings in this dataset fall between 1 and 6."
    )

st.markdown("---")


# ============================================================
# SECTION 04 · SEASONAL PATTERNS
# ============================================================

st.subheader("04 · Seasonal Patterns")
st.caption("Monthly averages for the filtered data — reveals seasonal trends.")

# ── Row 1: Wind line chart + Temperature box plot ────────────
col1, col2 = st.columns(2)

with col1:
    monthly_wind = (
        filtered_df.groupby("month_name")["wind_kph"]
        .mean()
        .reindex(MONTH_ORDER)
        .reset_index()
    )
    fig_mw = px.line(
        monthly_wind, x="month_name", y="wind_kph",
        markers=True,
        title="Monthly Average Wind Speed",
        labels={"month_name": "Month", "wind_kph": "Avg Wind (kph)"},
        color_discrete_sequence=[ACCENT_COLOR]
    )
    fig_mw.update_layout(height=360)
    st.plotly_chart(fig_mw, use_container_width=True)

with col2:
    temp_month = filtered_df.copy()
    temp_month["month_name"] = pd.Categorical(
        temp_month["month_name"],
        categories=MONTH_ORDER,
        ordered=True
    )
    temp_month = temp_month.sort_values("month_name")

    
    fig_bx = px.box(
        temp_month, x="month_name", y="temperature_celsius",
        title="Temperature Spread by Month",
        labels={"month_name": "Month", "temperature_celsius": "Temp (°C)"},
        color_discrete_sequence=["tomato"]
    )
    fig_bx.update_layout(height=360)
    st.plotly_chart(fig_bx, use_container_width=True)

# ── Monthly UV bar chart ─────────────────────────────────────
monthly_uv = (
    filtered_df.groupby("month_name")["uv_index"]
    .mean()
    .reindex(MONTH_ORDER)
    .reset_index()
)
fig_muv = px.bar(
    monthly_uv, x="month_name", y="uv_index",
    title="Monthly Average UV Index",
    labels={"month_name": "Month", "uv_index": "Avg UV Index"},
    color_discrete_sequence=["gold"]
)
fig_muv.update_layout(height=360)
st.plotly_chart(fig_muv, use_container_width=True)

# ── Temperature Heatmap ──────────────────────────────────────

st.markdown("#### Temperature Heatmap — Top 15 Countries × Month")
st.caption(
    "Each cell = average temperature for that country in that month. "
    "Red = hot · Blue = cold. Hover over any cell to see the exact value."
)

top15 = df["country"].value_counts().head(15).index
heatmap_data = (
    df[df["country"].isin(top15)]
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
    title="Average Temperature — Top 15 Countries by Month",
    labels={"color": "Temp (°C)"},
    aspect="auto"
)
fig_heat.update_layout(height=470)
st.plotly_chart(fig_heat, use_container_width=True)

insight(
    "Countries near the equator stay warm all year. "
    "Countries at higher latitudes show a dramatic "
    "hot-summer / cold-winter pattern — clearly visible in the heatmap."
)

st.markdown("---")


# ============================================================
# SECTION 05 · CORRELATION ANALYSIS
# ============================================================

st.subheader("05 · Correlation Analysis")
st.caption(
    "**+1** = always rise together  ·  "
    "**-1** = opposite directions  ·  "
    "**0** = no relationship"
)

corr_cols = [
    "temperature_celsius", "humidity", "wind_kph",
    "pressure_mb", "air_quality_PM2.5", "uv_index",
    "visibility_km", "cloud"
]


fig_corr = px.imshow(
    filtered_df[corr_cols].corr(),
    text_auto=True,
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    title="Correlation Matrix — Key Weather Variables"
)
fig_corr.update_layout(height=480)
st.plotly_chart(fig_corr, use_container_width=True)

insight(
    "Temperature and UV Index have a positive correlation — hotter places "
    "tend to have stronger UV. "
    "Humidity and visibility often move in opposite directions: "
    "high humidity (fog/haze) reduces how far you can see."
)

# ── Two scatter plots side by side ──────────────────────────

sample_data = filtered_df.sample(min(3000, len(filtered_df)), random_state=42)

sc1, sc2 = st.columns(2)

with sc1:
    st.markdown("#### PM2.5 vs PM10")
    st.caption("Do both pollutants rise together? The trendline shows the pattern.")
    fig_pm = px.scatter(
        sample_data,
        x="air_quality_PM2.5", y="air_quality_PM10",
        opacity=0.4,
        trendline="ols",   # OLS = straight line of best fit
        title="PM2.5 vs PM10 Concentration",
        labels={"air_quality_PM2.5": "PM2.5", "air_quality_PM10": "PM10"},
        color_discrete_sequence=["darkorange"]
    )
    st.plotly_chart(fig_pm, use_container_width=True)

with sc2:
    st.markdown("#### Temperature vs UV Index")
    st.caption("Do hotter places have higher UV?")
    fig_uv_sc = px.scatter(
        sample_data,
        x="temperature_celsius", y="uv_index",
        opacity=0.4,
        trendline="ols",
        title="Temperature vs UV Index",
        labels={"temperature_celsius": "Temp (°C)", "uv_index": "UV Index"},
        color_discrete_sequence=["gold"]
    )
    st.plotly_chart(fig_uv_sc, use_container_width=True)

st.markdown("---")


# ============================================================
# SECTION 06 · REGIONAL COMPARISON
# ============================================================

st.subheader("06 · Regional Comparison")

# ── Hottest & Coldest countries table ───────────────────────
st.markdown("#### Top 10 Hottest & Coldest Countries")
st.caption("Ranked by average temperature across all readings in the filtered data.")

country_avg = (
    filtered_df.groupby("country")["temperature_celsius"]
    .mean().reset_index()
)
country_avg.columns = ["Country", "Avg Temp (°C)"]
country_avg["Avg Temp (°C)"] = country_avg["Avg Temp (°C)"].round(1)

t1, t2 = st.columns(2)
with t1:
    top_hot = (country_avg
               .sort_values("Avg Temp (°C)", ascending=False)
               .head(10).reset_index(drop=True))
    top_hot.index += 1   # start rank at 1 not 0
    st.markdown("🔴 **Hottest Countries**")
    st.dataframe(top_hot, use_container_width=True)

with t2:
    top_cold = (country_avg
                .sort_values("Avg Temp (°C)")
                .head(10).reset_index(drop=True))
    top_cold.index += 1
    st.markdown("🔵 **Coldest Countries**")
    st.dataframe(top_cold, use_container_width=True)

if len(country_avg) >= 2:
    hottest = country_avg.sort_values("Avg Temp (°C)", ascending=False).iloc[0]
    coldest = country_avg.sort_values("Avg Temp (°C)").iloc[0]
    insight(
        f"In the filtered data, <b>{hottest['Country']}</b> "
        f"({hottest['Avg Temp (°C)']}°C) is the hottest country and "
        f"<b>{coldest['Country']}</b> ({coldest['Avg Temp (°C)']}°C) is the coldest."
    )

# ── Top-10 most recorded countries subset ───────────────────

top10_countries = filtered_df["country"].value_counts().head(10).index
df_top10        = filtered_df[filtered_df["country"].isin(top10_countries)]

# ── Temperature violin plot ──────────────────────────────────

st.markdown("#### Temperature Distribution — Top 10 Most Recorded Countries")
st.caption("Wider violin = more readings at that temperature.")

fig_vt = px.violin(
    df_top10, x="country", y="temperature_celsius",
    box=True,
    points=False,
    title="Temperature Distribution by Country",
    labels={"country": "Country", "temperature_celsius": "Temperature (°C)"},
    color_discrete_sequence=["tomato"]
)
st.plotly_chart(fig_vt, use_container_width=True)

# ── Most Polluted Countries table ───────────────────────────
st.markdown("#### Top 10 Most Polluted Countries (PM2.5)")
st.caption("Average PM2.5 — higher value = worse air quality.")

pm25_table = (
    filtered_df.groupby("country")["air_quality_PM2.5"]
    .mean().sort_values(ascending=False)
    .head(10).reset_index()
)
pm25_table.columns = ["Country", "Avg PM2.5"]
pm25_table["Avg PM2.5"] = pm25_table["Avg PM2.5"].round(2)
pm25_table.index = range(1, len(pm25_table) + 1)
st.dataframe(pm25_table, use_container_width=True)

if not pm25_table.empty:
    worst = pm25_table.iloc[0]
    insight(
        f"<b>{worst['Country']}</b> has the highest average PM2.5 "
        f"({worst['Avg PM2.5']}) in the filtered data — "
        f"a serious air pollution concern."
    )

st.markdown("---")


# ============================================================
# SECTION 07 · AIR QUALITY DEEP DIVE
# ============================================================

st.subheader("07 · Air Quality Deep Dive")

# ── Overlapping histogram: PM2.5 vs PM10 ────────────────────

st.caption("How are PM2.5 and PM10 concentrations distributed across all readings?")

aq_long = filtered_df[["air_quality_PM2.5", "air_quality_PM10"]].melt(
    var_name="Pollutant",
    value_name="Concentration"
)

fig_aq = px.histogram(
    aq_long,
    x="Concentration", color="Pollutant",
    nbins=60,
    barmode="overlay",
    opacity=0.6,
    title="PM2.5 vs PM10 Distribution",
    labels={"Concentration": "Pollutant Concentration",
            "Pollutant": "Pollutant Type"}
)
fig_aq.update_layout(height=400)
st.plotly_chart(fig_aq, use_container_width=True)

insight(
    "PM10 particles are larger and appear at higher concentrations, "
    "but PM2.5 particles are more dangerous — they are small enough "
    "to enter your bloodstream through the lungs."
)

# ── US EPA vs UK DEFRA bar chart ─────────────────────────────
st.markdown("#### 🇺🇸 US EPA vs 🇬🇧 UK DEFRA Air Quality Index Comparison")
st.caption(
    "The US and UK each use a different scale to rate air quality. "
    "Higher index level = worse air quality."
)

epa              = filtered_df["air_quality_us-epa-index"].value_counts().sort_index().reset_index()
epa.columns      = ["Index Level", "Count"]
epa["System"]    = "US EPA"

defra            = filtered_df["air_quality_gb-defra-index"].value_counts().sort_index().reset_index()
defra.columns    = ["Index Level", "Count"]
defra["System"]  = "UK DEFRA"

fig_aq_bar = px.bar(
    pd.concat([epa, defra]),
    x="Index Level", y="Count", color="System",
    barmode="group",
    title="US EPA vs UK DEFRA — Reading Counts by Index Level",
    labels={"Index Level": "AQI Level", "Count": "Number of Readings"},
    color_discrete_sequence=["royalblue", "crimson"]
)
st.plotly_chart(fig_aq_bar, use_container_width=True)

st.markdown("---")


# ============================================================
# SECTION 08 · EXTREME WEATHER EVENTS
# ============================================================
# "Extreme" is defined using percentiles

st.subheader("08 · Extreme Weather Events")
st.caption(
    "Heat > 95th percentile  ·  Cold < 5th percentile  ·  "
    "Wind > 95th percentile  ·  Pollution > 95th percentile"
)

heat_thresh = filtered_df["temperature_celsius"].quantile(0.95)
cold_thresh = filtered_df["temperature_celsius"].quantile(0.05)
wind_thresh = filtered_df["wind_kph"].quantile(0.95)
poll_thresh = filtered_df["air_quality_PM2.5"].quantile(0.95)

# Show counts in 4 metric boxes
e1, e2, e3, e4 = st.columns(4)
e1.metric("🔥 Extreme Heat",
          f"{(filtered_df['temperature_celsius'] >= heat_thresh).sum():,}",
          help=f"Temp >= {heat_thresh:.1f}°C")
e2.metric("🧊 Extreme Cold",
          f"{(filtered_df['temperature_celsius'] <= cold_thresh).sum():,}",
          help=f"Temp <= {cold_thresh:.1f}°C")
e3.metric("🌪️ Extreme Wind",
          f"{(filtered_df['wind_kph'] >= wind_thresh).sum():,}",
          help=f"Wind >= {wind_thresh:.1f} kph")
e4.metric("☠️ Extreme Pollution",
          f"{(filtered_df['air_quality_PM2.5'] >= poll_thresh).sum():,}",
          help=f"PM2.5 >= {poll_thresh:.1f}")

# ── Bar chart comparing all four extreme event types ─────────
extreme_summary = pd.DataFrame({
    "Event Type": ["Extreme Heat", "Extreme Cold", "Extreme Wind", "Extreme Pollution"],
    "Count": [
        int((filtered_df["temperature_celsius"] >= heat_thresh).sum()),
        int((filtered_df["temperature_celsius"] <= cold_thresh).sum()),
        int((filtered_df["wind_kph"]             >= wind_thresh).sum()),
        int((filtered_df["air_quality_PM2.5"]    >= poll_thresh).sum())
    ]
})

fig_ext = px.bar(
    extreme_summary, x="Event Type", y="Count",
    color="Event Type",
    title="Extreme Weather Event Counts",
    color_discrete_sequence=["tomato", "steelblue", "mediumseagreen", "saddlebrown"]
)
st.plotly_chart(fig_ext, use_container_width=True)

# ── Table: which countries have the most extreme heat? ───────
st.markdown("#### Countries with the Most Extreme Heat Events")
st.caption(f"Readings where temperature exceeded {heat_thresh:.1f}°C (95th percentile).")

heat_df    = filtered_df[filtered_df["temperature_celsius"] >= heat_thresh]
heat_table = (
    heat_df.groupby("country").size()
    .sort_values(ascending=False).head(10).reset_index()
)
heat_table.columns = ["Country", "Extreme Heat Readings"]
heat_table.index   = range(1, len(heat_table) + 1)
st.dataframe(heat_table, use_container_width=True)

if not heat_table.empty:
    insight(
        f"<b>{heat_table.iloc[0]['Country']}</b> has the most extreme heat "
        f"readings — {heat_table.iloc[0]['Extreme Heat Readings']:,} records "
        f"above {heat_thresh:.1f}°C."
    )

st.markdown("---")


# ============================================================
# SECTION 09 · VISIBILITY & CLOUD COVER
# ============================================================

st.subheader("09 · Visibility & Cloud Cover Analysis")
st.caption(
    "Visibility = how far you can see (km).  "
    "Cloud cover = percentage of sky that is covered (%)."
)

# ── Scatter: cloud cover vs visibility ──────────────────────
st.markdown("#### Does More Cloud Cover Reduce Visibility?")
st.caption("Each dot = one reading. The trendline shows the overall pattern.")

fig_vis = px.scatter(
    sample_data,
    x="cloud", y="visibility_km",
    opacity=0.35,
    trendline="ols",
    title="Cloud Cover (%) vs Visibility (km)",
    labels={"cloud": "Cloud Cover (%)", "visibility_km": "Visibility (km)"},
    color_discrete_sequence=["slateblue"]
)
st.plotly_chart(fig_vis, use_container_width=True)

insight(
    "The downward trendline confirms that cloudier skies generally "
    "reduce visibility — especially when low clouds bring fog or rain."
)

# ── Cloud cover violin by country ───────────────────────────
st.markdown("#### Cloud Cover Distribution — Top 10 Most Recorded Countries")
st.caption(
    "Wide near 100% = sky is often fully overcast.  "
    "Wide near 0% = sky is often clear."
)

fig_vc = px.violin(
    df_top10, x="country", y="cloud",
    box=True, points=False,
    title="Cloud Cover (%) Distribution by Country",
    labels={"country": "Country", "cloud": "Cloud Cover (%)"},
    color_discrete_sequence=["slategray"]
)
st.plotly_chart(fig_vc, use_container_width=True)

st.markdown("---")


# ============================================================
# SECTION 10 · ANOMALY DETECTION
# ============================================================

st.subheader("10 · Anomaly Detection")
st.caption(
    "Unusual readings flagged by two standard statistical methods: "
    "Z-Score (|z| > 3) and IQR fences."
)

# Worked on a copy so we don't add extra columns to filtered_df
fdf = filtered_df.copy()

# ── Temperature Z-scores ─────────────────────────────────────
fdf["z_temp"] = (
    (fdf["temperature_celsius"] - fdf["temperature_celsius"].mean())
    / fdf["temperature_celsius"].std()
)
Q1_t  = fdf["temperature_celsius"].quantile(0.25)
Q3_t  = fdf["temperature_celsius"].quantile(0.75)
IQR_t = Q3_t - Q1_t

z_temp_n   = int((fdf["z_temp"].abs() > 3).sum())
iqr_temp_n = int(
    ((fdf["temperature_celsius"] < Q1_t - 1.5 * IQR_t) |
     (fdf["temperature_celsius"] > Q3_t + 1.5 * IQR_t)).sum()
)

# ── Wind speed Z-scores ──────────────────────────────────────
fdf["z_wind"] = (
    (fdf["wind_kph"] - fdf["wind_kph"].mean())
    / fdf["wind_kph"].std()
)
Q1_w  = fdf["wind_kph"].quantile(0.25)
Q3_w  = fdf["wind_kph"].quantile(0.75)
IQR_w = Q3_w - Q1_w

z_wind_n   = int((fdf["z_wind"].abs() > 3).sum())
iqr_wind_n = int(
    ((fdf["wind_kph"] < Q1_w - 1.5 * IQR_w) |
     (fdf["wind_kph"] > Q3_w + 1.5 * IQR_w)).sum()
)

# ── PM2.5 Z-scores ───────────────────────────────────────────
fdf["z_pm25"] = (
    (fdf["air_quality_PM2.5"] - fdf["air_quality_PM2.5"].mean())
    / fdf["air_quality_PM2.5"].std()
)
z_pm25_n = int((fdf["z_pm25"].abs() > 3).sum())

# Shows counts in 5 metric boxes
a1, a2, a3, a4, a5 = st.columns(5)
a1.metric("Temp Z Anomalies",   f"{z_temp_n:,}",   help="|z| > 3")
a2.metric("Temp IQR Anomalies", f"{iqr_temp_n:,}", help="Outside IQR fences")
a3.metric("Wind Z Anomalies",   f"{z_wind_n:,}",   help="|z| > 3")
a4.metric("Wind IQR Anomalies", f"{iqr_wind_n:,}", help="Outside IQR fences")
a5.metric("PM2.5 Z Anomalies",  f"{z_pm25_n:,}",   help="|z| > 3")

# ── Z-score histograms — one for temp, one for wind ──────────
# The red dashed lines mark the +3 and -3 boundaries.
# Bars outside those lines = anomalies.
h1, h2 = st.columns(2)

with h1:
    fig_zt = px.histogram(
        fdf, x="z_temp", nbins=80,
        title="Temperature Z-Score Distribution",
        labels={"z_temp": "Z-Score"},
        color_discrete_sequence=["mediumpurple"]
    )
    fig_zt.add_vline(x= 3, line_dash="dash", line_color="red",
                     annotation_text="+3 boundary")
    fig_zt.add_vline(x=-3, line_dash="dash", line_color="red",
                     annotation_text="-3 boundary")
    fig_zt.update_layout(height=380)
    st.plotly_chart(fig_zt, use_container_width=True)

with h2:
    fig_zw = px.histogram(
        fdf, x="z_wind", nbins=80,
        title="Wind Speed Z-Score Distribution",
        labels={"z_wind": "Z-Score"},
        color_discrete_sequence=["mediumseagreen"]
    )
    fig_zw.add_vline(x= 3, line_dash="dash", line_color="red",
                     annotation_text="+3 boundary")
    fig_zw.add_vline(x=-3, line_dash="dash", line_color="red",
                     annotation_text="-3 boundary")
    fig_zw.update_layout(height=380)
    st.plotly_chart(fig_zw, use_container_width=True)

insight(
    f"The filtered data contains <b>{z_temp_n:,}</b> temperature anomalies "
    f"and <b>{z_wind_n:,}</b> wind speed anomalies — readings unusual enough "
    f"to deserve closer investigation."
)

st.markdown("---")


# ============================================================
# SECTION 11 · 30-READING ROLLING AVERAGE TRENDS
# ============================================================

st.subheader("11 · 30-Reading Rolling Average Trends")
st.caption(
    "Smoothed trends for Temperature, Wind Speed, and PM2.5. "
    "Try filtering to a single country above to see its individual trend clearly."
)

# Sort by date — rolling averages only make sense in time order
df_sorted = filtered_df.sort_values("last_updated").copy()

df_sorted["rolling_temp"] = df_sorted["temperature_celsius"].rolling(30).mean()
df_sorted["rolling_wind"] = df_sorted["wind_kph"].rolling(30).mean()
df_sorted["rolling_pm25"] = df_sorted["air_quality_PM2.5"].rolling(30).mean()

# The first 29 rows don't have enough history yet — dropped them
df_roll = df_sorted.dropna(subset=["rolling_temp", "rolling_wind", "rolling_pm25"])

fig_roll = px.line(
    df_roll,
    x="last_updated",
    y=["rolling_temp", "rolling_wind", "rolling_pm25"],
    title="30-Reading Rolling Averages — Temperature · Wind · PM2.5",
    labels={
        "last_updated": "Date",
        "value":        "Rolling Average",
        "variable":     "Metric"
    }
)
st.plotly_chart(fig_roll, use_container_width=True)

insight(
    "Rolling averages hide daily spikes and let you ask: "
    "is temperature or pollution trending up or down over time? "
    "Select a single country in the filter above to explore its own trend."
)

st.markdown("---")


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "🌍 ClimateScope · Global Weather Analytics · "
    "Built with Streamlit & Plotly · Rachel Ferns"
)
