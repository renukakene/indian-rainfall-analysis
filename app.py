"""
=============================================================================
BDA Mini-Project: Indian Rainfall Data Analysis Using PySpark (2021-2025)
Streamlit Dashboard Application (app.py)
=============================================================================
Architecture:
- Single scrollable page containing all major analysis sections top-to-bottom.
- Local selectors placed directly above their associated charts.
- No global sidebar analysis filters that cross-impact unrelated charts.
- Summary Parquet data generated during PySpark analysis loaded via pandas.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. Page Configuration & Presentation Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="🇮🇳 Indian Rainfall Analysis Dashboard (2021–2025)",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1F2937;
        margin-top: 1rem;
        margin-bottom: 0.4rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1D4ED8;
    }
    .event-card {
        background-color: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 1rem 1.2rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Data Loading Function (with Caching)
# -----------------------------------------------------------------------------
@st.cache_data
def load_datasets():
    """
    Loads summary Parquet files from local dashboard_data directory.
    Aggregated and cleaned during PySpark analysis.
    """
    base_dir = "dashboard_data"
    
    yearly_df = pd.read_parquet(os.path.join(base_dir, "yearly"))
    monthly_df = pd.read_parquet(os.path.join(base_dir, "monthly"))
    seasonal_df = pd.read_parquet(os.path.join(base_dir, "seasonal"))
    geographic_df = pd.read_parquet(os.path.join(base_dir, "geographic"))
    
    # Sort yearly data
    yearly_df = yearly_df.sort_values(by="year").reset_index(drop=True)
    
    # Map month numbers to readable names (Jan to Dec)
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    monthly_df["month_name"] = monthly_df["month"].map(month_names)
    monthly_df = monthly_df.sort_values(by=["year", "month"]).reset_index(drop=True)
    
    # Meteorological season ordering
    season_order = ["Winter", "Pre-Monsoon", "Southwest Monsoon", "Post-Monsoon"]
    seasonal_df["season"] = pd.Categorical(seasonal_df["season"], categories=season_order, ordered=True)
    seasonal_df = seasonal_df.sort_values(by=["year", "season"]).reset_index(drop=True)
    
    return yearly_df, monthly_df, seasonal_df, geographic_df


try:
    df_yearly, df_monthly, df_seasonal, df_geographic = load_datasets()
except Exception as e:
    st.error(f"Error loading dashboard Parquet files: {e}")
    st.info("Ensure 'dashboard_data' folder exists with yearly, monthly, seasonal, and geographic subfolders.")
    st.stop()

# Available years list for local dropdowns
available_years = sorted(df_yearly["year"].unique().tolist())


# -----------------------------------------------------------------------------
# 3. Sidebar: Project Info Only (No Global Analysis Filters)
# -----------------------------------------------------------------------------
st.sidebar.title("🌧️ Project Details")
st.sidebar.markdown("### Indian Rainfall Analysis (2021–2025)")
st.sidebar.markdown(
    "**Course**: Big Data Analytics (BDA)  \n"
    "**Engine**: PySpark in Google Colab  \n"
    "**Dashboard**: Streamlit & Plotly  \n"
    "**Grid Points**: 4,964 (0.25° × 0.25°)  \n"
    "**Total Records**: 9,064,185 observations"
)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📑 Page Sections")
st.sidebar.markdown(
    "1. [Top KPI Cards](#indian-rainfall-analysis-dashboard-2021-2025)  \n"
    "2. [Annual Rainfall Analysis](#1-annual-rainfall-analysis)  \n"
    "3. [Seasonal Rainfall Analysis](#2-seasonal-rainfall-analysis)  \n"
    "4. [Monthly Rainfall Analysis](#3-monthly-rainfall-analysis)  \n"
    "5. [Geographic Rainfall Distribution](#4-geographic-rainfall-distribution)  \n"
    "6. [Highest Rainfall Event & Insights](#5-highest-rainfall-event)  \n"
    "7. [Dataset Explorer](#7-dataset-explorer)"
)
st.sidebar.markdown("---")
st.sidebar.caption("All selectors are placed directly above their respective charts for clarity.")


# -----------------------------------------------------------------------------
# 4. Helper Function for Map Rendering
# -----------------------------------------------------------------------------
def plot_india_map(df, color_column, title_text, color_label):
    """
    Renders an interactive map of India showing all 4,964 spatial grid points.
    Compatible across Plotly 6+ (scatter_map) and Plotly 5 (scatter_mapbox).
    """
    labels_dict = {color_column: color_label}
    
    if hasattr(px, "scatter_map"):
        fig = px.scatter_map(
            df,
            lat="latitude",
            lon="longitude",
            color=color_column,
            size=color_column,
            color_continuous_scale="Viridis",
            size_max=7,
            zoom=3.8,
            center={"lat": 22.5, "lon": 82.0},
            map_style="open-street-map",
            title=title_text,
            labels=labels_dict,
            hover_data={
                "latitude": ":.2f",
                "longitude": ":.2f",
                color_column: ":.2f",
                "observations": True
            }
        )
    else:
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color=color_column,
            size=color_column,
            color_continuous_scale="Viridis",
            size_max=7,
            zoom=3.8,
            center={"lat": 22.5, "lon": 82.0},
            mapbox_style="open-street-map",
            title=title_text,
            labels=labels_dict,
            hover_data={
                "latitude": ":.2f",
                "longitude": ":.2f",
                color_column: ":.2f",
                "observations": True
            }
        )
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, height=550)
    return fig


# =============================================================================
# SECTION 1: Dashboard Header & KPI Cards
# =============================================================================
st.markdown('<div class="main-title">🇮🇳 Indian Rainfall Analysis Dashboard (2021–2025)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Big Data Analytics Mini-Project | PySpark-Engineered Cleaned Datasets</div>', unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_observations = int(df_yearly["observations"].sum())
total_grid_points = len(df_geographic)
year_range = f"{df_yearly['year'].min()}–{df_yearly['year'].max()}"
max_daily_rainfall = float(df_yearly["maximum_rainfall_mm"].max())

with kpi1:
    st.metric(
        label="Total Valid Observations (2021–2025)",
        value=f"{total_observations:,}",
        help="Total individual daily observation records processed by PySpark across India (2021-2025)."
    )

with kpi2:
    st.metric(
        label="Geographic Grid Points (2021–2025)",
        value=f"{total_grid_points:,}",
        help="Unique spatial 0.25° x 0.25° latitude/longitude grid cells covering the Indian landmass."
    )

with kpi3:
    st.metric(
        label="Analysis Years",
        value=year_range,
        help="Complete 5-year chronological coverage."
    )

with kpi4:
    st.metric(
        label="Maximum Daily Rainfall",
        value=f"{max_daily_rainfall:.2f} mm",
        help="Highest single-day precipitation recorded at any grid point across the entire dataset."
    )

st.markdown("---")


# =============================================================================
# SECTION 2: Annual Rainfall Analysis
# =============================================================================
st.subheader("1. Annual Rainfall Analysis")
st.markdown("Annual rainfall comparisons across all five years (2021–2025). No selector needed as both charts compare the full period.")

col_annual_1, col_annual_2 = st.columns(2)

with col_annual_1:
    # Chart 1: Average Daily Rainfall by Year (2021–2025)
    fig_annual_avg = px.bar(
        df_yearly,
        x="year",
        y="average_rainfall_mm",
        text="average_rainfall_mm",
        color="average_rainfall_mm",
        color_continuous_scale="Blues",
        title="<b>Average Daily Rainfall by Year (2021–2025)</b>",
        labels={"year": "Year", "average_rainfall_mm": "Average Daily Rainfall (mm)"}
    )
    fig_annual_avg.update_traces(texttemplate="%{text:.2f} mm", textposition="outside")
    overall_mean = df_yearly["average_rainfall_mm"].mean()
    fig_annual_avg.add_hline(
        y=overall_mean,
        line_dash="dash",
        line_color="red",
        annotation_text=f"5-Year Mean: {overall_mean:.2f} mm",
        annotation_position="bottom right"
    )
    fig_annual_avg.update_layout(height=400, coloraxis_showscale=False, margin={"t": 45, "b": 20})
    st.plotly_chart(fig_annual_avg, use_container_width=True)

with col_annual_2:
    # Chart 2: Southwest Monsoon Rainfall by Year (2021–2025)
    df_sw = df_seasonal[df_seasonal["season"] == "Southwest Monsoon"].sort_values(by="year").copy()
    fig_annual_sw = px.bar(
        df_sw,
        x="year",
        y="average_rainfall_mm",
        text="average_rainfall_mm",
        color="average_rainfall_mm",
        color_continuous_scale="Teal",
        title="<b>Southwest Monsoon Rainfall by Year (2021–2025)</b>",
        labels={"year": "Year", "average_rainfall_mm": "Average Daily Rainfall (mm)"}
    )
    fig_annual_sw.update_traces(texttemplate="%{text:.2f} mm", textposition="outside")
    fig_annual_sw.update_layout(height=400, coloraxis_showscale=False, margin={"t": 45, "b": 20})
    st.plotly_chart(fig_annual_sw, use_container_width=True)

st.markdown("---")


# =============================================================================
# SECTION 3: Seasonal Rainfall Analysis
# =============================================================================
st.subheader("2. Seasonal Rainfall Analysis")

# Local selector directly above seasonal chart
col_season_sel, _ = st.columns([1, 2])
with col_season_sel:
    selected_season_year = st.selectbox(
        "Select Year for Seasonal Analysis:",
        options=available_years,
        index=available_years.index(2024) if 2024 in available_years else 0,
        key="local_season_year_selector",
        help="Select a year to update only the seasonal bar chart below."
    )

# Filter seasonal data for chosen year and ensure meteorological order
season_order = ["Winter", "Pre-Monsoon", "Southwest Monsoon", "Post-Monsoon"]
df_season_year = df_seasonal[df_seasonal["year"] == selected_season_year].copy()
df_season_year["season"] = pd.Categorical(df_season_year["season"], categories=season_order, ordered=True)
df_season_year = df_season_year.sort_values(by="season").reset_index(drop=True)

# Exactly FOUR normal bars for the selected year (not stacked)
fig_seasonal = px.bar(
    df_season_year,
    x="season",
    y="average_rainfall_mm",
    text="average_rainfall_mm",
    color="season",
    title=f"<b>Average Daily Rainfall by Season — {selected_season_year}</b>",
    labels={"season": "Season", "average_rainfall_mm": "Average Daily Rainfall (mm)"},
    color_discrete_sequence=px.colors.qualitative.Safe
)
fig_seasonal.update_traces(texttemplate="%{text:.2f} mm", textposition="outside")
fig_seasonal.update_layout(
    showlegend=False,
    height=430,
    xaxis_title="Season",
    yaxis_title="Average Daily Rainfall (mm)",
    margin={"t": 50, "b": 20}
)
st.plotly_chart(fig_seasonal, use_container_width=True)

st.markdown("---")


# =============================================================================
# SECTION 4: Monthly Rainfall Analysis
# =============================================================================
st.subheader("3. Monthly Rainfall Analysis")

# Local selector directly above monthly chart
col_month_sel, _ = st.columns([1, 2])
with col_month_sel:
    selected_monthly_year = st.selectbox(
        "Select Year for Monthly Analysis:",
        options=available_years,
        index=available_years.index(2024) if 2024 in available_years else 0,
        key="local_monthly_year_selector",
        help="Select a year to update only the 12-month rainfall chart below."
    )

# Filter monthly data for chosen year: complete Jan-Dec pattern (all 12 months)
df_month_year = df_monthly[df_monthly["year"] == selected_monthly_year].sort_values(by="month").copy()

fig_monthly = px.bar(
    df_month_year,
    x="month_name",
    y="average_rainfall_mm",
    text="average_rainfall_mm",
    color="average_rainfall_mm",
    color_continuous_scale="Blues",
    title=f"<b>Average Daily Rainfall by Month — {selected_monthly_year}</b>",
    labels={"month_name": "Month", "average_rainfall_mm": "Average Daily Rainfall (mm)"}
)
fig_monthly.update_traces(texttemplate="%{text:.2f} mm", textposition="outside")
fig_monthly.update_layout(
    height=450,
    coloraxis_showscale=False,
    xaxis_title="Month",
    yaxis_title="Average Daily Rainfall (mm)",
    margin={"t": 50, "b": 20}
)
st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("---")


# =============================================================================
# SECTION 5: Geographic Rainfall Distribution
# =============================================================================
st.subheader("4. Geographic Rainfall Distribution")

# Local selector directly above the map
map_metric = st.radio(
    "Select Geographic Metric:",
    options=["Average Daily Rainfall (mm)", "Maximum Single-Day Rainfall (mm)"],
    horizontal=True,
    key="local_geo_metric_selector",
    help="Select which metric to visualize on the map of India below."
)

if map_metric == "Average Daily Rainfall (mm)":
    metric_col = "average_rainfall_mm"
    map_title = "<b>Spatial Distribution: 5-Year Average Daily Rainfall (mm)</b>"
    colorbar_label = "Average Daily Rainfall (mm)"
else:
    metric_col = "maximum_rainfall_mm"
    map_title = "<b>Spatial Distribution: Maximum Single-Day Rainfall (mm)</b>"
    colorbar_label = "Maximum Single-Day Rainfall (mm)"

fig_map = plot_india_map(df_geographic, metric_col, map_title, colorbar_label)
st.plotly_chart(fig_map, use_container_width=True)

st.caption("Note: Each point represents an analyzed geographic rainfall grid point. Colors indicate the selected rainfall metric.")

st.markdown("---")


# =============================================================================
# SECTION 6: Highest Rainfall Event & Data Insights
# =============================================================================
col_event, col_insights = st.columns([1, 1])

with col_event:
    st.subheader("5. Highest Rainfall Event")
    st.markdown("""
    <div class="event-card">
        <h4 style="color: #1E3A8A; margin-top: 0;">Record Daily Precipitation</h4>
        <p style="margin: 0.3rem 0; font-size: 1.05rem;"><strong>📅 Date:</strong> 17 June 2022</p>
        <p style="margin: 0.3rem 0; font-size: 1.05rem;"><strong>📍 Latitude:</strong> 25.25° N</p>
        <p style="margin: 0.3rem 0; font-size: 1.05rem;"><strong>📍 Longitude:</strong> 91.25° E</p>
        <p style="margin: 0.3rem 0; font-size: 1.15rem; color: #DC2626;"><strong>🌧️ Rainfall:</strong> 979.14 mm</p>
        <small style="color: #6B7280;">Extracted directly from PySpark validated daily records (Meghalaya region).</small>
    </div>
    """, unsafe_allow_html=True)

with col_insights:
    st.subheader("6. Data Insights")
    st.info(
        "• **Southwest Monsoon** has the highest average daily rainfall among the four analyzed seasons.\n\n"
        "• **2024** had the highest Southwest Monsoon average: **7.72 mm/day**.\n\n"
        "• **2023** had the lowest annual average daily rainfall: **2.96 mm/day**.\n\n"
        "• **2025** had the highest annual average daily rainfall: **3.47 mm/day**.\n\n"
        "• **Maximum observed rainfall**: **979.14 mm** on 17 June 2022 at latitude 25.25 and longitude 91.25."
    )

st.markdown("---")


# =============================================================================
# SECTION 7: Dataset Explorer
# =============================================================================
st.subheader("7. Dataset Explorer")
st.markdown("Inspect the underlying summary Parquet datasets generated by PySpark:")

dataset_choice = st.selectbox(
    "Select Dataset to Inspect:",
    options=["Yearly Summary", "Monthly Summary", "Seasonal Summary", "Geographic Summary (Sample)"],
    key="local_dataset_choice"
)

if dataset_choice == "Yearly Summary":
    st.write("📁 **Source**: `dashboard_data/yearly/` (5 rows × 5 columns)")
    st.dataframe(df_yearly, use_container_width=True, hide_index=True)

elif dataset_choice == "Monthly Summary":
    st.write("📁 **Source**: `dashboard_data/monthly/` (60 rows × 7 columns)")
    st.dataframe(df_monthly, use_container_width=True, hide_index=True)

elif dataset_choice == "Seasonal Summary":
    st.write("📁 **Source**: `dashboard_data/seasonal/` (20 rows × 6 columns)")
    st.dataframe(df_seasonal, use_container_width=True, hide_index=True)

elif dataset_choice == "Geographic Summary (Sample)":
    st.write("📁 **Source**: `dashboard_data/geographic/` (4,964 rows × 6 columns — displaying first 100 rows)")
    st.dataframe(df_geographic.head(100), use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# 8. Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Indian Rainfall Data Analysis (2021–2025) | Built with Streamlit, Pandas & Plotly | "
    "Big Data Analytics (BDA) Mini-Project Presentation"
)
