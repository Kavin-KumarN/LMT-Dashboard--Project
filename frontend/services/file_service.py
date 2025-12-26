import requests
import pandas as pd
import streamlit as st

API_URL = "http://localhost:8000/api/data"
FILES_API = "http://localhost:8000/api/files"


@st.cache_data(show_spinner=False)
def get_uploaded_files():
    res = requests.get(FILES_API)
    res.raise_for_status()
    return res.json()


@st.cache_data(show_spinner=False)
def fetch_data(file_name, filters=None):
    payload = {
        "file_name": file_name,
        "filters": filters or {}
    }

    res = requests.post(API_URL, json=payload)
    res.raise_for_status()
    return pd.DataFrame(res.json())
