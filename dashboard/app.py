import streamlit as st

st.set_page_config(
    page_title="NFHS-5 Healthcare Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("NFHS-5 Healthcare Analytics and District-Level Planning System")

st.markdown("""
This executive decision-support system is built to assist healthcare administrators and public health researchers in identifying district-level disparities and planning targeted interventions across India.

Using data from the National Family Health Survey (NFHS-5), the system segments 706 districts into three distinct healthcare development typologies based on 16 multidimensional indicators.

### Structure of the Dashboard
Please select a module from the sidebar to begin:
* **Overview:** System-level statistics, project background, and global cluster distribution.
* **District Explorer:** Deep dive into individual districts to examine specific indicators, comparisons, and cluster membership.
* **Cluster Explorer:** Review the distinct demographic, infrastructure, maternal, and child health profiles that define each cluster.
* **State Analysis:** Examine the macro-regional and state-level concentration of clusters to identify wider systemic patterns.
""")
