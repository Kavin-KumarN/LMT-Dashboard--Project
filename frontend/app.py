import streamlit as st
import requests
import pandas as pd

from ui.layout import page_header
from services.file_service import get_uploaded_files, fetch_data
from filters.data_filters import build_filters
from charts.charts import chart_section

if "filter_version" not in st.session_state:
    st.session_state.filter_version = 0

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def normalize_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == object:
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notna().sum() > 0:
                df[col] = converted
    return df


# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
st.session_state.setdefault("uploaded", False)
st.session_state.setdefault("selected_file", None)
st.session_state.setdefault("confirm_delete", False)
st.session_state.setdefault("filters", {})


# -------------------------------------------------
# PAGE SETUP
# -------------------------------------------------
page_header()


# -------------------------------------------------
# UPLOAD SECTION
# -------------------------------------------------
st.subheader("📤 Upload File")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file and not st.session_state.uploaded:
    response = requests.post(
        "http://localhost:8000/api/upload",
        files={"file": uploaded_file}
    )

    if response.status_code == 200:
        st.success("File uploaded successfully")
        st.session_state.uploaded = True
        st.session_state.selected_file = uploaded_file.name
        st.cache_data.clear()
        st.rerun()
    else:
        st.error("Upload failed")


# -------------------------------------------------
# FILE LIST
# -------------------------------------------------
files = get_uploaded_files()

if not files:
    st.warning("No uploaded files found.")
    st.stop()


# -------------------------------------------------
# FILE SELECTION
# -------------------------------------------------
st.subheader("📂 Select a File")

selected_file = st.selectbox(
    "Choose a file",
    files,
    index=files.index(st.session_state.selected_file)
    if st.session_state.selected_file in files else 0
)

if selected_file != st.session_state.selected_file:
    st.session_state.uploaded = False

st.session_state.selected_file = selected_file


# -------------------------------------------------
# DELETE FILE
# -------------------------------------------------
if st.button("🗑️ Delete Selected File"):
    st.session_state.confirm_delete = True

if st.session_state.confirm_delete:
    st.warning(f"Are you sure you want to delete '{selected_file}'?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✔ Yes, Delete Permanently"):
            res = requests.delete(
                f"http://localhost:8000/api/files/{selected_file}"
            )

            if res.status_code == 200:
                st.success("File deleted successfully")
                st.session_state.confirm_delete = False
                st.session_state.selected_file = None
                st.session_state.uploaded = False
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Failed to delete file")

    with col2:
        if st.button("✖ Cancel"):
            st.session_state.confirm_delete = False


# -------------------------------------------------
# LOAD RAW DATA
# -------------------------------------------------
base_df = fetch_data(selected_file)
base_df = normalize_numeric_columns(base_df)

if base_df.empty:
    st.warning("No data available.")
    st.stop()


# -------------------------------------------------
# RESET FILTERS (FIXED)
# -------------------------------------------------
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.filters = {}
    st.session_state.filter_version += 1
    st.rerun()

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
filters = build_filters(base_df)
st.session_state.filters = filters


# -------------------------------------------------
# FILTERED DATA
# -------------------------------------------------
df = fetch_data(selected_file, filters)
df = normalize_numeric_columns(df)


# -------------------------------------------------
# DATA PREVIEW
# -------------------------------------------------
with st.expander("📄 Show Raw Data (Original File)"):
    st.dataframe(base_df, use_container_width=True)

with st.expander("🔍 Show Filtered Data"):
    st.dataframe(df, use_container_width=True)


# -------------------------------------------------
# CHARTS
# -------------------------------------------------
chart_section(df)


# -------------------------------------------------
# FOOTNOTE
# -------------------------------------------------
st.warning(
    "Upload cleaned CSV or Excel files. "
    "Mixed data types or empty cells may affect chart rendering."
)
