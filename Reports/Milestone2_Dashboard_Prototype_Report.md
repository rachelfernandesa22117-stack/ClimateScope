Here is the README based strictly on your dashboard code:

---

# ClimateScope 🌍 — Global Weather Analytics Dashboard

## Milestone 2 Overview

This milestone delivers a functional, interactive Streamlit dashboard built on the GlobalWeatherRepository dataset. It transforms the raw data exploration from Milestone 1 into a visual analytics prototype with filterable charts, KPI metrics, anomaly detection, and regional comparisons. The dashboard is a working prototype — not a final product.

---

## Objectives

- Present global weather data through interactive, filterable visualisations
- Enable country- and month-level filtering across all charts simultaneously
- Surface key patterns in temperature, wind, air quality, and UV index
- Detect and flag statistical anomalies using Z-Score and IQR methods
- Build a clean, navigable multi-section layout suitable for further extension

---

## Features Implemented

**Filters**
- Multi-select filter by country and by month
- Filters apply globally across all charts and tables
- Graceful handling when filter selection returns no data

**Key Weather Indicators (KPIs)**
- Six headline metrics: average temperature, humidity, wind speed, pressure, UV index, and visibility

**Geographic Overview**
- Choropleth world map showing average temperature by country
- Dynamic insight highlighting the hottest country in the dataset

**Data Distributions**
- Histograms for temperature, humidity, wind speed, pressure, UV index, and visibility
- Organised into three tabs for readability

**Seasonal Patterns**
- Monthly average wind speed (line chart)
- Temperature spread by month (box plot)
- Monthly average UV index (bar chart)
- Temperature heatmap — top 15 countries × month

**Correlation Analysis**
- Full correlation matrix heatmap for 8 weather variables
- Scatter plots: PM2.5 vs PM10, and Temperature vs UV Index (with OLS trendline)

**Regional Comparison**
- Top 10 hottest and coldest countries (ranked tables)
- Temperature distribution violin plot for top 10 most-recorded countries
- Top 10 most polluted countries by average PM2.5

**Air Quality Deep Dive**
- Overlapping PM2.5 vs PM10 distribution histogram
- US EPA vs UK DEFRA air quality index comparison (grouped bar chart)

**Extreme Weather Events**
- Counts of extreme heat, cold, wind, and pollution events (95th/5th percentile thresholds)
- Bar chart summarising event counts by type
- Table listing countries with the most extreme heat readings

**Visibility & Cloud Cover**
- Scatter plot: cloud cover vs visibility with trendline
- Cloud cover violin plot by country

**Anomaly Detection**
- Z-Score (|z| > 3) and IQR fence anomaly counts for temperature and wind
- PM2.5 Z-Score anomaly count
- Z-score distribution histograms with ±3 boundary markers

**Rolling Average Trends**
- 30-reading rolling averages for temperature, wind speed, and PM2.5 over time

---

## Tech Stack

| Tool / Library | Purpose |
|---|---|
| Python 3 | Core language |
| Streamlit | Dashboard framework and UI |
| Pandas | Data loading, cleaning, filtering, aggregation |
| NumPy | Statistical calculations |
| Plotly Express | All interactive charts and maps |

---

## How It Works

1. **Data Loading:** The CSV is loaded once using `@st.cache_data` to avoid reloading on every interaction. Numeric columns are coerced and rows with missing temperature or country values are dropped.
2. **Feature Engineering:** `last_updated` is parsed into datetime; `year`, `month`, and `month_name` columns are extracted for time-based grouping.
3. **Filtering:** User selections from the sidebar filters produce a `filtered_df` that flows into every chart and table in the dashboard.
4. **Visualisation:** Each section uses the filtered data to compute aggregations on the fly and render Plotly charts. The world map and heatmap use the full dataset regardless of filters.
5. **Anomaly Detection:** Z-scores and IQR fences are computed on the filtered data at runtime; results are displayed as counts and histograms.

---

## Installation & Setup

**Prerequisites:** Python 3.8 or higher

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <your-repo-folder>

# 2. Install dependencies
pip install streamlit pandas numpy plotly

# 3. Place the dataset in the correct path
#    Update this line in the script to match your local file path:
#    df = pd.read_csv(r"C:\Users\...\GlobalWeatherRepository.csv")

# 4. Run the dashboard
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`.

---

## Usage

1. Open the dashboard in your browser
2. Use the **Filter** panel at the top to select one or more countries and/or months
3. Leave both filters empty to view the full global dataset
4. Scroll through sections 01–11 to explore KPIs, charts, comparisons, and anomalies
5. Hover over any chart for interactive tooltips and exact values
6. To explore a country's rolling trend, select just that country in the filter

---

## Current Limitations

- **Hardcoded file path:** The CSV path is hardcoded as a local Windows path — other users must manually update it before running
- **No deployment configuration:** No `requirements.txt`, `config.toml`, or cloud deployment setup is included
- **Wind speed outlier unresolved:** The extreme `wind_kph` max (~2963 km/h) flagged in Milestone 1 is still present in the data and may skew wind charts
- **Rolling averages are not country-aware:** The 30-reading rolling average is computed across all records sorted by date, mixing countries together unless filtered manually
- **World map uses full dataset only:** The choropleth map does not respond to the country/month filters
- **Scatter plots use a 3,000-row sample:** Correlation scatter plots are sampled for performance; this may not be representative for small filtered subsets
- **No input validation on filters:** Selecting contradictory filters (e.g. a country not present in a chosen month) triggers a generic warning rather than a guided message

---

## Future Enhancements

- Add a `requirements.txt` and support for a configurable or uploaded data file path
- Resolve the wind speed outlier through formal outlier treatment
- Make the choropleth map filter-responsive
- Introduce country-level rolling averages computed per group
- Add predictive or forecasting components (e.g. temperature trend projection)
- Include weather condition (`condition_text`) frequency analysis
- Deploy to Streamlit Community Cloud or another hosting platform
- Add download buttons to export filtered data or chart images

---

*ClimateScope · Global Weather Analytics · Built with Streamlit & Plotly · Rachel Fernandes*
