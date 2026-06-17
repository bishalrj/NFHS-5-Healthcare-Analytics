import streamlit as st
import pandas as pd
import sys
import os

# Add root directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dashboard.visualizations import prepare_geo_data, plot_dominant_cluster_map, plot_cluster_concentration_map, CLUSTER_NAMES

st.set_page_config(page_title="Geographic Analysis", page_icon="", layout="wide")

st.title(" Geographic Intelligence Layer")
st.markdown("""
This geographic layer aggregates the 706 NFHS-5 district clusters to the state-level to provide strategic planning insights.
*Note: Due to administrative boundary changes between the GADM base map and NFHS-5 definitions, state-level aggregation provides the most robust and accurate visualization.*
""")

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/district_clusters.csv")
    geo_path = "geo/india_district.geojson"
    merged_gdf, geojson_data = prepare_geo_data(df, geo_path)
    return merged_gdf, geojson_data

try:
    merged_gdf, geojson_data = load_data()
except Exception as e:
    st.error(f"Error loading geographic data: {str(e)}")
    st.stop()

# --- A. Dominant Healthcare Typology Map ---
st.header("Dominant Healthcare Typology by State")
st.markdown("Visualizes the predominant healthcare cluster assignment for each state based on district counts.")

dom_map_fig = plot_dominant_cluster_map(merged_gdf, geojson_data)
st.plotly_chart(dom_map_fig, use_container_width=True)

# --- B. Cluster Concentration Map ---
st.header("Cluster Concentration Explorer")
st.markdown("Explore the percentage concentration of specific healthcare typologies across states.")

selected_cluster = st.selectbox(
    "Select Healthcare Typology to Visualize:",
    options=[0, 1, 2],
    format_func=lambda x: CLUSTER_NAMES[x]
)

conc_map_fig = plot_cluster_concentration_map(merged_gdf, geojson_data, selected_cluster)
st.plotly_chart(conc_map_fig, use_container_width=True)

# --- C. State Detail Explorer ---
st.header("State Detail Explorer")

col1, col2 = st.columns([1, 2])

with col1:
    selected_state = st.selectbox("Select a State:", sorted(merged_gdf['State/UT'].unique()))
    state_data = merged_gdf[merged_gdf['State/UT'] == selected_state].iloc[0]

    st.metric("Total Districts", state_data['Total'])
    st.metric("Dominant Typology", state_data['Dominant Cluster'])

with col2:
    st.subheader(f"Typology Distribution in {selected_state}")
    dist_df = pd.DataFrame({
        "Typology": [CLUSTER_NAMES[0], CLUSTER_NAMES[1], CLUSTER_NAMES[2]],
        "Count": [state_data['Cluster 0'], state_data['Cluster 1'], state_data['Cluster 2']],
        "Percentage": [f"{state_data['Cluster 0 %']:.1f}%", f"{state_data['Cluster 1 %']:.1f}%", f"{state_data['Cluster 2 %']:.1f}%"]
    })
    st.dataframe(dist_df, hide_index=True, use_container_width=True)
