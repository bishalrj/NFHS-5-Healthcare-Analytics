import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add parent directory to path so we can import utils safely
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_district_data

from visualizations import plot_cluster_distribution_donut

st.set_page_config(page_title="System Overview", layout="wide")
st.title("System Overview")

try:
    df = load_district_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Metric cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Districts Analysed", len(df))
features = [c for c in df.columns if c not in ['State/UT', 'District Names', 'Cluster']]
col2.metric("Healthcare Indicators", len(features))
col3.metric("Identified Clusters", df['Cluster'].nunique())

st.markdown("---")

# Visualizations
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("Cluster Distribution")
    fig = plot_cluster_distribution_donut(df)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Executive Summary")
    st.markdown("""
    The analytical engine has processed all districts based on indicators across 8 major domains:
    * **Demographics & Education**
    * **Maternal Care & Family Planning**
    * **Child Health & Immunization**
    * **Nutrition & Undernutrition**
    * **Water, Sanitation & Hygiene (WASH)**
    * **Lifestyle Risks (Tobacco)**
    * **Financial Protection (Insurance & OOP Expense)**

    This taxonomy enables policy planners to shift from a uniform state-level allocation to district-level precision interventions.
    """)
