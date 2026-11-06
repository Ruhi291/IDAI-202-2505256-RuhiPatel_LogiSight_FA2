import pandas as pd


# ==========================================
# 1. CALCULATE DASHBOARD KPI METRICS
# ==========================================

def calculate_metrics(df):
    """
    Calculate key performance indicators
    using the selected delivery records.
    """

    if df.empty:
        return {
            "total_deliveries": 0,
            "average_delivery_time": 0,
            "late_delivery_percentage": 0,
            "average_agent_rating": 0,
        }

    total_deliveries = len(df)

    average_delivery_time = df["Delivery_Time"].mean()

    late_delivery_percentage = (
        df["Late_Delivery"].mean() * 100
    )

    average_agent_rating = df["Agent_Rating"].mean()

    return {
        "total_deliveries": total_deliveries,
        "average_delivery_time": average_delivery_time,
        "late_delivery_percentage": late_delivery_percentage,
        "average_agent_rating": average_agent_rating,
    }


# ==========================================
# 2. CALCULATE PERFORMANCE BY WEATHER
# ==========================================

def weather_performance(df):

    return (
        df.groupby("Weather", as_index=False)
        .agg(
            Average_Delivery_Time=("Delivery_Time", "mean"),
            Total_Deliveries=("Delivery_Time", "count"),
            Late_Percentage=("Late_Delivery", "mean"),
        )
        .assign(
            Late_Percentage=lambda x: x["Late_Percentage"] * 100
        )
    )


# ==========================================
# 3. CALCULATE PERFORMANCE BY TRAFFIC
# ==========================================

def traffic_performance(df):

    return (
        df.groupby("Traffic", as_index=False)
        .agg(
            Average_Delivery_Time=("Delivery_Time", "mean"),
            Total_Deliveries=("Delivery_Time", "count"),
            Late_Percentage=("Late_Delivery", "mean"),
        )
        .assign(
            Late_Percentage=lambda x: x["Late_Percentage"] * 100
        )
    )


# ==========================================
# 4. CALCULATE PERFORMANCE BY VEHICLE
# ==========================================

def vehicle_performance(df):

    return (
        df.groupby("Vehicle", as_index=False)
        .agg(
            Average_Delivery_Time=("Delivery_Time", "mean"),
            Total_Deliveries=("Delivery_Time", "count"),
        )
    )


# ==========================================
# 5. CALCULATE PERFORMANCE BY AREA
# ==========================================

def area_performance(df):

    return (
        df.groupby("Area", as_index=False)
        .agg(
            Average_Delivery_Time=("Delivery_Time", "mean"),
            Total_Deliveries=("Delivery_Time", "count"),
        )
    )


# ==========================================
# 6. CALCULATE PERFORMANCE BY CATEGORY
# ==========================================

def category_performance(df):

    return (
        df.groupby("Category", as_index=False)
        .agg(
            Average_Delivery_Time=("Delivery_Time", "mean"),
            Total_Deliveries=("Delivery_Time", "count"),
        )
    )