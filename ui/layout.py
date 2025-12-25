import streamlit as st

def setup_page(page_title, page_icon, layout):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout
    )
    st.title(page_title)


def show_raw_data(df, label="📄 Show Raw Data (Original File)"):
    with st.expander(label):
        st.dataframe(df.reset_index(drop=True), use_container_width=True)


def show_filtered_data(df, label="🔍 Show Filtered Data"):
    with st.expander(label):
        st.dataframe(df.reset_index(drop=True), use_container_width=True)
