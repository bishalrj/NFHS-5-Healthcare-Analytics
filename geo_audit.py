import geopandas as gpd
import pandas as pd

def main():
    # Load data
    geo_path = "geo/india_district.geojson"
    nfhs_path = "data/processed/district_clusters.csv"
    
    gdf = gpd.read_file(geo_path)
    df = pd.read_csv(nfhs_path)
    
    total_geo = len(gdf)
    total_nfhs = len(df)
    
    # Extract names
    # Assuming from previous step: NAME_2 is district, NAME_1 is state for GeoJSON
    # NFHS: District Names, State/UT
    geo_districts = set(gdf['NAME_2'].str.strip().str.lower().dropna())
    nfhs_districts = set(df['District Names'].str.strip().str.lower().dropna())
    
    # Exact match count
    exact_matches = geo_districts.intersection(nfhs_districts)
    num_matches = len(exact_matches)
    match_pct = (num_matches / total_nfhs) * 100
    
    # Unmatched
    unmatched_nfhs = list(nfhs_districts - geo_districts)
    unmatched_geo = list(geo_districts - nfhs_districts)
    
    unmatched_nfhs.sort()
    unmatched_geo.sort()
    
    # Quality assessment
    if match_pct > 90:
        quality = "Excellent"
    elif match_pct >= 80:
        quality = "Good"
    elif match_pct >= 60:
        quality = "Moderate"
    else:
        quality = "Poor"
        
    # Write Audit CSV
    # Re-extract with original cases for CSV
    geo_df = pd.DataFrame({'GeoJSON_District': sorted(list(gdf['NAME_2'].dropna().unique()))})
    nfhs_df = pd.DataFrame({'NFHS_District': sorted(list(df['District Names'].dropna().unique()))})
    geo_df['lower_name'] = geo_df['GeoJSON_District'].str.strip().str.lower()
    nfhs_df['lower_name'] = nfhs_df['NFHS_District'].str.strip().str.lower()
    
    audit_df = pd.merge(nfhs_df, geo_df, on='lower_name', how='outer', indicator=True)
    audit_df.to_csv('reports/district_matching_audit.csv', index=False)
    
    # Write Summary Markdown
    with open('reports/district_matching_summary.md', 'w') as f:
        f.write("## GeoJSON Summary\n\n")
        f.write(f"- **Total geographic records:** {total_geo}\n")
        f.write(f"- **GeoJSON column names:** {', '.join(gdf.columns)}\n")
        f.write("- **District name column:** NAME_2\n")
        f.write("- **State name column:** NAME_1\n\n")
        
        f.write("## Matching Statistics\n\n")
        f.write(f"- **Total GeoJSON districts:** {total_geo}\n")
        f.write(f"- **Total NFHS districts:** {total_nfhs}\n")
        f.write(f"- **Number of exact matches:** {num_matches}\n")
        f.write(f"- **Match percentage:** {match_pct:.1f}%\n")
        f.write(f"- **Quality Assessment:** {quality}\n\n")
        
        f.write("## Unmatched Districts (NFHS Only)\n\n")
        f.write("First 20:\n")
        for d in unmatched_nfhs[:20]:
            f.write(f"- {d.title()}\n")
        f.write("\n")
        
        f.write("## Unmatched Districts (GeoJSON Only)\n\n")
        f.write("First 20:\n")
        for d in unmatched_geo[:20]:
            f.write(f"- {d.title()}\n")
        f.write("\n")
        
        f.write("## Final Recommendation\n\n")
        if quality in ["Excellent", "Good"]:
            f.write("District-level choropleth maps can be built immediately with minimal fixing.\n")
        else:
            f.write("District-level choropleth maps CANNOT be built immediately due to poor exact string matching.\n")
            
        f.write("District name harmonization is required (likely due to spelling variations, newly formed districts, or differing naming conventions between GADM and NFHS-5).\n")
        f.write("Estimated effort required for harmonization: Medium-to-High. It will require building a fuzzy matching pipeline or manual dictionary mapping for the missing entities.")

if __name__ == "__main__":
    main()
