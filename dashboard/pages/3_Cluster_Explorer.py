import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_district_data, load_comparison_data
from visualizations import plot_radar_chart, plot_grouped_bar_comparison, plot_indicator_boxplots

st.set_page_config(page_title="Cluster Explorer", layout="wide")
st.title("Cluster Explorer")

try:
    df = load_district_data()
    comp_df = load_comparison_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.markdown("---")
st.subheader("Typology Comparison (Advanced Visual Analytics)")

key_focus_indicators = [
    "Institutional births (in the 5 years before the survey) (%)",
    "Children under 5 years who are stunted (height-for-age)18 (%)",
    "Female population age 6 years and above who ever attended school (%)",
    "Households using clean fuel for cooking3 (%)",
    "Population living in households that use an improved sanitation facility2 (%)",
    "Average out-of-pocket expenditure per delivery in a public health facility (for last birth in the 5 years before the survey) (Rs.)"
]

# Create radar chart and grouped bar chart side by side
col_viz1, col_viz2 = st.columns(2)
with col_viz1:
    radar_fig = plot_radar_chart(comp_df, key_focus_indicators)
    st.plotly_chart(radar_fig, use_container_width=True)
with col_viz2:
    national_means = df[key_focus_indicators].mean()
    bar_fig = plot_grouped_bar_comparison(comp_df, national_means, key_focus_indicators)
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("### Indicator Distribution Across Clusters")
# Box plot for a selected indicator
selected_indicator = st.selectbox("Select Indicator for Distribution Analysis (Box Plot)", key_focus_indicators)
box_fig = plot_indicator_boxplots(df, selected_indicator)
st.plotly_chart(box_fig, use_container_width=True)

st.markdown("---")
st.subheader("Detailed Cluster Profiles")

# Segmented controls / tabs
tab1, tab2, tab3 = st.tabs([
    "Cluster 0: High Intervention Priority", 
    "Cluster 1: High-Cost & Specific-Risk", 
    "Cluster 2: Healthcare Leaders"
])

cluster_names = {
    0: "High Intervention Priority Districts",
    1: "High-Cost & Specific-Risk Districts",
    2: "Healthcare Leaders"
}

def render_cluster_tab(cluster_id, tab):
    with tab:
        col_m1, col_m2 = st.columns([1, 2])
        cluster_districts = df[df['Cluster'] == cluster_id]
        with col_m1:
            st.metric("Total Districts in Cluster", len(cluster_districts))
            st.metric("Percentage of National Total", f"{(len(cluster_districts)/len(df))*100:.1f}%")
        with col_m2:
            st.write(f"**Profile Overview:** This cluster contains {len(cluster_districts)} districts.")
            if cluster_id == 0:
                st.write("""
                * **Key Deficits:** High child stunting, low immunization, low access to improved sanitation, and low maternal healthcare.
                * **Priorities:** Expand direct nutrition support (PMMVY, POSHAN Abhiyaan), upgrade rural sanitation facilities (SBM), and strengthen primary healthcare outreach.
                """)
            elif cluster_id == 1:
                st.write("""
                * **Key Deficits:** High out-of-pocket public delivery cost, high tobacco consumption, lower institutional birth rates relative to education levels.
                * **Priorities:** Financial audits of public delivery charges under JSSK, state-funded delivery vouchers, community tobacco cessation programs, and encouragement of institutional deliveries.
                """)
            elif cluster_id == 2:
                st.write("""
                * **Strengths:** High vaccination, high institutional births, strong coverage of maternal and child healthcare, well-developed sanitation.
                * **Priorities:** Maintain service standards, focus on second-generation health issues (e.g., lifestyle diseases, NCD screening), and share best practices with lower-performing districts.
                """)
        
        st.markdown("---")
        st.subheader("Indicator Centroids (Cluster Mean vs National Average)")
        
        # Pull the mean columns
        indicators = list(comp_df.index)
        cluster_means = comp_df[f"Cluster_{cluster_id}_mean"]
        national_means = df[indicators].mean()
        
        # Prepare comparison table
        tab_df = pd.DataFrame({
            'Indicator': indicators,
            'Cluster Mean': cluster_means,
            'National Mean': national_means
        })
        tab_df['Difference'] = tab_df['Cluster Mean'] - tab_df['National Mean']
        
        # Sort by difference to see defining characteristics
        tab_df = tab_df.sort_values(by='Difference', key=abs, ascending=False)
        
        # Show Top 5 absolute differences
        top_diff = tab_df.head(6)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Cluster Mean',
            y=top_diff['Indicator'],
            x=top_diff['Cluster Mean'],
            orientation='h',
            marker_color='#636EFA'
        ))
        fig.add_trace(go.Bar(
            name='National Mean',
            y=top_diff['Indicator'],
            x=top_diff['National Mean'],
            orientation='h',
            marker_color='#EF553B'
        ))
        fig.update_layout(
            barmode='group',
            title="Top Distinguishing Indicators (Mean %)",
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### All Indicators Centroids and Deviations")
        st.dataframe(tab_df.style.format({
            'Cluster Mean': '{:.2f}',
            'National Mean': '{:.2f}',
            'Difference': '{:+.2f}'
        }), use_container_width=True)

render_cluster_tab(0, tab1)
render_cluster_tab(1, tab2)
render_cluster_tab(2, tab3)
