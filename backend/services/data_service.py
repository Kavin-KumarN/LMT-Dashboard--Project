import pandas as pd
import os

UPLOAD_DIR = "frontend/uploaded_files"


# -----------------------------------
# LOAD DATA
# -----------------------------------
def load_data(file_name: str) -> pd.DataFrame:
    path = os.path.join(UPLOAD_DIR, file_name)

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {file_name}")

    if file_name.lower().endswith(".csv"):
        return pd.read_csv(path)

    if file_name.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)

    raise ValueError("Unsupported file type")


# -----------------------------------
# APPLY FILTERS (CATEGORY + NUMBER + DATE)
# -----------------------------------
def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Supported filters:
    - Categorical: {"Student": ["Ram", "Priya"]}
    - Numeric: {"Average": {"min": 40, "max": 90}}
    - Date: {"Order_Date": {"min": "2024-01-01", "max": "2024-02-01"}}
    """

    for col, condition in filters.items():
        if col not in df.columns:
            continue

        # -----------------------------
        # CATEGORICAL FILTER
        # -----------------------------
        if isinstance(condition, list):
            df = df[df[col].isin(condition)]

        # -----------------------------
        # RANGE FILTER (NUMERIC / DATE)
        # -----------------------------
        elif isinstance(condition, dict):
            series = df[col]

            # Try datetime conversion if strings detected
            if series.dtype == "object":
                converted = pd.to_datetime(series, errors="coerce")
                if converted.notna().any():
                    df[col] = converted
                    series = df[col]

            # Apply min
            if "min" in condition:
                value = condition["min"]
                value = pd.to_datetime(value, errors="coerce") if isinstance(value, str) else value
                df = df[series >= value]

            # Apply max
            if "max" in condition:
                value = condition["max"]
                value = pd.to_datetime(value, errors="coerce") if isinstance(value, str) else value
                df = df[series <= value]

    return df
