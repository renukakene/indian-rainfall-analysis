"""
=============================================================================
BDA Mini-Project: Indian Rainfall Data Analysis Using PySpark (2021-2025)
Streamlit Dashboard Application (app.py)
=============================================================================
Architecture:
- Single scrollable page containing all 10 major analysis sections top-to-bottom.
- Local selectors placed directly above their respective visualizations.
- No global analysis selectors in the sidebar.
- Strict data integrity: loads existing summary Parquet files from PySpark analysis.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. Page Configuration & Professional BDA Styling
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
        font-size: 2.25rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.3rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1D4ED8;
    }
    .event-card {
        background-color: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 1.1rem 1.4rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    .note-box {
        background-color: #F3F4F6;
        border-left: 4px solid #6B7280;
        padding: 0.8rem 1.1rem;
        border-radius: 4px;
        font-size: 0.92rem;
        color: #374151;
        margin-top: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Data Loading Function (with Caching)
# -----------------------------------------------------------------------------
@st.cache_data
def load_datasets():
    """
    Loads summary Parquet files generated during PySpark analysis phase.
    Strictly reads from dashboard_data/ without altering or creating mock datasets.
    """
    base_dir = "dashboard_data"
    
    yearly_df = pd.read_parquet(os.path.join(base_dir, "yearly"))
    monthly_df = pd.read_parquet(os.path.join(base_dir, "monthly"))
    seasonal_df = pd.read_parquet(os.path.join(base_dir, "seasonal"))
    geographic_df = pd.read_parquet(os.path.join(base_dir, "geographic"))
    
    # Sort yearly data
    yearly_df = yearly_df.sort_values(by="year").reset_index(drop=True)
    
    # Map month numbers to readable chronological names (Jan to Dec)
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
# 3. Sidebar: Project Metadata & Navigation Only
# -----------------------------------------------------------------------------
st.sidebar.title("🌧️ Project Details")
st.sidebar.markdown("### Indian Rainfall Analysis (2021–2025)")
st.sidebar.markdown(
    "**Course**: Big Data Analytics (BDA)  \n"
    "**Engine**: Apache PySpark in Google Colab  \n"
    "**Dashboard**: Streamlit, Pandas & Plotly  \n"
    "**Grid Points**: 4,964 (0.25° × 0.25° IMD Gridded)  \n"
    "**Total Observations**: 9,064,185 records"
)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📑 Section Directory")
st.sidebar.markdown(
    "1. [Dashboard Header & KPIs](#indian-rainfall-analysis-dashboard-2021-2025)  \n"
    "2. [Annual Rainfall Analysis](#2-annual-rainfall-analysis)  \n"
    "3. [Seasonal Rainfall Analysis](#3-seasonal-rainfall-analysis)  \n"
    "4. [Monthly Rainfall Analysis](#4-monthly-rainfall-analysis)  \n"
    "5. [Rainfall Intensity Analysis](#5-rainfall-intensity-analysis)  \n"
    "6. [Extreme Rainfall Analysis](#6-extreme-rainfall-analysis)  \n"
    "7. [Geographic Rainfall Distribution](#7-geographic-rainfall-distribution)  \n"
    "8. [Geographic Hotspots](#8-geographic-hotspots)  \n"
    "9. [Key Data Insights](#9-key-data-insights)  \n"
    "10. [Dataset Explorer](#10-dataset-explorer)"
)
st.sidebar.markdown("---")
st.sidebar.caption("All selectors are placed directly above their respective visualizations.")


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
# 1. DASHBOARD HEADER + KPI CARDS
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
        label="Total Valid Observations",
        value=f"{total_observations:,}",
        help="Total individual daily observation records processed by PySpark across India (2021-2025)."
    )

with kpi2:
    st.metric(
        label="Geographic Grid Points",
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
# 2. ANNUAL RAINFALL ANALYSIS
# =============================================================================
st.subheader("2. Annual Rainfall Analysis")
st.markdown("Multi-year rainfall comparisons across the five analyzed years (2021–2025). Both charts intentionally compare all five years without filtering.")

col_annual_1, col_annual_2 = st.columns(2)

with col_annual_1:
    # Chart 1: Average Daily Rainfall by Year (2021–2025) with 5-year mean line
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
    fig_annual_avg.update_layout(height=420, coloraxis_showscale=False, margin={"t": 45, "b": 20})
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
    fig_annual_sw.update_layout(height=420, coloraxis_showscale=False, margin={"t": 45, "b": 20})
    st.plotly_chart(fig_annual_sw, use_container_width=True)

st.markdown("---")


# =============================================================================
# 3. SEASONAL RAINFALL ANALYSIS
# =============================================================================
st.subheader("3. Seasonal Rainfall Analysis")

# Local year selector directly above the seasonal chart
col_season_sel, _ = st.columns([1, 2])
with col_season_sel:
    selected_season_year = st.selectbox(
        "Select Year for Seasonal Analysis:",
        options=available_years,
        index=available_years.index(2024) if 2024 in available_years else 0,
        key="local_season_year_selector",
        help="Select a year to update only the seasonal bar chart below."
    )

# Filter seasonal data for chosen year and sort in standard meteorological order
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
# 4. MONTHLY RAINFALL ANALYSIS
# =============================================================================
st.subheader("4. Monthly Rainfall Analysis")

# Local year selector directly above the monthly chart
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
# 5. RAINFALL INTENSITY ANALYSIS
# =============================================================================
st.subheader("5. Rainfall Intensity Analysis")
st.markdown("Comparison of mean daily rainfall intensity versus maximum recorded single-day peak intensity across the analyzed period.")

col_int1, col_int2 = st.columns(2)

with col_int1:
    fig_int_avg = px.bar(
        df_yearly,
        x="year",
        y="average_rainfall_mm",
        text="average_rainfall_mm",
        color="average_rainfall_mm",
        color_continuous_scale="Blues",
        title="<b>Annual Mean Daily Intensity (mm/day)</b>",
        labels={"year": "Year", "average_rainfall_mm": "Daily Mean (mm)"}
    )
    fig_int_avg.update_traces(texttemplate="%{text:.2f} mm", textposition="outside")
    fig_int_avg.update_layout(height=380, coloraxis_showscale=False, margin={"t": 45, "b": 20})
    st.plotly_chart(fig_int_avg, use_container_width=True)

with col_int2:
    fig_int_max = px.bar(
        df_yearly,
        x="year",
        y="maximum_rainfall_mm",
        text="maximum_rainfall_mm",
        color="maximum_rainfall_mm",
        color_continuous_scale="Teal",
        title="<b>Annual Maximum Single-Day Peak Intensity (mm)</b>",
        labels={"year": "Year", "maximum_rainfall_mm": "Maximum Peak (mm)"}
    )
    fig_int_max.update_traces(texttemplate="%{text:.2f} mm", textposition="outside")
    fig_int_max.update_layout(height=380, coloraxis_showscale=False, margin={"t": 45, "b": 20})
    st.plotly_chart(fig_int_max, use_container_width=True)

st.markdown("""
<div class="note-box">
    ℹ️ <strong>Note on Granular Intensity Bins</strong>: Categorizing individual daily rainfall into discrete IMD intensity classes 
    (e.g., Light &lt; 7.5 mm, Moderate 7.6–64.4 mm, Heavy &gt; 64.5 mm) requires exporting an intensity-categorized summary dataset 
    from the PySpark notebook. The above charts present verified intensity metrics (annual mean daily intensity vs. annual peak single-day intensity) 
    derived from the existing summary datasets.
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# =============================================================================
# 6. EXTREME RAINFALL ANALYSIS
# =============================================================================
st.subheader("6. Extreme Rainfall Analysis")

col_ex1, col_ex2 = st.columns([1, 1])

with col_ex1:
    st.markdown("""
    <div class="event-card">
        <h4 style="color: #1E3A8A; margin-top: 0; margin-bottom: 0.5rem;">Record Single-Day Precipitation Event</h4>
        <p style="margin: 0.35rem 0; font-size: 1.05rem;"><strong>📅 Date:</strong> 17 June 2022</p>
        <p style="margin: 0.35rem 0; font-size: 1.05rem;"><strong>📍 Latitude:</strong> 25.25° N</p>
        <p style="margin: 0.35rem 0; font-size: 1.05rem;"><strong>📍 Longitude:</strong> 91.25° E</p>
        <p style="margin: 0.35rem 0; font-size: 1.25rem; color: #DC2626;"><strong>🌧️ Rainfall:</strong> 979.14 mm</p>
        <p style="margin-top: 0.6rem; font-size: 0.95rem; color: #1F2937; line-height: 1.4;">
            <strong>Highest single-day rainfall observation in the analyzed PySpark dataset.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_ex2:
    st.markdown("#### Annual Maximum Recorded Precipitation by Year")
    df_peak_table = df_yearly[["year", "maximum_rainfall_mm", "average_rainfall_mm"]].copy()
    df_peak_table.columns = ["Year", "Annual Maximum Single-Day (mm)", "Annual Daily Average (mm)"]
    st.dataframe(
        df_peak_table.style.format({
            "Annual Maximum Single-Day (mm)": "{:.2f}",
            "Annual Daily Average (mm)": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")


# =============================================================================
# 7. GEOGRAPHIC RAINFALL DISTRIBUTION
# =============================================================================
st.subheader("7. Geographic Rainfall Distribution")

# Local metric selector placed directly above the map
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
# 8. GEOGRAPHIC HOTSPOTS
# =============================================================================
st.subheader("8. Geographic Hotspots")
st.markdown("Top 10 geographic grid points across India ranked by highest 5-year average daily rainfall, extracted from the verified spatial dataset.")

# Calculate Top 10 grid points by average rainfall
top10_hotspots = df_geographic.sort_values(by="average_rainfall_mm", ascending=False).head(10).reset_index(drop=True)
top10_hotspots["Rank"] = range(1, 11)
top10_hotspots["Location"] = top10_hotspots.apply(lambda r: f"{r.latitude:.2f}°N, {r.longitude:.2f}°E", axis=1)

col_hot1, col_hot2 = st.columns([1, 1])

with col_hot1:
    st.markdown("#### Top 10 Grid Points by Average Rainfall")
    table_hotspots = top10_hotspots[["Rank", "latitude", "longitude", "average_rainfall_mm", "maximum_rainfall_mm", "observations"]].copy()
    table_hotspots.columns = ["Rank", "Latitude", "Longitude", "Average Rainfall (mm)", "Maximum Rainfall (mm)", "Observations"]
    
    st.dataframe(
        table_hotspots.style.format({
            "Latitude": "{:.2f}",
            "Longitude": "{:.2f}",
            "Average Rainfall (mm)": "{:.2f}",
            "Maximum Rainfall (mm)": "{:.2f}",
            "Observations": "{:,}"
        }),
        use_container_width=True,
        hide_index=True
    )

with col_hot2:
    fig_hotspots = px.bar(
        top10_hotspots.iloc[::-1],
        x="average_rainfall_mm",
        y="Location",
        orientation="h",
        text="average_rainfall_mm",
        color="average_rainfall_mm",
        color_continuous_scale="Blues",
        title="<b>Top 10 Grid Points by Average Daily Rainfall (2021–2025)</b>",
        labels={"average_rainfall_mm": "Average Daily Rainfall (mm)", "Location": "Grid Coordinates"}
    )
    fig_hotspots.update_traces(texttemplate="%{text:.2f} mm", textposition="outside")
    fig_hotspots.update_layout(
        height=380,
        coloraxis_showscale=False,
        xaxis_title="Average Daily Rainfall (mm)",
        yaxis_title="Coordinates (Lat, Lon)",
        margin={"t": 45, "b": 20}
    )
    st.plotly_chart(fig_hotspots, use_container_width=True)

st.markdown("---")


# =============================================================================
# 9. KEY DATA INSIGHTS
# =============================================================================
st.subheader("9. Key Data Insights")
st.markdown("Findings strictly supported by the analyzed PySpark summary datasets:")

st.info(
    "• **Five-Year Mean Annual Average**: **3.31 mm/day** across all 4,964 grid points in India.\n\n"
    "• **2023 Annual Average**: Lowest annual average daily rainfall among 2021–2025 at **2.96 mm/day**.\n\n"
    "• **2025 Annual Average**: Highest annual average daily rainfall among 2021–2025 at **3.47 mm/day**.\n\n"
    "• **2024 Southwest Monsoon**: Highest Southwest Monsoon seasonal average among 2021–2025 at **7.72 mm/day**.\n\n"
    "• **Southwest Monsoon (Jun–Sep)**: Consistently exhibits the highest average daily rainfall among the four analyzed seasons.\n\n"
    "• **Maximum Observed Rainfall**: **979.14 mm** recorded on 17 June 2022 at latitude 25.25°N, longitude 91.25°E."
)

st.markdown("---")


# =============================================================================
# 10. DATASET EXPLORER
# =============================================================================
st.subheader("10. Dataset Explorer")
st.markdown("Inspect the underlying summary Parquet datasets generated by the PySpark pipeline:")

dataset_choice = st.selectbox(
    "Select Summary Dataset to Inspect:",
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
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Indian Rainfall Data Analysis and Visualization Using PySpark (2021–2025) | "
    "Big Data Analytics (BDA) Mini-Project Presentation"
)
