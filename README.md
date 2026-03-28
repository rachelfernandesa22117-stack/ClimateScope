# ClimateScope — Global Weather Analytics

## Introduction

ClimateScope is an interactive data analytics project built on the GlobalWeatherRepository dataset, covering weather readings from over 200 countries. The project transforms raw meteorological data into structured visual insights through a multi-section Streamlit dashboard.

The dashboard enables users to explore global weather patterns — including temperature distributions, air quality, wind behaviour, seasonal trends, and statistical anomalies — through filterable, interactive charts. All analysis updates dynamically based on country and month selections.

**Why it is relevant:**
Weather data in its raw form offers little actionable value. ClimateScope bridges that gap by organising readings into clear visual summaries, making it useful for researchers, analysts, and domain professionals who need to interpret global weather patterns at scale.

**Real-world application:**
The analytical foundation built in ClimateScope directly informed the development of SiteGuard — a construction weather risk dashboard derived from Milestone 2. SiteGuard extends the core ClimateScope logic by adding construction-specific risk classification (SAFE / CAUTION / DANGER), stop-work event tracking, composite risk scoring, and contextual safety alerts — demonstrating how a general-purpose analytics dashboard can be adapted into a domain-specific decision-support tool.

---

## Project Structure

This project is developed across three milestones, each building on the previous:

| Milestone | Description |
|---|---|
| Milestone 1 | Data exploration, cleaning, and preprocessing of the GlobalWeatherRepository dataset |
| Milestone 2 | Interactive Streamlit dashboard prototype with filtering, distributions, correlations, and anomaly detection |
| Milestone 3 | Final production dashboard with extended analysis, refined visualisations, and completed documentation |

---

## Milestone Reports

Detailed reports for each milestone are available in the repository:

[View All Milestone Reports](https://github.com/rachelfernandesa22117-stack/ClimateScope/tree/main/Reports)

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

## How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/rachelfernandesa22117-stack/ClimateScope.git
cd ClimateScope
```

Open the cloned folder in Visual Studio Code or your preferred IDE.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add the Dataset

Place `GlobalWeatherRepository.csv` in the project root directory, or update the `pd.read_csv()` path in the relevant script to match your local file location.

### 4. Run the Dashboard

**Milestone 2 prototype:**
```bash
streamlit run dashboard_M2.py
```

**Milestone 3 final dashboard:**
```bash
streamlit run climatescope_dashboard_M3.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## Project Status

This project was developed in three structured phases across the academic year.

| Milestone | Status |
|---|---|
| Milestone 1 — Data Exploration & Preprocessing | Complete |
| Milestone 2 — Dashboard Prototype | Complete |
| Milestone 3 — Final Dashboard & Analysis | Complete |

---

*ClimateScope — Built with Streamlit and Plotly · Rachel Fernandes · Data: GlobalWeatherRepository*
