import pandas as pd
from pathlib import Path


# ==========================================
# 1. DATASET PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Last mile Delivery Data.csv"


# ==========================================
# 2. LOAD DATASET
# ==========================================

def load_data():

    """
    Loads the original last-mile delivery dataset.
    """

    df = pd.read_csv(DATA_PATH)

    return df


# ==========================================
# 3. CLEAN DATASET
# ==========================================

def clean_data(df):

    """
    Cleans the delivery dataset and
    prepares it for dashboard analysis.
    """

    df = df.copy()

    original_rows = len(df)

    # --------------------------------------
    # REMOVE DUPLICATE RECORDS
    # --------------------------------------

    df = df.drop_duplicates()

    duplicates_removed = original_rows - len(df)

    # --------------------------------------
    # CLEAN TEXT COLUMNS
    # --------------------------------------

    categorical_columns = [
        "Weather",
        "Traffic",
        "Vehicle",
        "Area",
        "Category"
    ]

    for col in categorical_columns:

        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
        )

        df[col] = df[col].replace(
            {
                "": pd.NA,
                "NaN": pd.NA,
                "nan": pd.NA
            }
        )

        df[col] = df[col].fillna("Unknown")

    # Standardize the area spelling
    df["Area"] = df["Area"].replace(
        {
            "Metropolitian": "Metropolitan"
        }
    )

    # Standardize vehicle names
    df["Vehicle"] = df["Vehicle"].str.title()

    # --------------------------------------
    # CONVERT NUMERICAL COLUMNS
    # --------------------------------------

    numeric_columns = [
        "Agent_Age",
        "Agent_Rating",
        "Delivery_Time"
    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # --------------------------------------
    # HANDLE INVALID DELIVERY TIMES
    # --------------------------------------

    before_invalid_removal = len(df)

    df = df[
        df["Delivery_Time"].notna()
        & (df["Delivery_Time"] > 0)
    ].copy()

    invalid_delivery_rows = (
        before_invalid_removal - len(df)
    )

    # --------------------------------------
    # HANDLE INVALID AGENT AGES
    # --------------------------------------

    df.loc[
        ~df["Agent_Age"].between(18, 100),
        "Agent_Age"
    ] = pd.NA

    # --------------------------------------
    # HANDLE INVALID AGENT RATINGS
    # --------------------------------------

    df.loc[
        ~df["Agent_Rating"].between(1, 5),
        "Agent_Rating"
    ] = pd.NA

    # --------------------------------------
    # FILL MISSING NUMERICAL VALUES
    # --------------------------------------

    for col in ["Agent_Age", "Agent_Rating"]:

        median_value = df[col].median()

        if pd.notna(median_value):

            df[col] = df[col].fillna(
                median_value
            )

    # --------------------------------------
    # CONVERT DATE COLUMN
    # --------------------------------------

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    # --------------------------------------
    # CREATE AGENT AGE GROUPS
    # --------------------------------------

    df["Age_Group"] = pd.cut(
        df["Agent_Age"],

        bins=[
            0,
            25,
            40,
            float("inf")
        ],

        labels=[
            "Under 25",
            "25-39",
            "40+"
        ],

        right=False
    )

    # --------------------------------------
    # CREATE LATE DELIVERY INDICATOR
    # --------------------------------------

    average_time = df["Delivery_Time"].mean()

    std_time = df["Delivery_Time"].std()

    if pd.isna(std_time):
        std_time = 0

    late_threshold = average_time + std_time

    df["Late_Delivery"] = (
        df["Delivery_Time"] > late_threshold
    )

    # --------------------------------------
    # DATA CLEANING SUMMARY
    # --------------------------------------

    cleaning_report = {

        "Original Rows": original_rows,

        "Cleaned Rows": len(df),

        "Duplicates Removed": duplicates_removed,

        "Invalid Delivery Rows Removed": invalid_delivery_rows,

        "Average Delivery Time": average_time,

        "Late Delivery Threshold": late_threshold,

        "Late Delivery Percentage":
            df["Late_Delivery"].mean() * 100
    }

    return df, cleaning_report


# ==========================================
# 4. GROUP DATA FOR VISUALIZATIONS
# ==========================================

def prepare_grouped_data(df):

    """
    Prepares grouped data for the
    compulsory dashboard visualizations.
    """

    weather_traffic = (
        df.groupby(
            ["Weather", "Traffic"],
            as_index=False
        )["Delivery_Time"]
        .mean()
    )

    vehicle_performance = (
        df.groupby(
            "Vehicle",
            as_index=False
        )["Delivery_Time"]
        .mean()
    )

    area_performance = (
        df.groupby(
            "Area",
            as_index=False
        )["Delivery_Time"]
        .mean()
    )

    category_performance = (
        df.groupby(
            "Category",
            as_index=False
        )["Delivery_Time"]
        .mean()
    )

    return {
        "weather_traffic": weather_traffic,
        "vehicle": vehicle_performance,
        "area": area_performance,
        "category": category_performance
    }


# ==========================================
# 5. TEST DATA PROCESSING
# ==========================================

if __name__ == "__main__":

    print("\nLoading dataset...")

    raw_df = load_data()

    print("Original Dataset Shape:", raw_df.shape)

    print("\nCleaning dataset...")

    cleaned_df, report = clean_data(raw_df)

    print("\nDATA CLEANING REPORT")

    for key, value in report.items():

        print(f"{key}: {value}")

    print("\nCLEANED DATASET SHAPE")

    print(cleaned_df.shape)

    print("\nPREVIEW OF CLEANED DATA")

    print(cleaned_df.head())

    print("\nDATA PREPROCESSING COMPLETED!")