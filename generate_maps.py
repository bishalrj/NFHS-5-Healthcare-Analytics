import pandas as pd
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from dashboard.visualizations import prepare_geo_data, plot_dominant_cluster_map, plot_cluster_concentration_map

def generate_static_maps():
    df = pd.read_csv("data/processed/district_clusters.csv")
    geo_path = "geo/india_district.geojson"
    merged_gdf, geojson_data = prepare_geo_data(df, geo_path)

    # Dominant Map
    fig1 = plot_dominant_cluster_map(merged_gdf, geojson_data)
    fig1.write_html("reports/state_dominant_cluster_map.html")
    
    # Concentration Maps
    fig2 = plot_cluster_concentration_map(merged_gdf, geojson_data, 0)
    fig2.write_html("reports/state_cluster0_concentration.html")
    
    fig3 = plot_cluster_concentration_map(merged_gdf, geojson_data, 1)
    fig3.write_html("reports/state_cluster1_concentration.html")
    
    fig4 = plot_cluster_concentration_map(merged_gdf, geojson_data, 2)
    fig4.write_html("reports/state_cluster2_concentration.html")
    
    print("Static map generation complete.")

if __name__ == "__main__":
    generate_static_maps()
