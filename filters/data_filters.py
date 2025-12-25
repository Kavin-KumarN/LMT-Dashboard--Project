import pandas as pd
import streamlit as st

def apply_filters(df):
    st.sidebar.header("Filter Data")
    filtered = df.copy()

    # -------------------------------------------------
    # 1. DATE FILTER
    # -------------------------------------------------
    date_cols = [col for col in df.columns if "date" in col.lower()]

    if date_cols:
        st.sidebar.subheader("📅 Date Filter")

        date_col = date_cols[0]
        filtered[date_col] = pd.to_datetime(filtered[date_col], errors="coerce")

        min_date = filtered[date_col].min().date()
        max_date = filtered[date_col].max().date()

        start, end = st.sidebar.date_input(
            "Select Date Range",
            (min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        filtered = filtered[
            (filtered[date_col].dt.date >= start) &
            (filtered[date_col].dt.date <= end)
        ]

    # -------------------------------------------------
    # 2. CATEGORICAL FILTERS
    # -------------------------------------------------
    categorical_cols = [
        col for col in df.columns
        if col not in date_cols and not pd.api.types.is_numeric_dtype(df[col])
    ]

    if categorical_cols:
        st.sidebar.subheader("🏷️ Categorical Filters")

        for col in categorical_cols:
            values = df[col].dropna().unique()
            selected = st.sidebar.multiselect(
                f"{col}",
                values,
                default=values
            )
            filtered = filtered[filtered[col].isin(selected)]

    # -------------------------------------------------
    # 3. NUMERIC FILTERS
    # -------------------------------------------------
    numeric_cols = [
        col for col in df.select_dtypes(include="number").columns
        if col not in date_cols
    ]

    if numeric_cols:
        st.sidebar.subheader("🔢 Numeric Filters")

        for col in numeric_cols:
            min_v, max_v = float(df[col].min()), float(df[col].max())
            sel_min, sel_max = st.sidebar.slider(
                f"{col}",
                min_v,
                max_v,
                (min_v, max_v)
            )
            filtered = filtered[
                (filtered[col] >= sel_min) &
                (filtered[col] <= sel_max)
            ]

    return filtered
