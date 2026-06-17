import geopandas as gpd
import pandas as pd

def main():
    gdf = gpd.read_file('geo/india_district.geojson')
    df = pd.read_csv('reports/state_cluster_distribution.csv')
    
    nfhs_states = set(df.iloc[:, 0].str.strip().str.lower().dropna())
    geo_states = set(gdf['NAME_1'].str.strip().str.lower().dropna())
    
    match = nfhs_states.intersection(geo_states)
    unmatched_nfhs = nfhs_states - geo_states
    unmatched_geo = geo_states - nfhs_states
    
    print(f"Total NFHS States: {len(nfhs_states)}")
    print(f"Total GeoJSON States: {len(geo_states)}")
    print(f"Exact Matches: {len(match)}")
    
    print("\nUnmatched NFHS States:")
    for s in sorted(list(unmatched_nfhs)):
        print(s)
        
    print("\nUnmatched GeoJSON States:")
    for s in sorted(list(unmatched_geo)):
        print(s)

if __name__ == '__main__':
    main()
