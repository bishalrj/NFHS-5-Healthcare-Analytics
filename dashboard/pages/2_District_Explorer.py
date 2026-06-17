import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_district_data, load_comparison_data

st.set_page_config(page_title="District Explorer", layout="wide")
st.title("District Explorer")

try:
    df = load_district_data()
    comp_df = load_comparison_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

cluster_names = {
    0: "High Intervention Priority Districts",
    1: "High-Cost & Specific-Risk Districts",
    2: "Healthcare Leaders"
}

cluster_descriptions = {
    0: "This cluster exhibits systemic deficits across maternal care, immunization, and nutritional indicators. High child stunting and low access to clean fuels highlight the need for comprehensive infrastructure and health campaigns.",
    1: "Districts in this cluster have relatively high education and sanitation but face high out-of-pocket public delivery costs, low institutional birth rates, and significant lifestyle risks such as tobacco consumption.",
    2: "These districts perform exceptionally well across key healthcare indicators, showing high vaccination coverage, high institutional births, and well-developed sanitation and clean energy infrastructure."
}

# Search/Select workflow
st.markdown("Search or select a district to view its healthcare profile and how it compares to national averages.")

col_search1, col_search2 = st.columns(2)
with col_search1:
    state = st.selectbox("State/UT", sorted(df['State/UT'].unique()))
with col_search2:
    state_df = df[df['State/UT'] == state]
    district = st.selectbox("District", sorted(state_df['District Names'].unique()))

district_data = state_df[state_df['District Names'] == district].iloc[0]
cluster_id = int(district_data['Cluster'])

# Display typology card
st.markdown("---")
st.subheader(f"District Profile: {district}")
c1, c2 = st.columns([1, 2])
with c1:
    st.metric(label="Assigned Typology", value=cluster_names[cluster_id])
with c2:
    st.write(f"**Typology Description:** {cluster_descriptions[cluster_id]}")

st.markdown("---")
st.subheader("Indicator Comparisons")

# Let's show a bar chart of key indicators compared to National Mean and Cluster Mean
key_indicators = [
    "Institutional births (in the 5 years before the survey) (%)",
    "Children under 5 years who are stunted (height-for-age)18 (%)",
    "Households using clean fuel for cooking3 (%)",
    "Population living in households that use an improved sanitation facility2 (%)",
    "All women age 15-49 years who are anaemic22 (%)"
]

# Get national averages (mean of df)
national_means = df[key_indicators].mean()
# Get cluster averages from comp_df
cluster_means = comp_df[f"Cluster_{cluster_id}_mean"].loc[key_indicators]
district_vals = district_data[key_indicators]

# Plotly comparison chart
fig = go.Figure()
fig.add_trace(go.Bar(
    name=district,
    x=key_indicators,
    y=district_vals,
    marker_color='#636EFA'
))
fig.add_trace(go.Bar(
    name='Cluster Average',
    x=key_indicators,
    y=cluster_means,
    marker_color='#FECB52'
))
fig.add_trace(go.Bar(
    name='National Average',
    x=key_indicators,
    y=national_means,
    marker_color='#EF553B'
))

fig.update_layout(
    barmode='group',
    title="Comparison of Key Healthcare Indicators (%)",
    xaxis_tickangle=-25,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# Also show all indicators in a clean data table
st.markdown("### All Indicators Table")
all_indicators = [c for c in df.columns if c not in ['State/UT', 'District Names', 'Cluster']]
comparison_table = pd.DataFrame({
    'Indicator': all_indicators,
    'District Value': [district_data[c] for c in all_indicators],
    'National Average': [df[c].mean() for c in all_indicators]
})
comparison_table['Difference'] = comparison_table['District Value'] - comparison_table['National Average']
st.dataframe(comparison_table.style.format({'District Value': '{:.2f}', 'National Average': '{:.2f}', 'Difference': '{:+.2f}'}), use_container_width=True, hide_index=True)
