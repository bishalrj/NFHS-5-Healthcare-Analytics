import geopandas as gpd

file_path = 'geo/india_district.geojson'
try:
    gdf = gpd.read_file(file_path)
    
    print("=== GEOJSON ANALYSIS ===")
    print(f"1. Number of records: {len(gdf)}")
    print(f"2. All column names: {list(gdf.columns)}")
    
    # Try to find the district name column (usually named 'district', 'dist', 'name', 'dt_name')
    # Try to find state name column (usually 'state', 'st_name')
    
    print("\n3. First 5 district names (guessing column):")
    dist_cols = [c for c in gdf.columns if 'dist' in c.lower() or 'dt' in c.lower() or 'name' in c.lower()]
    if dist_cols:
        print(f"Using column '{dist_cols[0]}':")
        for val in gdf[dist_cols[0]].head(5):
            print(f" - {val}")
    else:
        print("Could not identify district column.")
        
    print("\n4. First 5 state names (guessing column):")
    st_cols = [c for c in gdf.columns if 'stat' in c.lower() or 'st' in c.lower()]
    if st_cols:
        print(f"Using column '{st_cols[0]}':")
        for val in gdf[st_cols[0]].head(5):
            print(f" - {val}")
    else:
        print("Could not identify state column.")
        
except Exception as e:
    print(f"Error loading GeoJSON: {e}")
