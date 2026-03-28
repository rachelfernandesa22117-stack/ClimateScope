# SiteGuard — Construction Weather Risk Dashboard

A data-driven analytics dashboard built to help civil engineers and site managers
make weather-informed scheduling decisions for outdoor construction work.

---

## Introduction

SiteGuard analyses global historical weather data to classify conditions as
SAFE, CAUTION, or DANGER for outdoor construction activity. It translates raw
meteorological readings — temperature, wind speed, air quality, humidity, and
visibility — into actionable risk signals relevant to construction safety.

The project addresses a practical gap: existing weather tools provide no
construction-specific context, leaving site managers to interpret raw data
manually. SiteGuard bridges that gap with structured risk thresholds, interactive
visualisations, and seasonal planning tools.

---

## Project Structure

The project is developed across three milestones, each building on the previous.

| Milestone | Description |
|---|---|
| Milestone 1 | Data exploration, cleaning, and preprocessing of the GlobalWeatherRepository dataset |
| Milestone 2 | Interactive Streamlit dashboard prototype with core visualisations and filtering |
| Milestone 3 | Final dashboard with risk classification, anomaly detection, and full analytical reporting |

---

## Milestone Reports

Detailed reports for each milestone are available in the repository:

[View All Milestone Reports](https://github.com/rachelfernandesa22117-stack/ClimateScope/tree/main/Reports)

---

## Tech Stack

- Python 3.8+
- Pandas
- NumPy
- Streamlit
- Plotly Express

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

**3. Run the dashboard**

For the Milestone 2 prototype:
```bash
streamlit run dashboard_M2.py
```

For the Milestone 3 final dashboard:
```bash
streamlit run climatescope_dashboard_M3.py
```

> Note: Place `GlobalWeatherRepository.csv` in the project root directory before
> running either app, and update the file path in the script if required.

---

## Project Status

This project was developed in three structured phases as part of an academic
assessment. All three milestones are complete. The final dashboard (Milestone 3)
represents the fully developed version of the application.

---

*SiteGuard — Built with Streamlit and Plotly · Rachel Fernandes · Data: GlobalWeatherRepository*
