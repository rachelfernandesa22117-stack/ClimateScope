Here is the README based strictly on your notebook content:

---

# Global Weather Analysis — Milestone 1: Data Exploration & Preprocessing

## Milestone Description

This milestone covers the initial stage of a global weather data analysis project. The focus is on loading the dataset, understanding its structure, performing basic data cleaning and preprocessing, and building foundational logic for feature engineering and aggregation. No modelling or visualisation has been attempted at this stage.

---

## Objectives

- Load and inspect the GlobalWeatherRepository dataset
- Understand the shape, data types, and completeness of the data
- Remove redundant or duplicate columns
- Engineer new features from existing variables
- Establish basic filtering, grouping, and correlation logic
- Normalise key numerical variables for future use

---

## Dataset Description

- **Source:** `GlobalWeatherRepository.csv` (local file)
- **Size:** 124,331 rows × 41 columns
- **Coverage:** 211 countries, 256 locations
- **Time Range:** May 2024 – February 2026

**Key Variables:**

| Category | Columns |
|---|---|
| Location | `country`, `location`, `latitude`, `longitude`, `timezone` |
| Time | `updated_datetime`, `updated_epoch`, `year`, `month`, `day`, `hour` |
| Temperature | `temperature_celsius`, `feels_like_celsius` |
| Atmosphere | `humidity`, `pressure_mb`, `visibility_km`, `cloud` |
| Wind | `wind_kph`, `wind_degree`, `wind_direction`, `gust_kph` |
| Precipitation | `precip_mm` |
| UV & Air Quality | `uv_index`, `pm25`, `pm10`, `epa_index`, `defra_index` |
| Celestial | `sunrise`, `sunset`, `moonrise`, `moonset`, `moon_phase` |
| Weather Label | `Weather` (condition text, 49 unique categories) |

---

## Approach / Methodology

**1. Data Loading & Inspection**
- Loaded CSV using pandas; inspected shape, column names, data types, and index

**2. Missing Value & Duplicate Check**
- Confirmed zero null values across all 41 columns
- Confirmed zero duplicate rows

**3. Data Cleaning**
- Dropped redundant imperial/duplicate unit columns (`temperature_fahrenheit`, `wind_mph`, `pressure_in`, `precip_in`, `feels_like_fahrenheit`, `visibility_miles`, `gust_mph`) and some air quality columns already renamed (`carbon_monoxide`, `ozone`, `nitrogen_dioxide`, `sulphur_dioxide`)
- Renamed columns for clarity (e.g. `condition_text` → `Weather`, `last_updated` → `updated_datetime`)

**4. Feature Engineering**
- Parsed `updated_datetime` into `year`, `month`, `day`, `hour`
- Computed `temp_difference` = `feels_like_celsius` − `temperature_celsius`
- Computed per-country average UV index and assigned a categorical risk level (Low / Moderate / High / Very High)

**5. Normalisation**
- Applied min-max normalisation to: `temperature_celsius`, `humidity`, `precip_mm`, `wind_kph`, `pressure_mb`, `visibility_km`, `uv_index`, `gust_kph`

**6. Aggregation**
- Grouped data by `country`, `year`, `month` to compute monthly averages for temperature, humidity, wind speed, and total precipitation

**7. Basic Analysis & Filtering**
- Identified high-pollution records (PM2.5 > 50)
- Identified extreme heat records (temperature > 35°C)
- Filtered on compound wind conditions (`wind_degree > 300` and `wind_direction == 'NW'`)
- Filtered on precipitation and low visibility events
- Computed correlation matrix for temperature, humidity, wind speed, and pressure
- Computed standard deviation of humidity and variance of UV index

---

## Key Findings / Observations

- **No missing data:** All 124,331 rows are complete across all columns — no imputation required.
- **Dominant weather conditions:** "Partly cloudy" and "Sunny" together account for the majority of records (~65%).
- **High-pollution locations:** 13,790 records have PM2.5 > 50, with notable entries including Luanda, Santiago, Jakarta, and Beijing.
- **Extreme heat:** 4,762 records exceed 35°C, concentrated in South/Southeast Asia and the Middle East.
- **Temperature–humidity correlation:** A moderate negative correlation (−0.35) exists between temperature and humidity; other variable pairs show weak correlations.
- **UV risk:** India's average UV index is approximately 4.40, classified as Moderate risk.
- **Wind anomaly in raw data:** Maximum `wind_kph` of 2963.2 is likely an outlier — this has been noted but not yet addressed.

---

## Tools & Libraries Used

- **Python 3**
- **pandas** — data loading, inspection, cleaning, grouping, filtering, feature engineering

---

## Limitations

- No visualisations have been created; all analysis is tabular
- The extreme `wind_kph` outlier (max 2963.2 km/h) has been identified but not treated
- Column renaming was applied mid-notebook inconsistently, which caused a reference error (`updated_datetime` used before the rename in one cell)
- Air quality column drops were partially mismatched — some target columns (`carbon_monoxide` etc.) appear to be already-renamed versions not present under their original names (`air_quality_Carbon_Monoxide`)
- Data source is a local CSV file; no API or reproducible data pipeline is in place yet
- No statistical testing or formal outlier detection has been performed

---

## Next Steps

- Resolve column naming inconsistencies and clean up the preprocessing pipeline
- Detect and handle outliers (especially in `wind_kph`)
- Build exploratory visualisations (distributions, time series, geographic maps)
- Perform deeper feature analysis (e.g. seasonal patterns, country-level comparisons)
- Investigate air quality trends alongside weather variables
- Prepare a clean, consolidated dataset for modelling in future milestones
