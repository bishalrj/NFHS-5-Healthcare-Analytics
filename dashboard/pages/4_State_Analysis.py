import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_district_data, load_state_data
from visualizations import plot_state_stacked_bar

st.set_page_config(page_title="State Analysis", layout="wide")
st.title("State Analysis")

try:
    df = load_district_data()
    state_df = load_state_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# We want to display state-level distributions and comparisons
st.markdown("Assess the geographical concentration and distribution of healthcare typologies across different Indian States & UTs.")

st.subheader("State-Wise Cluster Composition")

col_controls1, col_controls2 = st.columns(2)
with col_controls1:
    sort_by = st.selectbox(
        "Sort States By",
        ["Total Districts", "High Intervention Priority Districts", "High-Cost & Specific-Risk Districts", "Healthcare Leaders"]
    )
with col_controls2:
    top_n = st.slider("Show Top N States/UTs", min_value=5, max_value=36, value=15)

# Render the bar chart
fig = plot_state_stacked_bar(df, top_n=top_n, sort_by=sort_by)
st.plotly_chart(fig, use_container_width=True)

# Comparison/Detailed Data Table
st.subheader("Detailed State Distribution Table")
state_cluster = df.groupby(['State/UT', 'Cluster']).size().unstack(fill_value=0).reset_index()
state_cluster.columns = ['State/UT', 'Cluster 0 (High Intervention Priority)', 'Cluster 1 (High-Cost & Specific-Risk)', 'Cluster 2 (Healthcare Leaders)']
state_cluster['Total Districts'] = state_cluster.iloc[:, 1:].sum(axis=1)

st.dataframe(state_cluster.style.format({
    'Cluster 0 (High Intervention Priority)': '{:d}',
    'Cluster 1 (High-Cost & Specific-Risk)': '{:d}',
    'Cluster 2 (Healthcare Leaders)': '{:d}',
    'Total Districts': '{:d}'
}), use_container_width=True, hide_index=True)
