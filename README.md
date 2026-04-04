# ClimateScope — Making Sense of the World's Weather

---

## What is ClimateScope?

Raw weather data is noise. ClimateScope turns it into signal.

Built on the GlobalWeatherRepository dataset, ClimateScope is an interactive
Streamlit dashboard that lets you cut through the noise and explore real
meteorological patterns — across temperature, humidity, wind speed, air quality,
UV index, and visibility — for any country, any month, in seconds.

This is not a weather app. It is an analytics platform for people who want to
*understand* weather, not just check it.

---

## Why It Exists

Weather data is everywhere. Meaningful weather analysis is not.

ClimateScope was built to answer a simple question: what does global weather
actually look like when you organise it properly? The answer turned out to be
more interesting than expected — seasonal anomalies, cross-country air quality
gaps, temperature distributions that defy intuition, and correlations that only
become visible at scale.

The project also has a real-world extension. The analytical foundation built here
directly powered **SiteGuard** — a construction weather risk tool that classifies
every weather reading as SAFE, CAUTION, or DANGER for outdoor work scheduling.
One dataset. One codebase. Two completely different use cases. That is the point.

---

## How It Was Built

The project moves through three deliberate stages:

```
Milestone 1 — Understand the data
        |
        v
Milestone 2 — Build the prototype
        |
        v
Milestone 3 — Ship the final dashboard
```

No shortcuts. Each stage builds directly on the last.

---

## Repository Contents

| File / Folder | Description |
|---|---|
| [Milestone1.ipynb](https://github.com/Bhoomika26M/ClimateScope_B13/blob/Rachel-Fernandes/Milestone1.ipynb) | Jupyter Notebook — data exploration and preprocessing |
| [dashboard_M2.py](https://github.com/Bhoomika26M/ClimateScope_B13/blob/Rachel-Fernandes/dashboard_M2.py) | Milestone 2 — Streamlit dashboard prototype |
| [climatescope_dashboard_M3.py](https://github.com/Bhoomika26M/ClimateScope_B13/blob/Rachel-Fernandes/climatescope_dashboard_M3.py) | Milestone 3 — Final Streamlit dashboard |
| [Reports/](https://github.com/Bhoomika26M/ClimateScope_B13/tree/Rachel-Fernandes/Reports) | Milestone reports covering all stages of the project |

---

## What the Dashboard Actually Shows

- **Global choropleth map** — see weather patterns across countries at a glance
- **KPI metrics** — temperature, humidity, wind, UV, visibility, air quality
- **Seasonal trend charts** — how conditions shift month by month
- **Anomaly detection** — Z-score flagging of statistical outliers
- **Correlation matrix** — relationships between weather variables
- **Air quality analysis** — pollution breakdowns by region
- **Rolling averages** — smoothed trend lines over time

Every chart responds to a country and month filter applied globally across the
entire dashboard.

---

## How to Run the Project

**1. Clone the repository**
```bash
git clone https://github.com/rachelfernandesa22117-stack/ClimateScope.git
cd ClimateScope
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add the dataset**

Place `GlobalWeatherRepository.csv` in the project root directory, or update the
`pd.read_csv()` path in the relevant script to match your local file location.

**4. Run the dashboards**

Milestone 2 prototype:
```bash
streamlit run dashboard_M2.py
```

Milestone 3 final dashboard:
```bash
streamlit run climatescope_dashboard_M3.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## Tech Stack

| Tool / Library | Purpose |
|---|---|
| Python 3 | Core programming language |
| Pandas | Data loading, cleaning, and aggregation |
| NumPy | Statistical calculations |
| Streamlit | Dashboard framework and UI |
| Plotly Express | Interactive charts and maps |

---

## Project Status

| Milestone | Status |
|---|---|
| Milestone 1 — Data Exploration and Preprocessing | Complete |
| Milestone 2 — Dashboard Prototype | Complete |
| Milestone 3 — Final Dashboard | Complete |
| Milestone 4 — Combined Reports | Complete |

---

*Built by Rachel Fernandes · Powered by Streamlit and Plotly · Data: GlobalWeatherRepository*
