import os
import pandas as pd
import streamlit as st

def upload_file(upload_dir, allowed_types=("csv", "xlsx")):
    st.subheader("📁 Upload a File")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=list(allowed_types))

    if uploaded_file:
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' uploaded successfully.")
        return uploaded_file.name
    return None


def get_saved_files(upload_dir):
    files = os.listdir(upload_dir)
    if not files:
        st.warning("No files uploaded yet.")
        st.stop()
    return files


def load_file(upload_dir, filename):
    path = os.path.join(upload_dir, filename)
    if filename.endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_excel(path)


def delete_file(upload_dir, selected_file):
    file_path = os.path.join(upload_dir, selected_file)

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if st.button("🗑️ Delete File"):
        st.session_state.confirm_delete = True

    if st.session_state.confirm_delete:
        st.warning(f"Are you sure you want to delete '{selected_file}'?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✔ Yes, Delete Permanently"):
                os.remove(file_path)
                st.session_state.confirm_delete = False
                st.success(f"File '{selected_file}' deleted successfully.")
                st.rerun()

        with col2:
            if st.button("✖ Cancel"):
                st.session_state.confirm_delete = False
                st.info("Delete cancelled.")
