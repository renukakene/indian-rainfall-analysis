# 🇮🇳 Indian Rainfall Data Analysis Dashboard (2021–2025)

An interactive Big Data Analytics (BDA) mini-project dashboard analyzing 5 years of daily Indian precipitation data.

---

## 📌 Project Overview

- **Period**: 2021–2025 (5 Years)
- **Spatial Resolution**: 0.25° × 0.25° Grid Cells (4,964 spatial grid points covering India)
- **Valid Observations**: 9,064,185 daily records
- **Maximum Daily Rainfall Recorded**: 979.14 mm (17 June 2022 at Lat 25.25° N, Lon 91.25° E)

---

## ⚙️ Big Data Processing Pipeline

1. **Raw Data**: IMD High-Resolution Gridded NetCDF files.
2. **Preprocessing**: Python & `xarray` to convert multi-dimensional NetCDF arrays into columnar Parquet format.
3. **PySpark DataFrame Engine (Google Colab)**:
   - Data validation, filtering nulls/anomalies.
   - Temporal extractions (Year, Month, Season).
   - Aggregations into yearly, seasonal, monthly, and spatial summary datasets.
4. **Interactive Dashboard**: Streamlit, Pandas, and Plotly Express.

---

## 🚀 Live Demo & Deployment

This application is ready to deploy on **Streamlit Community Cloud**:
- **Main file path**: `app.py`
- **Dependencies**: `requirements.txt`
- **Data**: Summary tables located in `dashboard_data/`

---

## 💻 Local Setup & Execution

1. **Clone the repository**:
   ```bash
   git clone <your-github-repo-url>
   cd "Indian rainfall analysis"
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit dashboard**:
   ```bash
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

## 📊 Dashboard Structure (10 Analysis Sections)

1. **Dashboard Header & KPI Cards**: Total observations (9.06M), Grid points (4,964), Year range (2021–2025), and Maximum daily rainfall (979.14 mm).
2. **Annual Rainfall Analysis**: Multi-year comparisons of average daily precipitation and Southwest Monsoon intensity.
3. **Seasonal Rainfall Analysis**: Local year selector (2021–2025) displaying normal grouped bars for Winter, Pre-Monsoon, Southwest Monsoon, and Post-Monsoon.
4. **Monthly Rainfall Analysis**: Complete 12-month Jan–Dec progression for each selected year.
5. **Rainfall Intensity Analysis**: Annual mean daily intensity versus maximum single-day peak intensity.
6. **Extreme Rainfall Analysis**: Highest verified rainfall event (979.14 mm on 17 June 2022) with annual maximum records.
7. **Geographic Rainfall Distribution**: Interactive spatial map of India showing rainfall metrics across 4,964 grid cells.
8. **Geographic Hotspots**: Top 10 grid points ranked by average daily rainfall with tabular breakdown and horizontal bar chart.
9. **Key Data Insights**: Core findings strictly supported by the PySpark summary datasets.
10. **Dataset Explorer**: In-browser inspection of raw summary Parquet datasets.

---

## 🛠️ Tech Stack

- **Data Processing**: Apache PySpark, Python, Pandas, PyArrow
- **Visualization & UI**: Streamlit, Plotly Express
