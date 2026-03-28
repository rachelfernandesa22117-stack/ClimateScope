# SiteGuard — Construction Weather Risk Dashboard

> A data-driven Streamlit dashboard helping civil engineers and site managers schedule outdoor construction work safely — across multiple countries and seasons.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Objectives](#objectives)
4. [Scope of the Project](#scope-of-the-project)
5. [Dataset Description](#dataset-description)
6. [Data Preprocessing](#data-preprocessing)
7. [Methodology & Analysis](#methodology--analysis)
8. [Dashboard Features](#dashboard-features)
9. [Working of the Application](#working-of-the-application)
10. [Insights & Analysis](#insights--analysis)
11. [Hypotheses](#hypotheses)
12. [Results & Interpretation](#results--interpretation)
13. [Installation & Setup](#installation--setup)
14. [Usage](#usage)
15. [Project Structure](#project-structure)
16. [Limitations](#limitations)
17. [Future Scope](#future-scope)
18. [Conclusion](#conclusion)

---

## Introduction

**SiteGuard** is an interactive weather risk analytics dashboard built for construction professionals who need to make informed, safety-critical scheduling decisions. Rather than consulting raw weather reports, site managers can use SiteGuard to instantly understand which countries, months, and weather conditions pose the greatest risk to outdoor construction activity.

### Why Data-Driven Dashboards Matter

- Traditional weather apps show current conditions but offer no construction-specific safety context.
- Manual analysis of multi-country weather data is time-consuming and error-prone.
- Data-driven dashboards translate raw meteorological data into actionable construction risk signals, improving worker safety and project planning efficiency.

---

## Problem Statement

Outdoor construction work is highly sensitive to weather conditions. Extreme heat, strong winds, poor air quality, and low visibility can all trigger work stoppages, put workers at risk, and delay project timelines.

**The core problem:**
Site managers and civil engineers across different countries lack a unified, construction-specific tool to:
- Assess weather risk levels before scheduling critical outdoor tasks.
- Identify the safest months for concrete pours, crane lifts, and elevated work.
- Detect stop-work conditions across multiple weather parameters simultaneously.

Without this, decisions are made on intuition rather than data — leading to preventable safety incidents and costly rescheduling.

---

## Objectives

- **Classify** every weather reading as `SAFE`, `CAUTION`, or `DANGER` based on internationally recognised construction safety thresholds.
- **Visualise** global risk patterns using choropleth maps, trend charts, and heatmaps.
- **Enable seasonal planning** by revealing the best and worst months to schedule outdoor work.
- **Detect anomalies** in temperature, wind speed, and air quality using statistical methods.
- **Summarise** country-level suitability so site managers can compare locations at a glance.
- **Monitor trends** using rolling averages to flag worsening conditions over time.

---

## Scope of the Project

### Included

- Multi-country weather risk classification (`SAFE` / `CAUTION` / `DANGER`)
- Interactive filtering by country and month
- Twelve analytical dashboard sections covering temperature, wind, air quality, visibility, cloud cover, and rolling trends
- Statistical anomaly detection (Z-score, IQR)
- Correlation analysis between construction-relevant weather variables
- Country suitability summary table with colour-coded risk indicators
- Stop-work event tracker across five hazard types

### Excluded

- Real-time or live weather API integration (uses a static CSV dataset)
- Project-specific scheduling or cost modelling
- Predictive machine learning models
- User authentication or saved session state
- Mobile-optimised layout

---

## Dataset Description

### Source
- **File:** `GlobalWeatherRepository.csv`
- **Type:** Static CSV file loaded locally
- **Scale:** Multiple countries, multiple date/time readings

### Key Columns Used

| Column | Description |
|---|---|
| `country` | Country where the reading was recorded |
| `last_updated` | Timestamp of the weather reading |
| `temperature_celsius` | Ambient temperature in °C |
| `humidity` | Relative humidity (%) |
| `wind_kph` | Wind speed in kilometres per hour |
| `pressure_mb` | Atmospheric pressure in millibars |
| `air_quality_PM2.5` | Fine particulate matter concentration (µg/m³) |
| `air_quality_PM10` | Coarse particulate matter concentration (µg/m³) |
| `uv_index` | UV radiation index |
| `visibility_km` | Horizontal visibility in kilometres |
| `cloud` | Cloud cover percentage |
| `air_quality_us-epa-index` | US EPA air quality index |
| `air_quality_gb-defra-index` | UK DEFRA air quality index |

### Data Structure
- **Format:** Tabular (rows = individual weather readings, columns = meteorological variables)
- **Date granularity:** Sub-daily timestamps, aggregated to monthly level for trend analysis
- **Numeric types:** All meteorological columns converted to `float64` with `pd.to_numeric()`

---

## Data Preprocessing

### 1. Date Parsing & Feature Extraction
```python
df["last_updated"] = pd.to_datetime(df["last_updated"])
df["year"]         = df["last_updated"].dt.year
df["month"]        = df["last_updated"].dt.month
df["month_name"]   = df["last_updated"].dt.strftime("%b")
```
Timestamps are parsed and decomposed into `year`, `month`, and `month_name` to enable seasonal aggregation.

### 2. Type Coercion
All meteorological columns are explicitly cast to numeric types:
```python
df[col] = pd.to_numeric(df[col], errors="coerce")
```
Non-numeric values are silently converted to `NaN` rather than raising errors.

### 3. Null Value Handling
- Rows missing `temperature_celsius` or `country` are dropped (these are the two mandatory fields for risk classification and geographic filtering).
- Other columns retain `NaN` values and are handled gracefully in aggregations.

### 4. Risk Classification (Derived Column)
A new column `risk_level` is created for every row using a rule-based function applied via `df.apply()` with a named function `classify_risk`:

| Level | Trigger Conditions |
|---|---|
| `DANGER` | Temp >= 40°C, Temp <= 0°C, Wind >= 60 kph, PM2.5 >= 75 µg/m³ |
| `CAUTION` | Wind >= 40 kph, PM2.5 >= 35 µg/m³, UV >= 6, Humidity >= 85% |
| `SAFE` | None of the above conditions triggered |

Thresholds are sourced from international construction safety guidelines and centralised in a `THRESHOLDS` dictionary for maintainability.

### 5. Performance Optimisation
- Dataset loading is wrapped in `@st.cache_data` to avoid re-reading and reprocessing on every user interaction.
- Scatter plots use a random sample of up to 3,000 rows to keep browser rendering responsive.

---

## Methodology & Analysis

### Pandas Operations

| Function | Where Used |
|---|---|
| `groupby()` + `agg()` | Monthly aggregations, country-level summaries, stop-work counts |
| `pivot_table()` | Seasonal heatmap (country x month temperature matrix) |
| `value_counts(normalize=True)` | Risk level distribution per country |
| `rolling(30).mean()` | 30-reading rolling averages for trend monitoring |
| `merge()` | Joining risk scores with average temperature per country |
| `reindex()` | Enforcing correct month order (Jan to Dec) on all monthly charts |
| `quantile([0.25, 0.75])` | IQR fence calculation for outlier detection |
| `sample()` | Random downsampling for scatter plot performance |

### Vectorized Operations
- Risk classification is applied row-wise using `df.apply()` with a named function `classify_risk`.
- Z-scores are computed using vectorized arithmetic: `(x - x.mean()) / x.std()`.
- IQR fences are applied using boolean masks across entire Series columns.

### Statistical Techniques

| Technique | Purpose |
|---|---|
| Z-score (threshold: ±3) | Flags temperature, wind, and PM2.5 readings unusually far from the mean |
| IQR method (1.5 × IQR) | Non-parametric outlier detection for temperature and wind |
| Skewness | Measures directional asymmetry — positive skew indicates occasional extreme events |
| Correlation matrix | Pearson correlations between five key construction weather variables |
| Composite risk score | `DANGER% + 0.5 × CAUTION%` per country for map ranking |

---

## Dashboard Features

### Filters
- **Country multi-select:** Filter any combination of countries (defaults to all).
- **Month multi-select:** Restrict analysis to specific planned work months.
- All 12 dashboard sections update dynamically based on active filters.

### Visualisations

| Section | Chart Types |
|---|---|
| Site Conditions (KPIs) | Metric tiles, risk breakdown counters |
| Global Risk Map | Choropleth map (risk score + avg temperature) |
| Seasonal Planning | Line charts (wind, temperature), bar chart (% DANGER by month) |
| Seasonal Heatmap | Imshow heatmap (temperature by country x month) |
| Wind Risk | Plotly Express scatter with threshold lines via Graph Objects |
| Air Quality | Histogram (PM2.5), scatter (PM2.5 vs PM10), ranked bar chart |
| Stop-Work Tracker | Metric tiles + bar chart across 5 hazard types |
| Statistical Analysis | Z-score histograms, skewness metrics, IQR anomaly counts |
| Correlation Matrix | Heatmap (Pearson r values, 5 variables) |
| Visibility & Cloud | Scatter (cloud vs visibility), histogram, violin plots by country |
| Rolling Trend Monitor | Tabbed line charts (temperature, wind, PM2.5 30-reading rolling averages) |
| Country Summary Table | Sortable styled table with conditional colour coding |

### User Interaction
- Multi-select dropdowns for country and month filtering.
- Sortable and ascending/descending toggle on the country summary table.
- Tabbed interface for the rolling trend monitor (switch between parameters).
- Collapsible filter panel via `st.expander()`.

### Recommendation Logic
- Contextual alert boxes (green `safe-box`, orange `site-note`, red `danger-box`) appear automatically based on computed values.
- Safest and riskiest countries/months are identified automatically and surfaced in alerts.
- The worst air quality country triggers a mandatory respirator recommendation.

---

## Working of the Application

```
User Input (Filters)
       |
       v
Filter DataFrame (country, month)
       |
       v
Compute Aggregations (groupby, pivot, rolling)
       |
       v
Apply Statistical Methods (Z-score, IQR, skewness, correlation)
       |
       v
Render Charts (Plotly Express / Graph Objects)
       |
       v
Evaluate Thresholds -> Trigger Alert Boxes
       |
       v
Display Insights & Recommendations to User
```

### Backend Logic
1. The full dataset is loaded and cached once on app start.
2. User filter selections create a `filtered_df` subset in memory.
3. All aggregations, statistics, and charts operate on `filtered_df`.
4. Threshold comparisons run after each section's aggregation to determine which alert box to display.
5. No external API calls or database queries are made during runtime.

---

## Insights & Analysis

### Temperature Patterns
- Equatorial countries maintain consistently high temperatures year-round, keeping them in CAUTION or DANGER for heat-related risk across all months.
- Higher-latitude countries show strong seasonal variance, with clear safe windows in spring and autumn (10–30°C range).

### Wind Risk
- Wind speed data exhibits positive skewness — the majority of readings are moderate, but rare extreme wind events push well past the 60 kph stop-work threshold.
- Low atmospheric pressure combined with high wind speed identifies the most dangerous storm conditions for crane and elevated work.

### Air Quality
- PM2.5 and PM10 concentrations are strongly correlated — when fine particles rise, coarse particles rise in tandem. This is critical for sites generating construction dust.
- Countries with high average PM2.5 consistently exceed WHO 24-hour guidelines, requiring mandatory PPE even before site dust is added.

### Visibility & Cloud Cover
- Humid, overcast days show reduced visibility — a compounding hazard when PM2.5 is simultaneously elevated.
- The correlation matrix confirms a negative relationship between PM2.5 and visibility, validating the dual-trigger approach in the dashboard's alert logic.

### Seasonal Effects
- Monthly DANGER percentage charts clearly reveal seasonal peaks, allowing planners to avoid scheduling concrete pours, crane lifts, and foundation work during the highest-risk months.
- The 30-reading rolling average smooths short-term spikes and reveals whether conditions are structurally improving or deteriorating over time.

---

## Hypotheses

### H1 — Temperature and UV Index Are Closely Linked
**Claim:** Hot days are also high-UV days, creating compounding heat stress risk for outdoor workers.
**Reasoning:** Solar radiation drives both ambient temperature and UV index — a strong positive correlation is expected and confirmed in the correlation matrix.

### H2 — High PM2.5 Correlates With Reduced Visibility
**Claim:** Dusty or polluted air reduces visibility, meaning air quality and machinery safety risks occur together.
**Reasoning:** Suspended fine particles scatter light, cutting visibility — a negative PM2.5 vs visibility correlation is expected and confirmed.

### H3 — Wind Speed Follows a Right-Skewed Distribution
**Claim:** Most readings record moderate wind, but a small number of extreme events drive the stop-work trigger count disproportionately.
**Reasoning:** Atmospheric wind distributions are well-known to be positively skewed (Weibull-like), with rare but severe gusts.

### H4 — Countries Near the Equator Have Higher Year-Round Risk Scores
**Claim:** Heat and humidity in tropical zones keep risk scores elevated throughout the year, unlike temperate countries with distinct safe seasons.
**Reasoning:** Seasonal temperature variance is low near the equator, meaning danger-level heat conditions persist without the relief of a cooler season.

---

## Results & Interpretation

- **Risk classification** successfully segments readings into three actionable tiers, giving site managers an immediate go/caution/stop signal without reading raw meteorological data.
- **The composite risk score** (DANGER% + 0.5 × CAUTION%) provides a single comparable metric across all countries, enabling direct prioritisation of which locations need the most robust weather contingency planning.
- **Anomaly detection** via Z-score and IQR identifies readings far outside normal ranges — these are the specific dates and locations where standard precautions are insufficient.
- **The correlation matrix** validates that temperature, UV, humidity, visibility, and PM2.5 do not move independently — multi-factor compound risk is real and measurable.
- **Seasonal heatmaps and monthly DANGER charts** confirm that scheduling is the most powerful lever available to site managers — choosing the right month can reduce DANGER exposure by a significant margin.

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/rachelfernandesa22117-stack/ClimateScope.git
cd ClimateScope
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**`requirements.txt` includes:**
```
streamlit
pandas
numpy
plotly
```

### 3. Add the Dataset
Download `GlobalWeatherRepository.csv` from [Kaggle](https://www.kaggle.com/) and place it in the project root directory. The app expects the file at the root level — if `pd.read_csv()` in `climatescope_dashboard_M3.py` contains a hardcoded path, replace it with `"GlobalWeatherRepository.csv"` to use the project root location.

### 4. Run the Streamlit App

Run either dashboard depending on the milestone you want to launch:

```bash
# Milestone 2
streamlit run dashboard_M2.py

# Milestone 3 (full dashboard)
streamlit run climatescope_dashboard_M3.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`.

---

## Usage

1. Launch the app using `streamlit run dashboard_M2.py` or `streamlit run climatescope_dashboard_M3.py` (see Installation Step 4).
2. Expand the filter panel at the top of the page.
3. Select one or more countries from the multi-select dropdown (leave empty for all countries).
4. Select one or more months to focus on your planned work window.
5. Scroll through the 12 sections — each updates automatically based on your selections.
6. Read the coloured alert boxes — green means safe to schedule, orange means monitor closely, red means stop-work risk.
7. Use the Country Summary Table (Section 12) to sort and compare all locations at a glance.
8. Switch tabs in the Rolling Trend Monitor (Section 11) to check temperature, wind, or PM2.5 trends independently.

**Tip:** Select a single country in the filter for the Rolling Trend Monitor to show that location's trend cleanly without multi-country noise.

---

## Project Structure

```
ClimateScope/
|
|-- dashboard_M2.py                # Milestone 2 Streamlit dashboard
|-- climatescope_dashboard_M3.py   # Milestone 3 Streamlit dashboard (full)
|-- GlobalWeatherRepository.csv   # Source dataset (not included in repo -- download separately from Kaggle)
|-- requirements.txt              # Python dependencies
|-- README.md                     # Project documentation
```

**`climatescope_dashboard_M3.py` is organised into 12 labelled sections:**

| Section | Content |
|---|---|
| CSS & Styling | Custom colour scheme, alert box styles |
| Constants | `THRESHOLDS` dictionary, `MONTH_ORDER` list |
| Data Loading | `load_data()` with caching and risk classification |
| Sections 01–12 | Sequential dashboard panels (KPIs to Summary Table) |

---

## Limitations

- **Static dataset:** No live weather data — the dashboard reflects historical readings in the CSV file only. Conditions may differ from current reality.
- **Hardcoded file path:** The `pd.read_csv()` path may be hardcoded to a local path in `climatescope_dashboard_M3.py` and must be updated to `"GlobalWeatherRepository.csv"` per user environment.
- **No time-zone handling:** All timestamps are treated as-is without timezone normalisation, which may affect cross-country time comparisons.
- **Threshold-based classification only:** The `SAFE/CAUTION/DANGER` model uses fixed cutoffs — it does not account for combined multi-factor risk (e.g., moderate wind + moderate heat simultaneously without either breaching a threshold alone).
- **Scatter plots are sampled:** To maintain rendering performance, scatter plots use up to 3,000 randomly sampled rows — extreme outliers may occasionally be excluded from visual display.
- **No export functionality:** Users cannot download filtered data, charts, or reports directly from the dashboard.
- **Country name matching:** Choropleth maps rely on Plotly's `country names` location mode — countries with non-standard name formats in the dataset may not render on the map.
- **`applymap()` deprecation:** The styled Country Summary Table (Section 12) uses `.applymap()` for conditional colour coding. This method is deprecated in pandas ≥ 2.1 and will raise a `FutureWarning`. Replace with `.map()` if running a newer pandas version.

---

## Future Scope

### Data & Integration
- Live weather API integration (e.g., OpenWeatherMap, WeatherAPI) to replace the static CSV with real-time feeds.
- Project calendar overlay — allow users to import a construction programme and map risk levels directly onto task dates.

### Analytics
- Multi-factor compound risk scoring — combine temperature, wind, and PM2.5 simultaneously into a single weighted index rather than independent thresholds.
- Machine learning risk prediction — train a classifier on historical readings to predict tomorrow's risk level based on current conditions.
- Time-series forecasting — use ARIMA or Prophet to project 7–30 day weather risk windows.

### User Experience
- Exportable PDF/CSV reports — allow site managers to download a filtered risk report for a specific country and date range.
- Email/SMS alerts — notify site managers when rolling averages breach threshold levels.
- Mobile-responsive layout — adapt the dashboard for use on tablets and smartphones on-site.
- User authentication — support multi-user access with saved filter preferences per project.

### Scalability
- Database backend — replace CSV with a cloud database (PostgreSQL, BigQuery) to handle larger datasets efficiently.
- Multi-language support — localise the interface for site managers operating in non-English markets.

---

## Conclusion

SiteGuard demonstrates how weather data can be transformed from raw meteorological readings into clear, construction-specific safety intelligence. By combining rule-based risk classification (SAFE / CAUTION / DANGER), statistical anomaly detection (Z-score, IQR, skewness), seasonal and geographic visualisation (heatmaps, choropleth maps, rolling trends), and contextual alert logic (automated stop-work and safe-schedule recommendations), the dashboard gives civil engineers and site managers a practical planning tool that reduces reliance on intuition and improves decision-making around worker safety and project scheduling.

**Key learnings from this project:**
- Translating domain knowledge (construction safety thresholds) into code produces far more useful outputs than generic data exploration.
- Caching and sampling are essential for keeping interactive dashboards responsive at scale.
- Correlation analysis between weather variables reveals compound risk patterns that single-metric thresholds miss.
- Clear visual hierarchy and contextual alert boxes significantly improve how users interpret and act on analytical outputs.

---

*SiteGuard — Built with Streamlit & Plotly · Rachel Fernandes · Data: GlobalWeatherRepository · Thresholds based on international construction safety guidelines*
