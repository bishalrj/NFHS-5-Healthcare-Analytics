import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLOR_MAP = {
    0: "#EF553B", # High Intervention Priority
    1: "#FECB52", # High-Cost & Specific-Risk
    2: "#636EFA", # Healthcare Leaders
    "High Intervention Priority Districts": "#EF553B",
    "High-Cost & Specific-Risk Districts": "#FECB52",
    "Healthcare Leaders": "#636EFA"
}

CLUSTER_NAMES = {
    0: "High Intervention Priority Districts",
    1: "High-Cost & Specific-Risk Districts",
    2: "Healthcare Leaders"
}

def plot_cluster_distribution_donut(df: pd.DataFrame):
    """Generates a donut chart for cluster distribution."""
    counts = df['Cluster'].value_counts().reset_index()
    counts.columns = ['Cluster ID', 'Number of Districts']
    counts['Cluster Name'] = counts['Cluster ID'].map(CLUSTER_NAMES)
    
    fig = px.pie(
        counts, 
        values='Number of Districts', 
        names='Cluster Name',
        color='Cluster Name',
        color_discrete_map=COLOR_MAP,
        hole=0.5,
        title="District Distribution by Healthcare Typology"
    )
    fig.update_traces(textinfo='percent+value', textfont_size=14)
    fig.update_layout(
        showlegend=True, 
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=40, b=0, l=0, r=0),
        font=dict(family="Arial, sans-serif", size=14)
    )
    return fig

def plot_radar_chart(comp_df: pd.DataFrame, indicators: list):
    """Generates a radar chart comparing the 3 clusters across given indicators."""
    fig = go.Figure()
    
    for cluster_id in [0, 1, 2]:
        means = comp_df.loc[indicators, f"Cluster_{cluster_id}_mean"].values
        # Add the first value to the end to close the radar loop
        means = list(means) + [means[0]]
        theta = indicators + [indicators[0]]
        
        # Format labels for radar (truncate if too long)
        theta_labels = [label[:25] + "..." if len(label) > 25 else label for label in theta]
        
        fig.add_trace(go.Scatterpolar(
            r=means,
            theta=theta_labels,
            fill='toself',
            name=CLUSTER_NAMES[cluster_id],
            line_color=COLOR_MAP[cluster_id],
            opacity=0.7
        ))
        
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        title="Multidimensional Cluster Profile Comparison",
        font=dict(family="Arial, sans-serif")
    )
    return fig

def plot_indicator_boxplots(df: pd.DataFrame, indicator: str):
    """Generates box plots for a specific indicator to show cluster differentiation."""
    plot_df = df.copy()
    plot_df['Typology'] = plot_df['Cluster'].map(CLUSTER_NAMES)
    
    fig = px.box(
        plot_df, 
        x='Typology', 
        y=indicator, 
        color='Typology',
        color_discrete_map=COLOR_MAP,
        title=f"Distribution of: {indicator}",
        points="all" # Shows underlying data points
    )
    fig.update_layout(
        xaxis_title="", 
        yaxis_title="Value (%)",
        showlegend=False,
        font=dict(family="Arial, sans-serif", size=12)
    )
    return fig

def plot_grouped_bar_comparison(comp_df: pd.DataFrame, national_means: pd.Series, indicators: list):
    """Generates a grouped bar chart for detailed indicator comparison."""
    fig = go.Figure()
    
    for cluster_id in [0, 1, 2]:
        vals = comp_df.loc[indicators, f"Cluster_{cluster_id}_mean"].values
        fig.add_trace(go.Bar(
            name=CLUSTER_NAMES[cluster_id],
            x=indicators,
            y=vals,
            marker_color=COLOR_MAP[cluster_id]
        ))
        
    # Add National Average
    fig.add_trace(go.Bar(
        name='National Average',
        x=indicators,
        y=national_means[indicators].values,
        marker_color='#333333',
        opacity=0.6
    ))
    
    fig.update_layout(
        barmode='group',
        title="Key Indicator Comparison across Typologies",
        xaxis_tickangle=-30,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Arial, sans-serif")
    )
    return fig

def plot_state_stacked_bar(df: pd.DataFrame, top_n: int = 15, sort_by: str = 'Total Districts'):
    """Generates a stacked bar chart for state-wise cluster concentration."""
    state_cluster = df.groupby(['State/UT', 'Cluster']).size().unstack(fill_value=0).reset_index()
    state_cluster.columns = ['State/UT', CLUSTER_NAMES[0], CLUSTER_NAMES[1], CLUSTER_NAMES[2]]
    state_cluster['Total Districts'] = state_cluster.iloc[:, 1:].sum(axis=1)
    
    if sort_by == "Total Districts":
        state_cluster = state_cluster.sort_values(by='Total Districts', ascending=False)
    else:
        state_cluster = state_cluster.sort_values(by=sort_by, ascending=False)
        
    sorted_states = state_cluster['State/UT'].head(top_n).tolist()
    
    melted = state_cluster.melt(
        id_vars=['State/UT', 'Total Districts'],
        value_vars=[CLUSTER_NAMES[0], CLUSTER_NAMES[1], CLUSTER_NAMES[2]],
        var_name='Typology',
        value_name='Count'
    )
    
    plot_data = melted[melted['State/UT'].isin(sorted_states)]
    
    fig = px.bar(
        plot_data,
        x='State/UT',
        y='Count',
        color='Typology',
        color_discrete_map=COLOR_MAP,
        title=f"Geographical Concentration: Top {top_n} States/UTs",
        category_orders={'State/UT': sorted_states}
    )
    fig.update_layout(
        xaxis_tickangle=-45, barmode='stack',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Arial, sans-serif")
    )
    return fig

def prepare_geo_data(df: pd.DataFrame, geojson_path: str):
    import geopandas as gpd
    import json
    
    # Load GeoJSON
    gdf = gpd.read_file(geojson_path)
    
    # Map NFHS State names to GeoJSON State names
    state_mapping = {
        'andaman & nicobar islands': 'Andaman and Nicobar',
        'dadra and nagar haveli & daman and diu': 'Dadra and Nagar Haveli',
        'jammu & kashmir': 'Jammu and Kashmir',
        'ladakh': 'Jammu and Kashmir',
        'maharastra': 'Maharashtra',
        'nct of delhi': 'Delhi',
        'odisha': 'Orissa',
        'telangana': 'Andhra Pradesh',
        'uttarakhand': 'Uttarancahal'
    }
    
    # Group NFHS data by state
    state_cluster = df.groupby(['State/UT', 'Cluster']).size().unstack(fill_value=0)
    state_cluster.columns = ['Cluster 0', 'Cluster 1', 'Cluster 2']
    state_cluster['Total'] = state_cluster.sum(axis=1)
    state_cluster['Cluster 0 %'] = (state_cluster['Cluster 0'] / state_cluster['Total']) * 100
    state_cluster['Cluster 1 %'] = (state_cluster['Cluster 1'] / state_cluster['Total']) * 100
    state_cluster['Cluster 2 %'] = (state_cluster['Cluster 2'] / state_cluster['Total']) * 100
    
    # Determine dominant cluster
    state_cluster['Dominant Cluster ID'] = state_cluster[['Cluster 0', 'Cluster 1', 'Cluster 2']].idxmax(axis=1).str.extract('(\d+)').astype(int)
    state_cluster['Dominant Cluster'] = state_cluster['Dominant Cluster ID'].map(CLUSTER_NAMES)
    
    # Create mapped name column for joining
    state_cluster['Geo_State'] = state_cluster.index.str.strip().str.lower().map(lambda x: state_mapping.get(x, x.title()))
    # Fix the .title() behavior for states that didn't need mapping
    state_cluster['Geo_State'] = state_cluster.index.to_series().replace({k.title(): v for k, v in state_mapping.items()})
    state_cluster['Geo_State'] = state_cluster.index.map(lambda x: state_mapping.get(x.lower().strip(), x.title()))
    
    # Dissolve GeoJSON to State level
    gdf['Geo_State_Join'] = gdf['NAME_1'].str.strip().str.title()
    # Apply some manual fixes for GeoJSON states to match title case perfectly
    gdf_state = gdf.dissolve(by='Geo_State_Join').reset_index()
    
    # Merge
    merged = gdf_state.merge(state_cluster.reset_index(), left_on='Geo_State_Join', right_on='Geo_State', how='inner')
    
    return merged, json.loads(gdf_state.to_json())

def plot_dominant_cluster_map(merged_gdf, geojson_data):
    fig = px.choropleth(
        merged_gdf,
        geojson=geojson_data,
        locations='Geo_State_Join',
        featureidkey='properties.Geo_State_Join',
        color='Dominant Cluster',
        color_discrete_map=COLOR_MAP,
        hover_name='State/UT',
        hover_data={
            'Geo_State_Join': False,
            'Total': True,
            'Cluster 0': True,
            'Cluster 1': True,
            'Cluster 2': True
        },
        title="Dominant Healthcare Typology by State"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

def plot_cluster_concentration_map(merged_gdf, geojson_data, cluster_id: int):
    cluster_col = f'Cluster {cluster_id} %'
    cluster_name = CLUSTER_NAMES[cluster_id]
    
    fig = px.choropleth(
        merged_gdf,
        geojson=geojson_data,
        locations='Geo_State_Join',
        featureidkey='properties.Geo_State_Join',
        color=cluster_col,
        color_continuous_scale="Reds" if cluster_id == 0 else "Oranges" if cluster_id == 1 else "Blues",
        hover_name='State/UT',
        hover_data={
            'Geo_State_Join': False,
            'Total': True,
            cluster_col: ':.1f',
        },
        title=f"Concentration of {cluster_name}"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig
