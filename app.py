import streamlit as st
import pandas as pd
import plotly.express as px

from src.preprocess import load_data, clean_data

from src.metrics import (
    calculate_metrics,
    weather_performance,
    traffic_performance,
    vehicle_performance,
    area_performance,
    category_performance,
)

from src.visualizations import (
    delay_analyzer_chart,
    vehicle_comparison_chart,
    agent_performance_chart,
    area_heatmap_chart,
    category_boxplot_chart,
    style_chart,
)


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LogiSight | Logistics Analytics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "LogiSight Logistics Analytics — "
            "A platform for exploring delivery performance, "
            "fleet efficiency, operational delays, "
            "and regional logistics trends."
        )
    }
)


# ============================================================
# 2. COLOR PALETTE
# ============================================================

COLORS = [
    "#00D4FF",
    "#A855F7",
    "#FF6B9A",
    "#22C55E",
    "#F59E0B",
    "#3B82F6",
    "#EF4444",
    "#FACC15",
    "#14B8A6",
    "#8B5CF6",
]


# ============================================================
# 3. THEME DETECTION
# ============================================================

try:
    DARK_MODE = st.context.theme.type == "dark"
except (AttributeError, KeyError):
    DARK_MODE = True


# ============================================================
# 4. LOAD AND PREPARE DATA
# ============================================================

@st.cache_data(show_spinner="Preparing delivery analytics...")
def get_data():

    raw_data = load_data()

    cleaned_data, cleaning_report = clean_data(raw_data)

    return raw_data, cleaned_data, cleaning_report


try:

    raw_df, df, cleaning_report = get_data()

except Exception as error:

    st.error("Unable to load delivery analytics.")

    st.exception(error)

    st.stop()


if df.empty:

    st.error("No valid delivery records are available.")

    st.stop()


# ============================================================
# 5. SIDEBAR NAVIGATION
# ============================================================

PAGES = [
    "🏠 Command Center",
    "🚦 Delay Intelligence",
    "🚗 Fleet & Agent Analytics",
    "📍 Regional & Product Insights",
    "🧹 Data Quality Lab",
    "📖 Dashboard Guide",
]


with st.sidebar:

    st.title("🚚 LogiSight")

    st.caption("LOGISTICS ANALYTICS")

    st.divider()

    st.subheader("🧭 Navigation")

    page = st.radio(
        "Dashboard sections",
        options=PAGES,
        label_visibility="collapsed",
        key="navigation"
    )

    st.divider()


# ============================================================
# 6. FILTER CONFIGURATION
# ============================================================

FILTERS = {
    "Weather": "weather_filter",
    "Traffic": "traffic_filter",
    "Vehicle": "vehicle_filter",
    "Category": "category_filter",
    "Area": "area_filter",
}


def filter_options(column):

    return sorted(
        df[column].dropna().unique().tolist()
    )


# Initialize filter values
for column, key in FILTERS.items():

    if key not in st.session_state:

        st.session_state[key] = filter_options(column)


# Reset only dashboard filters
def reset_filters():

    for column, key in FILTERS.items():

        st.session_state[key] = filter_options(column)


# ============================================================
# 7. INTERACTIVE SIDEBAR FILTERS
# ============================================================

with st.sidebar:

    st.subheader("🎛️ Control Center")

    st.caption(
        "Customize the analytics using the filters below."
    )

    st.button(
        "🔄 Reset All Filters",
        on_click=reset_filters,
        use_container_width=True,
        type="primary"
    )

    with st.expander(
        "🌦️ Weather Conditions",
        expanded=True
    ):

        weather_filter = st.multiselect(
            "Select Weather",
            options=filter_options("Weather"),
            key="weather_filter"
        )

    with st.expander(
        "🚦 Traffic Conditions",
        expanded=True
    ):

        traffic_filter = st.multiselect(
            "Select Traffic",
            options=filter_options("Traffic"),
            key="traffic_filter"
        )

    with st.expander(
        "🚗 Vehicle Types",
        expanded=False
    ):

        vehicle_filter = st.multiselect(
            "Select Vehicles",
            options=filter_options("Vehicle"),
            key="vehicle_filter"
        )

    with st.expander(
        "📦 Product Categories",
        expanded=False
    ):

        category_filter = st.multiselect(
            "Select Categories",
            options=filter_options("Category"),
            key="category_filter"
        )

    with st.expander(
        "📍 Delivery Areas",
        expanded=False
    ):

        area_filter = st.multiselect(
            "Select Areas",
            options=filter_options("Area"),
            key="area_filter"
        )


# ============================================================
# 8. APPLY SIDEBAR FILTERS
# ============================================================

filtered_df = df[
    df["Weather"].isin(weather_filter)
    & df["Traffic"].isin(traffic_filter)
    & df["Vehicle"].isin(vehicle_filter)
    & df["Category"].isin(category_filter)
    & df["Area"].isin(area_filter)
].copy()


# ============================================================
# 9. SIDEBAR LIVE STATUS
# ============================================================

with st.sidebar:

    st.divider()

    st.subheader("📡 Live Operations")

    with st.container(border=True):

        st.metric(
            "Active Delivery Records",
            f"{len(filtered_df):,}"
        )

        percentage = (
            len(filtered_df) / len(df) * 100
        )

        st.progress(
            min(len(filtered_df) / len(df), 1.0)
        )

        st.caption(
            f"{percentage:.1f}% of available records"
        )

    st.divider()

    with st.expander("⚙️ Appearance Settings"):

        st.write(
            "Switch between Dark and Light mode "
            "using the application Settings menu."
        )

        st.caption(
            "⋮ → Settings → Theme"
        )

    st.caption("© LogiSight Analytics")


# ============================================================
# 10. MAIN DASHBOARD HEADER
# ============================================================

st.caption(
    "LOGISIGHT  /  LOGISTICS INTELLIGENCE"
)

st.title("🚚 Logistics Analytics")

st.write(
    "Explore delivery efficiency, fleet performance, "
    "operational delays, and regional logistics trends."
)

st.divider()


# ============================================================
# 11. HANDLE EMPTY FILTER RESULTS
# ============================================================

if filtered_df.empty:

    st.warning(
        "No delivery records match your selected filters."
    )

    st.info(
        "Adjust your selections or click Reset All Filters."
    )

    st.stop()


# ============================================================
# 12. KPI CALCULATIONS
# ============================================================

metrics = calculate_metrics(filtered_df)


def show_kpis():

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        with st.container(border=True):

            st.metric(
                "📦 Total Deliveries",
                f"{metrics['total_deliveries']:,}"
            )

    with col2:

        with st.container(border=True):

            st.metric(
                "⏱️ Avg. Delivery Time",
                f"{metrics['average_delivery_time']:.1f} min"
            )

    with col3:

        with st.container(border=True):

            st.metric(
                "🚨 Late Deliveries",
                f"{metrics['late_delivery_percentage']:.1f}%"
            )

    with col4:

        with st.container(border=True):

            st.metric(
                "⭐ Agent Rating",
                f"{metrics['average_agent_rating']:.2f}/5"
            )


# ============================================================
# 13. COMMAND CENTER PAGE
# ============================================================

if page == "🏠 Command Center":

    st.header("📊 Operations Command Center")

    st.caption(
        "Monitor logistics performance and delivery efficiency."
    )

    show_kpis()

    st.divider()

    st.subheader("📈 Operational Performance")

    col1, col2 = st.columns(2)

    # Traffic Performance
    with col1:

        with st.container(border=True):

            traffic_df = traffic_performance(filtered_df)

            fig = px.bar(
                traffic_df,

                x="Traffic",

                y="Average_Delivery_Time",

                color="Traffic",

                color_discrete_sequence=COLORS,

                title="Delivery Time by Traffic",

                labels={
                    "Average_Delivery_Time":
                        "Average Delivery Time (min)",
                    "Traffic": "Traffic Conditions"
                },

                text_auto=".1f"
            )

            fig.update_layout(
                showlegend=False
            )

            st.plotly_chart(
                style_chart(fig, DARK_MODE),
                width="stretch"
            )

    # Weather Performance
    with col2:

        with st.container(border=True):

            weather_df = weather_performance(filtered_df)

            fig = px.bar(
                weather_df,

                x="Weather",

                y="Average_Delivery_Time",

                color="Weather",

                color_discrete_sequence=COLORS,

                title="Delivery Time by Weather",

                labels={
                    "Average_Delivery_Time":
                        "Average Delivery Time (min)",
                    "Weather": "Weather Conditions"
                },

                text_auto=".1f"
            )

            fig.update_layout(
                showlegend=False
            )

            st.plotly_chart(
                style_chart(fig, DARK_MODE),
                width="stretch"
            )

    st.divider()

    # Delivery Distribution
    with st.container(border=True):

        st.subheader("📊 Delivery Time Distribution")

        fig = px.histogram(
            filtered_df,

            x="Delivery_Time",

            nbins=40,

            color_discrete_sequence=["#00D4FF"],

            title="Distribution of Delivery Durations",

            labels={
                "Delivery_Time": "Delivery Time (minutes)",
                "count": "Number of Deliveries"
            }
        )

        st.plotly_chart(
            style_chart(fig, DARK_MODE),
            width="stretch"
        )

    st.info(
        "💡 Use the Control Center filters to explore "
        "performance under different operating conditions."
    )


# ============================================================
# 14. DELAY INTELLIGENCE PAGE
# ============================================================

elif page == "🚦 Delay Intelligence":

    st.header("🚦 Delay Intelligence")

    st.write(
        "Analyze how weather and traffic conditions "
        "influence delivery performance."
    )

    show_kpis()

    st.divider()

    with st.container(border=True):

        st.plotly_chart(
            delay_analyzer_chart(
                filtered_df,
                DARK_MODE
            ),
            width="stretch"
        )

    traffic_df = traffic_performance(filtered_df)

    worst_traffic = traffic_df.loc[
        traffic_df["Average_Delivery_Time"].idxmax()
    ]

    st.warning(
        "🚨 Highest average delivery time: "
        f"{worst_traffic['Traffic']} traffic conditions."
    )

    st.subheader("📋 Traffic Performance Details")

    st.dataframe(
        traffic_df,
        width="stretch",
        hide_index=True
    )


# ============================================================
# 15. FLEET & AGENT ANALYTICS PAGE
# ============================================================

elif page == "🚗 Fleet & Agent Analytics":

    st.header("🚗 Fleet & Agent Analytics")

    st.write(
        "Evaluate vehicle efficiency and "
        "delivery agent performance."
    )

    tab1, tab2 = st.tabs(
        [
            "🚗 Vehicle Performance",
            "👤 Agent Performance"
        ]
    )

    # Vehicle Comparison
    with tab1:

        with st.container(border=True):

            st.plotly_chart(
                vehicle_comparison_chart(
                    filtered_df,
                    DARK_MODE
                ),
                width="stretch"
            )

        vehicle_df = vehicle_performance(filtered_df)

        fastest = vehicle_df.loc[
            vehicle_df["Average_Delivery_Time"].idxmin()
        ]

        st.success(
            "🏆 Lowest average delivery time: "
            f"{fastest['Vehicle']}"
        )

        st.dataframe(
            vehicle_df,
            width="stretch",
            hide_index=True
        )

    # Agent Scatter Plot
    with tab2:

        with st.container(border=True):

            st.plotly_chart(
                agent_performance_chart(
                    filtered_df,
                    DARK_MODE
                ),
                width="stretch"
            )

        st.info(
            "💡 Each point represents a delivery record. "
            "Colors distinguish delivery agent age groups."
        )


# ============================================================
# 16. REGIONAL & PRODUCT INSIGHTS PAGE
# ============================================================

elif page == "📍 Regional & Product Insights":

    st.header("📍 Regional & Product Insights")

    st.write(
        "Identify geographical delivery challenges "
        "and compare product-category performance."
    )

    tab1, tab2 = st.tabs(
        [
            "📍 Regional Heatmap",
            "📦 Product Categories"
        ]
    )

    # Area Heatmap
    with tab1:

        with st.container(border=True):

            st.plotly_chart(
                area_heatmap_chart(
                    filtered_df,
                    DARK_MODE
                ),
                width="stretch"
            )

        area_df = area_performance(filtered_df)

        slowest = area_df.loc[
            area_df["Average_Delivery_Time"].idxmax()
        ]

        st.warning(
            "📍 Area with highest average delivery time: "
            f"{slowest['Area']}"
        )

        st.dataframe(
            area_df,
            width="stretch",
            hide_index=True
        )

    # Category Boxplot
    with tab2:

        with st.container(border=True):

            st.plotly_chart(
                category_boxplot_chart(
                    filtered_df,
                    DARK_MODE
                ),
                width="stretch"
            )

        category_df = category_performance(filtered_df)

        st.subheader("Category Performance Summary")

        st.dataframe(
            category_df,
            width="stretch",
            hide_index=True
        )


# ============================================================
# 17. DATA QUALITY LAB
# ============================================================

elif page == "🧹 Data Quality Lab":

    st.header("🧹 Data Quality & Preparation")

    st.write(
        "Review dataset quality, preparation steps, "
        "and processed delivery records."
    )

    st.subheader("📊 Data Quality Overview")

    original_rows = len(raw_df)

    cleaned_rows = len(df)

    removed_rows = original_rows - cleaned_rows

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.metric(
                "Original Records",
                f"{original_rows:,}"
            )

    with col2:

        with st.container(border=True):

            st.metric(
                "Cleaned Records",
                f"{cleaned_rows:,}"
            )

    with col3:

        with st.container(border=True):

            st.metric(
                "Records Removed",
                f"{removed_rows:,}"
            )

    st.divider()

    # Cleaning Summary
    st.subheader("🧹 Cleaning Summary")

    report_df = pd.DataFrame(
        list(cleaning_report.items()),
        columns=["Metric", "Value"]
    )

    st.dataframe(
        report_df,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # Missing Values
    st.subheader("🔍 Missing Values")

    missing_df = (
        raw_df.isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Column",
        "Missing Values"
    ]

    st.dataframe(
        missing_df,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # Processing Pipeline
    st.subheader("🔄 Data Processing Pipeline")

    with st.expander(
        "View Preparation Steps",
        expanded=True
    ):

        st.write("1. Load original delivery records.")

        st.write("2. Remove duplicate records.")

        st.write("3. Handle missing categorical values.")

        st.write("4. Convert numerical columns.")

        st.write("5. Handle invalid delivery durations.")

        st.write("6. Prepare agent information.")

        st.write("7. Create agent age groups.")

        st.write("8. Calculate delivery statistics.")

        st.write(
            "9. Identify late deliveries using "
            "mean plus standard deviation."
        )

        st.write(
            "10. Prepare grouped data for visualizations."
        )

    st.divider()

    # Dataset Explorer
    st.subheader("📋 Delivery Data Explorer")

    st.dataframe(
        filtered_df,
        width="stretch"
    )

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Filtered Dataset",
        data=csv,
        file_name="logisight_delivery_data.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# 18. DASHBOARD GUIDE
# ============================================================

elif page == "📖 Dashboard Guide":

    st.header("📖 Dashboard Guide")

    st.write(
        "Explore the capabilities of LogiSight Analytics."
    )

    st.subheader("🎯 Platform Overview")

    st.info(
        "LogiSight provides interactive insights into "
        "delivery operations, fleet efficiency, "
        "operational delays, and regional performance."
    )

    with st.expander(
        "🏠 Command Center",
        expanded=True
    ):

        st.write(
            "Monitor key delivery indicators and "
            "overall operational performance."
        )

    with st.expander("🚦 Delay Intelligence"):

        st.write(
            "Compare delivery times across "
            "weather and traffic conditions."
        )

    with st.expander("🚗 Fleet & Agent Analytics"):

        st.write(
            "Compare vehicle efficiency and "
            "delivery agent performance."
        )

    with st.expander("📍 Regional & Product Insights"):

        st.write(
            "Explore area-based delivery patterns "
            "and product-category distributions."
        )

    with st.expander("🧹 Data Quality Lab"):

        st.write(
            "Review cleaning results and "
            "download filtered delivery data."
        )

    st.divider()

    st.subheader("⚙️ Interactive Controls")

    st.write(
        "Use the sidebar filters to explore delivery records "
        "by weather, traffic, vehicle, category, and area."
    )

    st.write(
        "Charts and performance indicators update "
        "automatically when filters change."
    )

    st.write(
        "Use Reset All Filters to restore "
        "the complete dataset."
    )

    st.write(
        "Switch between Dark and Light mode "
        "using the application Settings menu."
    )


# ============================================================
# 19. FOOTER
# ============================================================

st.divider()

st.caption(
    "© LogiSight Analytics | Logistics Intelligence"
)