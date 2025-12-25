import streamlit as st
from config.settings import UPLOAD_DIR
from ui.layout import setup_page, show_raw_data, show_filtered_data
from services.file_service import upload_file, get_saved_files, load_file, delete_file
from filters.data_filters import apply_filters
from charts.charts import chart_section

def main():
    setup_page("Dashboard Project", "📊", "wide")

    upload_file(UPLOAD_DIR)

    files = get_saved_files(UPLOAD_DIR)
    selected_file = st.selectbox("Select file", files)
    delete_file(UPLOAD_DIR, selected_file)

    df = load_file(UPLOAD_DIR, selected_file)
    show_raw_data(df)

    filtered_df = apply_filters(df)
    show_filtered_data(filtered_df)

    chart_section(filtered_df)

if __name__ == "__main__":
    main()
