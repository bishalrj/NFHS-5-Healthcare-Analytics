import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_district_data() -> pd.DataFrame:
    path = "data/processed/district_clusters.csv"
    if not os.path.exists(path):
        path = "../data/processed/district_clusters.csv"
    return pd.read_csv(path)

@st.cache_data
def load_state_data() -> pd.DataFrame:
    path = "reports/state_cluster_distribution.csv"
    if not os.path.exists(path):
        path = "../reports/state_cluster_distribution.csv"
    df = pd.read_csv(path)
    if df.columns[0] != 'State/UT':
        df = df.rename(columns={df.columns[0]: 'State/UT'})
    return df

@st.cache_data
def load_comparison_data() -> pd.DataFrame:
    path = "reports/cluster_comparison_table.csv"
    if not os.path.exists(path):
        path = "../reports/cluster_comparison_table.csv"
    return pd.read_csv(path, index_col=0)
