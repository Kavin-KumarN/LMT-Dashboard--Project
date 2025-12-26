import streamlit as st
import altair as alt
import plotly.express as px


# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def is_id_column(series):
    return (
        series.is_unique and
        series.notna().all() and
        series.dtype.kind in "iu"
    )


def validate_axes(df, x, y):
    if x == y:
        st.error("X-axis and Y-axis cannot be the same column.")
        return False
    if x not in df.columns or y not in df.columns:
        st.error("Selected columns are not available.")
        return False
    return True


def get_label_angle(series, threshold=10):
    """
    Tilt labels only if values are long
    """
    try:
        max_len = series.astype(str).map(len).max()
        return -30 if max_len > threshold else 0
    except Exception:
        return 0


def build_altair_chart(df, x, y, chart_type):
    label_angle = get_label_angle(df[x])

    base = (
        alt.Chart(df)
        .encode(
            x=alt.X(
                x,
                sort=None,
                axis=alt.Axis(
                    labelAngle=label_angle,
                    labelOverlap=False
                )
            ),
            y=y,
            tooltip=df.columns.tolist()
        )
        .properties(height=420)
        .interactive()
    )

    if chart_type == "Line":
        return base.mark_line()
    if chart_type == "Bar":
        return base.mark_bar()
    if chart_type == "Area":
        return base.mark_area()
    if chart_type == "Scatter":
        return base.mark_circle(size=60)

    return None


# -------------------------------------------------
# CHART SECTION
# -------------------------------------------------
def chart_section(df):
    st.subheader("📊 Charts")

    all_cols = df.columns.tolist()

    numeric_cols = [
        c for c in df.select_dtypes(include="number").columns
        if not is_id_column(df[c])
    ]

    if not numeric_cols:
        st.warning("No valid numeric columns available for charts.")
        return

    # -------- Chart Type Selector --------
    chart_type = st.radio(
        "Chart Type",
        ["Line", "Bar", "Area", "Scatter", "Pie"],
        horizontal=True
    )

    # -------- Axis Controls --------
    if chart_type == "Pie":
        categorical_cols = [c for c in all_cols if c not in numeric_cols]

        if not categorical_cols:
            st.warning("No categorical columns available for pie chart.")
            return

        category = st.selectbox(
            "Category",
            categorical_cols,
            key="pie_category"
        )

        fig = px.pie(df, names=category)
        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            "⬇ Download Pie Chart (PNG)",
            fig.to_image(format="png"),
            file_name="pie_chart.png"
        )

    else:
        col1, col2 = st.columns(2)

        with col1:
            x = st.selectbox("X-axis", all_cols, key="x_axis")

        with col2:
            y_options = [c for c in numeric_cols if c != x]
            y = st.selectbox("Y-axis", y_options, key="y_axis")

        if validate_axes(df, x, y):
            chart = build_altair_chart(df, x, y, chart_type)
            st.altair_chart(chart, use_container_width=True)

            st.download_button(
                "⬇ Download Chart (Vega JSON)",
                chart.to_json(),
                file_name=f"{chart_type.lower()}_chart.json"
            )
