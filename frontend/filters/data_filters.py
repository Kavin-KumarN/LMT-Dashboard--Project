import streamlit as st
import pandas as pd


def is_id_column(series: pd.Series) -> bool:
    return (
        series.is_unique and
        series.notna().all() and
        series.dtype.kind in "iu"
    )


def build_filters(df: pd.DataFrame):
    st.sidebar.header("🔍 Filters")
    filters = {}
    v = st.session_state.filter_version  # 🔑 version

    # ===============================
    # DATE FILTERS
    # ===============================
    date_cols = [
        c for c in df.columns
        if "date" in c.lower() or pd.api.types.is_datetime64_any_dtype(df[c])
    ]

    if date_cols:
        st.sidebar.subheader("📅 Date Filters")

        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            min_date = df[col].min()
            max_date = df[col].max()

            if pd.isna(min_date) or pd.isna(max_date):
                continue

            selected = st.sidebar.date_input(
                col,
                value=(min_date.date(), max_date.date()),
                key=f"date_{v}_{col}"
            )

            if (
                isinstance(selected, tuple)
                and len(selected) == 2
                and selected[0] is not None
                and selected[1] is not None
                and selected[0] <= selected[1]
            ):
                filters[col] = {
                    "min": selected[0].isoformat(),
                    "max": selected[1].isoformat()
                }

    # ===============================
    # CATEGORY FILTERS
    # ===============================
    st.sidebar.subheader("🏷️ Category Filters")

    for col in df.columns:
        if col in date_cols:
            continue

        if not pd.api.types.is_numeric_dtype(df[col]):
            values = df[col].dropna().unique().tolist()
            selected = st.sidebar.multiselect(
                col,
                values,
                default=values,
                key=f"cat_{v}_{col}"
            )
            filters[col] = selected

    # ===============================
    # NUMERIC FILTERS
    # ===============================
    st.sidebar.subheader("🔢 Numeric Filters")

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            min_v = float(df[col].min())
            max_v = float(df[col].max())

            selected = st.sidebar.slider(
                col,
                min_v,
                max_v,
                (min_v, max_v),
                key=f"num_{v}_{col}"
            )

            filters[col] = {
                "min": selected[0],
                "max": selected[1]
            }

    return filters
