# ClimateScope — Global Weather Analytics

<<<<<<< HEAD
## Project Overview

ClimateScope is a data analytics project built on the GlobalWeatherRepository
dataset, covering weather readings from over 200 countries. The project moves
through three structured stages — from raw data exploration to a fully interactive
Streamlit dashboard — with the goal of turning meteorological data into clear,
actionable visual insights.

The core dashboard allows users to explore global weather patterns across
temperature, humidity, wind speed, air quality, UV index, and visibility — all
filterable by country and month.

**Why it matters:**
Weather data in its raw form offers limited value without structure and context.
ClimateScope organises that data into a readable, interactive format suitable for
researchers, analysts, and domain professionals working with large-scale
meteorological datasets.

**Real-world application:**
The analytical foundation established in Milestone 2 directly informed the
development of SiteGuard — a construction weather risk dashboard derived from the
ClimateScope prototype. SiteGuard applies the same data and dashboard logic to a
domain-specific problem: classifying every weather reading as SAFE, CAUTION, or
DANGER for outdoor construction scheduling, and surfacing stop-work conditions
across five hazard types. It demonstrates how a general-purpose analytics dashboard
can be extended into a professional decision-support tool.

---

## Project Structure

The project progresses across three milestones:
```
Data Exploration (Milestone 1)
        |
        v
Dashboard Prototype (Milestone 2)
        |
        v
Final Dashboard + Analysis (Milestone 3)
```

---

## Repository Contents

| File / Folder | Description |
|---|---|
| [Milestone1.ipynb](https://github.com/rachelfernandesa22117-stack/ClimateScope/blob/main/Milestone1.ipynb) | Jupyter Notebook — data exploration and preprocessing |
| [dashboard_M2.py](https://github.com/rachelfernandesa22117-stack/ClimateScope/blob/main/dashboard_M2.py) | Milestone 2 — Streamlit dashboard prototype |
| [climatescope_dashboard_M3.py](https://github.com/rachelfernandesa22117-stack/ClimateScope/blob/main/climatescope_dashboard_M3.py) | Milestone 3 — Final Streamlit dashboard |
| [Reports/](https://github.com/rachelfernandesa22117-stack/ClimateScope/tree/main/Reports) | Milestone reports for all stages |

---

## Milestone Breakdown

**Milestone 1 — Data Exploration and Preprocessing**
Initial examination of the GlobalWeatherRepository dataset using a Jupyter Notebook.
Covers data loading, structure inspection, null value checks, feature engineering,
normalisation, and basic statistical analysis.

**Milestone 2 — Dashboard Prototype**
A functional Streamlit dashboard implementing core visualisations: KPI metrics,
a global choropleth map, distribution histograms, seasonal trend charts, a
correlation matrix, air quality analysis, anomaly detection, and rolling averages.
Includes country and month filtering applied globally across all sections.

**Milestone 3 — Final Dashboard**
The production-ready version of the dashboard with refined visualisations, extended
analysis, and completed documentation. Builds directly on the Milestone 2 prototype
with improved structure, additional sections, and a cleaner user experience.

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

## Additional Notes

**Project Status**

| Milestone | Status |
|---|---|
| Milestone 1 — Data Exploration and Preprocessing | Complete |
| Milestone 2 — Dashboard Prototype | Complete |
| Milestone 3 — Final Dashboard | Complete |
| Milestone 4 — Combined Reports | Complete |

This project was developed in structured phases as part of an academic data
analytics programme. All milestone reports are available in the
[Reports](https://github.com/rachelfernandesa22117-stack/ClimateScope/tree/main/Reports)
folder.

---

*ClimateScope — Built with Streamlit and Plotly · Rachel Fernandes ·
Data: GlobalWeatherRepository*
=======
<<<<<<< Updated upstream
=======
## Project Status
- Dataset successfully downloaded  
- Data cleaned and standardized  
- Missing values inspected  
- Dataset aggregated  
- Ready for visualization using Plotly & Streamlit  

---

**Author:** Rachel Fernandes

<h1>Milestone 2: Core Analysis & Visualization Design</h1>
<h3>Project: ClimateScope – Visualizing Global Weather Trends</h3>
<p><strong>Author:</strong> Rachel Fernandes</p>

<hr>

<ul>
  <li>Performed statistical exploration of the dataset</li>
  <li>Identified seasonal climate trends</li>
  <li>Analyzed regional differences</li>
  <li>Detected extreme weather events using percentile thresholds</li>
  <li>Designed a visualization strategy aligned with analytical findings</li>
</ul>

<h2>Dashboard Layout Plan</h2>
<ol>
  <li>Key weather indicators (summary metrics)</li>
  <li>Global geographic overview</li>
  <li>Distribution analysis</li>
  <li>Seasonal trends</li>
  <li>Correlation analysis</li>
  <li>Regional comparison</li>
  <li>Extreme events summary</li>
  <li>Country deep dive</li>
</ol>

<p>
I will incorporate interactive filters to allow users to explore data by country, month, and percentile thresholds.
</p>

<hr>

</body>
</html>
>>>>>>> Stashed changes
>>>>>>> c58bb30 (Updated README before switching branch)
