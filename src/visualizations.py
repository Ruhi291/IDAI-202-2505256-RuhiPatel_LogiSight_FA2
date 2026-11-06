import colorsys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==========================================
# 1. COLOR PALETTE
# ==========================================

COLORS = [
    "#00D4FF",  # Cyan
    "#A855F7",  # Purple
    "#FF6B9A",  # Pink
    "#22C55E",  # Green
    "#F59E0B",  # Orange
    "#3B82F6",  # Blue
    "#EF4444",  # Red
    "#FACC15",  # Yellow
    "#14B8A6",  # Teal
    "#8B5CF6",  # Violet
]


def generate_colors(n):
    """
    Generate a different color for each bar.
    """

    if n <= len(COLORS):
        return COLORS[:n]

    result = []

    for i in range(n):
        hue = i / n

        r, g, b = colorsys.hsv_to_rgb(
            hue, 0.75, 0.95
        )

        result.append(
            "#{:02X}{:02X}{:02X}".format(
                int(r * 255),
                int(g * 255),
                int(b * 255)
            )
        )

    return result


# ==========================================
# 2. CHART STYLING
# ==========================================

def style_chart(fig, dark_mode=True):
    """
    Style Plotly charts for dark/light mode.
    """

    text_color = "#FFFFFF" if dark_mode else "#102A43"
    grid_color = "#243747" if dark_mode else "#E0E7EF"

    fig.update_layout(
        template="plotly_dark" if dark_mode else "plotly_white",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial",
            size=13,
            color=text_color
        ),

        title_font=dict(
            size=19,
            color=text_color
        ),

        margin=dict(
            l=30,
            r=30,
            t=70,
            b=35
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),

        hoverlabel=dict(
            bgcolor="#142537" if dark_mode else "#FFFFFF",
            font_color="#FFFFFF" if dark_mode else "#102A43"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor=grid_color,
        zeroline=False
    )

    return fig


# ==========================================
# 3. DELAY ANALYZER — COMPULSORY CHART 1
# ==========================================

def delay_analyzer_chart(df, dark_mode=True):

    delay_data = (
        df.groupby(
            ["Weather", "Traffic"],
            as_index=False
        )["Delivery_Time"]
        .mean()
    )

    delay_data["Condition"] = (
        delay_data["Weather"].astype(str)
        + " | "
        + delay_data["Traffic"].astype(str)
    )

    conditions = delay_data["Condition"].tolist()

    colors = generate_colors(len(conditions))

    color_map = dict(zip(conditions, colors))

    fig = px.bar(
        delay_data,
        x="Weather",
        y="Delivery_Time",
        color="Condition",
        barmode="group",
        color_discrete_map=color_map,

        title="Average Delivery Time by Weather and Traffic",

        labels={
            "Weather": "Weather Condition",
            "Delivery_Time": "Average Delivery Time (minutes)",
            "Condition": "Weather / Traffic"
        },

        hover_data=["Traffic"]
    )

    return style_chart(fig, dark_mode)


# ==========================================
# 4. VEHICLE COMPARISON — COMPULSORY CHART 2
# ==========================================

def vehicle_comparison_chart(df, dark_mode=True):

    vehicle_data = (
        df.groupby(
            "Vehicle",
            as_index=False
        )["Delivery_Time"]
        .mean()
        .sort_values("Delivery_Time")
    )

    vehicles = vehicle_data["Vehicle"].tolist()

    colors = generate_colors(len(vehicles))

    color_map = dict(zip(vehicles, colors))

    fig = px.bar(
        vehicle_data,
        x="Vehicle",
        y="Delivery_Time",
        color="Vehicle",
        color_discrete_map=color_map,

        title="Average Delivery Time by Vehicle Type",

        labels={
            "Vehicle": "Vehicle Type",
            "Delivery_Time": "Average Delivery Time (minutes)"
        },

        text_auto=".1f"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False
    )

    return style_chart(fig, dark_mode)


# ==========================================
# 5. AGENT PERFORMANCE — COMPULSORY CHART 3
# ==========================================

def agent_performance_chart(df, dark_mode=True):

    scatter_data = df.dropna(
        subset=[
            "Agent_Rating",
            "Agent_Age",
            "Age_Group"
        ]
    )

    fig = px.scatter(
        scatter_data,

        x="Agent_Rating",
        y="Delivery_Time",
        color="Age_Group",

        color_discrete_sequence=[
            "#00D4FF",
            "#A855F7",
            "#FF6B9A"
        ],

        opacity=0.55,

        title="Agent Rating vs Delivery Time",

        labels={
            "Agent_Rating": "Agent Rating",
            "Delivery_Time": "Delivery Time (minutes)",
            "Age_Group": "Agent Age Group"
        },

        hover_data=[
            "Agent_Age",
            "Vehicle"
        ]
    )

    fig.update_traces(
        marker=dict(size=7)
    )

    return style_chart(fig, dark_mode)


# ==========================================
# 6. AREA HEATMAP — COMPULSORY CHART 4
# ==========================================

def area_heatmap_chart(df, dark_mode=True):

    area_data = (
        df.groupby(
            "Area",
            as_index=False
        )["Delivery_Time"]
        .mean()
    )

    area_data["Metric"] = "Average Delivery Time"

    heatmap_data = area_data.pivot(
        index="Area",
        columns="Metric",
        values="Delivery_Time"
    )

    fig = px.imshow(
        heatmap_data,

        color_continuous_scale=[
            "#22C55E",
            "#FACC15",
            "#F97316",
            "#EF4444"
        ],

        aspect="auto",

        title="Average Delivery Time Across Areas",

        labels={
            "color": "Delivery Time (minutes)"
        },

        text_auto=".1f"
    )

    return style_chart(fig, dark_mode)


# ==========================================
# 7. CATEGORY BOXPLOT — COMPULSORY CHART 5
# ==========================================

def category_boxplot_chart(df, dark_mode=True):

    categories = sorted(
        df["Category"].dropna().unique().tolist()
    )

    colors = generate_colors(len(categories))

    color_map = dict(zip(categories, colors))

    fig = px.box(
        df,

        x="Category",
        y="Delivery_Time",
        color="Category",

        color_discrete_map=color_map,

        title="Delivery Time Distribution by Product Category",

        labels={
            "Category": "Product Category",
            "Delivery_Time": "Delivery Time (minutes)"
        },

        points="outliers"
    )

    fig.update_layout(
        showlegend=False
    )

    return style_chart(fig, dark_mode)