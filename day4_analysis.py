import pandas as pd
import numpy as np
import json
import os

def main():
    # Load data
    df = pd.read_csv('data/processed/district_clusters.csv')
    
    # Separate identifier columns and numerical feature columns
    identifiers = ['District Names', 'State/UT', 'Cluster']
    feature_cols = [c for c in df.columns if c not in identifiers]
    
    # 1. Overall averages and standard deviations
    overall_stats = df[feature_cols].agg(['mean', 'std']).T
    overall_stats.columns = ['overall_mean', 'overall_std']
    
    # 2. Cluster sizes
    cluster_counts = df['Cluster'].value_counts().sort_index()
    
    cluster_profiles = {}
    comparison_table = pd.DataFrame(index=feature_cols)
    
    for cluster_id in sorted(df['Cluster'].unique()):
        cluster_data = df[df['Cluster'] == cluster_id][feature_cols]
        cluster_mean = cluster_data.mean()
        cluster_std = cluster_data.std()
        
        # Calculate standard deviation difference from overall mean to identify strong/weak indicators
        # Z-score-like metric for how far cluster mean is from overall mean
        diff_from_overall = cluster_mean - overall_stats['overall_mean']
        z_diff = diff_from_overall / overall_stats['overall_std']
        
        profile = {
            'size': int(cluster_counts[cluster_id]),
            'metrics': {}
        }
        
        for col in feature_cols:
            profile['metrics'][col] = {
                'mean': float(cluster_mean[col]),
                'std': float(cluster_std[col]),
                'diff_from_overall': float(diff_from_overall[col]),
                'z_diff': float(z_diff[col])
            }
            # For comparison table
            comparison_table[f'Cluster_{cluster_id}_mean'] = cluster_mean
            comparison_table[f'Cluster_{cluster_id}_z_diff'] = z_diff
            
        cluster_profiles[str(cluster_id)] = profile

    # Save cluster summary statistics and comparison table
    os.makedirs('reports', exist_ok=True)
    comparison_table.to_csv('reports/cluster_comparison_table.csv')
    
    with open('reports/cluster_profiles.json', 'w') as f:
        json.dump({
            'overall_stats': overall_stats.to_dict(orient='index'),
            'cluster_profiles': cluster_profiles
        }, f, indent=4)
        
    print("Day 4 cluster interpretation metrics successfully computed.")

if __name__ == '__main__':
    main()
